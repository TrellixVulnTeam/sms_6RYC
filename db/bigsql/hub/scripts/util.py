from __future__ import print_function, division

##################################################################
##########     Copyright (c) 2015-2018 BigSQL      ###############
##################################################################

PGC_VERSION = "4.0.4"

from subprocess import Popen, PIPE, STDOUT
from datetime import datetime, timedelta

import os, sys, socket, platform, sqlite3, getpass, signal, hashlib
import json, uuid, logging, tempfile, shutil, filecmp, traceback
import api
import uuid


isPy3 = False
if sys.version_info >= (3, 0):
  isPy3 = True

try:
  from distutils.dir_util import copy_tree
except:
  ## this is a problem in the default Python3.6 distro on Ubuntu 18.04
  print("ERROR: Missing python3-distutils module")

try:
  # For Python 3.0 and later
  from urllib import request as urllib2
except ImportError:
  # Fall back to Python 2's urllib2
  import urllib2

scripts_lib_path = os.path.join(os.path.dirname(__file__), 'lib')
if scripts_lib_path not in sys.path:
  sys.path.append(scripts_lib_path)

this_platform_system = str(platform.system())
platform_lib_path = os.path.join(scripts_lib_path, this_platform_system)
if os.path.exists(platform_lib_path):
  if platform_lib_path not in sys.path:
    sys.path.append(platform_lib_path)


import semver
import pgclog

my_logger = logging.getLogger('pgcli_logger')
PGC_HOME = os.getenv('PGC_HOME', '..' + os.sep + '..')
pid_file = os.path.join(PGC_HOME, 'conf', 'pgc.pid')

def source_env_file(p_env_file):
  try:
    command = ['bash', '-c', 'source ' + p_env_file + ' && env']
    proc = Popen(command, stdout=PIPE)
    for line in proc.stdout:
      (key, _, value) = line.partition("=")
      os.environ[key] = value.strip()
    proc.communicate()

  except Exception as e:
    exit_message(str(e), 1, False)
  
  return


def encrypt(plaintext, key):
  """
  Encrypt the plaintext with AES method.

  Parameters:
      plaintext -- String to be encrypted.
      key       -- Key for encryption.
  """
  try:
    import base64

    from Crypto import Random
    from Crypto.Cipher import AES
  except ImportError as e:
    exit_message(str(e), 1, False)

  iv = Random.new().read(AES.block_size)
  cipher = AES.new(pad(key), AES.MODE_CFB, iv)
  # If user has entered non ascii password (Python2)
  # we have to encode it first
  if hasattr(str, 'decode'):
    plaintext = plaintext.encode('utf-8')
  encrypted = base64.b64encode(iv + cipher.encrypt(plaintext))

  return encrypted


def decrypt(ciphertext, key):
  """
  Decrypt the AES encrypted string.

  Parameters:
      ciphertext -- Encrypted string with AES method.
      key        -- key to decrypt the encrypted string.
  """
  try:
    import base64

    from Crypto.Cipher import AES
  except ImportError as e:
    exit_message(str(e), 1, False)

  padding_string = b'}'

  ciphertext = base64.b64decode(ciphertext)
  iv = ciphertext[:AES.block_size]
  cipher = AES.new(pad(key), AES.MODE_CFB, iv)
  decrypted = cipher.decrypt(ciphertext[AES.block_size:])

  return decrypted


def pad(str):
  """Add padding to the key."""

  padding_string = b'}'
  str_len = len(str)

  # Key must be maximum 32 bytes long, so take first 32 bytes
  if str_len > 32:
    return str[:32]

  # If key size id 16, 24 or 32 bytes then padding not require
  if str_len == 16 or str_len == 24 or str_len == 32:
    return str

  # Add padding to make key 32 bytes long
  return str + ((32 - len(str) % 32) * padding_string)


def get_parent_dir_path(p_path):
  from os.path import dirname
  parent_path = dirname(p_path)
  if not os.path.isdir(p_path):
      parent_path = dirname(parent_path)
  return parent_path


## directory listing ##########################################
def dirlist(p_isJSON, p_path):
  import glob

  dir_list = []
  for name in glob.iglob(p_path):
    dir_dict = {}
    dir_dict['name'] = name
    if os.path.isdir(name):
      dir_dict['type'] = "d"
    else:
      dir_dict['type'] = "-"
    last_accessed = datetime.fromtimestamp(os.path.getatime(name))
    dir_dict['last_accessed'] = last_accessed.strftime("%Y-%m-%d %H:%M:%S")
    dir_list.append(dir_dict)

  if len(dir_list) > 0:
    dir_list = sorted(dir_list, key=lambda k: (k['type'].lower, os.path.getatime(k['name'])), reverse = True)
  parent_path = get_parent_dir_path(os.path.split(p_path)[0])
  if not parent_path.endswith(os.sep):
    parent_path = parent_path + os.sep
  if os.path.exists(parent_path):
    parent_dict = {
        'type':'.',
        'name':  parent_path,
        'last_accessed':datetime.fromtimestamp(os.path.getatime(parent_path)).strftime("%Y-%m-%d %H:%M:%S")
    }
    dir_list.insert(0,parent_dict)
  if p_isJSON:
    json_dict = {}
    json_dict['data'] = dir_list
    json_dict['state'] = 'completed'
    print(json.dumps([json_dict]))
    return(0)

  print("DIRLIST for '" + p_path + "':")
  for d in dir_list:
    print("  " + d['type'] + " " + d['name'] + " " + d['last_accessed'])

  return 0


## terminate abruptly #########################################
def fatal_error(p_msg):
  msg = "ERROR: " + p_msg
  if os.getenv("isJson", None):
    sys.stdout = previous_stdout
    jsonMsg = {}
    jsonMsg['status'] = "error"
    jsonMsg['msg'] = msg
    print (json.dumps([jsonMsg]))
  else:
    print (msg)
  sys.exit(1)


def escape_ansi_chars(p_str):
  import re
  ansi_escape = re.compile(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]')
  final_lines = ansi_escape.sub("", p_str)
  striped_lines = str(final_lines).strip()
  return striped_lines


def getoutput(p_cmd):
  if sys.version_info < (2, 7):
    import commands
    out=commands.getoutput(p_cmd)
    return out.strip()
  else:
    from subprocess import check_output
    out=check_output(p_cmd, shell=True)
    return out.strip().decode('ascii')


## is this a Linux SystemD platform ############################
def is_systemd():
  if get_platform() != "Linux":
    return False

  return((os.path.isfile('/usr/bin/systemctl') and os.access('/usr/bin/systemctl', os.X_OK))
         or (os.path.isfile('/bin/systemctl') and os.access('/bin/systemctl', os.X_OK)))


## run as SUDO (if not already) ###############################
def run_sudo(p_cmd, p_display=True, p_isJSON=False):
  cmd = p_cmd
  if os.getenv("SUDO_USER", "") == "":
    cmd = "sudo " + cmd

  if p_display:
    message("$ " + cmd, "info", p_isJSON)

  outp = getoutput(cmd)
  message("\n" + outp, "info", p_isJSON)

  return(0)


# Find the appropriate systemd directory (system service) #####
def get_systemd_dir():
  systemd_dir="/usr/lib/systemd/system"
  if os.path.isdir(systemd_dir):
    # This directory is common to RedHat based systems
    return(systemd_dir)

  systemd_dir="/lib/systemd/system"
  if os.path.isdir(systemd_dir):
    # This directory is common to deb / ubuntu
    return(systemd_dir)

  return("")


def get_service_status(p_svcname):
  if get_platform() == "Windows":
      import win32serviceutil, win32service
      try:
          svc_status = win32serviceutil.QueryServiceStatus(p_svcname)
          if svc_status[1]==win32service.SERVICE_RUNNING:
              return "Running"
          elif svc_status[1]==win32service.SERVICE_STOPPED:
              return "Stopped"
      except Exception as e:
          return "?"

  if get_platform() == "Linux":
    if is_systemd():
      cmd = "sudo systemctl status " + p_svcname
    else:
      cmd = "sudo service " + p_svcname + " status"

    p = Popen(cmd, shell=True, stdout=PIPE,
              stderr=PIPE, executable=None,
              close_fds=False)
    (stdout, stderr) = p.communicate()
    if p.returncode==0:
      return "Running"
    else:
      return "Stopped"

  return "?"


def delete_service_win(svcName):
    import win32serviceutil
    is_service_installed = False
    try:
        win32serviceutil.QueryServiceStatus(svcName)
        is_service_installed = True
    except:
        is_service_installed = False
    if is_service_installed:
        sc_path = os.getenv("SYSTEMROOT", "") + os.sep + "System32" + os.sep + "sc"
        system(sc_path + " delete " + svcName, is_admin=True)
    return True


## is this component PostgreSQL ##################################
def is_postgres(p_comp):
  pgXX = ['pg93', 'pg94', 'pg95', 'pg96', 'pg10', 'pg11']
  if p_comp in pgXX:
    return True
                
  pgdgXX = ['pgdg93', 'pgdg94', 'pgdg95', 'pgdg96', 'pgdg10', 'pgdg11']
  if p_comp in pgdgXX:
    return True

  return False


## get the owner of the file/directory
def get_owner_name(p_path=None):
  file_path = p_path
  if not p_path:
      file_path = os.getenv("PGC_HOME")
  import pwd
  st = os.stat(file_path)
  uid = st.st_uid
  userinfo = pwd.getpwuid(uid)
  ownername = userinfo.pw_name
  return ownername


## anonymous data from the INFO command
def get_anonymous_info():
    jsonInfo = api.info(True, "", "", False)
    platform = jsonInfo['platform']
    os = jsonInfo['os']
    mem = str(jsonInfo['mem'])
    cores = str(jsonInfo['cores'])
    cpu = jsonInfo['cpu']
    anon = "(" + platform + "; " + os + "; " + mem + "; " + \
              cores + "; " + cpu + ")"
    return(anon)


## abruptly terminate with a codified message
def exit_message(p_msg, p_rc, p_isJSON=False):
  if p_rc == 0:
    message(p_msg, "info", p_isJSON)
  else:
    message(p_msg, "error", p_isJSON)

  sys.exit(p_rc)


## print codified message to stdout & logfile
def message(p_msg, p_state="info", p_isJSON=False):
  if p_state == "error":
    my_logger.error(p_msg)
    prefix = "ERROR: "
  else:
    my_logger.info(p_msg)
    prefix = ""

  if p_isJSON:
    json_dict = {}
    json_dict['state'] = p_state 
    json_dict['msg'] = p_msg
    print (json.dumps([json_dict]))
  else:
    print (prefix + p_msg)

  return


def verify(p_json):
  try:
    c = cL.cursor()
    sql = "SELECT component, version, platform, release_date " + \
          " FROM versions WHERE is_current = 1 " + \
          "ORDER BY 4 DESC, 1"
    c.execute(sql)
    data = c.fetchall()
    for row in data:
      comp_ver = str(row[0]) + "-" + str(row[1])
      plat = str(row[2])
      if plat == "":
        verify_comp(comp_ver)
      else:
        if "win" in plat:
          verify_comp(comp_ver + "-win64")
        if "osx" in plat:
          verify_comp(comp_ver + "-osx64")
        if "linux" in plat:
          verify_comp(comp_ver + "-linux64")
  except Exception as e:
    fatal_sql_error(e,sql,"verify()")

  return


def verify_comp(p_comp_ver_plat):
  base = get_value("GLOBAL", "REPO") + "/" + p_comp_ver_plat
  url_file = base + ".tar.bz2"
  rc1 = http_is_file(url_file)

  url_checksum = url_file + ".sha512"
  rc2 = http_is_file(url_checksum)

  if rc1 == 0 and rc2 == 0:
    print ("GOOD: " + base)
    return 0

  print ("BAD:  " + base)
  return 1


def get_relnotes(p_comp, p_ver=""):
  comp_name = p_comp
  parent_comp = get_parent_component(comp_name,0)
  if parent_comp!="":
      comp_name=p_comp.replace("-" + parent_comp,"")

  file = "relnotes-" + comp_name + ".txt"
  ver = ""
  if is_postgres(comp_name):
    if p_ver == "":
      if p_comp == "pg10":
        ver = "10.0"
      elif p_comp == "pg96":
        ver = "9.6.0"
      elif p_comp == "pg95":
        ver = "9.5.0"
      elif p_comp == "pg94":
        ver = "9.4.0"
      elif p_comp == "pg93":
        ver = "9.3.0"
      elif p_comp == "pg92":
        ver = "9.2.0"
    else:
      ## remove the "-n" suffix
      ver = p_ver[:-2]
    file = "relnotes-" + comp_name + "-" + ver + ".txt"
  repo = get_value("GLOBAL", "REPO")
  repo_file = repo + "/" + file
  out_dir = PGC_HOME + os.sep + "conf" + os.sep + "cache"

  if http_is_file(repo_file) == 1:
    return("not available")

  if http_get_file(False, file, repo, out_dir, False, ""):
    out_file = out_dir + os.sep + file
    rel_notes_text = read_file_string(out_file)
    final_txt = unicode(str(rel_notes_text),sys.getdefaultencoding(),errors='ignore').strip()
    return final_txt

  return ""

def utc_to_local(dt):
  import time
  dt_obj=datetime.strptime(dt, "%Y-%m-%d %H:%M:%S")
  time_stamp = time.mktime(dt_obj.timetuple())
  now_timestamp = time.time()
  offset = datetime.fromtimestamp(now_timestamp) - datetime.utcfromtimestamp(now_timestamp)
  dt_local=dt_obj + offset
  return dt_local


def update_installed_date(p_app):
  try:
    c = cL.cursor()
    install_date=datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    sql = "UPDATE components SET install_dt = ? WHERE component = ?"
    c.execute(sql, [install_date, p_app])
    cL.commit()
    c.close()
  except Exception as e:
    fatal_sql_error(e,sql,"update_installed_date()")

  return


def update_hosts(p_host, p_unique_id, updated=False):
  last_update_utc = datetime.utcnow()

  current_time = last_update_utc

  cmd = os.path.abspath(PGC_HOME) + os.sep + "pgc update"

  if p_unique_id:
    unique_id = p_unique_id
  else:
    unique_id = str(uuid.uuid4())

  if updated:
    exec_sql("UPDATE hosts " + \
             "   SET last_update_utc = '" + last_update_utc.strftime("%Y-%m-%d %H:%M:%S") + "', " + \
             "       unique_id = '" + str(unique_id) + "' " + \
             " WHERE host = '" + str(p_host) + "'")
  return


def get_versions_sql():
  return get_value ("GLOBAL", "VERSIONS", "versions.sql")


def get_stage():
  return get_value ("GLOBAL", "STAGE", "off")


def get_value (p_section, p_key, p_value=""):
  try:
    c = cL.cursor()
    sql = "SELECT s_value FROM settings WHERE section = ? AND s_key = ?"
    c.execute(sql, [p_section, p_key])
    data = c.fetchone()
    if data is None:
      return p_value
  except Exception as e:
    fatal_sql_error(e,sql,"get_value()")
  return data[0]


def set_value (p_section, p_key, p_value):
  try:
    c = cL.cursor()
    sql = "DELETE FROM settings WHERE section = ? AND s_key = ?"
    c.execute(sql, [p_section, p_key])
    sql = "INSERT INTO settings (section, s_key, s_value) VALUES (?, ?, ?)"
    c.execute(sql, [p_section, p_key, p_value])
    cL.commit()
    c.close()
  except Exception as e:
    fatal_sql_error(e, sql, "set_value()")
  return


def unset_value (p_section, p_key):
  try:
    c = cL.cursor()
    sql = "DELETE FROM settings WHERE section = ? AND s_key = ?"
    c.execute(sql, [p_section, p_key])
    cL.commit()
    c.close()
  except Exception as e:
    fatal_sql_error(e, sql, "unset_value()")
  return


def get_pgc_hosts_file_name():
  pw_file=""
  pgc_host_dir = os.path.join(PGC_HOME, "conf")
  if get_platform() == "Windows":
    pw_file = os.path.join(pgc_host_dir, "pgc_hosts.conf")
  else:
    pw_file = os.path.join(pgc_host_dir, ".pgc_hosts")
  return(pw_file)


def get_pgc_host(p_host):
  host_dict = {}
  try:
    c = cL.cursor()
    sql = "SELECT host, name, pgc_home FROM hosts where name=?"
    c.execute(sql, [p_host])
    data = c.fetchone()
    if data:
      host_dict = {}
      host_dict['host'] = str(data[0])
      host_dict['host_name'] = str(data[1])
      host_dict['pgc_home'] = str(data[2])
  except Exception as e:
    print("ERROR: Retrieving host info")
    exit_message(str(e), 1)
  return (host_dict)


def get_host_with_id(p_host_id):
  try:
    c = cL.cursor()
    sql = "SELECT host FROM hosts where host_id=?"
    c.execute(sql,[p_host_id])
    data = c.fetchone()
    if data:
      return True
  except Exception as e:
    print ("ERROR: Retrieving host")
    exit_message(str(e), 1)
  return False


def get_host_with_name(p_host_name):
  try:
    c = cL.cursor()
    sql = "SELECT host FROM hosts where name=?"
    c.execute(sql,[p_host_name])
    data = c.fetchone()
    if data:
      return True
  except Exception as e:
    print ("ERROR: Retrieving host")
    exit_message(str(e), 1)
  return False


def timedelta_total_seconds(timedelta):
  return (timedelta.microseconds + 0.0 + (timedelta.seconds + timedelta.days * 24 * 3600) * 10 ** 6) / 10 ** 6


def read_hosts (p_host):
  sql = "SELECT last_update_utc, unique_id \n" + \
        "  FROM hosts WHERE host = '" + p_host + "'"

  try:
    c = cL.cursor()
    c.execute(sql)
    data = c.fetchone()
    if data is None:
      return ["", "", "", ""]
  except Exception as e:
    fatal_sql_error(e,sql,"get_host()")

  last_update_utc = data[0]
  last_update_local = ''
  if last_update_utc:
    last_update_local = str(utc_to_local(data[0]))
  unique_id = data[1]

  return [last_update_utc, last_update_local, unique_id]


def is_password_less_ssh():
  cmd = "ssh -o 'PreferredAuthentications=publickey' localhost 'echo' >/dev/null 2>&1"
  rc = os.system(cmd)
  if rc:
    print("Error trying to do password-less SSH to localhost.")
    return False
  return True


def read_env_file(component):
  if str(platform.system()) == "Windows":
    from subprocess import check_output
    script = os.path.join(PGC_HOME, component, component+'-env.bat')
    if os.path.isfile(script):
      try:
        vars = check_output([script, '&&', 'set'], shell=True)
        for var in vars.splitlines():
          k, _, v = map(str.strip, var.strip().partition('='))
          if k.startswith('?'):
            continue
          os.environ[k] = v
      except Exception as e:
        my_logger.error(traceback.format_exc())
        pass
  else:
    script = os.path.join(PGC_HOME, component, component+'.env')
    if os.path.isfile(script):
        try:
          pipe1 = Popen(". %s; env" % script, stdout=PIPE, shell=True, executable="/bin/bash")
          output = str(pipe1.communicate()[0].strip())
          lines = output.split("\n")
          env = dict((line.split("=", 1) for line in lines))
          for e in env:
            os.environ[e] = env[e]
        except Exception as e:
          my_logger.error(traceback.format_exc())
          pass

  return


def remember_pgpassword(p_passwd, p_port):
  if get_platform() == "Windows":
    pw_dir = os.getenv("APPDATA") + "\postgresql"
    if not os.path.isdir(pw_dir):
      os.mkdir(pw_dir)
    pw_file = pw_dir + "\pgpass.conf"
  else:
    try:
      pw_file = os.getenv("HOME") + "/.pgpass"
    except:
      home = get_unix_user_home()
      if home is not None:
        pw_file = home + "/.pgpass"
      else:
        fatal_error("No valid HOME for user %s" % get_user())

  if os.path.isfile(pw_file):
    s_pw = read_file_string(pw_file)
  else:
    s_pw = ""

  file = open(pw_file, 'w')

  ## pre-pend the new
  escaped_passwd = p_passwd
  escaped_passwd = escaped_passwd.replace("\\", "\\\\")
  escaped_passwd = escaped_passwd.replace(":", "\:")
  s_localhost = "localhost:" + p_port + ":*:postgres:" + escaped_passwd
  file.write(s_localhost + "\n")
  s_127 = "127.0.0.1:" + p_port + ":*:postgres:" + escaped_passwd
  file.write(s_127 + "\n")

  ## append the old (skipping duplicate lines)
  if s_pw > "":
    lines = s_pw.split("\n")
    for line in lines:
      if ((line == s_localhost) or (line == s_127)):
        pass
      else:
        file.write(line + "\n")

  file.close()

  if not get_platform() == "Windows":
    os.chmod(pw_file, 0o600)

  print (" ")
  print ("Password securely remembered in the file: " + pw_file)
  return pw_file


def update_postgresql_conf(p_pgver, p_port, is_new=True,update_listen_addr=True):
  ## does 'postgresql.conf' file exist for updating
  pg_data = get_column('datadir', p_pgver)
  config_file = pg_data + os.sep + "postgresql.conf"
  if not os.path.isfile(config_file):
    print ("ERROR: You may not (config)ure before (init)ialization.")
    sys.exit(1)
  if not os.access(config_file, os.W_OK):
    print ("ERROR: Write permission denied on 'postgresql.conf'.")
    sys.exit(1)

  ## set port in sqlite metadata
  set_column("port", p_pgver, str(p_port))

  ## set port in postgresql.conf
  s = read_file_string(config_file)
  ns = ""
  lines = s.split('\n')
  for line in lines:
    if line.startswith("port") or line.startswith("#port"):
      # always override port
      pt = "port = " + str(p_port) + \
             "\t\t\t\t# (change requires restart)"
      ns = ns + "\n" + pt

    elif is_new and line.startswith("#listen_addresses = 'localhost'") and update_listen_addr:
      # override default to match default for pg_hba.conf
      la = "listen_addresses = '*'" + \
              "\t\t\t# what IP address(es) to listen on;"
      ns = ns + "\n" + la

    elif is_new and line.startswith("#logging_collector"):
      ns = ns + "\n" + "logging_collector = on"

    elif is_new and line.startswith("#log_directory"):
      log_directory = os.path.join(PGC_HOME, "data", "logs", p_pgver).replace("\\", "/")
      ns = ns + "\n" + "log_directory = '" + log_directory + "'"

    elif is_new and line.startswith("#log_filename"):
      ns = ns + "\n" + "log_filename = 'postgresql-%a.log'"

    elif is_new and line.startswith("#log_line_prefix"):
      ns = ns + "\n" + "log_line_prefix =  '%t [%p]: [%l-1] user=%u,db=%d,app=%a,client=%h '"

    elif is_new and line.startswith("#log_truncate_on_rotation"):
      ns = ns + "\n" + "log_truncate_on_rotation = on "

    elif is_new and line.startswith("#log_checkpoints"):
      ns = ns + "\n" + "log_checkpoints = on"

    elif is_new and line.startswith("#log_autovacuum_min_duration"):
      ns = ns + "\n" + "log_autovacuum_min_duration = 0"

    elif is_new and line.startswith("#log_temp_files"):
      ns = ns + "\n" + "log_temp_files = 0"

    elif is_new and line.startswith("#log_lock_waits"):
      ns = ns + "\n" + "log_lock_waits = on"

    elif is_new and line.startswith("#checkpoint_segments"):
      ns = ns + "\n" + "checkpoint_segments = 16"

    elif is_new and line.startswith("#maintenance_work_mem"):
      ns = ns + "\n" + "maintenance_work_mem = 64MB"

    elif is_new and line.startswith("#max_wal_senders"):
      ns = ns + "\n" + "max_wal_senders = 5"

    elif is_new and line.startswith("#track_io_timing"):
      ns = ns + "\n" + "track_io_timing = on"

    elif is_new and line.startswith("#wal_keep_segments"):
      ns = ns + "\n" + "wal_keep_segments = 32"

    elif is_new and line.startswith("#max_replication_slots"):
      ns = ns + "\n" + "max_replication_slots = 5"

    elif is_new and line.startswith("#wal_level"):
      ns = ns + "\n" + "wal_level = hot_standby"

    elif is_new and line.startswith("#update_process_title") and get_platform() == "Windows":
      ns = ns + "\n" + "update_process_title = off"

    else:
      if ns == "":
        ns = line
      else:
        ns = ns + "\n" + line
  write_string_file(ns, config_file)

  print (" ")
  print ("Using PostgreSQL Port " + str(p_port))
  return


def get_superuser_passwd():
  print (" ")
  try:
    while True:
      pg_pass1 = getpass.getpass(str("Superuser Password [password]: "))
      if pg_pass1.strip() == "":
        pg_pass1 = "password"
        break
      pg_pass2 = getpass.getpass(str("Confirm Password: "))
      if pg_pass1 == pg_pass2:
        break
      else:
        print (" ")
        print ("Password mis-match, try again.")
        print (" ")
        continue
  except KeyboardInterrupt as e:
    sys.exit(1)
  return pg_pass1;


def write_pgenv_file(p_pghome, p_pgver, p_pgdata, p_pguser, p_pgdatabase, p_pgport, p_pgpassfile):
  pg_bin_path = os.path.join(p_pghome, "bin")
  if get_platform() == "Windows":
    export = "set "
    source = "run"
    newpath = export + "PATH=" + pg_bin_path + ";%PATH%"
    env_file = p_pghome + os.sep + p_pgver + "-env.bat"
  else:
    export = "export "
    source = "source"
    newpath = export + "PATH=" + pg_bin_path + ":$PATH"
    env_file = p_pghome + os.sep + p_pgver + ".env"

  try:
    file = open(env_file, 'w')
    if get_platform() == "Windows":
      file.write('@echo off\n')
    file.write(export + 'PGHOME=' + p_pghome + '\n')
    file.write(export + 'PGDATA=' + p_pgdata + '\n')
    file.write(newpath + '\n')
    file.write(export + 'PGUSER=' + p_pguser + '\n')
    file.write(export + 'PGDATABASE=' + p_pgdatabase + '\n')
    file.write(export + 'PGPORT=' + p_pgport + '\n')
    if p_pgpassfile:
      file.write(export + 'PGPASSFILE=' + p_pgpassfile + '\n')
    file.write(export + 'PYTHONPATH=' + os.path.join(PGC_HOME, p_pgver, "python", "site-packages") + '\n')
    file.write(export + 'GDAL_DATA=' + os.path.join(p_pghome, "share", "gdal") + '\n')
    file.close()
    os.chmod(env_file, 0o755)
  except IOError as e:
    return 1

  print (" ")
  print ("to load this postgres into your environment, " + source + " the env file: ")
  print ("    " + env_file)
  print (" ")
  return 0


####################################################################
# Check if port is already assigned
####################################################################
def is_port_assigned(p_port, p_comp):
  try:
    c = cL.cursor()
    sql = "SELECT port FROM components WHERE component != '" + \
          p_comp + "' and port='" + str(p_port) + "' and datadir !=''"
    c.execute(sql)
    data = c.fetchone()
    if data is None:
      return False
  except Exception as e:
    fatal_sql_error(e, sql, "is_port_assigned()")
  return True


####################################################################
# Get an available port
####################################################################
def get_avail_port(p_prompt, p_def_port, p_comp="", p_interactive=False, isJSON=False):
  def_port = int(p_def_port)

  ## iterate to first non-busy port
  while (is_socket_busy(def_port, p_comp)):
    def_port = def_port + 1
    continue

  err_msg="Port must be between 1000 and 9999, try again."

  while True:
    if p_interactive:
      s_port = raw_input(p_prompt + "[" + str(def_port) + "]? ")
      if s_port == "":
        s_port = str(def_port)
    else:
      s_port = str(def_port)

    if (s_port.isdigit() == False):
      print (err_msg)
      continue

    i_port = int(s_port)

    if ( i_port < 1000 ) or ( i_port > 9999 ):
      print (err_msg)
      continue

    if is_port_assigned(i_port, p_comp) or is_socket_busy(i_port, p_comp):
      if not isJSON:
        print ("Port " + str(i_port) + " is in use.")
      def_port = str(i_port + 1)
      continue

    break

  return i_port


####################################################################
# delete a directory using OS specific commands
####################################################################
def delete_dir(p_dir):
  if (get_platform() == "Windows"):
    cmd = 'RMDIR "' + p_dir + '" /s /q'
  else:
    cmd = 'rm -rf "' + p_dir + '"'
  rc = os.system(cmd)
  return rc


####################################################################
# optionally run a system level command as Admin/root
####################################################################
def  system(p_cmd, is_admin=False, is_display=False):
  if is_display:
    print ("\n## " + p_cmd + " ##########")

  if is_admin:
    rc = runas_win_admin(p_cmd)
  else:
    rc = os.system(p_cmd)

  if is_display:
    print ("rc = " + str(rc))

  return rc


####################################################################
# round to scale & show integers without the ".0"
####################################################################
def pretty_rounder(p_num, p_scale):
  rounded = round(p_num, p_scale)
  if not (rounded % 1):
    return int(rounded)
  return rounded


####################################################################
# retrieve PGC version
####################################################################
def get_pgc_version():
  return (PGC_VERSION)


####################################################################
# retrieve project dependencies
####################################################################
def get_depend():
  dep = []
  try:
    c = cL.cursor()
    sql = "SELECT DISTINCT r1.component, r2.component, p.start_order \n" + \
          "  FROM projects p, releases r1, releases r2, versions v \n" + \
          " WHERE v.component = r1.component \n" + \
          "   AND " + like_pf("v.platform") +  " \n" + \
          "   AND p.project = r1.project \n" + \
          "   AND p.depends = r2.project \n" + \
          "ORDER BY 3"
    c.execute(sql)
    data = c.fetchall()
    for row in data:
      component = str(row[0])
      depends = str(row[1])
      p = component + " " + depends
      dep.append(p.split())
  except Exception as e:
    fatal_sql_error(e,sql,"get_depend()")
  return dep


##################################################################
# Run the sql statements in a command file
##################################################################
def process_sql_file(p_file, p_json):
  isSilent = os.environ.get('isSilent', None)

  rc = True

  ## verify the hub version ##################
  file = open(p_file, 'r')
  cmd = ""
  for line in file:
    line_strip = line.strip()
    if line_strip == "":
      continue
    cmd = cmd + line
    if line_strip.endswith(";"):
      if ("hub" in cmd) and ("INSERT INTO versions" in cmd) and ("1," in cmd):
        cmdList = cmd.split(',')
        newHubV = cmdList[1].strip().replace("'", "")
        oldHubV = get_pgc_version()
        msg_frag = "'hub' from v" + oldHubV + " to v" + newHubV + "."
        if newHubV == oldHubV:
          msg = "'hub' is v" + newHubV
        if newHubV > oldHubV:
          msg = "Automatic updating " + msg_frag
        if newHubV < oldHubV:
          msg = "ENVIRONMENT ERROR:  Cannot downgrade " + msg_frag
          rc = False
        if p_json:
          print ('[{"status":"wip","msg":"'+msg+'"}]')
        else:
          if not isSilent:
            print (msg)
        my_logger.info(msg)
        break
      cmd = ""
  file.close()

  if rc == False:
    if p_json:
      print ('[{"status":"completed","has_updates":0}]')
    return False

  ## process the file ##########################
  file = open(p_file, 'r')
  cmd = ""
  for line in file:
    line_strip = line.strip()
    if line_strip == "":
      continue
    cmd = cmd + line
    if line_strip.endswith(";"):
      exec_sql(cmd)
      cmd = ""
  file.close()

  return True


##################################################################
# execute a sql command & commit it
##################################################################
def exec_sql(cmd):
  try:
    c = cL.cursor()
    c.execute(cmd)
    cL.commit()
    c.close()
  except Exception as e:
    fatal_sql_error(e,cmd,"exec_sql()")


##################################################################
# Print key server metrics
##################################################################
def show_metrics(p_home, p_port, p_data, p_log, p_pid):
  return
  if not p_home == None:
    print ("  --homedir " + str(p_home))
  if not p_port == None:
    print ("  --port    " + str(p_port))
  if not p_data == None:
    print ("  --datadir " + p_data)
  if not p_log == None:
    print ("  --logfile " + p_log)
  if not p_pid == None:
    print ("  --pidfile " + p_pid)


####################################################################################
# Retrieve the string value of a column from Components table
####################################################################################
def get_column(p_column, p_comp, p_env=''):
  try:
    c = cL.cursor()
    sql = "SELECT " + p_column + " FROM components WHERE component = '" + p_comp + "'"
    c.execute(sql)
    data = c.fetchone()
    if data is None:
      return "-1"
    col_val = str(data[0])
    if col_val == "None" or col_val == "" or col_val is None:
      if p_env > '':
        if p_env.startswith('$'):
          env = os.getenv(p_env[1:], '')
        else:
          env = p_env
        if env > '':
          set_column(p_column, p_comp, env)
          return env
        else:
          return "-1"
  except Exception as e:
    fatal_sql_error(e,sql,"get_column()")
  return col_val


####################################################################################
# Update the value of a column for Components table
####################################################################################
def set_column(p_column, p_comp, p_value):
  try:
    c = cL.cursor()
    sql = "UPDATE components SET " + p_column + " = '" + str(p_value) + "' " + \
          " WHERE component = '" + p_comp + "'"
    c.execute(sql)
    cL.commit()
    c.close()
  except Exception as e:
    fatal_sql_error(e,sql,"set_column()")


def fatal_sql_error(err,sql,func):
  msg = "#"
  msg = msg + "\n" + "################################################"
  msg = msg + "\n" + "FATAL SQL Error in " + func
  msg = msg + "\n" + "    SQL Message =  " + err.args[0]
  msg = msg + "\n" + "  SQL Statement = " + sql
  msg = msg + "\n" + "################################################"
  print (msg)
  if str(err.args[0]).startswith("no such table: versions") and func.startswith("get_depend()"):
      pass
  else:
      my_logger.error(msg)
  sys.exit(1)


####################################################################################
# Return the SHA512 checksum of a file
####################################################################################
def get_file_checksum(p_filename):
  BLOCKSIZE = 65536
  hasher = hashlib.sha512()
  with open(p_filename, 'rb') as afile:
    buf = afile.read(BLOCKSIZE)
    while len(buf) > 0:
        hasher.update(buf)
        buf = afile.read(BLOCKSIZE)
  return(hasher.hexdigest())


####################################################################################
# Read contents of a small file directly into a string
####################################################################################
def read_file_string(p_filename):
  try:
    f = open(p_filename, 'r')
    filedata = f.read()
    f.close()
    return(filedata)
  except IOError as e:
    print (e)
    return ""


####################################################################################
# Write contents of string into file
####################################################################################
def write_string_file(p_stringname, p_filename):
  f = open(p_filename,'w')
  f.write(p_stringname)
  f.close()


####################################################################################
# search and replace simple strings on a file, in-place
####################################################################################
def replace(p_olddata, p_newdata, p_filename):
  filestring = read_file_string(p_filename)
  print("  replace (" + p_olddata + ") with (" + p_newdata + ") on file (" + p_filename + ")")
  newstring = filestring.replace(p_olddata, p_newdata)
  write_string_file(newstring, p_filename)
  return


####################################################################################
# get pid of a running process which cannot create it's own pidfile
####################################################################################
def get_pid(name):
  from subprocess import check_output
  return check_output(["pidof",name])


####################################################################################
# abruptly terminate a process id
####################################################################################
def kill_pid(pid):
  if (pid < 1):
    return
  if (get_platform() == "Windows"):
    os.kill(pid, 2)
  else:
    os.kill(pid, signal.SIGKILL)
  return

# Terminate a process tree with the PID
def kill_process_tree(pid):
  import psutil
  process = psutil.Process(pid)
  for proc in process.children(recursive=True):
    proc.kill()
  process.kill()
  return True

def is_pid_running(p_pid):
  import psutil
  return psutil.pid_exists(int(p_pid))


####################################################################################
# use the java JPS command to locate one or more java process id's by keyword
####################################################################################
def get_jps_pid(keyword):
  pid = 0
  out = ""
  err = ""

  args = ['jps', '-lm']

  try:
    proc = Popen(args, stdout=PIPE, stderr=PIPE, shell=False)
    out, err = proc.communicate()
    rc = proc.returncode
  except OSError as e:
    msg = "unexpected error running the command '" + str(args) + "'"
    print (msg)
    my_logger.error(msg)
    my_logger.error(traceback.format_exc())
    return -1

  line = ""
  for char in out:
    if ( char == "\n" ):
      if keyword in line:
        return int(line.split()[0])
      line = ""
    else:
      line = line + str(char)

  return pid


####################################################################################
# use the java JPS command to kill a process id by keyword
####################################################################################
def kill_jps_pid(keyword):
  v_pid = get_jps_pid(keyword)
  if v_pid > 0:
    msg = "  killing " + keyword + " (" + str(v_pid) + ")"
    print (msg)
    my_logger.info(msg)
    kill_pid(v_pid)
  else:
    msg = keyword + " is not running."
    print ("  " + msg)
    my_logger.info(msg)
  return 0


####################################################################################
# return the OS platform (Linux, Windows or Darwin)
####################################################################################
def get_platform():
  return str(platform.system())


####################################################################################
# returns the OS (osx, win, el6, el7, xenial, precise, trusty...)
####################################################################################
def get_os():
  if platform.system() == "Darwin":
    return ("osx")

  if platform.system() == "Windows":
    return ("win")

  try:
    if os.path.exists("/etc/redhat-release"):
      ver = read_file_string("/etc/redhat-release").split()[3]
      if ver.startswith("7"):
        return "el7"
      else:
        return "el6"

    if os.path.exists("/etc/system-release"):
      ## Amazon Linux
      return "el6"

    if os.path.exists("/etc/lsb-release"):
      return(getoutput("cat /etc/lsb-release | grep DISTRIB_CODENAME | cut -d= -f2"))

  except Exception as e:
    pass

  return ("linux")



####################################################################################
# return if the user has admin rights
####################################################################################
def has_admin_rights():
  status = True
  if get_platform() == "Windows":
    from win32com.shell import shell
    status = shell.IsUserAnAdmin()
  return status


####################################################################################
# return the default BIGSQL platform based on the OS
####################################################################################
def get_default_pf():
  if get_platform() == "Darwin":
    return "osx64"

  if get_platform() == "Windows":
    return "win64"

  ## for now we will always use LINUX64
  if get_platform() == "Linux":
    return "linux64"

  try:
    if os.path.exists("/etc/redhat-release"):
      ver = read_file_string("/etc/redhat-release").split()[3]
      if ver.startswith("7"):
        return "el7-x64"
      else:
        return "linux64"
    if os.path.exists("/etc/lsb-release"):
      this_os = getoutput("cat /etc/lsb-release | grep DISTRIB_DESCRIPTION | cut -d= -f2 | tr -d '\"'")
      ver = this_os.split()[1]
      if ver.startswith("14"):
        return "ubu14-x64"
  except Exception as e:
    return "linux64"

  return "linux64"


####################################################################################
# return the BIGSQL platform
####################################################################################
def get_pf():
  return (get_value("GLOBAL", "PLATFORM", ""))


####################################################################################
# build up a LIKE clause for a SQL fragment appropriate for the platform
####################################################################################
def like_pf(p_col):
  pf = get_pf()
  OR = " OR "
  c1 = p_col + " LIKE ''"
  c2 = p_col + " LIKE '%" + pf + "%'"
  clause = "(" + c1 + OR + c2
  if pf in ("el7-x64", "ubu14-x64"):
    c3 = p_col + " LIKE '%linux64%'"
    clause = clause + OR + c3 + ")"
  else:
    clause = clause + ")"

  return clause


####################################################################################
# check if the current platform is in the list of component platforms
####################################################################################
def has_platform(p_platform):
  pf = get_pf()
  if "linux64" in p_platform and pf in ("el7-x64", "ubu14-x64"):
    return 0
  return p_platform.find(pf)


####################################################################################
# set the env variables
####################################################################################
def set_lang_path():
  perl_home = PGC_HOME + os.sep + 'perl5' + os.sep + 'perl'
  if os.path.exists(perl_home):
    os.environ['PERL_HOME'] = perl_home
    path = os.getenv('PATH')
    os.environ['PATH'] = perl_home + os.sep + 'site' + os.sep + 'bin' + os.pathsep + \
        perl_home + os.sep + 'bin' + os.pathsep + \
        PGC_HOME + os.sep + 'perl5' + os.sep + 'c' + os.sep + 'bin' + os.pathsep + path
  tcl_home = PGC_HOME + os.sep + 'tcl86'
  if os.path.exists(tcl_home):
    os.environ['TCL_HOME'] = tcl_home
    path = os.getenv('PATH')
    os.environ['PATH'] = tcl_home + os.sep + 'bin' + os.pathsep + path
  java_home = PGC_HOME + os.sep + 'java8'
  if os.path.exists(java_home):
    os.environ['JAVA_HOME'] = java_home
    path = os.getenv('PATH')
    os.environ['PATH'] = java_home + os.sep + 'bin' + os.pathsep + path


####################################################################################
# return the OS user name
####################################################################################
def get_user():
  if get_platform() == "Windows":
    my_logger.debug2("Windows user detection")
    return (os.getenv('USERNAME'))

  my_logger.debug2("Unix user detection")
  os_user = os.getenv("SUDO_USER","")
  my_logger.debug2("SUDO_USER: '%s'", os_user)
  if os_user == "":
    os_user = os.getenv("USER")
    my_logger.debug2("USER: '%s'", os_user)

  if os_user is None or os_user == "":
    my_logger.debug2("Executing id command")
    uid = getoutput("id -u")
    my_logger.debug2("uid: '%s'", uid)

    if str(uid) == "0":
      os_user = "root"

  my_logger.debug("Detected username: %s", os_user)

  return (os_user)


def get_unix_user_home():
  username = get_user()
  if username is None:
    my_logger.debug("Cannot determine username")
  home = None
  with open('/etc/passwd') as f:
    for line in f:
      luser = line.split(":")[0]
      lhome = line.split(":")[5]
      if luser == username:
        home = lhome

  my_logger.debug("Detected HomeDirectory: %s", home)
  return home

####################################################################################
# return the OS hostname
####################################################################################
def get_host():
  fqdn = ""
  if get_platform() == "Windows":
    try:
      fqdn = socket.getfqdn()
    except Exception as e:
      fqdn = "127.0.0.1"
  else:
    try:
      fqdn = getoutput("hostname -f 2>/dev/null")
    except Exception as e:
      fqdn = ""
  return (fqdn)

def get_host_short():
  if get_platform() == "Windows":
    return ("127.0.0.1")
  else:
    try:
      host_short = getoutput("hostname -s")
    except Exception as e:
      host_short = ""
    return (host_short)

def get_host_ip():
  try:
    host_ip = socket.gethostbyname(get_host())
  except Exception as e:
    host_ip = "127.0.0.1"
  return(host_ip)


####################################################################################
# convert a Windows file name to a URI
####################################################################################
def make_uri(in_name):
  if get_platform() != "Windows":
    return (in_name)
  else:
    return('///' + in_name.replace("\\", "/"))


####################################################################################
# run a background job detached from the terminal
####################################################################################
def launch_daemon(arglist, p_logfile_name):

  if p_logfile_name == None:
    f_logfile = os.devnull
  else:
    f_logfile = p_logfile_name

  with open(f_logfile, "wb") as outfile:
    Popen(arglist, stdin=PIPE, stdout=outfile, stderr=STDOUT)

  return 0


####################################################################################
# delete a file (if it exists)
####################################################################################
def delete_file(p_file_name):
  if (os.path.isfile(p_file_name)):
    os.remove(p_file_name)
  return


def http_is_file(p_url):
  try:
    req = urllib2.Request(p_url, None, http_headers())
    u = urllib2.urlopen(req, timeout=10)
  except KeyboardInterrupt as e:
    sys.exit(1)
  except Exception as e:
    return(1)

  return(0)


def urlEncodeNonAscii(b):
  import re
  return re.sub('[\x80-\xFF]', lambda c: '%%%02x' % ord(c.group(0)), b)


def http_headers():
  user_agent = 'PGC/' + get_pgc_version() + " " + get_anonymous_info()
  headers = { 'User-Agent' : urlEncodeNonAscii(user_agent) }
  return(headers)


## retrieve a remote file via http #################################################
def http_get_file(p_json, p_file_name, p_url, p_out_dir, p_display_status, p_msg, component_name=None):
  file_exists = False
  file_name_complete = p_out_dir + os.sep + p_file_name
  file_name_partial = file_name_complete + ".part"
  json_dict = {}
  json_dict['state'] = "download"
  if component_name is not None:
    json_dict['component'] = component_name
  if p_display_status:
    if not p_json:
      print (p_msg)
  try:
    delete_file(file_name_partial)
    file_url = p_url + '/' + p_file_name
    req = urllib2.Request(file_url, None, http_headers())
    u = urllib2.urlopen(req, timeout=10)
    meta = u.info()
    if isPy3:
        file_size = int(meta.get_all("Content-Length")[0])
    else:
        file_size = int(meta.getheaders("Content-Length")[0])
    file_size_dl = 0
    block_sz = 8192
    old_pct = 0.0
    old_size = 0
    f = open(file_name_partial,"wb")
    file_exists = True
    log_file_name = p_file_name.replace(".tar.bz2",'')
    log_msg = "Downloading file %s " % log_file_name
    is_checksum = False
    if p_file_name.find("sha512") >= 0:
      is_checksum = True
      log_file_name = p_file_name.replace(".tar.bz2.sha512",'')
      log_msg = "Downloading checksum for %s " % log_file_name
    if p_display_status:
      my_logger.info(log_msg)
    previous_time = datetime.now()
    while True:
      if not p_file_name.endswith(".txt") \
              and not p_file_name.startswith("install.py") \
              and not p_file_name.startswith("bigsql-pgc") \
              and not os.path.isfile(pid_file):
        raise KeyboardInterrupt("No lock file exists.")
      buffer = u.read(block_sz)
      if not buffer:
        break
      file_size_dl += len(buffer)
      f.write(buffer)
      file_size_dl_mb = (file_size_dl / 1024 / 1024)
      download_pct = int(file_size_dl * 100 / file_size)
      if p_display_status:
        if (file_size_dl_mb != old_size) or (download_pct != old_pct):
          if p_json:
            json_dict['status'] = "wip"
            json_dict['mb'] = get_file_size(file_size_dl)
            json_dict['pct'] = download_pct
            json_dict['file'] = p_file_name
            if component_name:
              json_dict['component'] = component_name
            print (json.dumps([json_dict]))
          else:
            status = r"%s [%s]     " % (get_file_size(file_size_dl), (str(download_pct) + "%"))
            status = status + chr(8)*(len(status)+1)
            print("\r" + status, end="")
            current_time=datetime.now()
            log_diff = current_time-previous_time
            if log_diff.seconds>0:
              previous_time=current_time
      old_size = file_size_dl_mb
      old_pct = download_pct
    if p_display_status and p_json:
      json_dict.clear()
      if component_name is not None:
        json_dict['component'] = component_name
      json_dict['state'] = "download"
      json_dict['status'] = "complete"
      print (json.dumps([json_dict]))
  except (urllib2.URLError, urllib2.HTTPError) as e:
    msg = "url=" + p_url + ", file=" + p_file_name
    if p_json:
      json_dict.clear()
      json_dict['msg'] = "Unable to download."
      if component_name is not None:
        json_dict['component'] = component_name
        json_dict['msg'] = "Unable to download " + component_name + " component."
      json_dict['state'] = "error"
      print (json.dumps([json_dict]))
    else:
      print("\n" + "ERROR: " + str(e))
      print("       " + msg)
    my_logger.error("URL Error while dowloading file %s (%s)",p_file_name,str(e))
    if file_exists and not f.closed:
      f.close()
    delete_file(file_name_partial)
    file_exists = False
    return(False)
  except socket.timeout as e:
    if p_json:
      json_dict.clear()
      if component_name is not None:
        json_dict['component'] = component_name
      json_dict['state'] = "error"
      json_dict['msg'] = "Connection timed out while downloading."
      print (json.dumps([json_dict]))
    else:
      print("\n" + str(e))
    my_logger.error("Timeout Error while dowloading file %s (%s)",p_file_name,str(e))
    if file_exists and not f.closed:
      f.close()
    delete_file(file_name_partial)
    file_exists = False
    return(False)
  except (IOError, OSError) as e:
    if p_json:
      json_dict.clear()
      if component_name is not None:
        json_dict['component'] = component_name
      json_dict['state'] = "error"
      json_dict['msg'] = str(e)
      print (json.dumps([json_dict]))
    else:
      print("\n" + str(e))
    my_logger.error("IO Error while dowloading file %s (%s)",p_file_name,str(e))
    if file_exists and not f.closed:
      f.close()
    delete_file(file_name_partial)
    file_exists = False
    return(False)
  except KeyboardInterrupt as e:
    if p_json:
      json_dict.clear()
      if component_name is not None:
        json_dict['component'] = component_name
      json_dict['state'] = "download"
      json_dict['status'] = "cancelled"
      json_dict['msg'] = "Download cancelled"
      print (json.dumps([json_dict]))
    else:
      print("Download Cancelled")
    my_logger.error("Cancelled dowloading file %s ",p_file_name)
    if file_exists and not f.closed:
      f.close()
    delete_file(file_name_partial)
    file_exists = False
    return(False)
  except ValueError as e:
    if p_json:
      json_dict.clear()
      if component_name is not None:
        json_dict['component'] = component_name
      json_dict['state'] = "error"
      json_dict['msg'] = str(e)
      print (json.dumps([json_dict]))
    else:
      print("\n" + str(e))
    my_logger.error("Value Error while dowloading file %s (%s)",p_file_name,str(e))
    if file_exists and not f.closed:
      f.close()
    delete_file(file_name_partial)
    file_exists = False
    return(False)
  finally:
    if file_exists and not f.closed:
      f.close()
  delete_file(file_name_complete)
  f.close()
  os.rename(file_name_partial, file_name_complete)
  return(True);


def is_writable(path):
    try:
        testfile = tempfile.TemporaryFile(dir = path)
        testfile.close()
    except (IOError, OSError) as err:
        return False
    return True


## is running with Admin/Root priv's #########################################
def is_admin():
  rc = 0
  if get_platform() == "Windows":
    try:
      import subprocess
      result = subprocess.Popen("net session", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
      std_out, std_err = result.communicate()
      rc = result.returncode
      if rc != 0:
        my_logger.error(std_err)
    except Exception as e:
      my_logger.error(str(e))
      rc = e.errno
  else:
    rc = getoutput("id -u")

  if str(rc) == "0":
    return(True)
  else:
    return(False)


## run command escalated as Windows Administrator ############################
def runas_win_admin(p_cmd, p_wait=True):
    if os.name != 'nt':
        raise RuntimeError("This function is only implemented on Windows.")

    import win32con, win32event, win32process
    from win32com.shell.shell import ShellExecuteEx
    from win32com.shell import shellcon

    list_cmd = p_cmd.split()

    cmd = '"%s"' % (list_cmd[0],)
    params = " ".join(['"%s"' % (x,) for x in list_cmd[1:]])
    cmdDir = ''
    showCmd = win32con.SW_SHOWNORMAL
    lpVerb = 'runas'  # causes UAC elevation prompt.

    procInfo = ShellExecuteEx(nShow=showCmd,
                              fMask=shellcon.SEE_MASK_NOCLOSEPROCESS,
                              lpVerb=lpVerb,
                              lpFile=cmd,
                              lpParameters=params)

    if p_wait:
        procHandle = procInfo['hProcess']
        obj = win32event.WaitForSingleObject(procHandle, win32event.INFINITE)
        rc = win32process.GetExitCodeProcess(procHandle)
    else:
        rc = None

    return rc


def is_protected(p_comp, p_platform):
  if p_comp.startswith("python") or p_comp.startswith("postgres"):
    return True
  return False


def is_server(p_comp):
  try:
    c = cL.cursor()
    sql = "SELECT pidfile, port FROM components WHERE component = ?"
    c.execute(sql,[p_comp])
    data = c.fetchone()
    if data is None:
      return False
  except Exception as e:
    fatal_sql_error(e,sql,"get_comp_state()")

  pidfile = data[0]
  port = data[1]

  if str(pidfile) != "None" and str(pidfile) > " ":
    return True

  if str(port) > "1":
    return True

  return False


def print_error(p_error):
  print('')
  print('ERROR: ' + p_error)
  return


## Get Component Datadir ###################################################
def get_comp_datadir(p_comp):
  try:
    c = cL.cursor()
    sql = "SELECT datadir FROM components WHERE component = ?"
    c.execute(sql,[p_comp])
    data = c.fetchone()
    if data is None:
      return "NotInstalled"
  except Exception as e:
    fatal_sql_error(e,sql,"get_comp_state()")
  if data[0] is None:
    return ""
  return str(data[0])


## Get postgres components installed
def get_installed_postgres_components():
  try:
    c = cL.cursor()
    sql = "SELECT component, project, version, port, datadir, logdir FROM components WHERE project = 'pg' "
    c.execute(sql)
    data = c.fetchall()
    return data
  except Exception as e:
    fatal_sql_error(e, sql, "get_installed_postgres_components()")
  return None


## Get parent component for extension
def get_parent_component(p_ext, p_ver):
  try:
    c = cL.cursor()
    sql = "SELECT parent FROM versions WHERE component = ? "
    if p_ver!=0:
      sql = sql + " AND version = '" + p_ver + "'"
    c.execute(sql,[p_ext])
    data = c.fetchone()
    if data is None:
      return ""
  except Exception as e:
    fatal_sql_error(e, sql, "get_parent_component()")
  return str(data[0])


## Get Component State #####################################################
def get_comp_state(p_comp):
  try:
    c = cL.cursor()
    sql = "SELECT status FROM components WHERE component = ?"
    c.execute(sql,[p_comp])
    data = c.fetchone()
    if data is None:
      return "NotInstalled"
  except Exception as e:
    fatal_sql_error(e,sql,"get_comp_state()")
  return str(data[0])


## Get Component Port ######################################################
def get_comp_port(p_comp):
  try:
    c = cL.cursor()
    sql = "SELECT port FROM components WHERE component = ?"
    c.execute(sql,[p_comp])
    data = c.fetchone()
    if data is None:
      return "-1"
  except Exception as e:
    fatal_sql_error(e,sql,"get_comp_port()")
  return str(data[0])


## Get Component PID File###################################################
def get_comp_pidfile(p_comp):
  try:
    c = cL.cursor()
    sql = "SELECT pidfile FROM components WHERE component = ?"
    c.execute(sql,[p_comp])
    data = c.fetchone()
    if data is None:
      return "-1"
  except Exception as e:
    fatal_sql_error(e,sql,"get_comp_pidfile()")
  return str(data[0])


# Check if the port is in use
def is_socket_busy(p_port, p_comp=''):

  if p_comp > '':
    if get_platform() == "Windows":
      is_ready_file = "pg_isready.exe"
    else:
      is_ready_file = "pg_isready"
    isready = os.path.join(os.getcwd(), p_comp, 'bin', is_ready_file)
    if os.path.isfile(isready):
      rc = os.system(isready + ' -q -p ' + str(p_port))
      if rc == 0:
        return True

  s =  socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  result = s.connect_ex((get_host_ip(), p_port))
  s.close()
  if result == 0:
    return True
  else:
    return False


## Get Component category ######################################################
def get_comp_category(p_comp):
  try:
    c = cL.cursor()
    sql = "SELECT p.category FROM projects p,components c WHERE component = ? and p.project=c.project"
    c.execute(sql,[p_comp])
    data = c.fetchone()
    if data is None:
      return None
  except Exception as e:
    fatal_sql_error(e,sql,"get_comp_port()")
  return data[0]


#get the list for files in a folder recursively:
def get_files_recursively(directory):
  for root, dirs, files in os.walk(directory):
    for basename in files:
      filename = os.path.join(root, basename)
      yield filename


# create the manifest file for the extension
def create_manifest(ext_comp, parent_comp,upgrade=None):
  PARENT_DIR = os.path.join(PGC_HOME, parent_comp)
  COMP_DIR = os.path.join(PGC_HOME, ext_comp)
  if upgrade:
      COMP_DIR=os.path.join(COMP_DIR+"_new", ext_comp)

  manifest = {}
  manifest['component'] = ext_comp
  manifest['parent'] = parent_comp

  target_files = []

  files_list = get_files_recursively(COMP_DIR)
  for file in files_list:
    target_file = file.replace(COMP_DIR, PARENT_DIR)
    target_files.append(target_file)

  manifest['files'] = target_files

  manifest_file_name = ext_comp + ".manifest"

  manifest_file_path = os.path.join(PGC_HOME, "conf", manifest_file_name)

  try:
    with open(manifest_file_path, 'w') as f:
      json.dump(manifest, f, sort_keys = True, indent = 4)
  except Exception as e:
    my_logger.error(str(e))
    my_logger.error(traceback.format_exc())
    print (str(e))
    pass

  return True


#copy the extension files to parent component
def copy_extension_files(ext_comp, parent_comp,upgrade=None):
  PARENT_DIR = os.path.join(PGC_HOME, parent_comp)
  COMP_DIR = os.path.join(PGC_HOME, ext_comp)
  if upgrade:
      COMP_DIR=os.path.join(COMP_DIR+"_new", ext_comp)
  comp_dir_list = os.listdir(COMP_DIR)
  for l in comp_dir_list:
    source = os.path.join(COMP_DIR, l)
    try:
      if os.path.isdir(source):
        target = os.path.join(PARENT_DIR, l)
        copy_tree(source, target, preserve_symlinks=True)
      else:
        shutil.copy(source, PARENT_DIR)
    except Exception as e:
      my_logger.error("Failed to copy " + str(e))
      my_logger.error(traceback.format_exc())
      print (str(e))
      pass

  return True


#Check and delete the files mentioned in the manifest file
def delete_extension_files(manifest_file,upgrade=None):
    my_logger.info("checking for extension files.")
    try:
        with open(manifest_file) as data_file:
            data = json.load(data_file)
    except Exception as e:
        print (str(e))
        exit(1)
    for file in data['files']:
        if os.path.isfile(file) or os.path.islink(file):
            pass
        else:
            continue
        try:
            fp = open(file)
            fp.close()
        except IOError as e:
            if upgrade:
                raise e
            print (str(e))
            exit(1)
    my_logger.info("deleting extension files.")
    for file in data['files']:
        if os.path.isfile(file) or os.path.islink(file):
            pass
        else:
            continue
        try:
            os.remove(file)
        except IOError as e:
            my_logger.error("failed to remove " + file)
            my_logger.error(str(e))
            my_logger.error(traceback.format_exc())
            print (str(e))
    return True


## Get file size in readable format
def get_file_size(file_size,precision=1):
    suffixes=['B','KB','MB','GB','TB']
    suffixIndex = 0
    while file_size > 1024:
        suffixIndex += 1 #increment the index of the suffix
        file_size = file_size/1024.0 #apply the division
    return "%.*f %s"%(precision,file_size,suffixes[suffixIndex])


def get_readable_time_diff(amount, units='seconds', precision=0):

    def process_time(amount, units):

        INTERVALS = [1, 60,
                     60*60,
                     60*60*24,
                     60*60*24*7,
                     60*60*24*7*4,
                     60*60*24*7*4*12]

        NAMES = [('second', 'seconds'),
                 ('minute', 'minutes'),
                 ('hour', 'hours'),
                 ('day', 'days'),
                 ('week', 'weeks'),
                 ('month', 'months'),
                 ('year', 'years')]

        result = []

        unit = list(map(lambda a: a[1], NAMES)).index(units)
        # Convert to seconds
        amount = amount * INTERVALS[unit]

        for i in range(len(NAMES)-1, -1, -1):
            a = amount // INTERVALS[i]
            if a > 0:
                result.append((a, NAMES[i][1 % a]))
                amount -= a * INTERVALS[i]

        return result

    if int(amount)==0:
      return "0 Seconds"
    rd = process_time(int(amount), units)
    cont = 0
    for u in rd:
        if u[0] > 0:
            cont += 1

    buf = ''
    i = 0

    if precision > 0 and len(rd) > 2:
        rd = rd[:precision]
    for u in rd:
        if u[0] > 0:
            buf += "%d %s" % (u[0], u[1])
            cont -= 1

        if i < (len(rd)-1):
            if cont > 1:
                buf += ", "
            else:
                buf += " and "

        i += 1

    return buf


# recursively check and restore all env / extension files during upgrade
def recursively_copy_old_files(dcmp, diff_files=[], ignore=None):
  for name in dcmp.left_only:
    if ignore and name in ignore:
        continue
    try:
      source_file = os.path.join(dcmp.left, name)
      shutil.move(source_file, dcmp.right)
    except Exception as e:
      my_logger.error("Failed to restore the file %s due to %s" % (os.path.join(dcmp.right, name), str(e)))
      my_logger.error(traceback.format_exc())
      diff_files.append([name, dcmp.left, dcmp.right])
  for sub_dcmp in dcmp.subdirs.values():
    allfiles = diff_files
    recursively_copy_old_files(sub_dcmp, allfiles)
  return diff_files


# restore any extensions or env/conf files during upgrade
def restore_conf_ext_files(src, dst, ignore=None):
  if os.path.isdir(dst):
    diff = filecmp.dircmp(src, dst)
    extension_files_list = recursively_copy_old_files(diff, ignore=ignore)
  return True


def check_running_version(ver, running_version):
    try:

        version = semver.parse(ver)
        installed_version = semver.parse(running_version)
        for k in ["major", "minor", "patch"]:
            if installed_version[k] == version[k]:
                continue
            else:
                return False
    except Exception as e:
        return ver.startswith(running_version)
    return True


# create a short link in windows start menu and taskbar
def create_short_link_windows(short_link, target_link, link_desc=None,
                              parent_folder="PostgreSQL",
                              add_to_taskbar=False, logged_user_only=False):
  cmd_file = tempfile.mktemp(".ps1")
  fh = open(cmd_file, "w")
  fh.write('$objShell = New-Object -ComObject ("WScript.Shell")' + '\n')
  shortlink_dir = os.path.join(os.getenv("programdata"), "Microsoft",
                               "Windows", "Start Menu", "Programs",
                               parent_folder)
  if logged_user_only:
    shortlink_dir = os.path.join(os.getenv("appdata"), "Microsoft",
                                 "Windows", "Start Menu", "Programs",
                                 parent_folder)

  if not os.path.exists(shortlink_dir):
    os.mkdir(shortlink_dir)

  shortlink_file = os.path.join(shortlink_dir, short_link)
  fh.write('$objShortCut = $objShell.CreateShortcut("{0}")'.format(shortlink_file) + '\n')
  fh.write('$objShortCut.TargetPath="{0}"'.format(target_link) + '\n')

  if link_desc:
    fh.write('$objShortCut.Description="{0}"'.format(link_desc) + '\n')

  fh.write('$objShortCut.Save()' + '\n')

  # add to taskbar
  if add_to_taskbar:
    fh.write('$Shell = New-Object -ComObject Shell.Application' + '\n')
    fh.write('$FilePath = "{0}"'.format(target_link) + '\n')
    fh.write('$NameSpace = $Shell.NameSpace((Split-Path $FilePath))' + '\n')
    fh.write('$File = $NameSpace.ParseName((Split-Path $FilePath -Leaf))' + '\n')
    fh.write('$verb = $File.Verbs() | ? {$_.Name -eq "Pin to Tas&kbar"}' + '\n')
    fh.write('if ($verb) {$verb.DoIt()}' + '\n')

  fh.close()

  powershell_path = os.path.join(os.getenv("SYSTEMROOT"),
                                 "System32", "WindowsPowerShell",
                                 "v1.0", "powershell.exe")
  command_to_run = "{0} -ExecutionPolicy ByPass -NoProfile {1}".format(powershell_path, cmd_file)
  system(command_to_run, is_admin=True)


# delete the shortlinks
def delete_shortlink_windows(short_link, parent_folder="PostgreSQL"):
    parent_path = os.path.join(os.getenv("programdata"), "Microsoft",
                               "Windows", "Start Menu", "Programs",
                               parent_folder)
    shortlink_path = os.path.join(parent_path, short_link)
    delete_file(shortlink_path)
    if not os.listdir(parent_path):
        delete_dir(parent_path)


# Add the application to launchpad in OSX
def create_shortlink_osx(short_link, target_link):
    short_link_path = os.path.join("/Applications", short_link)
    cmd = "ln -s '{0}' '{1}'".format(target_link, short_link_path)
    os.system(cmd)
    os.system('killall Dock')


# delete the application from launchpad in OSX
def delete_shortlink_osx(short_link):
    short_link_path = os.path.join("/Applications", short_link)
    cmd = "rm '{0}'".format(short_link_path)
    if os.path.exists(short_link_path):
        os.system(cmd)
        os.system('killall Dock')


## MAINLINE ################################################################
cL = sqlite3.connect(PGC_HOME + os.sep + "conf" + os.sep + "pgc_local.db", check_same_thread=False)
