from os import curdir
import os
import time
from pynput.keyboard import Controller as KeyboardController
from pynput.mouse import Controller as MouseController, Button
from time import sleep
from random import uniform as rand, randint, shuffle
from PIL import ImageGrab
from dotenv import load_dotenv

keyboard = KeyboardController()
mouse = MouseController()

cur_dir = curdir
img_dir = '\\FUTImgs'

load_dotenv()

class ImageCord:
    
    # Image Locations
    no_transfers_found = os.getenv('no_transfers_found')            # White magnifiying glass when transfers not found.
    player_red_cross = os.getenv('player_red_cross')                # Red cross on player search bar, middle of red cross.
    card_type_red_cross = os.getenv('card_type_red_cross')          # Red cross on card quality pulldown, middle of red cross.
    card_pos = os.getenv('card_pos')                                # List of positions that the card tile (i.e the top left gold section on a gold card, 6 different locations) appears during a search.
    check_logged_out = os.getenv('check_logged_out')                # Area next to ok when logged out error message pops up.
    check_not_logged_out = os.getenv('check_not_logged_out')        # Area in the bottom right of the screen when the message pops up, screen goes dark if msg pops up, so this area will be darker than usual.
    duplicate_item = os.getenv('duplicate_item')                    # One of the white characters in the word 'Item' when item is duplicate ('Swap Duplicate item' text)


class ImageColour:

    # Image colours
    red_cross_colour = os.getenv('red_cross_colour') 
    dark_generic_colour = os.getenv('dark_generic_colour') 
    darkened_corner_colour = os.getenv('darkened_corner_colour') 
    white_generic_colour = os.getenv('white_generic_colour')
    item_not_there_colour = os.getenv('item_not_there_colour') 


class MouseCord:

        # Mouse Positions
        name_location = os.getenv('name_location')                  # Text box location of player search
        name_press_location = os.getenv('name_press_location')      # Location of first player name when typing in a name
        mouse_off_text_box = os.getenv('mouse_off_text_box')        # Space for the mouse to move off the text box after finding a name
        card_type = os.getenv('card_type')                          # Card quality box location
        special_card_type = os.getenv('special_card_type')          # Special card quality location after pressing quality box
        card_type_cross = os.getenv('card_type_cross')              # Red cross that deselects card quality
        logged_out_ok = os.getenv('logged_out_ok')                  # Location of 'OK' button if asked to log back in
        search_button = os.getenv('search_button')                  # Location of search button
        max_BIN_price = os.getenv('max_BIN_price')                  # Location of max BIN Price text box

        #FUTSnipeEXE Locations
        shortcuts = os.getenv('shortcuts')                          # Location of exeSniper shortcuts button
        buy_it_price = os.getenv('buy_it_price')                    # Location of search + buy it now + OK text box value on exeSniper shortcuts
        list_on_market_BIN = os.getenv('list_on_market_BIN')        # Location of list on market 1 text box BIN value on exeSniper shortcuts


key_dict = {
    'searchBuy': 'o',
    'listItem': 'f',
    'sendToTL': 't',
    'sendToClub': 's',
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
    mouse_click(MouseCord.name_location, 1)
    type_word(player, 1.5)
    sleep(2.5)
    mouse_click(MouseCord.name_press_location, 0.1)
    sleep(0.5)

    if is_pixel(ImageCord.card_type_red_cross, (0,0), ImageColour.red_cross_colour):
        mouse_click(MouseCord.card_type_cross, 0.3)

    if is_special:

        mouse_click(MouseCord.card_type, 0.3)
        mouse_click(MouseCord.special_card_type, 0.3)


    mouse_click(MouseCord.max_BIN_price, 0.5)
    type_word(price, 0.1)
    mouse_click(MouseCord.mouse_off_text_box, 0.5)


def send_or_tl_player():
    rand_sleep(0.5)
    if is_pixel(ImageCord.duplicate_item, (0,0), ImageColour.dark_generic_colour):
        key_press(key_dict['sendToClub'], 1)
    else:
        key_press(key_dict['sendToTL'], 1)


def search_for_player(delay_length=25, num_cycles=10, send_to_club=False):
    
    for c in range(num_cycles):
        sleep(2)
        
        if is_pixel(ImageCord.check_logged_out, (0,0), ImageColour.dark_generic_colour) and is_pixel(ImageCord.check_not_logged_out, (0,0), ImageColour.darkened_corner_colour):
            sleep(2)
            mouse_click(MouseCord.logged_out_ok, 3)
            return True

        key_press(key_dict['rMinBIN'], 0.1)
        counter = 0
        while counter < 8:
            key_press(key_dict['searchBuy'], 1)          
            no_results = False
            while True:
                sleep(0.1)
                # Check if any results appeared
                if is_pixel(ImageCord.no_transfers_found, (0,0), ImageColour.white_generic_colour):
                    no_results = True

                
                if no_results or not is_pixel(ImageCord.card_pos[0], (0,0), ImageColour.item_not_there_colour):
                    break      

            if not no_results:
                rand_sleep(1)
                if send_to_club:
                    send_or_tl_player()
                else:
                    list_player()                

            key_press(key_dict['back'], 0.5)
            key_press(key_dict['iMinBIN'], 0.1)
            counter += 1

        key_press(key_dict['rMinBIN'])      # Reset Min BIN
        if not (c+1) % 5:
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
        mouse_click(MouseCord.search_button, 3)
        num_players = 0
        for box in ImageCord.card_pos:
            if not is_pixel(box, (0,0), ImageColour.item_not_there_colour):
                num_players += 1
            else:
                break
        print("Number of players:", num_players)
        
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
    buying_pice = int(bin_price * 0.95) - min_undercut

    mouse_click(MouseCord.shortcuts, 0.3)
    mouse_click(MouseCord.list_on_market_BIN, 0.3, 2)
    type_word(bin_price, 0.2)
    mouse_click(MouseCord.buy_it_price, 0.3, 2)
    type_word(buying_pice + 1000, 0.2)
    mouse_click(MouseCord.shortcuts, 0.3)
    mouse_click(MouseCord.mouse_off_text_box, 0.5)


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
            if is_pixel(ImageCord.player_red_cross, (0,0), ImageColour.red_cross_colour):
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


def buy_players_only(delay_length, num_cycles):
    start_time = time.time()
    
    cut_early = search_for_player(delay_length, num_cycles, send_to_club=True)

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
    The last boolean is whether the card is a 'special' type or not, like a TOTW.
    """
    players = [('ziyech', 20750, True), ('Verratti', 41000, True), ('Digne', 23000, True)]
    run(players, min_undercut=300, num_loops=2, random=True, delay_length=30)
