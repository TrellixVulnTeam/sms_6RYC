��            )         �  X   �  
   
       3   1  ?   e  H   �  1   �  (      >   I  f   �  $   �  2     &   G  !   n  8   �  !   �  .   �  ;     0   V      �  &   �  4   �               ,     E     `  ,   t  &   �     �  �  �  `   a	     �	     �	  ;   �	  @   +
  M   l
  ?   �
  %   �
  c      �   �  7     P   G  "   �  #   �  I   �  ;   )  F   e  >   �  :   �  %   &  $   L  6   q  "   �     �  (   �  %   	     /  B   E  *   �     �                                             
                            	                                                               
If no data directory (DATADIR) is specified, the environment variable PGDATA
is used.

 
Options:
   %s [OPTION]... [DATADIR]
   -?, --help             show this help, then exit
   -V, --version          output version information, then exit
   -r RELFILENODE         check only relation with specified relfilenode
   -v, --verbose          output verbose messages
  [-D, --pgdata=]DATADIR  data directory
 %s verifies data checksums in a PostgreSQL database cluster.

 %s: checksum verification failed in file "%s", block %u: calculated checksum %X but block contains %X
 %s: checksums verified in file "%s"
 %s: cluster must be shut down to verify checksums
 %s: could not open directory "%s": %s
 %s: could not open file "%s": %s
 %s: could not read block %u in file "%s": read %d of %d
 %s: could not stat file "%s": %s
 %s: data checksums are not enabled in cluster
 %s: invalid relfilenode specification, must be numeric: %s
 %s: invalid segment number %d in file name "%s"
 %s: no data directory specified
 %s: pg_control CRC value is incorrect
 %s: too many command-line arguments (first is "%s")
 Bad checksums:  %s
 Blocks scanned: %s
 Checksum scan completed
 Data checksum version: %d
 Files scanned:  %s
 Report bugs to <pgsql-bugs@postgresql.org>.
 Try "%s --help" for more information.
 Usage:
 Project-Id-Version: pg_verify_checksums (PostgreSQL) 11
Report-Msgid-Bugs-To: pgsql-bugs@postgresql.org
POT-Creation-Date: 2018-10-10 21:17+0000
PO-Revision-Date: 2018-10-13 10:13+0300
Last-Translator: Abdullah Gülner
Language-Team: Turkish <ceviri@postgresql.org.tr>
Language: tr
MIME-Version: 1.0
Content-Type: text/plain; charset=UTF-8
Content-Transfer-Encoding: 8bit
X-Generator: Poedit 1.8.7.1
 
Eğer hiçbir veri dizini (DATADIR) belirtilmezse, PGDATA çevresel değişkeni
kullanılır.

 
Seçenekler:
   %s [SEÇENEK]... [DATADIR]
   -?, --help             bu yardımı göster, sonra çık
   -V, --version          sürüm bilgisini göster, sonra çık
   -r RELFILENODE         sadece belirtilen relfilenode'lu nesneyi kontrol et
   -v, --verbose            detaylı (verbose) mesajlar göster
  [-D, --pgdata=]DATADIR  veri dizini
 %s bir PostgreSQL veritabanı kümesi (cluster) içindeki veri sağlama toplamlarını doğrular.

 %s:  "%s" dosyasında sağlama toplamı doğrulaması başarısız oldu, blok %u: hesaplanan sağlama toplamı %X fakat blokta %X bulundu
 %s: "%s" dosyasında sağlama toplamları doğrulandı
 %s: sağlama toplamlarının doğrulanması için küme (cluster) kapatılmalı
 %s:  "%s" dizini açılamadı: %s
 %s: "%s" dosyası açılamadı: %s
 %1$s: "%3$s" dosyasında %2$u bloğu okunamadı: %5$d nin %4$d si okundu
 %s: "%s" dosyasının durumu görüntülenemedi (stat): %s
 %s: kümede (cluster) veri sağlama toplamaları etkinleştirilmemiş
 %s: geçersiz relfilenode tanımlaması, sayısal olmalı: %s
 %1$s: "%3$s" dosyasında geçersiz segment numarası %2$d
 %s: hiçbir veri dizini belirtilmedi
 %s: pg_control CRC değeri yanlış
 %s: Çok fazla komut satırı girdisi var (ilki "%s")
 Yanlış sağlama toplamları: %s
 Taranan bloklar: %s
 Sağlama toplamı taraması tamamlandı
 Veri sağlama toplamı sürümü: %d
 Taranan dosyalar: %s
 Hataları <pgsql-bugs@postgresql.org> adresine bildirebilirsiniz.
 Daha fazla bilgi için "%s --help" yazın
 Kullanımı:
 