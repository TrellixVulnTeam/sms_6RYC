Þ    p                 p	     q	  9   	  -   Å	  D   ó	  ;   8
  B   t
  G   ·
  º   ÿ
  ?   º  9   ú  K   4  I     I   Ê  .     9   C  0   }  +   ®     Ú  >   ö  /   5  F   e  !   ¬  ,   Î  +   û  '   '  )   O  6   y  #   °  <   Ô  &     -   8  !   f  1     ?   º  &   ú  !   !  5   C  =   y  "   ·  (   Ú  z        ~  #     \   ·  +     0   @      q  2     @   Å  B     ¦   I  4   ð  G   %  &   m  -        Â     â  )   ò  )     )   F     p  )     )   ·  )   á  )     )   5  )   _  )        ³  V   Ð  )   '  )   Q  )   {  ,   ¥  )   Ò  )   ü  )   &  )   P  )   z  )   ¤  )   Î  )   ø  )   "  )   L  )   v  )      )   Ê  )   ô  )     )   H  )   r  )     )   Æ  )   ð  )     )   D  	   n  )   x      ¢  &   C  !   j  )        ¶  -   Í     û       )        ;  )   ?     i  )   l  Á       X   d   p   J   Õ   J    !  R   k!     ¾!  X   N"  í   §"  ]   #  F   ó#  [   :$     $  a   %%  =   %  T   Å%  =   &  G   X&  4    &  a   Õ&  C   7'  [   {'  &   ×'  G   þ'  @   F(  H   (  @   Ð(  V   )  :   h)  e   £)  F   	*  R   P*  @   £*  \   ä*  F   A+  R   +  :   Û+  I   ,  `   `,  :   Á,  @   ü,  Ò   =-     .  0   (.  ±   Y.  T   /  S   `/  >   ´/  `   ó/  \   T0  n   ±0      1  D    1  X   å1  K   >2  N   2  '   Ù2     3  @   3  9   T3  7   3     Æ3  >   ã3  9   "4  9   \4  6   4  <   Í4  2   
5  2   =5     p5  }   5  7   6  7   F6  7   ~6  :   ¶6  =   ñ6  7   /7  7   g7  7   7  7   ×7  8   8  7   H8  8   8  7   ¹8  8   ñ8  8   *9  3   c9  8   9  ,   Ð9  ,   ý9  ,   *:  .   W:  ,   :  -   ³:  ,   á:  -   ;  ,   <;     i;  =   {;    ¹;  3   Ó<  (   =  4   0=  7   e=  O   =     í=  	   ú=  ,   >     1>  ,   8>     e>  3   l>     <   X   h   S      p      D       N      ]   Q   /              E      $   C   \   e   Y   ;   3              k   W      )       
   (   H          b   .          T   "   `           j   2   4   m   @   _      R   B   V   :             6           a   #          n                Z       &   *             d         L   +   f       %   !         9   1       8   0   o   K   U   i                     7   J           =   G      O       ^       M      -      l           >                   c   '      F       A   	       I       P       [       g   5   ?   ,        

Values to be changed:

 
If these values seem acceptable, use -f to force reset.
 
Report bugs to <pgsql-bugs@postgresql.org>.
       --wal-segsize=SIZE         size of WAL segments, in megabytes
   -?, --help                     show this help, then exit
   -O, --multixact-offset=OFFSET  set next multitransaction offset
   -V, --version                  output version information, then exit
   -c, --commit-timestamp-ids=XID,XID
                                 set oldest and newest transactions bearing
                                 commit timestamp (zero means no change)
   -e, --epoch=XIDEPOCH           set next transaction ID epoch
   -f, --force                    force update to be done
   -l, --next-wal-file=WALFILE    set minimum starting location for new WAL
   -m, --multixact-ids=MXID,MXID  set next and oldest multitransaction ID
   -n, --dry-run                  no update, just show what would be done
   -o, --next-oid=OID             set next OID
   -x, --next-transaction-id=XID  set next transaction ID
  [-D, --pgdata=]DATADIR          data directory
 %s resets the PostgreSQL write-ahead log.

 %s: OID (-o) must not be 0
 %s: WARNING: cannot create restricted tokens on this platform
 %s: argument of --wal-segsize must be a number
 %s: argument of --wal-segsize must be a power of 2 between 1 and 1024
 %s: cannot be executed by "root"
 %s: could not allocate SIDs: error code %lu
 %s: could not change directory to "%s": %s
 %s: could not close directory "%s": %s
 %s: could not create pg_control file: %s
 %s: could not create restricted token: error code %lu
 %s: could not delete file "%s": %s
 %s: could not get exit code from subprocess: error code %lu
 %s: could not open directory "%s": %s
 %s: could not open file "%s" for reading: %s
 %s: could not open file "%s": %s
 %s: could not open process token: error code %lu
 %s: could not re-execute with restricted token: error code %lu
 %s: could not read directory "%s": %s
 %s: could not read file "%s": %s
 %s: could not read permissions of directory "%s": %s
 %s: could not start process for command "%s": error code %lu
 %s: could not write file "%s": %s
 %s: could not write pg_control file: %s
 %s: data directory is of wrong version
File "%s" contains "%s", which is not compatible with this program's version "%s".
 %s: fsync error: %s
 %s: invalid argument for option %s
 %s: lock file "%s" exists
Is a server running?  If not, delete the lock file and try again.
 %s: multitransaction ID (-m) must not be 0
 %s: multitransaction offset (-O) must not be -1
 %s: no data directory specified
 %s: oldest multitransaction ID (-m) must not be 0
 %s: pg_control exists but has invalid CRC; proceed with caution
 %s: pg_control exists but is broken or wrong version; ignoring it
 %s: pg_control specifies invalid WAL segment size (%d byte); proceed with caution
 %s: pg_control specifies invalid WAL segment size (%d bytes); proceed with caution
 %s: too many command-line arguments (first is "%s")
 %s: transaction ID (-c) must be either 0 or greater than or equal to 2
 %s: transaction ID (-x) must not be 0
 %s: transaction ID epoch (-e) must not be -1
 %s: unexpected empty file "%s"
 64-bit integers Blocks per segment of large relation: %u
 Bytes per WAL segment:                %u
 Catalog version number:               %u
 Current pg_control values:

 Data page checksum version:           %u
 Database block size:                  %u
 Database system identifier:           %s
 Date/time type storage:               %s
 First log segment after reset:        %s
 Float4 argument passing:              %s
 Float8 argument passing:              %s
 Guessed pg_control values:

 If you are sure the data directory path is correct, execute
  touch %s
and try again.
 Latest checkpoint's NextMultiOffset:  %u
 Latest checkpoint's NextMultiXactId:  %u
 Latest checkpoint's NextOID:          %u
 Latest checkpoint's NextXID:          %u:%u
 Latest checkpoint's TimeLineID:       %u
 Latest checkpoint's full_page_writes: %s
 Latest checkpoint's newestCommitTsXid:%u
 Latest checkpoint's oldestActiveXID:  %u
 Latest checkpoint's oldestCommitTsXid:%u
 Latest checkpoint's oldestMulti's DB: %u
 Latest checkpoint's oldestMultiXid:   %u
 Latest checkpoint's oldestXID's DB:   %u
 Latest checkpoint's oldestXID:        %u
 Maximum columns in an index:          %u
 Maximum data alignment:               %u
 Maximum length of identifiers:        %u
 Maximum size of a TOAST chunk:        %u
 NextMultiOffset:                      %u
 NextMultiXactId:                      %u
 NextOID:                              %u
 NextXID epoch:                        %u
 NextXID:                              %u
 OldestMulti's DB:                     %u
 OldestMultiXid:                       %u
 OldestXID's DB:                       %u
 OldestXID:                            %u
 Options:
 Size of a large-object chunk:         %u
 The database server was not shut down cleanly.
Resetting the write-ahead log might cause data to be lost.
If you want to proceed anyway, use -f to force reset.
 Try "%s --help" for more information.
 Usage:
  %s [OPTION]... DATADIR

 WAL block size:                       %u
 Write-ahead log reset
 You must run %s as the PostgreSQL superuser.
 by reference by value newestCommitTsXid:                    %u
 off oldestCommitTsXid:                    %u
 on pg_control version number:            %u
 Project-Id-Version: PostgreSQL 10
Report-Msgid-Bugs-To: pgsql-bugs@postgresql.org
POT-Creation-Date: 2018-08-31 16:21+0900
PO-Revision-Date: 2018-08-20 16:55+0900
Last-Translator: Kyotaro Horiguchi <horiguchi.kyotaro@lab.ntt.co.jp>
Language-Team: jpug-doc <jpug-doc@ml.postgresql.jp>
Language: ja
MIME-Version: 1.0
Content-Type: text/plain; charset=UTF-8
Content-Transfer-Encoding: 8bit
Plural-Forms: nplurals=1; plural=0;
X-Generator: Poedit 1.5.4
 

å¤æ´ãããå¤:

 
ãã®å¤ã§é©åã¨å¤æ­ããã®ã§ããã°ã-fã§ãªã»ãããå¼·å¶ãã¦ãã ããã
 
ä¸å·åã¯<pgsql-bugs@postgresql.org>ã¾ã§å ±åãã¦ãã ããã
       --wal-segsize=SIZE         WALã»ã°ã¡ã³ãã®ãµã¤ãº(MBåä½)
   -?, --help                     ãã®ãã«ããè¡¨ç¤ºãã¦ãçµäºãã¾ã
   -O, --multixact-offset=OFFSET  æ¬¡ã®ãã«ããã©ã³ã¶ã¯ã·ã§ã³ã®ãªãã»ãããè¨­å®ã
                                 ã¾ã
   -V, --version                  ãã¼ã¸ã§ã³æå ±ãè¡¨ç¤ºãã¦ãçµäºãã¾ã
   -c, --commit-timestamp-ids=XID,XID
                                 ã³ãããã¿ã¤ã ã¹ã¿ã³ããä»ä¸ããã¦ããæå¤ã¨
                                 ææ°ã®ãã©ã³ã¶ã¯ã·ã§ã³ãè¨­å® (ã¼ã­ã¯å¤æ´ãªã)
   -e, --epoch=XIDEPOCH           æ¬¡ã®ãã©ã³ã¶ã¯ã·ã§ã³IDã®èµ·ç¹ãè¨­å®ãã¾ã
   -f, --force                    å¼·å¶çã«æ´æ°ãå®æ½ãã¾ã
   -l, --next-wal-file=WALFILE    æ°ããWALã®æå°éå§ãã¤ã³ããæå®ãã¾ã
   -m, --multixact-ids=MXID,MXID  æ¬¡ããã³æå¤ã®ãã«ããã©ã³ã¶ã¯ã·ã§ã³IDãè¨­å®ã
                                 ã¾ã
   -n, --dry-run                  æ´æ°ããããåã«ä½ãè¡ãªããããè¡¨ç¤ºãã¾ã
   -o, --next-oid=OID             æ¬¡ã®OIDãè¨­å®ãã¾ã
   -x, --next-transaction-id=XID  æ¬¡ã®ãã©ã³ã¶ã¯ã·ã§ã³IDãæå®ãã¾ã
  [-D, --pgdata=]DATADIR          ãã¼ã¿ãã£ã¬ã¯ããª
 %sã¯PostgreSQLã®åè¡æ¸ãè¾¼ã¿ã­ã°ããªã»ãããã¾ãã

 %s: OID(-o)ã¯0ä»¥å¤ã§ãªããã°ãªãã¾ãã
 %s: è­¦å: ãã®ãã©ãããã©ã¼ã ã§ã¯å¶éä»ããã¼ã¯ã³ãä½æã§ãã¾ãã
 %s: --wal-segsize ã®å¼æ°ã¯æ°å¤ã§ãªããã°ãªãã¾ãã
 %s: --wal-segsize ã®å¼æ°ã¯1ä»¥ä¸1024ä»¥ä¸ã®2ã®ç´¯ä¹ã§ãªããã°ãªãã¾ãã
 %s: "root"ã§ã¯å®è¡ã§ãã¾ãã
 %s: SIDãå²ãå½ã¦ããã¾ããã§ãã: ã¨ã©ã¼ã³ã¼ã %lu
 %s: ãã£ã¬ã¯ããª"%s"ã«ç§»åã§ãã¾ããã§ãã: %s
 %s: ãã£ã¬ã¯ããª "%s" ãã¯ã­ã¼ãºã§ãã¾ããã§ãã: %s
 %s: pg_controlãã¡ã¤ã«ãä½æã§ãã¾ããã§ãã: %s
 %s: å¶éä»ããã¼ã¯ã³ãä½æã§ãã¾ããã§ãã: ã¨ã©ã¼ã³ã¼ã %lu
 %s: ãã¡ã¤ã«"%s"ãåé¤ã§ãã¾ããã§ãã: %s
 %s: ãµããã­ã»ã¹ã®çµäºã³ã¼ããåå¾ã§ãã¾ããã§ããã: ã¨ã©ã¼ã³ã¼ã %lu
 %s: ãã£ã¬ã¯ããª"%s"ããªã¼ãã³ã§ãã¾ããã§ãã: %s
 %s: èª­ã¿åãç¨ã®ãã¡ã¤ã«"%s"ããªã¼ãã³ã§ãã¾ããã§ãã: %s
 %s: ãã¡ã¤ã«"%s"ããªã¼ãã³ã§ãã¾ããã§ãã: %s
 %s: ãã­ã»ã¹ãã¼ã¯ã³ããªã¼ãã³ã§ãã¾ããã§ãã: ã¨ã©ã¼ã³ã¼ã %lu
 %s: å¶éä»ããã¼ã¯ã³ã§åå®è¡ã§ãã¾ããã§ãã: %lu
 %s: ãã£ã¬ã¯ããª"%s"ãèª­ã¿åããã¨ãã§ãã¾ããã§ããã: %s
 %s: ãã¡ã¤ã«"%s"ãèª­ã¿è¾¼ãã¾ããã§ãã: %s
 %s: ãã£ã¬ã¯ããª"%s"ã®æ¨©éãèª­ã¿åãã¾ããã§ãã: %s
 %s: "%s"ã³ãã³ãç¨ã®ãã­ã»ã¹ãèµ·åã§ãã¾ããã§ãã: ã¨ã©ã¼ã³ã¼ã %lu
 %s: ãã¡ã¤ã«"%s"ãæ¸ãè¾¼ãã¾ããã§ãã: %s
 %s: pg_controlãã¡ã¤ã«ãæ¸ãè¾¼ãã¾ããã§ãã: %s
 %s: ãã¼ã¿ãã£ã¬ã¯ããªã¯ééã£ããã¼ã¸ã§ã³ã®ãã®ã§ã
ãã¡ã¤ã«"%s"ã®åå®¹ã¯"%s"ã§ãããããã¯ãã®ãã­ã°ã©ã ã®ãã¼ã¸ã§ã³"%s"ã¨ã¯äºææ§ãããã¾ããã
 %s: fsyncã¨ã©ã¼: %s
 %s: ãªãã·ã§ã³ %s ã®å¼æ°ãç¡å¹ã§ã
 %s: ã­ãã¯ãã¡ã¤ã«"%s"ãããã¾ã
ãµã¼ããç¨¼åãã¦ãã¾ããã? ç¨¼åãã¦ããªããã°ã­ãã¯ãã¡ã¤ã«ãåé¤ãåå®è¡ãã¦ãã ããã
 %s: ãã«ããã©ã³ã¶ã¯ã·ã§ã³ID(-m)ã¯0ä»¥å¤ã§ãªããã°ãªãã¾ãã
 %s: ãã«ããã©ã³ã¶ã¯ã·ã§ã³ãªãã»ãã(-O)ã¯-1ã§ã¯ããã¾ãã
 %s: ãã¼ã¿ãã£ã¬ã¯ããªãæå®ããã¦ãã¾ãã
 %s: æãå¤ããã«ããã©ã³ã¶ã¯ã·ã§ã³ID(-m)ã¯0ä»¥å¤ã§ãªããã°ãªãã¾ãã
 %s: pg_controlãããã¾ããããCRCãä¸æ­£ã§ã; æ³¨æãã¦é²ãã¦ãã ãã
 %s: pg_controlãããã¾ããããç ´æãã¦ãããééã£ããã¼ã¸ã§ã³ã§ã; ç¡è¦ãã¾ã
 %s: pg_control ãä¸æ­£ãªWALã»ã°ã¡ã³ããµã¤ãºãæå®ãã¦ãã¾ã(%dãã¤ã); æ³¨æãã¦é²ãã¦ãã ãã
 %s: ã³ãã³ãã©ã¤ã³å¼æ°ãå¤ããã¾ãã(å§ãã¯"%s")
 %s: ãã©ã³ã¶ã¯ã·ã§ã³ID(-c)ã¯0ãããã¯2ä»¥ä¸ã§ãªããã°ãªãã¾ãã
 %s: ãã©ã³ã¶ã¯ã·ã§ã³ID(-x)ã¯0ä»¥å¤ã§ãªããã°ãªãã¾ãã
 %s: ãã©ã³ã¶ã¯ã·ã§ã³IDèµ·ç¹(-e)ã¯ -1 ã§ãã£ã¦ã¯ãªãã¾ãã
 %s: æ³å®å¤ã®ç©ºã®ãã¡ã¤ã«"%s"
 64ãããæ´æ° å¤§ããªãªã¬ã¼ã·ã§ã³ã®ã»ã°ã¡ã³ããã­ãã¯æ°:%u
 WALã»ã°ã¡ã³ãå½ããã®ãã¤ãæ°:           %u
 ã«ã¿ã­ã°ãã¼ã¸ã§ã³çªå·:                  %u
 ç¾å¨ã®pg_controlã®å¤:

 ãã¼ã¿ãã¼ã¸ãã§ãã¯ãµã ã®ãã¼ã¸ã§ã³:    %u
 ãã¼ã¿ãã¼ã¹ãã­ãã¯ãµã¤ãº:              %u
 ãã¼ã¿ãã¼ã¹ã·ã¹ãã è­å¥å­:              %s
 æ¥ä»/æå»åã®æ ¼ç´æ¹å¼                    %s
 ãªã»ããå¾ã®æåã®ã­ã°ã»ã°ã¡ã³ã:        %s
 Float4å¼æ°ã®æ¸¡ãæ¹:                      %s
 Float8å¼æ°ã®æ¸¡ãæ¹:                      %s
 æ¨æ¸¬ããpg_controlã®å¤:

 ç¢ºå®ã«ãã¼ã¿ãã£ã¬ã¯ããªã®ãã¹ãæ­£ãããã°ã
  touch %s
ãå®è¡ããåå®è¡ãã¦ãã ããã

 æçµãã§ãã¯ãã¤ã³ãã®NextMultiOffset:   %u
 æçµãã§ãã¯ãã¤ã³ãã®NextMultiXactId:   %u
 æçµãã§ãã¯ãã¤ã³ãã®NextOID:           %u
 æçµãã§ãã¯ãã¤ã³ãã®NextXID:           %u:%u
 æçµãã§ãã¯ãã¤ã³ãã®ã¿ã¤ã ã©ã¤ã³ID:    %u
 æçµãã§ãã¯ãã¤ã³ãã®full_page_writes:  %s
 æçµãã§ãã¯ãã¤ã³ãã®newestCommitTsXid: %u
 æçµãã§ãã¯ãã¤ã³ãã®oldestActiveXID:   %u
 æçµãã§ãã¯ãã¤ã³ãã®oldestCommitTsXid: %u
 æçµãã§ãã¯ãã¤ã³ãã®oldestMultiã®DB:   %u
 æçµãã§ãã¯ãã¤ã³ãã®oldestMultiXid:    %u
 æçµãã§ãã¯ãã¤ã³ãã®oldestXIDã®DB:     %u
 æçµãã§ãã¯ãã¤ã³ãã®oldestXID:         %u
 ã¤ã³ããã¯ã¹åã®æå¤§åæ°:                %u
 æå¤§ã®ãã¼ã¿ã¢ã©ã¤ã¡ã³ã:                %u
 è­å¥å­ã®æå¤§é·:                          %u
 TOASTãã£ã³ã¯ä¸åã®æå¤§ãµã¤ãº:           %u
 NextMultiOffset:                         %u
 NextMultiXactId:                         %u
 NextOID:                                 %u
 NextXIDèµ·ç¹:                             %u
 NextXID:                                 %u
 OldestMultiã®DB:                         %u
 OldestMultiXid:                          %u
 OldestXIDã®DB:                           %u
 OldestXID:                               %u
 ãªãã·ã§ã³:
 ã©ã¼ã¸ãªãã¸ã§ã¯ããã£ã³ã¯ã®ãµã¤ãº:      %u
 ãã¼ã¿ãã¼ã¹ãµã¼ããæ­£ããã·ã£ãããã¦ã³ããã¦ãã¾ããã
åè¡æ¸ãè¾¼ã¿ã­ã°ããªã»ããããã¨ãã¼ã¿æå¤±ã®æããããã¾ãã
ã¨ã«ããé²ãããã®ã§ããã°ã-fãä½¿ç¨ãã¦å¼·å¶çã«ãªã»ãããã¦ãã ããã
 è©³ç´°ã¯"%s --help"ãå®è¡ãã¦ãã ããã
 ä½¿ç¨æ¹æ³:
  %s [OPTION]... DATADIR

 WALã®ãã­ãã¯ãµã¤ãº:                     %u
 åè¡æ¸ãè¾¼ã¿ã­ã°ã¯ãªã»ããããã¾ãã
 PostgreSQLã®ã¹ã¼ãã¼ã¦ã¼ã¶ã§%sãå®è¡ããªããã°ãªãã¾ãã
 åç§æ¸¡ã å¤æ¸¡ã newestCommitTsXid:                       %u
 ãªã oldestCommitTsXid:                       %u
 ãªã³ pg_controlãã¼ã¸ã§ã³çªå·:                %u
 