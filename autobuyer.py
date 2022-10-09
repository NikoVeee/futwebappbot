from os import curdir
import os
import time
from pynput.keyboard import Controller as KeyboardController
from pynput.mouse import Controller as MouseController, Button
from time import sleep
from random import uniform as rand, randint, shuffle
from PIL import ImageGrab
from dotenv import load_dotenv
import ast

keyboard = KeyboardController()
mouse = MouseController()

cur_dir = curdir
img_dir = '\\FUTImgs'

load_dotenv()

class ImageCord:
    
    # Image Locations
    no_transfers_found = ast.literal_eval(os.getenv('no_transfers_found'))                          # White magnifiying glass when transfers not found.
    player_red_cross = ast.literal_eval(os.getenv('player_red_cross'))                              # Red cross on player search bar, middle of red cross.
    card_type_red_cross = ast.literal_eval(os.getenv('card_type_red_cross'))                        # Red cross on card quality pulldown, middle of red cross.
    card_pos = ast.literal_eval(os.getenv('card_pos'))                                              # List of positions that the card tile (i.e the top left gold section on a gold card, 6 different locations) appears during a search.
    check_logged_out = ast.literal_eval(os.getenv('check_logged_out'))                              # Area next to ok when logged out error message pops up.
    check_not_logged_out = ast.literal_eval(os.getenv('check_not_logged_out'))                      # Area in the bottom right of the screen when the message pops up, screen goes dark if msg pops up, so this area will be darker than usual.
    duplicate_item = ast.literal_eval(os.getenv('duplicate_item'))                                  # One of the white characters in the word 'Item' when item is duplicate ('Swap Duplicate item' text).
    failed_purchase = ast.literal_eval(os.getenv('failed_purchase'))                                # Box that appears if purchase failed.
    transfer_found = ast.literal_eval(os.getenv('transfer_found'))                                  # Orange 'watch' button that appears if a result occurs.
    

class ImageColour:

    # Image colours
    red_cross_colour = ast.literal_eval(os.getenv('red_cross_colour'))                              # Red cross colour.
    dark_generic_colour = ast.literal_eval(os.getenv('dark_generic_colour'))                        # Generic dark blue colour for buttons.
    darkened_corner_colour = ast.literal_eval(os.getenv('darkened_corner_colour'))                  # Colour of the corner pixel when darkened (i.e. logged out message)
    white_generic_colour = ast.literal_eval(os.getenv('white_generic_colour'))                      # White generic text colour.
    tranfer_found_box_information_bg_colour = ast.literal_eval(os.getenv('tranfer_found_box_information_bg_colour'))                    # Generic orange colour for buttons.
    item_not_there_colour = ast.literal_eval(os.getenv('item_not_there_colour'))                    # Colour of transfer results when item is not there (background of item selection).


class MouseCord:

    # Mouse Positions
    name_location = ast.literal_eval(os.getenv('name_location'))                                    # Text box location of player search.
    name_press_location = ast.literal_eval(os.getenv('name_press_location'))                        # Location of first player name when typing in a name.
    mouse_off_text_box = ast.literal_eval(os.getenv('mouse_off_text_box'))                          # Space for the mouse to move off the text box after finding a name.
    card_type = ast.literal_eval(os.getenv('card_type'))                                            # Card quality box location.
    special_card_type = ast.literal_eval(os.getenv('special_card_type'))                            # Special card quality location after pressing quality box.
    card_type_cross = ast.literal_eval(os.getenv('card_type_cross'))                                # Red cross that deselects card quality.
    logged_out_ok = ast.literal_eval(os.getenv('logged_out_ok'))                                    # Location of 'OK' button if asked to log back in.                               # Location of search button.
    player_max_BIN_price = ast.literal_eval(os.getenv('player_max_BIN_price'))                      # Location of max BIN Price text box.
    consumables_max_BIN_price = ast.literal_eval(os.getenv('consumables_max_BIN_price'))            # Consumables max BIN price text box.
    player_search_tab = ast.literal_eval(os.getenv('player_search_tab'))                            # Player search tab.
    consumables_search_tab = ast.literal_eval(os.getenv('consumables_search_tab'))                  # Consumables search tab.
    consumable_dropdown = ast.literal_eval(os.getenv('consumable_dropdown'))                        # Location of consumable dropdown menu. 
    chemstyle_dropdown = ast.literal_eval(os.getenv('chemstyle_dropdown'))                          # Location of chemstyle dropdown menu. 
    chemstyle_menu_scroll = ast.literal_eval(os.getenv('chemstyle_menu_scroll'))                    # Chem style menu location for scrolling.
    chemstyle_option = ast.literal_eval(os.getenv('chemstyle_option'))                              # Location of chemstyle choice dropdown.
    first_chemstyle_choice_select = ast.literal_eval(os.getenv('first_chemstyle_choice_select'))    # Location of the first chem style on the list - use scroll to select which item will be there.
    clear_sold_button = ast.literal_eval(os.getenv('clear_sold_button'))                            # Location of the clear sold button on the transfer list page.
    reset_all_transfer_search = ast.literal_eval(os.getenv('reset_all_transfer_search'))            # Location of the reset button on the transfer screen.
    

    #FUTSnipeEXE Locations
    shortcuts = ast.literal_eval(os.getenv('shortcuts'))                                            # Location of exeSniper shortcuts button
    buy_it_price = ast.literal_eval(os.getenv('buy_it_price'))                                      # Location of search + buy it now + OK text box value on exeSniper shortcuts
    list_on_market_BIN = ast.literal_eval(os.getenv('list_on_market_BIN'))                          # Location of list on market 1 text box BIN value on exeSniper shortcuts


key_dict = {
    'searchBuy': 'o',
    'searchNoBuy': 'p',
    'listItem': 'f',
    'sendToTL': 't',
    'sendToClub': 's',
    'dMinBIN': 'u',
    'iMinBIN': 'i',
    'rMinBIN': 'r',
    'dMinBid': 'j',
    'iMinBid': 'k',
    'rMinBid': 'h',
    'iMaxBIN': '/',
    'dMaxBIN': '.',
    'rMaxBIN': ',',
    'back': '9',
    'transSearch': '2',
    'transList': '3',
}

consumable_scroll_dict = {
    'anchor': 13,
    'hunter': 14,
    'shadow': 15
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


def set_up_player(player, price, is_special):
    mouse_click(MouseCord.player_search_tab, 1)
    mouse_click(MouseCord.reset_all_transfer_search, 1)
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

    mouse_click(MouseCord.player_max_BIN_price, 0.5)
    type_word(price, 0.1)
    mouse_click(MouseCord.mouse_off_text_box, 0.5)


def set_up_consumable(consumable):
    mouse_click(MouseCord.consumables_search_tab, 1)
    mouse_click(MouseCord.reset_all_transfer_search, 1)
    mouse_click(MouseCord.consumable_dropdown, 1)
    mouse_click(MouseCord.chemstyle_option,1)
    mouse_click(MouseCord.chemstyle_dropdown,1)
    try:
        mouse.position = MouseCord.chemstyle_menu_scroll
        rand_sleep(1)
        mouse_scroll(n=consumable_scroll_dict[consumable]*-1)
        rand_sleep(1)
    except KeyError:
        raise Exception("No chemstyle found for that scroll value.")
    mouse_click(MouseCord.first_chemstyle_choice_select, 1)


def sent_or_tl_item():
    rand_sleep(0.5)
    if is_pixel(ImageCord.duplicate_item, (0,0), ImageColour.dark_generic_colour):
        key_press(key_dict['sendToClub'], 1)
    else:
        key_press(key_dict['sendToTL'], 1)


def search_for_item(delay_length=25, num_cycles=10, send_to_club=False):
    
    for c in range(num_cycles):
        sleep(1)
        
        if is_pixel(ImageCord.check_logged_out, (0,0), ImageColour.dark_generic_colour) and is_pixel(ImageCord.check_not_logged_out, (0,0), ImageColour.darkened_corner_colour):
            sleep(2)
            mouse_click(MouseCord.logged_out_ok, 3)
            return True 

        key_press(key_dict['rMinBIN'], 0.1)
        counter = 0
        while counter < 8:
            key_press(key_dict['searchBuy'], 0.6)          
            no_results = False
            while True:
                sleep(0.2)
                # Check if any results appeared
                if is_pixel(ImageCord.no_transfers_found, (0,0), ImageColour.white_generic_colour):
                    no_results = True
                    break
                
                # Check if results appeared - if neither, then loop again.
                if is_pixel(ImageCord.transfer_found, (0,0), ImageColour.tranfer_found_box_information_bg_colour):
                    break      

            if not no_results:
                rand_sleep(0.5)
                if not is_pixel(ImageCord.failed_purchase, (0,0), ImageColour.red_cross_colour):
                    rand_sleep(0.5)
                    if send_to_club:
                        sent_or_tl_item()
                    else:
                        list_item()       

            key_press(key_dict['back'], 0.5)
            key_press(key_dict['iMinBIN'], 0.1)
            counter += 1

        key_press(key_dict['rMinBIN'], 0.2)      # Reset Min BIN
        if not (c+1) % 5:
            rand_sleep(delay_length)

        # Increase min bid to 150 every cycle to reset the cached searching.
        if c%2:
            key_press(key_dict['iMinBid'], 0.2)
        else:
            key_press(key_dict['rMinBid'], 0.2)        

    return False


def list_item():
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
        key_press(key_dict['searchNoBuy'], 3)
        num_items = 0
        for box in ImageCord.card_pos:
            if not is_pixel(box, (0,0), ImageColour.item_not_there_colour):
                num_items += 1
            else:
                break
        print("Number of items:", num_items)
        
        key_press(key_dict['back'], 1)

        if num_items <= 3:
            if first:
                return find_transfer_price(cur_price)
            else: 
                return cur_price
        else:
            key_press(key_dict['dMaxBIN'], 0.3)
            cur_price = decrement_price(cur_price)

        first = False


def clear_tranfer_list():
    key_press(key_dict['transList'], 4)
    mouse_click(MouseCord.clear_sold_button, 4)


def set_up_price(price, min_undercut, consumable=False):
    key_press(key_dict['rMinBIN'], 0.2)
    buying_pice = int(price * 0.95) - min_undercut

    # Set up Max BIN price in search.
    if consumable:
        mouse_click(MouseCord.consumables_max_BIN_price, 0.5)
    else:
        mouse_click(MouseCord.player_max_BIN_price, 0.5)
    
    type_word(buying_pice, 0.1)
    mouse_click(MouseCord.mouse_off_text_box, 0.5)

    # Set up exeShortcuts to right price values.
    mouse_click(MouseCord.shortcuts, 0.3)
    mouse.position = MouseCord.list_on_market_BIN
    mouse_scroll(20)
    mouse_click(MouseCord.list_on_market_BIN, 0.3, 2)
    type_word(price, 0.2)
    mouse_click(MouseCord.buy_it_price, 0.3, 2)
    type_word(int(buying_pice*1.05), 0.2)
    mouse_click(MouseCord.shortcuts, 0.3)
    mouse_click(MouseCord.mouse_off_text_box, 0.5)


def player_sniping(players, min_undercut=500, num_loops=1, random=False, delay_length=10):
    loops = 0
    if random:
        shuffle(players)
    
    key_press(key_dict['transSearch'], 3)
    
    while loops < num_loops:
        key_press(key_dict['rMinBIN'], 0.2)
        for player, price, is_special in players:
            set_up_player(player, price, is_special)
            rand_sleep(1)
            cut_early = True

            # Failover: if player isn't selected DO NOT SEARCH.
            if is_pixel(ImageCord.player_red_cross, (0,0), ImageColour.red_cross_colour):
                new_price = find_transfer_price(price)
                set_up_price(new_price, min_undercut, consumable=False)
                cut_early = search_for_item(delay_length, num_cycles=20)

            if cut_early:
                break

        if cut_early:
            break
            
        loops += 1


def chemstyle_sniping(consumables, min_undercut=100, num_loops=1, delay_length=10):
    loops = 0
    
    while loops < num_loops:
        
        key_press(key_dict['transSearch'], 2)
        key_press(key_dict['rMinBIN'], 0.2)
        for chemstyle, price in consumables:
            set_up_consumable(chemstyle)
            rand_sleep(1)
            cut_early = True
            set_up_price(price, min_undercut, consumable=True)
            cut_early = search_for_item(delay_length, num_cycles=20)

            if cut_early:
                break
        
        clear_tranfer_list()

        if cut_early:
            break
        
        loops += 1


def run(players=None, consumables=None, min_undercut=500, num_loops=1, random=False, delay_length=10):

    start_time = time.time()

    sleep(2)    
    if players:
        cut_early = player_sniping(players, min_undercut, num_loops, random, delay_length)

    elif consumables:
        cut_early = chemstyle_sniping(consumables, min_undercut, num_loops, delay_length)
    
    elapsed_time = time.time() - start_time
    hours = elapsed_time // 3600
    minutes = (elapsed_time - hours*3600)//60
    seconds = elapsed_time - hours*3600 - minutes*60

    print(f"{'Operation Halted Early. ' if cut_early else ''}Time taken for operation: {hours:02.0f}h {minutes:02.0f}m {seconds:02.0f}s")


def ryan(delay_length, num_cycles):

    start_time = time.time()
    
    cut_early = search_for_item(delay_length, num_cycles)

    elapsed_time = time.time() - start_time
    hours = elapsed_time // 3600
    minutes = (elapsed_time - hours*3600)//60
    seconds = elapsed_time - hours*3600 - minutes*60

    print(f"{'Operation Halted Early. ' if cut_early else ''}Time taken for operation: {hours:02.0f}h {minutes:02.0f}m {seconds:02.0f}s")


def buy_players_only(delay_length, num_cycles):
    start_time = time.time()
    
    cut_early = search_for_item(delay_length, num_cycles, send_to_club=True)

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
    # players = [('cuadrado', 13500, False), ('frimpong', 11500, False), ('clauss', 13500, True), ('sorloth', 16500, True)]
    # run(players=players, min_undercut=500, num_loops=5, random=True, delay_length=10)
    chemstyles = [('anchor', 1300), ('hunter', 1700), ('shadow', 3000)]
    run(consumables=chemstyles, min_undercut=100, num_loops=6, delay_length=20)