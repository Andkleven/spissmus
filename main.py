from split_image import split
from objekt import image, kjeve, first, mirror, draw_multi
import cv2
from measure import run
from tengne import draw, finn_punkt, draw_img
import csv
import pathlib
import uuid
from pathlib import Path

def plot(image,k):
    cv2.imshow('Bilde '+str(k), image)
    key = cv2.waitKey(0)
    if key == 27 or key == 32:
        cv2.destroyAllWindows()

while True:   
    text = input('Dra bilde fra mapen sin hit:  ')
    while len(text)<4:
        text = input('Dra bilde fra mapen sin hit:  ')
    if "'" in text: 
        path = text.split("'", 1)[1]
        path = path.split("'", 1)[0]
    if '"' in text: 
        path = text.split('"', 1)[1]
        path = path.split('"', 1)[0]
    img = cv2.imread(path) 
    img_img = split(img)
    art_list = {}
    img_list = {}

    index_start = 0
    _list = [key for key in img_img.keys()]
    # start = input('Hvilken rute vil du start i, trykk enter om du vil start på nummer en:  ')
    # if not start.isnumeric() or int(start) < 1: start = 1
    # try:
    #     index_start = _list.index(int(start))
    # except ValueError:
    #     index_start = 1   
    # except:
    #     print('kontakt Anders')
    #     start = input('Var ikke noe bilde i ruten, prøv igjen:  ')
    # index = index_start
    # while index < len(_list):
    #     k = _list[index]
    #     v = img_img[k]
       
    #     try:
    #         koor, orig, nervehule, punkt_c, rent_bilde = image(v)
    #         chack = True

    #     except:
    #         orig, orig1, orig2, first = kjeve(v)
    #         first = first(orig1,orig2)
    #         orig = mirror(orig, first)
    #         print('Nummer {} går ikke'.format(k))
    #         chack = False
    #     print("Et bilde i et nytt vindu vil dukke opp. Du må trykk på NERVEHULET med musen også mellomroms knapen. Om du gjort feil eller bommet kan du trykke på O for å gjøre det om igjen.For å gå til neste bilde trykk N. om du vil gå tilbake til forige bilde trykk T")
    #     print(koor)
    #     if chack:
    #         koor, nervehule, back = draw_img(orig, koor, nervehule, k)
    #         while back == 2:
    #             koor, nervehule, back = draw_img(orig, koor, nervehule, k)
    #         if back == 0: index += 1 
    #         else: 
    #             index -= 1
    #             continue
    #     else: 
    #         koor, _, q, back = draw(orig, False, k)
    #         while back == 2:
    #             koor, _, q, back = draw(orig, False, k)
    #         print(koor)
    #         if back == 0: index += 1 
    #         else: 
    #             index -= 1
    #             continue
    #         if len(koor) <= 5:
    #             index += 1
    #             continue
    #         koor, punkt_c = finn_punkt(koor)
    #         orig = draw_multi(koor, orig)
    #         nervehule = True
    #     img_list.update({k: [koor, orig, nervehule, punkt_c]})
    #     art, img, measur, prosent = run(img_list[k])
    #     art_list.update({k: [art, prosent]})
    #     print(art, str(prosent*100)+'%')
    #     print('Neste bilde...')
    #     chack = False

    print("Analyserer bildene... ")
    index = index_start
    while index < len(_list):
        print(f'Ferdig med bilde {index-index_start+1}/{len(_list)-index_start}')
        k = _list[index]
        v = img_img[k]
        try:
            koor, orig, nervehule, punkt_c, rent_bilde = image(v)
            chack = True
        except:
            orig, orig1, orig2, first = kjeve(v)
            first = first(orig1,orig2)
            orig = mirror(orig, first)
            print('Nummer {} går ikke'.format(k))
            chack = False
        img_list.update({k: [koor, orig, nervehule, punkt_c, chack]})
        chack = False
        index += 1
    print("BRUKSANVISNING")
    print("Et bilde vil åpnes i et nytt vindu. Du må trykk på NERVEHULET med musen for å markere det om det ikke er markert allered")
    print("Om du gjort feil eller bommet kan du trykke på O for å marker på nytt. For å gå til neste bilde trykk N.")
    print("")
    index = index_start
    while index < len(_list):
        k = _list[index]
        koor, orig, nervehule, punkt_c, chack = img_list[k]
        if chack:
            koor, nervehule, back = draw_img(orig, koor, nervehule, k)
            while back == 2:
                koor, nervehule, back = draw_img(orig, koor, nervehule, k)
            if back == 0: index += 1 
            else: 
                index -= 1
                continue
        else: 
            koor, _, q, back = draw(orig, False, k)
            while back == 2:
                koor, _, q, back = draw(orig, False, k)
            if back == 0: index += 1 
            else: 
                index -= 1
                continue
            if len(koor) <= 5:
                index += 1
                continue
            koor, punkt_c = finn_punkt(koor)
            orig = draw_multi(koor, orig)
            nervehule = True
        img_list.update({k: [koor, orig, nervehule, punkt_c, chack]})
        art, img, measur, prosent = run(img_list[k])
        art_list.update({k: [art, prosent]})
        print(f'Arten er {art}')
        print(f'Sannsylighet for Isodon: {prosent*100}%')
        print('')
        chack = False
    print('Ferdig, lagrer all dataen i en fil')
    file_name = uuid.uuid1()
    with open(f'{file_name}.csv', 'w') as f:
        for key in art_list.keys():
            f.write("%s: %s, %s%s\n"%(key,art_list[key][0],art_list[key][1]*100,'%'))
    path = pathlib.Path().absolute()
    print(f'Fil er lagret her: {path}\{file_name}.csv')
    inpu = input('Trykk "S" for å stoppe programmet, Trykk "A" for ny analyse:   ')
    while len(list(inpu))==0: inpu = input('Trykk "S" for å stoppe programmet, Trykk "A" for ny analyse:   ')
    if inpu == 's' or inpu == 'S':
        break
