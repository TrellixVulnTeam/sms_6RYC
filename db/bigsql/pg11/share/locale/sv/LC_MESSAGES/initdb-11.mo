��    �      <  �   \
      �  R   �     ,  
   J     U  -   f  @   �  `   �  �   6  W   �  W   Q    �  A   �  5   �  J   (  ?   s     �  6   �  P     C   W  :   �  Q   �  5   (  ]   ^  4   �  B   �  H   4  G   }  >   �  G     4   L  9   �  3   �  ?   �  /   /  -   _  5   �  4   �  >   �  /   7  F   g  y   �  (   (  #   Q  ,   u  -   �  7   �  (     6   1  ,   h  '   �  5   �  F   �  "   :  <   ]  &   �  -   �  -   �  !     1   ?  ?   q  &   �  /   �  +     =   4  !   r  "   �  6   �  +   �       #   1  /   U  0   �  $   �  &   �       $      ~   E  1   �  <   �     3   G   Q   3   �   J   �   �   !     �!      �!  C   "      X"  ,   y"  -   �"  !   �"     �"  J   #  /   Y#  4   �#  R   �#  K   $  "   ]$  !   �$  �   �$  d   (%     �%     �%  �   �%  O   A&  R   �&  K   �&     0'     I'     g'  <   '  ;   �'  �   �'  @   �(  ;   �(    )  u   *  q   �*  f   �*  s   f+  &   �+     ,  t   	,  /   ~,     �,  &   �,  0   �,  .   -  )   D-  )   n-     �-     �-  &   �-  #   �-      .  $   -.  (   R.  +   {.  "   �.     �.  "   �.  !   /  ,   */  $   W/  *   |/  %   �/  !   �/     �/     
0  0   '0     X0     l0     t0     x0     �0  -   �0     �0  &   �0  %   1  3   21     f1     �1  (   �1  b  �1  K    3     l3  
   �3     �3  2   �3  9   �3  q   4  �   �4  J   b5  R   �5  �    6  E    7  1   F7  L   x7  ?   �7     8  =   %8  Q   c8  E   �8  B   �8  U   >9  ;   �9  c   �9  @   4:  D   u:  G   �:  ?   ;  A   B;  K   �;  >   �;  6   <  8   F<  <   <  2   �<  8   �<  <   (=  3   e=  <   �=  6   �=  N   >  ~   \>  ,   �>  (   ?  (   1?  0   Z?  :   �?  (   �?  @   �?  .   0@  *   _@  ?   �@  Q   �@  0   A  ?   MA  '   �A  1   �A  2   �A  #   B  0   >B  F   oB  &   �B  0   �B  /   C  =   >C  '   |C  #   �C  <   �C  /   D  !   5D  .   WD  ,   �D  -   �D  .   �D  3   E     DE  !   dE  |   �E  <   F  @   @F     �F  B   �F  =   �F  c   G  �   �G     CH  !   WH  A   yH     �H  +   �H  ,   I     3I     SI  K   qI  6   �I  8   �I  ^   -J  L   �J  +   �J  '   K  �   -K  T   �K     L  2   &L  �   YL  F   �L  a   %M  C   �M  #   �M  #   �M     N  9   (N  6   bN  �   �N  :   .O  G   iO  .  �O  �   �P  r   eQ  u   �Q  o   NR  /   �R     �R  z   �R  -   wS     �S      �S  -   �S  )   T  %   -T  %   ST     yT     �T  %   �T  $   �T  "   �T  5   U  *   QU  2   |U  #   �U     �U  "   �U  %   V  .   9V  8   hV  4   �V  '   �V     �V     W     5W  4   PW     �W     �W     �W     �W     �W  (   �W     �W  1   X  0   DX  1   uX     �X     �X  3   �X            v   ;   .       �   �   _   �      �       Q       n   <   O       ]      �   �      R   �   9   �   @   t   P       j                  |              g   W   \   q   }              �      4   {      �       ~   �   o          �   c   N       D   0          i          5   *   �   E       �          b   Y   �   '   �   �   )   �                  >   ^           �       6   [   2   �   +   1       S          �   8   �       �   k   J   �           G              F       �       !   ?          /   #       ,   �      �   (   s                         L   �      K   X                   w   
       h   �   B   -               a   $          M       z   f   �       y   H       U   `   "   u   �   I   l       Z         �      7   	      &   3                 �   A   m   p   :   �   V   =   %          T       �   �   C   x   r   d       e       �    
If the data directory is not specified, the environment variable PGDATA
is used.
 
Less commonly used options:
 
Options:
 
Other options:
 
Report bugs to <pgsql-bugs@postgresql.org>.
 
Success. You can now start the database server using:

    %s

 
Sync to disk skipped.
The data directory might become corrupt if the operating system crashes.
 
WARNING: enabling "trust" authentication for local connections
You can change this by editing pg_hba.conf or using the option -A, or
--auth-local and --auth-host, the next time you run initdb.
       --auth-host=METHOD    default authentication method for local TCP/IP connections
       --auth-local=METHOD   default authentication method for local-socket connections
       --lc-collate=, --lc-ctype=, --lc-messages=LOCALE
      --lc-monetary=, --lc-numeric=, --lc-time=LOCALE
                            set default locale in the respective category for
                            new databases (default taken from environment)
       --locale=LOCALE       set default locale for new databases
       --no-locale           equivalent to --locale=C
       --pwfile=FILE         read password for the new superuser from file
       --wal-segsize=SIZE    size of WAL segments, in megabytes
   %s [OPTION]... [DATADIR]
   -?, --help                show this help, then exit
   -A, --auth=METHOD         default authentication method for local connections
   -E, --encoding=ENCODING   set default encoding for new databases
   -L DIRECTORY              where to find the input files
   -N, --no-sync             do not wait for changes to be written safely to disk
   -S, --sync-only           only sync data directory
   -T, --text-search-config=CFG
                            default text search configuration
   -U, --username=NAME       database superuser name
   -V, --version             output version information, then exit
   -W, --pwprompt            prompt for a password for the new superuser
   -X, --waldir=WALDIR       location for the write-ahead log directory
   -d, --debug               generate lots of debugging output
   -g, --allow-group-access  allow group read/execute on data directory
   -k, --data-checksums      use data page checksums
   -n, --no-clean            do not clean up after errors
   -s, --show                show internal settings
  [-D, --pgdata=]DATADIR     location for this database cluster
 %s initializes a PostgreSQL database cluster.

 %s: "%s" is not a valid server encoding name
 %s: WAL directory "%s" not removed at user's request
 %s: WAL directory location must be an absolute path
 %s: WARNING: cannot create restricted tokens on this platform
 %s: argument of --wal-segsize must be a number
 %s: argument of --wal-segsize must be a power of 2 between 1 and 1024
 %s: cannot be run as root
Please log in (using, e.g., "su") as the (unprivileged) user that will
own the server process.
 %s: could not access directory "%s": %s
 %s: could not access file "%s": %s
 %s: could not allocate SIDs: error code %lu
 %s: could not change permissions of "%s": %s
 %s: could not change permissions of directory "%s": %s
 %s: could not create directory "%s": %s
 %s: could not create restricted token: error code %lu
 %s: could not create symbolic link "%s": %s
 %s: could not execute command "%s": %s
 %s: could not find suitable encoding for locale "%s"
 %s: could not find suitable text search configuration for locale "%s"
 %s: could not fsync file "%s": %s
 %s: could not get exit code from subprocess: error code %lu
 %s: could not open directory "%s": %s
 %s: could not open file "%s" for reading: %s
 %s: could not open file "%s" for writing: %s
 %s: could not open file "%s": %s
 %s: could not open process token: error code %lu
 %s: could not re-execute with restricted token: error code %lu
 %s: could not read directory "%s": %s
 %s: could not read password from file "%s": %s
 %s: could not rename file "%s" to "%s": %s
 %s: could not start process for command "%s": error code %lu
 %s: could not stat file "%s": %s
 %s: could not write file "%s": %s
 %s: data directory "%s" not removed at user's request
 %s: directory "%s" exists but is not empty
 %s: encoding mismatch
 %s: failed to remove WAL directory
 %s: failed to remove contents of WAL directory
 %s: failed to remove contents of data directory
 %s: failed to remove data directory
 %s: failed to restore old locale "%s"
 %s: file "%s" does not exist
 %s: file "%s" is not a regular file
 %s: input file "%s" does not belong to PostgreSQL %s
Check your installation or specify the correct path using the option -L.
 %s: input file location must be an absolute path
 %s: invalid authentication method "%s" for "%s" connections
 %s: invalid locale name "%s"
 %s: invalid locale settings; check LANG and LC_* environment variables
 %s: locale "%s" requires unsupported encoding "%s"
 %s: must specify a password for the superuser to enable %s authentication
 %s: no data directory specified
You must identify the directory where the data for this database system
will reside.  Do this with either the invocation option -D or the
environment variable PGDATA.
 %s: out of memory
 %s: password file "%s" is empty
 %s: password prompt and password file cannot be specified together
 %s: removing WAL directory "%s"
 %s: removing contents of WAL directory "%s"
 %s: removing contents of data directory "%s"
 %s: removing data directory "%s"
 %s: setlocale() failed
 %s: superuser name "%s" is disallowed; role names cannot begin with "pg_"
 %s: symlinks are not supported on this platform %s: too many command-line arguments (first is "%s")
 %s: warning: specified text search configuration "%s" might not match locale "%s"
 %s: warning: suitable text search configuration for locale "%s" is unknown
 Data page checksums are disabled.
 Data page checksums are enabled.
 Encoding "%s" implied by locale is not allowed as a server-side encoding.
The default database encoding will be set to "%s" instead.
 Encoding "%s" is not allowed as a server-side encoding.
Rerun %s with a different locale selection.
 Enter it again:  Enter new superuser password:  If you want to create a new database system, either remove or empty
the directory "%s" or run %s
with an argument other than "%s".
 If you want to store the WAL there, either remove or empty the directory
"%s".
 It contains a dot-prefixed/invisible file, perhaps due to it being a mount point.
 It contains a lost+found directory, perhaps due to it being a mount point.
 Passwords didn't match.
 Rerun %s with the -E option.
 Running in debug mode.
 Running in no-clean mode.  Mistakes will not be cleaned up.
 The database cluster will be initialized with locale "%s".
 The database cluster will be initialized with locales
  COLLATE:  %s
  CTYPE:    %s
  MESSAGES: %s
  MONETARY: %s
  NUMERIC:  %s
  TIME:     %s
 The default database encoding has accordingly been set to "%s".
 The default text search configuration will be set to "%s".
 The encoding you selected (%s) and the encoding that the
selected locale uses (%s) do not match.  This would lead to
misbehavior in various character string processing functions.
Rerun %s and either do not specify an encoding explicitly,
or choose a matching combination.
 The files belonging to this database system will be owned by user "%s".
This user must also own the server process.

 The program "postgres" is needed by %s but was not found in the
same directory as "%s".
Check your installation.
 The program "postgres" was found by "%s"
but was not the same version as %s.
Check your installation.
 This might mean you have a corrupted installation or identified
the wrong directory with the invocation option -L.
 Try "%s --help" for more information.
 Usage:
 Using a mount point directly as the data directory is not recommended.
Create a subdirectory under the mount point.
 cannot duplicate null pointer (internal error)
 caught signal
 child process exited with exit code %d child process exited with unrecognized status %d child process was terminated by exception 0x%X child process was terminated by signal %d child process was terminated by signal %s command not executable command not found could not change directory to "%s": %s could not close directory "%s": %s
 could not find a "%s" to execute could not get junction for "%s": %s
 could not identify current directory: %s could not look up effective user ID %ld: %s could not open directory "%s": %s
 could not read binary "%s" could not read directory "%s": %s
 could not read symbolic link "%s" could not remove file or directory "%s": %s
 could not set junction for "%s": %s
 could not stat file or directory "%s": %s
 could not write to child process: %s
 creating configuration files ...  creating directory %s ...  creating subdirectories ...  fixing permissions on existing directory %s ...  invalid binary "%s" logfile ok
 out of memory
 pclose failed: %s performing post-bootstrap initialization ...  running bootstrap script ...  selecting default max_connections ...  selecting default shared_buffers ...  selecting dynamic shared memory implementation ...  syncing data to disk ...  user does not exist user name lookup failure: error code %lu Project-Id-Version: PostgreSQL 10
Report-Msgid-Bugs-To: pgsql-bugs@postgresql.org
POT-Creation-Date: 2018-04-28 22:16+0000
PO-Revision-Date: 2018-08-26 07:42+0200
Last-Translator: Dennis Björklund <db@zigo.dhs.org>
Language-Team: Swedish <sv@li.org>
Language: sv
MIME-Version: 1.0
Content-Type: text/plain; charset=UTF-8
Content-Transfer-Encoding: 8bit
 
Om datakatalogen inte anges så tas den från omgivningsvariabeln PGDATA.
 
Mindre vanliga flaggor:
 
Flaggor:
 
Andra flaggor:
 
Rapportera fel till <pgsql-bugs@postgresql.org>.
 
Lyckades. Du kan nu starta databasservern med:

    %s

 
Avstod från synkning mot lagringsmedium.
Datakatalogen kan komma att fördärvas om operativsystemet störtar.
 
VARNING: Autentiseringsmetod "trust" är aktiv för någon uppkoppling.
Du kan ändra detta genom att redigera "pg_hba.conf" eller genom att sätta
flaggor -A eller --auth-local och --auth-host nästa gång du kör initdb.
       --auth-host=METOD     autentiseringsmetod för TCP/IP-förbindelser
       --auth-local=METOD    autentiseringsmetod för förbindelser via unix-uttag
       --lc-collate=, --lc-ctype=, --lc-messages=LOKAL
      --lc-monetary=, --lc-numeric=, --lc-time=LOKAL
                            sätter standardlokal i utvald kategori för
                            nya databaser (förval hämtas ur omgivningen)
       --locale=LOKAL        sätter standardlokal för nya databaser
       --no-locale           samma som --locale=C
       --pwfile=FIL          läser lösenord för superanvändare från fil
       --wal-segsize=STORLEK storlek på WAL-segment i megabyte
   %s [FLAGGA]... [DATAKATALOG]
   -?, --help                visa denna hjälp, avsluta sedan
   -A, --auth=METOD          förvald autentiseringsmetod för alla förbindelser
   -E, --encoding=KODNING    sätter teckenkodning för nya databaser
   -L KATALOG                katalog där indatafiler skall sökas
   -N, --no-sync             vänta inte på att ändingar säkert skrivits till disk
   -S, --sync-only           synkning endast av datakatalog
   -T, --text-search-config=CFG
                            standardkonfiguration för textsökning
   -U, --username=NAMN       namn på databasens superanvändare
   -V, --version             visa versionsinformation, avsluta sedan
   -W, --pwprompt            efterfråga lösenord för superanvändare
   -X, --waldir=WALDIR       katalog för write-ahead-log (WAL)
   -d, --debug               generera massor med debug-utskrifter
   -g, --allow-group-access  tillåt läs/kör för grupp på datakatalogen
   -k, --data-checksums      använd checksummor på datablock
   -n, --no-clean            städa inte upp efter fel
   -s, --show                visa interna inställningar
  [-D, --pgdata=]DATAKATALOG läge för detta databaskluster
 %s initierar ett databaskluster för PostgreSQL.

 %s: "%s" är inte en giltig teckenkodning för servern.
 %s: WAL-katalog "%s" ej borttagen på användares begäran.
 %s: WAL-katalogen måste vara en absolut sökväg.
 %s: VARNING: "Restricted Token" stöds inte av plattformen.
 %s: argumentet till --wal-segsize måste vara ett tal
 %s: argumentet till --wal-segsize måste vara en tvåpotens mellan 1 och 1024
 %s: kan inte köras som root
Logga in (t.ex. med "su") som den (opriviligerade) användare
vilken skall äga serverprocessen.
 %s: kunde inte komma åt katalogen "%s": %s
 %s: kunde inte komma åt filen "%s": %s
 %s: kunde inte tilldela SID: felkod %lu
 %s: kunde inte ändra rättigheter på "%s": %s
 %s: kunde inte ändra rättigheter på katalogen "%s": %s
 %s: kunde inte skapa katalogen "%s": %s
 %s: kunde inte skapa restriktivt styrmärke (token): felkod %lu
 %s: kunde inte skapa symbolisk länk "%s": %s
 %s: kunde inte utföra kommandot "%s": %s
 %s: kunde inte välja en lämplig kodning för lokalnamn "%s".
 %s: kunde inte hitta en lämplig textsökningskonfiguration för lokalnamn "%s".
 %s: kunde inte utföra fsync på filen "%s": %s
 %s: kunde inte utvinna statuskod för underprocess: felkod %lu
 %s: kunde inte öppna katalog "%s": %s
 %s: kunde inte öppna fil "%s" för läsning: %s
 %s: kunde inte öppna fil "%s" för skrivning: %s
 %s: kunde inte öppna fil "%s": %s
 %s: kunde inte öppna process-token: felkod %lu
 %s: kunde inte upprepa med restriktivt styrmärke (token): felkod %lu
 %s: kunde inte läsa katalog "%s": %s
 %s: kunde inte läsa lösenord i filen "%s": %s
 %s: kunde inte döpa om fil "%s" till "%s": %s
 %s: kunde inte starta process för kommando "%s": felkod %lu
 %s: kunde ta status på filen "%s": %s
 %s: kunde inte skriva fil "%s": %s
 %s: Datakatalog "%s" ej borttagen på användares begäran.
 %s: katalogen "%s" existerar men är inte tom.
 %s: Oförenliga teckenkodningar.
 %s: misslyckades med att ta bort WAL-katalog.
 %s: misslyckades med att tömma WAL-katalog
 %s: misslyckades med att tömma datakatalog.
 %s: misslyckades med att ta bort datakatalog.
 %s: misslyckades att återställa lokalspråk "%s"
 %s: Filen "%s" existerar inte.
 %s: "%s" är inte en normal fil.
 %s: Indatafilen "%s" hör inte till PostgreSQL %s.
Kontrollera din installation eller ange korrekt sökväg med flaggan -L.
 %s: plats för indatafiler måste vara en absolut sökväg.
 %s: Ogiltig autentiseringsmetod "%s" vid förbindelseslag "%s".
 %s: okänt lokalnamn "%s".
 %s: ogiltigt språkval. Kontrollera miljövariablerna LANG, LC_*.
 %s: Lokalnamn "%s" kräver otillgänglig teckenkodning "%s".
 %s: Du måste ange ett lösenord för superanvändaren för att
kunna slå på autentisering "%s".
 %s: Ingen datakatalog angiven.
Du måste uppge den katalog där data för detta databassystem
skall lagras. Gör det antingen med flaggan -D eller genom att
sätta omgivningsvariabeln PGDATA.
 %s: slut på minne
 %s: lösenordsfilen "%s" är tom
 %s: lösenordsfråga och lösenordsfil kan inte anges samtidigt.
 %s: tar bort WAL-katalog "%s"
 %s: tömmer innehållet i WAL-katalog "%s"
 %s: tömmer innehållet i datakatalog "%s".
 %s: tar bort datakatalog "%s".
 %s: setlocale() misslyckades
 %s: superuser-namn "%s" tillåts inte; rollnamn får inte börja på "pg_"
 %s: symboliska länkar stöds inte på denna plattform %s: för många kommandoradsargument (första är "%s")
 %s: Varning: Uppgiven textsökningskonfiguration "%s" passar
kanske inte till lokalnamn "%s".
 %s: Varning: Ingen lämplig textsökningskonfiguration för lokalnamn "%s".
 Checksummor för datablock är avstängda.
 Checksummor för datablock är aktiva.
 Teckenkodning "%s", tagen ur lokalnamnet, är inte godtagbar för servern.
I dess ställe sättes databasens förvalda teckenkodning till "%s".
 Teckenkodning "%s" är inte godtagbar för servern.
Upprepa %s med annat lokalnamn.
 Mata in det igen:  Mata in ett nytt lösenord för superanvändaren:  Om du vill skapa ett nytt databassystem, tag då antingen bort
eller töm katalogen "%s" eller kör %s
med annat argument än "%s".
 Om du vill spara WAL där, antingen radera eller töm
katalogen "%s".
 Den innehåller en gömd fil, med inledande punkt i namnet; kanske är detta en monteringspunkt.
 Den innehåller "lost+found"; kanske är detta en monteringspunkt.
 Lösenorden stämde inte överens.
 Upprepa %s, men nu med flaggan -E.
 Kör i debug-läge.
 Kör i no-clean-läge. Misstag kommer inte städas bort.
 Databasklustret kommer att skapas med lokalnamn "%s".
 Databasklustret kommer att initieras med lokalkategorier:
  COLLATE:  %s
  CTYPE:    %s
  MESSAGES: %s
  MONETARY: %s
  NUMERIC:  %s
  TIME:     %s
 Förvald teckenkodning för databaser är satt till "%s".
 Förvald textsökningskonfiguration för databaser är satt till "%s".
 Teckenkodningen du har valt (%s) och kodningen svarande
mot lokalnamnet (%s), de passar inte ihop. Detta kan leda
till problem för funktioner som arbetar med strängar. Detta
undgås genom att utföra %s igen och då låta bli bli att
sätta kodning, eller i annat fall att välja bättre teckensats.
 Filer tillhörande databasen kommer att ägas av användaren "%s".
Denna användare måste också vara ägare av server-processen.

 Programmet "postgres" behövs av %s men kunde inte hittas
i samma katalog som "%s".
Kontrollera din installation.
 Programmet "postgres" hittades av "%s",
men det är inte byggt i samma version som %s.
Kontrollera din installation.
 Detta kan betyda att du har en korrupt installation eller att du har
angivit felaktig katalog till flaggan -L.
 Försök med "%s --help" för mer information.
 Användning:
 Att använda en monteringspunkt som datakatalog rekommenderas inte.
Skapa först en underkatalog under monteringspunkten.
 kan inte duplicera null-pekare (internt fel)
 mottog signal
 barnprocess avslutade med kod %d barnprocess avslutade med okänd statuskod %d barnprocess terminerades med avbrott 0x%X barnprocess terminerades av signal %d barnprocess terminerades av signal %s kommandot är inte körbart kommandot kan ej hittas kunde inte byta katalog till "%s": %s kunde inte stänga katalog "%s": %s
 kunde inte hitta en "%s" att köra kunde inte få en knutpunkt (junction) för "%s": %s
 kunde inte identifiera aktuell katalog: %s kunde inte slå upp effektivt användar-id %ld: %s kunde inte öppna katalog "%s": %s
 kunde inte läsa binär "%s" kunde inte läsa katalog "%s": %s
 kunde inte läsa symbolisk länk "%s" kunde inte ta bort fil eller katalog "%s": %s
 kunde inte sätta en knutpunkt (junction) för "%s": %s
 kunde inte ta status på fil eller katalog "%s": %s
 kunde inte skriva till barnprocess: %s
 skapar konfigurationsfiler ...  skapar katalog %s ...  Skapar underkataloger ...  sätter rättigheter på existerande katalog %s ...  ogiltig binär "%s" loggfil ok
 slut på minne
 pclose misslyckades: %s utför initiering efter uppstättning... kör uppsättningsskript... sätter förvalt värde för max_connections ...  sätter förvalt värde för shared_buffers ...  väljer mekanism för dynamiskt, delat minne ...  synkar data till disk ...  användaren finns inte misslyckad sökning efter användarnamn: felkod %lu 