#Import Statements
from os import curdir
import time
from pynput.keyboard import Controller as keyCont, Key
from pynput.mouse import Controller, Button
from time import sleep
from random import uniform as rand, randint, shuffle
from PIL import ImageGrab

keyboard = keyCont()
mouse = Controller()

cur_dir = curdir
img_dir = '\\FUTImgs'

class Cord:
    
    # Image Locations
    no_transfers_found = (1000, 522, 1001, 523)
    player_red_cross = (1481, 402, 1482, 403)

    card_type_red_cross = (970, 466, 971, 467)

    card_pos = [(490, 350, 491, 351), (490, 470, 491, 471), (490, 589, 491, 590), (490, 706, 491, 707), (490, 823, 491, 824), (490, 908, 491, 909)]

    check_logged_out = (1155, 501, 1156, 502)
    check_not_logged_out = (562, 380, 563, 381)
    

    # Mouse Positions
    name_location = (462, 321)
    name_press_location = (453, 381)

    max_BIN_price = (874, 686)

    search_button = (997, 754)
    
    mouse_off_text_box = (1001, 651)

    card_type = (518, 375)
    special_card_type = (498, 522)
    card_type_cross = (775, 374)

    logged_out_ok = (708, 518)

    #FUTSnipeEXE Locations

    shortcuts = (1289, 158)
    buy_it_price = (240, 267)

    list_on_market_bid = (196, 305)
    list_on_market_BIN = (240, 305)


"""
MAKE SURE YOUR BROWSER WINDOW IS ON 75% ZOOM!!!
MAKE SURE YOUR COMPUTER DISPLAY HAS A RESOLUTION OF 1920 x 1080 pixels, 
AND that it has an 125% Scaling and Layout!


Set-up the exeSniper extension with the following settings:

Search + Buy it now + OK: O
Sent to Transfer List: T

List on Market 1: A

Decrease Min BIN: U
Increase Min BIN: I
Reset Min BIN: R

Decrease Max BIN: J
Increase Max BIN: K
Reset Max BIN: H

Back Page: 9

Below is the dictionary where you can change these values if you so desire.
"""

key_dict = {
    'searchBuy': 'o',
    'listItem': 'a',
    'sendToTL': 't',
    'dMinBIN': 'u',
    'iMinBIN': 'i',
    'rMinBIN': 'r',
    'dMaxBIN': 'j',
    'iMaxBIN': 'k',
    'rMaxBIN': 'h',
    'back': '9',
    'transSearch': '2',
    'transList': '3',
}


def rand_sleep(time):
    margin = time*0.15
    sleep(rand(time-margin, time+margin))


def key_press(key, tsleep=0):
    keyboard.press(key)
    keyboard.release(key)
    rand_sleep(tsleep)


def mouse_scroll(n=-10, tsleep=0):
    mouse.scroll(0,n)
    rand_sleep(tsleep)


def mouse_click(coords, tsleep=0, num_clicks=1):
    mouse.position = coords
    sleep(0.1)
    for _ in range(num_clicks):
        mouse.click(Button.left, 1)
        sleep(0.1)
    rand_sleep(tsleep)


def type_word(word, tsleep=0.1):
    for char in str(word):
        key_press(char, 0.03)

    rand_sleep(tsleep)


def is_pixel(box, coord, pixel, im=None):
    if box or box==():
        im = screenGrab(box, False)
    try:
        return True if im.getpixel(coord)==pixel else False
    except:
        print("'im' object not provided")


def screenGrab(box=(), save=True):
    im = ImageGrab.grab(box)
    if save:
        imgname = 'img__' +str(randint(0,50)) + '.png'
        im.save(cur_dir + img_dir, 'PNG')
        return imgname
    else:
        return im


def decrement_price(price):
    if price <= 1000:
        return price - 50
    elif price <= 10000:
        return price - 100   
    elif price <= 50000:
        return price - 250     
    elif price <= 100000:
        return price - 500    
    return price - 1000


def increment_price(price):
    if price == 0:
        return 200
    elif price < 1000:
        return price + 50
    elif price < 10000:
        return price + 100
    elif price < 50000:
        return price + 250
    elif price < 100000:
        return price + 500
    return price + 1000


def set_as_special():
    pass


def set_up_player(player, price, is_special):
    mouse_click(Cord.name_location, 1)
    type_word(player, 1.5)
    sleep(2.5)
    mouse_click(Cord.name_press_location, 0.1)
    sleep(0.5)

    if is_pixel(Cord.card_type_red_cross, (0,0), (227, 22, 56)):
        mouse_click(Cord.card_type_cross, 0.3)

    if is_special:

        mouse_click(Cord.card_type, 0.3)
        mouse_click(Cord.special_card_type, 0.3)


    mouse_click(Cord.max_BIN_price, 0.5)
    type_word(price, 0.1)
    mouse_click(Cord.mouse_off_text_box, 0.5)


def search_for_player(delay_length=25, num_cycles=10):
    
    for c in range(num_cycles):
        sleep(2)
        
        if is_pixel(Cord.check_logged_out, (0,0), (28, 31, 38)) and not is_pixel(Cord.check_not_logged_out, (0,0), (28, 31, 38)):
            sleep(2)
            mouse_click(Cord.logged_out_ok, 3)
            return True

        key_press(key_dict['rMinBIN'], 0.1)
        counter = 0
        while counter < 6:          
            key_press(key_dict['searchBuy'], 2)
            # TODO: Loop checking pixel if changed.
            
            # Check if any results appeared
            if not is_pixel(Cord.no_transfers_found, (0,0), (242,242,242)):
                list_player()

            key_press(key_dict['back'], 0.5)
            key_press(key_dict['iMinBIN'], 0.1)
            counter += 1

        key_press(key_dict['rMinBIN'])      # Reset Min BIN
        if not (c+1) % 3:
            rand_sleep(delay_length)

    return False


def list_player():
    rand_sleep(2)
    key_press(key_dict['listItem'], 4)    


def find_transfer_price(est_price):
    cur_price = est_price
    for _ in range(3):
        cur_price = increment_price(cur_price)
        key_press(key_dict['iMaxBIN'])   
    
    sleep(1)
    first = True 
    while True:
        mouse_click(Cord.search_button, 3)
        num_players = 0
        for box in Cord.card_pos:
            if not is_pixel(box, (0,0), (28, 31, 38)):
                num_players += 1
            else:
                break
        
        key_press(key_dict['back'], 1)

        if num_players <= 3:
            if first:
                return find_transfer_price(cur_price)
            else: 
                return cur_price
        else:
            key_press(key_dict['dMaxBIN'], 0.3)
            cur_price = decrement_price(cur_price)

        first = False


def set_up_price(price, min_undercut):
    key_press(key_dict['rMinBIN'], 0.2)
    bin_price = price
    bid_price = decrement_price(price)
    buying_pice = int(bin_price * 0.95) - min_undercut

    mouse_click(Cord.shortcuts, 0.3)
    mouse_click(Cord.list_on_market_bid, 0.3, 2)
    type_word(bid_price, 0.2)
    mouse_click(Cord.list_on_market_BIN, 0.3, 2)
    type_word(bin_price, 0.2)
    mouse_click(Cord.buy_it_price, 0.3, 2)
    type_word(buying_pice + 500, 0.2)
    mouse_click(Cord.shortcuts, 0.3)

    mouse_click(Cord.max_BIN_price, 0.3)
    type_word(buying_pice, 0.1)
    mouse_click(Cord.mouse_off_text_box, 0.5)


def run(players, min_undercut=500, num_loops=1, random=False, delay_length=10):

    start_time = time.time()

    sleep(2)
    loops = 0
    if random:
        shuffle(players)
    
    while loops < num_loops:
        key_press(key_dict['rMinBIN'], 0.2)
        for player, price, is_special in players:
            set_up_player(player, price, is_special)
            rand_sleep(1)
            cut_early = True

            # Failover: if player isn't selected DO NOT SEARCH.
            if is_pixel(Cord.player_red_cross, (0,0), (227,22,56)):
                new_price = find_transfer_price(price)
                set_up_price(new_price, min_undercut)
                cut_early = search_for_player(delay_length, num_cycles=20)

            if cut_early:
                break

        if cut_early:
            break
            
        loops += 1

    elapsed_time = time.time() - start_time
    hours = elapsed_time // 3600
    minutes = (elapsed_time - hours*3600)//60
    seconds = elapsed_time - hours*3600 - minutes*60

    print(f"{'Operation Halted Early. ' if cut_early else ''}Time taken for operation: {hours:02.0f}h {minutes:02.0f}m {seconds:02.0f}s")


def ryan(delay_length, num_cycles):

    start_time = time.time()
    
    cut_early = search_for_player(delay_length, num_cycles)

    elapsed_time = time.time() - start_time
    hours = elapsed_time // 3600
    minutes = (elapsed_time - hours*3600)//60
    seconds = elapsed_time - hours*3600 - minutes*60

    print(f"{'Operation Halted Early. ' if cut_early else ''}Time taken for operation: {hours:02.0f}h {minutes:02.0f}m {seconds:02.0f}s")


if __name__ == "__main__":
    """
    In the Players list, the price does not need to be accurate at all, just a general area. The program finds the price automatically. 

    Importantly, the player MUST be spelt correctly and must appear as the FIRST option on the dropdown menu when you type their name in.
    If you are searching for Luis Suarez, make sure you put their full name in, whereas if you are looking for Sancho, you only need to type
    'Sancho' as it appears as the first option.
    The last boolean is whether the card is a 'special' type or not, like an TOTW.

    To use the Ryan() function, put in a delay time (probably between 15-25 seconds) for every 8 searches. If you are away from the computer for a while,
    do a longer delay and it will be less likely you get kicked off. The second number is the number of cycles, which is the number of times the bot
    will search 8 times.
    """
    players = [('De Paul', 26000, True), ('Jonathan David', 27000, True), ('Tchouameni', 19000, True), ('Tchouameni', 19000, True), ('Courtois', 27000, False), ('Tonali', 16000, True)]
    run(players, min_undercut=300, num_loops=2, random=True, delay_length=20)
    # ryan(30, 60)