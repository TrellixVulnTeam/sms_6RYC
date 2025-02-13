from __future__ import print_function, division
 
####################################################################
######          Copyright (c)  2015-2018 BigSQL           ##########
####################################################################

import argparse, util, os, sys, shutil, subprocess, getpass, json
import startup

PGC_HOME = os.getenv('PGC_HOME', '')

sys.path.append(os.path.join(PGC_HOME, 'hub', 'scripts', 'lib'))

from ConsoleLogger import ConsoleLogger


def fatal_error(p_msg):
  if isJson:
    sys.stdout = previous_stdout
    jsonMsg = {}
    jsonMsg['status'] = "error"
    jsonMsg['msg'] = p_msg
    print(json.dumps([jsonMsg]))
  else:
    print(p_msg)
  sys.exit(1)
  return

#######################################################
##                     MAINLINE                      ##
#######################################################
pgver = "pg11"

app_datadir = util.get_comp_datadir(pgver)
update_install_date=False
if app_datadir == "":
  update_install_date=True

parser = argparse.ArgumentParser()
parser.add_argument("--datadir", type=str, default="")
parser.add_argument("--svcuser", type=str, default="")
parser.add_argument("--port", type=int, default=0)
parser.add_argument("--options", type=str, default="")
parser.add_argument("--pwfile", type=str, default="")
args = parser.parse_args()


isSilent = os.getenv("isSilent", None)

## Initialize the ConsoleLogger to redirect the console output log file
previous_stdout = sys.stdout
sys.stdout = ConsoleLogger()

isJson = os.getenv("isJson", None)

pg_home = os.path.join(PGC_HOME, pgver)

print(" ")
print("## Initializing " + pgver + " #######################")

## PORT ###############################################
if args.port > 0:
  i_port = args.port
else:
  i_port =  util.get_avail_port("PG Port", 5432, pgver)

## DATA ###############################################
data_root = os.path.join(PGC_HOME, "data")
if not os.path.isdir(data_root):
  os.mkdir(data_root)
if args.datadir == "":
  pg_data = os.path.join(data_root, pgver)
else:
  pg_data = args.datadir

if os.path.isdir(pg_data):
  if not os.listdir(pg_data) == []:
    fatal_error("ERROR: datadir not empty - " + pg_data)
else:
  os.mkdir(pg_data)

## SVCUSER ###########################################
svcuser = ""
curr_user = ""
if util.get_platform() == "Linux":
  svcuser = args.svcuser
  if util.is_admin() :
    if svcuser == "":
      svcuser="postgres"
  else:
    if svcuser > "":
      fatal_error("ERROR: --svcuser cannot be specified if not root")
    svcuser = util.get_user()
    curr_user = svcuser

## PASSWD #############################################
is_password=False
pgpass_file = pg_home + os.sep + ".pgpass"
if args.pwfile:
  pgpass_file = args.pwfile
  if not os.path.isfile(pgpass_file):
    fatal_error("Error: Invalid --pwfile")

if os.path.isfile(pgpass_file):
  is_password=True
  file = open(pgpass_file, 'r')
  line = file.readline()
  pg_password = line.rstrip()
  file.close()
else:
  if not isSilent:
    pg_password = util.get_superuser_passwd()
    file = open(pgpass_file, 'w')
    file.write(pg_password + '\n')
    file.close()
    is_password=True

if is_password:
  os.chmod(pgpass_file, 0o600)

## LOGS ###############################################
data_root_logs = os.path.join(data_root, "logs")
if not os.path.isdir(data_root_logs):
  os.mkdir(data_root_logs)
pg_log = os.path.join(data_root_logs, pgver)
if not os.path.isdir(pg_log):
  os.mkdir(pg_log)

## PERMISSIONS ########################################
print("Setting directory and file permissions.")
if util.get_platform() == "Windows":
  cur_user = getpass.getuser()
  batcmd = 'icacls "' + pg_data + '" /grant "' + cur_user + \
           '":(OI)(CI)F'
  err = os.system(batcmd)
  if err:
    msg = "ERROR: Unable to set permissions on data dir " + \
          " (err=" + str(err) + ")"
    fatal_error(msg)
  print("setting permission to log dir")
  cur_user = getpass.getuser()
  batcmd = 'icacls "' + pg_log + '" /grant "' + cur_user + \
           '":(OI)(CI)F'
  err = os.system(batcmd)
  if err:
    msg = "ERROR: Unable to set permissions on log dir " + \
          " (err=" + str(err) + ")"
    fatal_error(msg)
else:
  if util.is_admin():
    chown_cmd = "chown " + svcuser + ":" + svcuser
    if util.get_platform() == "Linux":
      if not startup.user_exists(svcuser):
        startup.useradd_linux(svcuser)
      os.system(chown_cmd + " " + pg_data)
    os.system(chown_cmd + " " + pgpass_file)
    os.system(chown_cmd + " " + pg_log)
  os.chmod(pg_data, 0o600)


logfile = os.path.join(pg_log, "install.log")

## INITDB #############################################
print(' ')
print('Initializing Postgres DB with:')
initdb_cmd = os.path.join(pg_home, 'bin', 'initdb')

# default to utf8 across platforms
if args.options == "":
  init_options = '-E UTF8 --no-locale'
else:
  init_options = args.options

# Does the user want to assign a password ?
if is_password:
  batcmd = initdb_cmd + ' -U postgres -A md5 ' + init_options + \
           ' -D "' + pg_data + '" ' + \
           '--pwfile="' + pgpass_file + '" > "' + logfile + '" 2>&1'
else:
  # If not, use -A ident (actually sets peer for local and ident for loopback)
  batcmd = initdb_cmd + ' -U postgres -A ident ' + init_options + \
           ' -D "' + pg_data + '" ' + \
           ' > "' + logfile + '" 2>&1'

if svcuser > "" and svcuser != curr_user:
  batcmd = "sudo su - " + svcuser + " -c '" + batcmd + "'"

print('  ' + batcmd)
err = os.system(batcmd)


if err:
  msg = "ERROR: Unable to Initialize PG. see logfile: " + logfile
  fatal_error(msg)

util.set_column('datadir', pgver, pg_data)
util.set_column('svcuser', pgver, svcuser)
util.set_column('logdir', pgver, pg_log)

util.update_postgresql_conf(pgver, i_port, update_listen_addr=is_password)

if is_password:
  pg_pass_file = util.remember_pgpassword(pg_password, str(i_port))
else:
  pg_pass_file=None

util.write_pgenv_file(pg_home, pgver, pg_data, 'postgres', 'postgres', str(i_port), pg_pass_file)

if is_password:
  src_dir = pg_home + os.sep + "init" + os.sep
  shutil.copy(src_dir + "pg_hba.conf", pg_data)

if is_password:
  os.remove(pgpass_file)

if isJson:
  sys.stdout = previous_stdout
  msg = '[{"status":"complete","msg":"Initialization completed.","component":"' + pgver + '"}]'
  print(msg)

if update_install_date:
  util.update_installed_date(pgver)

if util.get_platform() == 'Linux' and util.is_admin():
  systemsvc = 'postgresql' + pgver[2:4]
  start_lvl = '85'
  kill_lvl  = '15'
  pg_ctl = os.path.join(PGC_HOME, pgver, 'bin', 'pg_ctl')
  cmd_start  = pg_ctl + ' start  -D ' + pg_data + ' -s -w -t 300'
  cmd_stop   = pg_ctl + ' stop   -D ' + pg_data + ' -s -m fast'
  cmd_reload = pg_ctl + ' reload -D ' + pg_data + ' -s'
  cmd_status = pg_ctl + ' status -D ' + pg_data
  cmd_log = '-l ' + pg_data + '/pgstartup.log'
  startup.config_linux(pgver, systemsvc, start_lvl, kill_lvl, svcuser,
                         cmd_start, cmd_log, cmd_stop, cmd_reload, cmd_status)
  util.set_column('svcname', pgver, systemsvc)
  util.set_column('autostart', pgver, 'on')
