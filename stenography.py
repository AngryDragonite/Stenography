import sys
from PIL import Image

def kodowanieWiad(wiadomosc):                                       # Funkcja zamieniajaca wiadomośc w pliku txt na odpowiedni string, który będzie użyty podczas modyfikacji pixeli
    wiad = open(wiadomosc)                                          #
    wiad = wiad.read()                                              # odczytanie wiadomości
    wiadList = list(wiad)                                           # zamiana znaków w wiadomości na listę, której elementami są poszczególne  te znaki, np wiadList == ["c", "o", "ś", " "t", "u", " ", "j", "e", "s", "t"]
    wiadBin = [format(ord(i), "07b") for i in wiadList]             # zamiana elementów w wiadList na kod ascii, następnie na ich odpowiedniki w systemie binarnym.
    wiadBinR = []                                                   # pusta lista, która zbiera elementy pochodzące od pętli While
    i = 0                                                           # "pomocnik" numerujący, odpowiada za zakończenie pętli While gdy skończy się wiadomość
    while True:                                                     #
            if i<len(wiadBin)-1:                                    #
                x = wiadBin[i] + "00"                                # do elementu dodaje się "0" na koniec, wykorzystam to podczas dekodowania
                wiadBinR.append(x)                                  # przyłączenie elementu do listy wiadBinR
                i = i+1                                             # 
            else:                                                   #
                x = wiadBin[i] + "01"                                # jesli element był ostatnim w wiadomości, to zamiast "0", na koniec dodaję "1"
                wiadBinR.append(x)                                  #
                break                                               # Zakonczenie pętli While
    wiadBinStr = "".join(wiadBinR)                                  # Złączenie elementów listy wiadBinR w jeden string, np: wiadBinStr = "1010001010100010....1"
    return wiadBinStr



def odkodowanieWiad(otrzymanyStrBin):                               # Funkcja, która przyjmuje str wartości najmniej ważnych liczb składowych pixeli w postaci str, następnia zamienia ją na wiadomość którą można odczytać, tworzy nowy plik tekstowy z tą wiadomością (to samo co poprzednia funkcja, tylko że z odwotną kolejnością)
    lista = (list(map(''.join, zip(*[iter(otrzymanyStrBin)]*9))))   # to dzieli otrzymany str z pixeli ("101101011010010101001010111011110...10101") w formie binarnej na elementy o 8 znakach, po czym dodaje je do "lista", np: lista = ["10010100","10010100",...."10010101"]
    lista2 = []                                                     # lista do magazynowania "produktów" pętli While
    i=0                                                             # "pomocnik" numerujący, odpowiada za zakończenie pętli While gdy skończy się wiadomość
    while True:                                                     #
        if lista[i].endswith("00"):                                  # jesli i-ty element kończy się na 0, to należy go zdekodować i kontynuować iterację 
            x = lista[i].removesuffix("00")                          # usuwanie końcówki "0" dodanej przy kodowaniu
            x = int(x, 2)                                           # zamiana elementu z liczby binarnej na dziesiętną (powstaje znak w kodzie ascii)
            x = chr(x)                                              # zamiana elementu z kodu ascii na określony znak
            lista2.append(x)                                        # dodanie tego znaku do lista2
            i = i+1                                                 # 
        elif lista[i].endswith("01"):                                # jesli i-ty element kończy się na 0, to należy go zdekodować, i zakończyć pętle While (koniec zakodowanej wiadomości)
            x = lista[i].removesuffix("01")                          #                          
            x = int(x, 2)                                           #
            x = chr(x)                                              #
            lista2.append(x)                                        #
            break                                                   #        
    wiad = "".join(lista2)                                          # złączenie elementów lista2 - utworzenie z nich odkodowanej wiadomości
    wiadtxt = open(wyjście, "w")                                    # stworzenie nowego pliku txt
    wiadtxt.write(wiad)                                             # zapisanie w tym pliku odkodowanej wiadomości
    wiadtxt.close()                                                 # zapisanie i zamknięcie pliku txt


def zmianaPix(wiadBinStr):
    zdj = Image.open(wejście)                                       # odczytanie wejściowego pliku jpg
    leng = len(wiadBinStr)                                           # obliczenie długości otrzymanyStrBin
    wielkX, wielkY = zdj.size                                       # opisanie wielkości pliku jpg
    i = 0                                                           # dla każdego elementu otrzymanyBinStr   
    if i<= wielkX*wielkY:        
        for y in range(0, wielkY):                                  #
            for x in range(0, wielkX):                                          
                if i<leng:
                    pixel = list(zdj.getpixel((x,y)))                   # np [234, 123, 154]
                    pixelMod = []                                       # tworzenie zmodyfikowanego pixela
                    for n in pixel:                                     # biorę każdy element pixel (rozkładam na r, g, b)
                        if n%2 == 1:                                    # Jeśli najmniej znaczący bit (NNb) danej składowej pixela jest równy 1 
                            if wiadBinStr[i] == "1":                    # jeśli i-ty element wiadBinStr jest także równy 1, nic nie zmieniam i dodaje tą składową do pixelMod
                                pixelMod.append(n)
                                i = i+1                                 # 
                            elif wiadBinStr[i] == "0":                  # jeśli i-ty element wiadBinStr jest równy 0, dodaje do składowej pixela 1 i dodaję tą składową do pixelMod
                                pixelMod.append(n-1)
                                i = i+1                                 #
                        elif n%2 == 0:                                  # A jeśli NNb danej składowej pixela jest równy 0
                            if wiadBinStr[i] == "1":                    # jeśli i-ty element wiadBinStr jest równy 1, to odejmuje od niego 1 i dodaję tą składowądo pixelMod
                                pixelMod.append(n+1)
                                i = i+1                                 # 
                            elif wiadBinStr[i] == "0":                  # jeśli i-ty element wiadBinStr jest także równy 0, to nic nie zmieniam i dodaję tą składową do pixelMod
                                pixelMod.append(n)
                                i = i+1
                    
                    zdj.putpixel((x,y), tuple(pixelMod))                # Zamiana pixel na  pixelMod w pliku jpg              
                else:
                        i=i+1
    else:       
        print("kuniec")
    zdj.save(wyjście)


def odkodPix(zakodZdjecie):                                         # Funkcja przyjmująca jako argument zdjęcie z zakodowaną wiadomością, następnie dekoduje ją i tworzy string w formie binarnej ("otrzymanyStrBin")
    zdj = Image.open(zakodZdjecie)                                  # otworzenie zakodowanego zdjęcia
    wielkX, wielkY = zdj.size                                       # opisanie wielkości pliku
    listaOdczytana = []                                             # lista w której będą znajdować się NNb składowych każdego pixela
    for y in range(0, wielkY):                                      # rozbijam plik jpg na pionowe kolumny o szerokości 1px i wysokości wielkY
        for x in range(0, wielkX):                                  # rozbijam tą kolumne na pojedyncze pixele
            pixel = list(zdj.getpixel((x,y)))                       # odczytanie składowych pixeli, zamiana ich na liste        np pixel == [123, 142, 232]
            for n in pixel:                                         # rozbicie na pojedyncze składowe (r, g, b)
                if n % 2 == 0:                                      # Jeśli NNb = 0, to do listaOdczytana dodaje "0"
                    listaOdczytana.append("0")                      # 
                elif n % 2 == 1:                                    # Jeśli NNb = 1, to do listaOdczytana dodaje "1"
                    listaOdczytana.append("1")                      #
    otrzymanyStrBin = "".join(listaOdczytana)                       # zamiana listaOdczytana na spójny string "otrzymanyStrBin"
    return otrzymanyStrBin


tryb = str(sys.argv[1])                                             # wybór trybu encode lub decode 
     

if tryb == "encode":
    
    
    
    wiadomość = str(sys.argv[2])                                    # plik w formie .txt
    wejście = str(sys.argv[3])                                      # ENCODE: plik w formacie .jpg na którym zakoduje sie wiadomość   
    wyjście = str(sys.argv[4])                                      # ENCODE: plik w formacie .jpg na którym zakodowano wiadomość     

    WiadBinStr = kodowanieWiad(wiadomość)
    zmianaPix(WiadBinStr)

elif tryb == "decode":
    wejście = str(sys.argv[2])
    wyjście = str(sys.argv[3])    
    
    
    otrzymanyBinStr = odkodPix(wejście)
    odkodowanieWiad(otrzymanyBinStr)