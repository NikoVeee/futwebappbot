#Import Statements
from pynput.keyboard import Controller as keyCont, Key
from pynput.mouse import Controller, Button
from time import sleep
from random import uniform as rand, randint
import pytesseract
from PIL import ImageGrab, Image
import PIL.ImageOps   
import os
import time

keyboard = keyCont()
mouse = Controller()

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

new_dir = 'C:\\Users\\niko\\Desktop\\FUTImgs'
os.chdir(new_dir)

leagues_dict = {
    True: ["ESP1","ENG1","ITA1","GER1","FRA1","SUD","LIB","NED1","MLS","CHN1","SAU1","BEL1","MEX1","ENG2","TUR1","POR1","ARG1","CHI1","COL1"],
    False: ["ESP1","ENG1","ITA1","GER1","FRA1","SUD","LIB","ARG1","CHI1","COL1"]
}
class Cord:
    
    league_box_list = [(528,774,594,812),(520,1020,586,1058),(520,1266,586,1304),(520,1512,586,1550),(520,1758,586,1796)]

    pos_box_list = [(450, 752, 498, 782), (450, 998, 498, 1028), (450, 1244, 498, 1274), (450, 1490, 498, 1520), (450, 1736, 498, 1766)]
    
    card_pos = [(315,395),(315,505),(315,625),(315,745),(315,865)]

    name_pos_box = [(616, 712, 1008, 756), (608, 958, 1000, 1002), (608, 1204, 1000, 1248), (608, 1450, 1000, 1494), (608, 1696, 1000, 1740)]

    price_box = [(2466,1036,2616,1078), (2466,1285,2616,1327), (2466,1534,2616,1576)]
    
    item_unlock_box = (440,600,442,602)
    coin_gold = (92,48)
    back_bronze = ()
    manager = (-26, 88)
    squad_builder = (1230,765)
    leagues_button = (1230,760)
    league = (1230,522)
    build = (1310,880)
    submit = (1000,880)
    claim = (735,735)
    favourites = (582, 245)
    bronze_upgrade_sbc = (557, 406)
    silver_upgrade_sbc = (1062, 389)
    work_area = (233,873)
    back = (125,180)
    o_bundes = (1193, 650)

    pos_dict = {
    'ls':(450,365),
    'rs': (805, 365),
    'cam': (628, 420),
    'rm': (873, 510),
    'lm': (377, 509),
    'cdm': (627, 553),
    'lb': (269, 653),
    'lcb': (466, 663),
    'rcb': (785, 666),
    'rb': (982, 653),
    'gk': (625, 772)}
    

    bench_pos_dict = {
    'b':(238, 624),
    'f':(345, 624),
    'd':(452, 624),
    'a':(559, 624),
    'k':(666, 624),
    'e':(773, 624),
    'j':(880, 624),
    'l':(987, 624),
    'i':(238, 740),
    'h':(345, 740),
    'c':(452, 740),
    'g':(559, 740)}

    """
    a = 4
    b = 1
    c = 11
    d = 3
    e = 6
    f = 2
    g = 12
    h = 10
    i = 9
    j = 7
    k = 5
    l = 8

    """
    
        
    
    store_tab = (50, 500)
    my_packs = (608, 251)

    transfers_tab = (50, 440)
    sbc_tab = (50, 380)

    transfer_list = (570, 720)
    clear_sold = (964, 301)
    relist = (981, 512)
    confirm = (756, 653)
    unsold_red_box = (420,1100,422,1102)
    sold_green_box = (420, 684, 422, 686)
    listed_price_box = (1670,1232, 1790, 1278)
    minus_price = (1087, 769)
    check_in_club_box = (2390,1620,2392,1622)

    list_on_tm = (1198, 531)
    search_results = (1230,644)
    relist_item = (1230, 600)
    
    start_price_tl = (1203, 692)
    bn_price_tl = (1190, 768)
    confirm_trans_tl = (1196, 895)
    
    start_price = (1174, 617)
    bn_price = (1164, 691)
    confirm_trans = (1252, 822)
    
    change_view = (1480, 180)

    open_icon = (840,500)
    swap_dup = (1213, 559)

def screenGrab(box=(), save=True):
    im = ImageGrab.grab(box)
    if save:
        imgname = 'img__' +str(randint(0,50))+'.png'
        im.save(new_dir + '\\' + imgname, 'PNG')
        return imgname
    else:
        return im
    
def readImage(box, num_only=False):
    imgname = screenGrab(box)
    value=Image.open(imgname)
    if num_only:
        text=pytesseract.image_to_string(value,config="-c tessedit_char_whitelist=0123456789 --psm 6")
    else:
        text=pytesseract.image_to_string(value,config="-c tessedit_char_whitelist=ABCDEFGHIJKLMNOPRSTUVWXZ1234 --psm 6")
    return text


def find_league(box):
    text = readImage(box)
    t = text.replace(" ", "").upper()
    return t

def is_pixel(box, coord, pixel, im=None):
    if box or box==():
        im = screenGrab(box, False)
    try:
        return True if im.getpixel(coord)==pixel else False
    except:
        print("'im' object not provided")


def mouse_scroll(n=-10, tsleep=0):
    mouse.scroll(0,n)
    sleep(tsleep)

def mouse_click(coords, tsleep=0):
    mouse.position = coords
    sleep(0.1)
    mouse.click(Button.left, 1)
    sleep(tsleep)
    
def mouse_drag(coord1, coord2, tsleep=0):
    mouse.position = coord1
    sleep(0.1)
    mouse.press(Button.left)
    sleep(0.2)
    mouse.position = coord2
    sleep(0.4)
    mouse.release(Button.left)
    sleep(tsleep)

def mouse_hold_and_release(coord1, coord2, coord3, tsleep=0):
    mouse.position = coord1
    sleep(0.1)
    mouse.press(Button.left)
    sleep(0.1)
    mouse.position = coord2
    sleep(0.3)
    mouse.position = coord3
    sleep(0.2)
    mouse.release(Button.left)
    sleep(tsleep)

def key_press(key, tsleep=0):
    keyboard.press(key)
    keyboard.release(key)
    sleep(tsleep)

def func():
    sleep(2)
    sell_player()

def sell_player(in_club=False, tl=False):
    prices = []
    counter = 0
    status = ""
    stop = False
    key_press('c', 1.2)
    
    if not tl and is_pixel((1660,825,1662,827), (0,0), (221,221,221)):
        key_press(Key.enter, 2)
        stop = True
    sleep(1)
    
    if not stop:  
        f = True
        for i in range(6):
            break_ = True
            for j in range(3):
                price = readImage(Cord.price_box[j], num_only=True)
                if price:
                    break_ = False
                    
                    prices.append(int(price))
                    if (int(price) <=200 and not in_club) or (int(price) <= 250 and in_club):
                        counter+=1
            if counter >= 2:
                status = "quicksell"
                break
                        
            if break_ and not f and not tl:
                if len(prices)<=6:
                    status = "transferlist"
                break
            if i != 5:
                mouse.position = Cord.search_results
                mouse_scroll(-3.74,0.1)
            f = False
        
        if status == "quicksell":
            if in_club:
                SendToClub()
            else:
                Quicksell()
        elif status == "transferlist" or (list(set(prices)) == 1 and list(set(prices))[0] == 10000):
            if tl:
                mouse_click(Cord.relist_item, 0.5)
                mouse_click(Cord.minus_price, 0.1)
                mouse_click(Cord.minus_price, 0.3)
                mouse_click(Cord.confirm_trans_tl, 1.5)
                sleep(3)
            else:
                Transferlist()
        else:
            sell_price = get_price(prices)
            if sell_price == None:
                if in_club:
                    Transferlist()
                else:
                    SendToClub()
            else:
                list_item(sell_price, tl)
    
def get_price(lst):
    sorted_lst = sorted(lst)
    for _ in range(len(lst)):
        try:
            sorted_lst.remove(10000)
        except ValueError:
            break
        
    if len(sorted_lst) > 3:
        if sorted_lst[0]/sorted_lst[1] <= 0.75:
            sorted_lst.pop(0)
        elif sorted_lst[0] <= 200:
            sorted_lst.pop(0)

    try:
        low_price = sorted_lst[0]
        return (low_price//10)*9 if low_price <= 1500 else (low_price//20)*19
    except:
        return None
    

def list_item(sell_price, tl=False):
    global num_trans_players
    key_press('0', 0.8)
    bid_price = (sell_price//5) * 4

    if tl:
        mouse_click(Cord.relist_item, 1.5)
        mouse_click(Cord.start_price_tl, 0.1)
        
        for char in str(bid_price):
            key_press(char, 0.03)
            
        mouse_click(Cord.bn_price_tl, 0.1)
        
        for char in str(sell_price):
            key_press(char, 0.03)
            
        mouse_click(Cord.confirm_trans_tl, 3)
        
    else:
        mouse_click(Cord.list_on_tm, 1.5)
        mouse_click(Cord.start_price, 0.1)
            
        for char in str(bid_price):
            key_press(char, 0.03)
        
        mouse_click(Cord.bn_price, 0.1)
            
        for char in str(sell_price):
            key_press(char, 0.03)
    
        mouse_click(Cord.confirm_trans, 3)
        
    try:
        num_trans_players += 1
    except:
        pass

def Transferlist():
    key_press("0", 0.8)
    key_press("t", 1.5)

def Quicksell():
    key_press("0", 0.8)
    key_press("q", 1.5)

def SendToClub():
    key_press("0", 0.8)
    key_press("s", 1.5)

def build_squad(leagues,card_type):
    if card_type == 'b':
        mouse_click(Cord.bronze_upgrade_sbc, 2)
    elif card_type == 's':
        mouse_click(Cord.silver_upgrade_sbc, 2)
    mouse.position = Cord.squad_builder
    mouse_scroll()
    sleep(0.3)
    mouse_click(Cord.squad_builder, 1.5)
    mouse_scroll()
    sleep(0.3)
    mouse_click(Cord.leagues_button, 1)
    for char in leagues[0]:
        key_press(char, rand(0.01, 0.03))
        
    if len(leagues) > 1:
        mouse_click(Cord.league, rand(0.3,0.5))
    else:
        mouse_click(Cord.o_bundes, rand(0.3,0.5))
    
    mouse_click(Cord.build, 3)
    
def check_submit(im):
    return True if im.getpixel((Cord.submit[0]*2, Cord.submit[1]*2))==(252,69,84) else False

def clear_transfer_list():
    mouse_click(Cord.transfers_tab, 2)
    mouse_click(Cord.transfer_list, 3)
    mouse_click(Cord.clear_sold, 4)
    mouse_click(Cord.relist, 2)
    mouse_click(Cord.confirm, 5)

def move_players(pos_list, bench_list):
    for i in range(min(len(pos_list), len(bench_list))):
        mouse_click(Cord.work_area,0.5)
        mouse_hold_and_release(Cord.bench_pos_dict[bench_list[i]],Cord.pos_dict["cam"],Cord.pos_dict[pos_list[i]], 1)

def enumerating_items(dupes):
    selling_items = []
    f = True
        
    for i, box in enumerate(Cord.league_box_list):
        res = find_league(box)
        if res == "" and not f:
            break
            
        if res in leagues_dict[dupes]:
            if not is_pixel((box[0]+Cord.manager[0], box[1]+Cord.manager[1], box[0]+Cord.manager[0]+2, box[1]+Cord.manager[1]+2), (0,0), (144, 122, 91)) and not \
            is_pixel((box[0]+Cord.manager[0], box[1]+Cord.manager[1], box[0]+Cord.manager[0]+2, box[1]+Cord.manager[1]+2), (0,0), (167, 143, 105)):
                selling_items.append(i)
                         
        f = False
        
    if selling_items:    
        for i in selling_items[::-1]:
            mouse_click(Cord.card_pos[i], 0.2)
            sell_player(in_club=(not dupes)) 
        
def submit():
    mouse_click(Cord.submit,2.5)
    mouse_click(Cord.claim,1)
        
def complete_sbc(card):
    mouse_click(Cord.sbc_tab, 5)
    mouse_click(Cord.favourites, 5)

    leagues = ["efl l", "efl league t", "d", "c", "bundesliga 2", "3", "laliga sm", "3f", "a", "el","f","h","hy", "k","lea", "liga i", "me", "pk", "r", "sc","so", "ss", "u"]
    #leagues = ["so", "ss", "u"]
    count = 0
    while leagues:
        build_squad(leagues,card)
        im = screenGrab(save=False)
        league_is_empty = True if is_pixel(False, (1200,1030), (251,251,251),im=im) else False
        if check_submit(im):
            sleep(2)
            submit()
            count+=1
        else:
            empty_posies = [pos for pos in sorted(Cord.pos_dict.keys()) if is_pixel(False, (Cord.pos_dict[pos][0]*2,Cord.pos_dict[pos][1]*2),(63,70,77),im=im)]
            mouse_click(Cord.work_area,1)
            sleep(1)
            im_bench = screenGrab(save=False)            
            bench_posies = [pos for pos in sorted(Cord.bench_pos_dict.keys()) if not is_pixel(False,(Cord.bench_pos_dict[pos][0]*2,Cord.bench_pos_dict[pos][1]*2),(63,70,77),im=im_bench)]

            if len(empty_posies) > len(bench_posies):
                move_players(empty_posies, bench_posies)
                sleep(1)
                leagues.pop(0)
                mouse_click(Cord.back, 2)
            elif league_is_empty:
                leagues.pop(0)
                key_press(Key.enter,0.5)
                mouse_click(Cord.back, 2)
            else:
                move_players(empty_posies, bench_posies)
                sleep(1)
                submit()
                count+=1
        
def relist_transfers():
    mouse_click(Cord.transfers_tab, 1.5)
    mouse_click(Cord.transfer_list, 2.5)
    while True:
        if is_pixel(Cord.sold_green_box, (0,0), (45, 190, 45)):
            mouse_click(Cord.clear_sold, 3.5)
            
        if not is_pixel(Cord.unsold_red_box,(0,0), (244,68,68)):
            break
        sleep(1)
        try:
            old_price = int(readImage(Cord.listed_price_box, True))
        except:
            old_price == 500
        if old_price == 200:
            key_press('q', 1.5)
            sleep(2)
        elif old_price >= 2400:
            inclub = True if is_pixel(Cord.check_in_club_box, (0,0), (255,255,255)) else False
            sell_player(in_club=inclub, tl=True)
            sleep(3.5)
        else:
            mouse_click(Cord.relist_item, 0.5)
            if old_price == 250:
                mouse_click(Cord.minus_price, 0.3)
            elif old_price <= 900:
                mouse_click(Cord.minus_price, 0.2)
                mouse_click(Cord.minus_price, 0.2)
            else:
                mouse_click(Cord.minus_price, 0.2)
                mouse_click(Cord.minus_price, 0.2)
                mouse_click(Cord.minus_price, 0.2)
                
            mouse_click(Cord.confirm_trans_tl, 1.5)
            sleep(3.5)

        

def open_packs():
    mouse_click(Cord.open_icon, 2)
    mouse_click((780, 340), 5)
    key_press('x',2)
    
    while is_pixel(False, (4,2), (247,157,164),im=screenGrab((419,582,424,585),save=False)):
        mouse_click(Cord.swap_dup,3)
        if is_pixel(False, (8,8), (11,18,24), im=screenGrab((1415,930,1425,940), save=False)):
            key_press(Key.enter, 0.8)
            key_press("q", 2)
        else:
            sell_player()
            sleep(2)
        
    key_press('0',3)
    

def open_bronze_packs(): 
    key_press('b',8.4)
    
    enumerating_items(False)
    
    key_press('x', 0.5)
        
    mouse_click((780, 340), 1.5)
    mouse.position = (rand(600,780), rand(200,340))

    if is_pixel(Cord.item_unlock_box, (0,0), (252, 69, 84)):
        key_press('s',2)

    enumerating_items(True)         
               
    key_press('a',2)
    key_press('0')
    sleep(1.5)

def run_bpm(num=None, sets=None):
    global num_trans_players
    
    if not num or not sets:
        num = int(input("How many packs? "))
        sets = int(input("How many sets? "))  
    
    for i in range(sets):
        print("----------------")
        sleep(2)
        num_trans_players = 0
        mouse_click(Cord.store_tab, 3)
        start_time = time.time()
        for _ in range(num):
            open_bronze_packs()
        cur_time = time.time()
        total_time = cur_time-start_time
        time_string = f"{round(total_time)//3600:0>2}h{(round(total_time)%3600)//60:0>2}m{(round(total_time)%3600)%60:0<2}s"
        print(f"Number of players transfer listed on pack set {i+1}:", num_trans_players)
        print(f"Time taken on pack set {i+1}: {time_string}")
        print(f"Average pack duration on pack set {i+1}: {(total_time)/num:.2f}")
        sleep(5)
        if sets == 1:
            break
        relist_transfers()

def run_complete_sbc(card_type=None):
    if not card_type:
        card_type = input("Would you like to complete sbc with silver or bronze players? ")
        
    sleep(2)
    complete_sbc(card_type.lower()[0])
    relist_transfers()

def run_open_packs(num=None):
    
    if not num:
        num = int(input("How many packs would you like to open? "))
    sleep(2)
    mouse_click(Cord.store_tab,3)
    for _ in range(num):
        mouse_click(Cord.my_packs,0.5)
        mouse.position=(800,400)
        mouse_scroll(10,0.3)
        open_packs()

if __name__ == "__main__":
    
    run_bpm(50,4)
    

    
    


        
