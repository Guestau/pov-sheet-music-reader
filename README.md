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
 - převede obraz na binární metodou OTSU
 - udělá se histogram podle y osy
 - linky osnovy udělají 5 velkých vrcholů, za linku je považován každý vrchol větší než 80% maxima
 - oddělí se jednotlivé řádky podle počtu linek
 - najde se sirka linky (nejčastější šířka vrcholu), najde se výška řádku (nejčastější rozestup mezi vrcholy – a to po počátku první linky k počátku druhé linky)
 - pro každou osnovu se odeberou linky. To funguje tak, že se projíždí obrázek pro každý vrchol histogramu. Zjistí se kolik je černých pixelů směrem nahoru a kolik dolů. Pokud je to menší rovno výšce řádku +-2 pixely tak se černé pixely vymažou. 
 - Alternativně se nejdříve detekují hlavičky (na linkách a mezi linkami), u odstraňování linek se zohlední hlavičky not, aby nedocházelo rozbití celých a půlových not
 - potom se od sebe oddělí jednotlivé symboly a najde se jejich obdélníkový bounding-box. cv2.findContours
 - zjistí se, které ve kterých symbolech jsou noty a kde ne. Nota má hlavičku a ta jde "lehce" najít, cv2.matchTemplate. Tady bude problém s celými a půlovými notami, takže je možná pro zjednodušení vynecháme.
 - symboly se klasifikují nejspíše kNN nebo SVM, jako feature vektor poslouží buď celý obrázek nebo HOG. Train-set od Audiveris.
 - noty se klasifikují zvlášť hlavička (celá, půlová), zvlášť prapor/vlajka. Pozor na to, že některé noty jsou spojeny vertikálně stéblem/stonkem nebo horizontálně pomocí praporu/vlajky. Hlavičky mohou být také nad sebou (i mírně vedle sebe) v akordu. A také mohou mít za nebo nad sebou tečku nebo před sebou posuvky. Tohle by mělo přešít nalezení kontur popsané výše.
 - pak se podle první linky a pozice a rozestupem mezi linkami zjistí výška tónu

 - a je to :)
 
Trénovací sada na symboly notového zápisu je ve zdrojích. Také budeme potřebovat napsat nejaké testy to znamená připravit nějaké jednoduché noty, přepsat (prohnat jiným toolem, aby zjistil noty) a pak porovnat, že naše appka dává stejný výsledek. 

# Zjednodušení – předpoklady
 - Dokonale rovný obrázek (např.: převeden z PDF)
 - Neuvažujeme:
 - Akordy
 - Rytmické notové skupiny http://musescore.org/cs/p%C5%99%C3%ADru%C4%8Dka/notov%C3%BD-z%C3%A1pis/hlasy tedy noty spojené v taktu, tak i noty spojené přes více řádků (mezi klíči). Obecně i propojení více řádků, například závorkami a čárami
 - Notové zápisy bubnů a jiných specifických nástrojů
 - Linky http://musescore.org/cs/linky
 - Svorky http://musescore.org/cs/svorky a obecně doplňující text (slova písně, tempo atd.)  nad a pod osnovou
 - Legata http://musescore.org/cs/legato
 - Ligatury http://musescore.org/cs/ligatura
 - Hlasy http://musescore.org/cs/p%C5%99%C3%ADru%C4%8Dka/notov%C3%BD-z%C3%A1pis/hlasy
 - Volta http://musescore.org/cs/volta


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
