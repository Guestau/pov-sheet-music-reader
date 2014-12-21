pov-sheet-music-reader
======================

POV - Sheet Music Reader

# Zadnání jak jsem ho navrhl Hradišovi 

Implementujte OCR metodu pro přepis tištěných not. Můžete předpokládat, že jsou obrazy stránek velmi dobře pořízené a že nejsou stránky geometricky deformované. Přesnost rozpoznání vyhodnoťte na vhodné sadě obrázků.
Standardní a poměrně jednoduchý přístup může být:
-	detekce notové osnovy - například pomocí sumace pixelů v horizontálním směru a hledání maxim intenzit, což budou mezery mezi řádky
-	odstranění linek notové osnovy
-	segmentace objektů - adaptivní prahování a nalezení spojitých komponent
-	extrakce příznaků z segmentovaných útvarů
-	klasifikace segmentů na základě extrahovaných příznaků
Existují i mnohem zajímavější a robustnější přístupy, ale zvažte své možnosti a schopnost. 
 
# Co to bude dělat
 - veme to obrázek
 - :white_check_mark: převede na binární (metodou otsu?)
 - (?) najde homografii a upraví rotaci. Pokud se fotí foťákem nikdy to nebude rovně. Ale pro začátek můžeme předpokládat zprávně natočený obrázek a není zkreslený.
 - :white_check_mark: udělá se histogram podle y osy
 - :white_check_mark: linky osnovy udělají 5 velkých vrcholů
 - (?) oddělí se jednotlivé řádky. 
 - :white_check_mark: najde se sirka linky
 - :white_check_mark: najde se vyska radku
 - :white_check_mark: pro každou osnovu se odeberou linky. To funguje tak že se projíždí obrázek tam kde jsou ty velké vrcholy z histogramu. Zjistí se kolik je černych pixelů směrem nahoru a kolik dolů, to se sečte Ppokud je to menšírovno vyšce řádku +-2 pixely tak se to černé pixely vymažou.
  - Alternativně se nejdříve detekují hlavičky (na linkách a mezi linkami), u odstraňování linek se zohlední hlavičky not, abyt nedocházelo rozbití celých a půlových not
 - :white_check_mark: potom se od sebe oddělí jenotlivé symboly a najde se jejich nejmenší obdelníkový bounding-box. cv2.findContours
 - teď víme kde jsou jednotlivé symboly, ty je třeba rozeznat
 - zjistí se, které jsou noty a které ne. Nota má hlavičku a ta jde "lehce" najít, viz. zdroje, cv2.matchTemplate. Tady bude problem s celými a půlovými notami
 - symboly se klasifikují (buď nejaké klasické OCR neco lepšího) viz. opencv. Musí být invariantní vůči měřítku/scale.
 - noty se klasifikují zvlášt hlavička (celá, půlová), zvlášt prapor/vlajka. Pozor na to, že některé noty jsou spojeny vertikálně stéblem/stonekem nebo horizontálně pomocí praporu/vlajky. A také mohou mít za sebou tečku nebo před sebou křížek, béčko nebo hraj-normálně. Tohle ještě nemám domyšleno.
 - Pak se podle první linky a pozice a rozestupem mezi linkami zjistí výška tónu
 - (?) to se nacpe do syntetizeru a přehraje
 
Trénovací sada na symboly notového zápisu je ve zdrojích. Také budeme potřebovat napsat nejaké testy to znamená připravit nějaké jednoduché noty, přepsat (prohnat jiným toolem, aby zjistil noty) a pak porovnat, že naše appka dává stejný výsledek. 

## Technologie
 - python 2.7 (opencv nepodporuje 3.3 :/)
 - opencv verze 2.4.10 [viz.](http://www.lfd.uci.edu/~gohlke/pythonlibs/#opencv)
 
## Zatím známe závislosti
 - [Numpy](http://sourceforge.net/projects/numpy/files/NumPy/1.7.1/numpy-1.7.1-win32-superpack-python2.7.exe/download) (doporučeno opencv)
 - [Matplotlib](https://downloads.sourceforge.net/project/matplotlib/matplotlib/matplotlib-1.3.0/matplotlib-1.3.0.win32-py2.7.exe) (doporučeno opencv)
 - Matplotlib má další závislosti, které si z nějakého zahádného důvodu neumí nainstalovat sám. Mi stačilo doinstalovat následující věci. Všechno je možné najít tady http://www.lfd.uci.edu/~gohlke/pythonlibs/
 - python-dateutil-2.2.win32-py2.7
 - pyparsing-2.0.3.win32-py2.7
 - six-1.8.0.win32-py2.7
 - (?) syntetizer
 

# Nějaké zdroje, ze kterých asi budeme/můžeme čerpat
- http://msw3.stanford.edu/~mmakar/mentorship/ee368_4.pdf
- https://github.com/acieroid/overscore
- http://www.ece.rutgers.edu/~kdana/Capstone2012/Reports/CDG3.pdf
- stackoverflow.com/questions/675077/ocr-for-sheet-music
- existující mobilní appka na andriod https://play.google.com/store/apps/details?id=com.gearup.iseenotes&hl=cs
- www.quora.com/How-can-I-make-my-own-OMR-reader-using-image-processing-with-C++-and-OpenCV
