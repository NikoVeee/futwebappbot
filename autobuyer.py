from os import curdir
import os
import time
from typing import List, Tuple
from pynput.keyboard import Controller as KeyboardController
from pynput.mouse import Controller as MouseController, Button
from time import sleep
from random import uniform as rand, randint, shuffle
from PIL import ImageGrab, Image
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
    cannot_authenticate = ast.literal_eval(os.getenv('cannot_authenticate'))                        # Header of the cannot authenticate error message.
    duplicate_item = ast.literal_eval(os.getenv('duplicate_item'))                                  # One of the white characters in the word 'Item' when item is duplicate ('Swap Duplicate item' text).
    failed_purchase = ast.literal_eval(os.getenv('failed_purchase'))                                # Box that appears if purchase failed.
    transfer_found = ast.literal_eval(os.getenv('transfer_found'))                                  # Orange 'watch' button that appears if a result occurs.
    

class ImageColour:

    # Image colours
    red_cross_colour = ast.literal_eval(os.getenv('red_cross_colour'))                              # Red cross colour.
    dark_generic_colour = ast.literal_eval(os.getenv('dark_generic_colour'))                        # Generic dark blue colour for buttons.
    purple_cannot_auth = ast.literal_eval(os.getenv('purple_cannot_auth'))                          # Colour of the cannot authenticate header (i.e. logged out message),
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
    # Maps chemstyle to amount of scrolling required.
    'anchor': 13,
    'hunter': 14,
    'shadow': 15
}


def rand_sleep(time: float) -> None:
    """
    Sleeps for some amount of time randomised between 15% lower or higher than given time input.

    Args:
        time (float): Number of seconds the computer will wait before executing next command.
    """
    margin = time*0.15
    sleep(rand(time-margin, time+margin))


def key_press(key: str, tsleep: float = 0) -> None:
    """
    Presses a key on the keyboard based on the key supplied.

    Args:
        key (str): Some keyboard input.
        tsleep (float, optional): Number of seconds to sleep after pressed. Defaults to 0.
    """
    keyboard.press(key)
    keyboard.release(key)
    rand_sleep(tsleep)


def mouse_scroll(n: int=-10, tsleep: float=0) -> None:
    """
    Scrolls the mouse vertically based on the n value supplied.
    Negative values scroll down, positive up.

    Args:
        n (int, optional): Number of scrolls performed. Defaults to -10.
        tsleep (float, optional): Number of seconds to sleep after pressed. Defaults to 0.
    """
    mouse.scroll(0,n)
    rand_sleep(tsleep)


def mouse_click(coords: Tuple[int, int], tsleep: float = 0, num_clicks: int = 1) -> None:
    """
    Performs a left mouse click at some position on the screen, any amount of times.

    Args:
        coords (Tuple[int, int]): Position on the screen in coordinates of where the mouse click is to be done.
        tsleep (float, optional): Amount of time to sleep after pressed. Defaults to 0.
        num_clicks (int, optional): Number of left clicks required. Defaults to 1.
    """
    mouse.position = coords
    sleep(0.1)
    for _ in range(num_clicks):
        mouse.click(Button.left, 1)
        sleep(0.1)
    rand_sleep(tsleep)


def type_word(word: str, tsleep: float = 0.1) -> None:
    """
    Types a word using key_press function.

    Args:
        word (str): The word to be typed.
        tsleep (float, optional): Number of seconds to sleep after pressed. Defaults to 0.1 secs.
    """
    for char in str(word):
        key_press(char, 0.03)

    rand_sleep(tsleep)


def is_pixel(box: Tuple[int, int, int, int], coord: Tuple[int, int], pixel_colour: Tuple[int, int, int]) -> bool:
    """
    Checks if a pixel is of a certain colour in an image.

    Args:
        box (Tuple[int, int, int, int]): Image box to be captured based on screen coordinates.
        coord (Tuple[int, int]): Coordinates relative to the image of which pixel is to be checked.
        pixel_colour (Tuple[int, int, int]): Colour in RGB form of what is to be compared to the pixel image.

    Returns:
        bool: Returns a boolean as to whether the pixel colour matches what is being tested.s
    """
    if box or box==():
        im = screenGrab(box, False)
    try:
        return True if im.getpixel(coord)==pixel_colour else False
    except:
        print("'im' object not provided")


def screenGrab(box: Tuple[int, int, int, int] = (), save: bool = True) -> Image:
    """
    Generates a screen capture based on the 4 coordinates provided by box.
    Will save to a folder supplied by img_dir if desired.

    Args:
        box (Tuple[int, int, int, int], optional): Image box to be captured based on screen coordinates. Defaults to ().
        save (bool, optional): Boolean deciding if image is to be saved to memory. Defaults to True.

    Returns:
        Image: _description_
    """
    im = ImageGrab.grab(box)
    if save:
        imgname = 'img__' +str(randint(0,50)) + '.png'
        im.save(cur_dir + img_dir, 'PNG')
        return imgname
    else:
        return im


def decrement_price(price: int) -> int:
    """
    Returns a decrement value of price based on FUT prices.

    Args:
        price (int): Price to be decremented.

    Returns:
        int: Price that is decremented.
    """

    if price <= 1000:
        return price - 50
    elif price <= 10000:
        return price - 100   
    elif price <= 50000:
        return price - 250     
    elif price <= 100000:
        return price - 500    
    return price - 1000


def increment_price(price : int) -> int:
    """
    Returns a increment value of price based on FUT prices.

    Args:
        price (int): Price to be incremented.

    Returns:
        int: Price that is incremented.
    """
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


def set_up_player(player: str, price: int, is_special: bool) -> None:
    """
    Sets up the parameters for searching for a specific player. Can be a special card.

    Args:
        player (str): Name of the player.
        price (int): Buying estimated price of the player.
        is_special (bool): Is a special card?
    """
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


def set_up_chemstyle(chemstyle: str) -> None:
    """
    Sets up the parameters for searching for a chemstyle.

    Args:
        chemstyle (str): Name of the chemstyle.

    Raises:
        Exception: Chemstyle not in dictionary.
    """
    mouse_click(MouseCord.consumables_search_tab, 1)
    mouse_click(MouseCord.reset_all_transfer_search, 1)
    mouse_click(MouseCord.consumable_dropdown, 1)
    mouse_click(MouseCord.chemstyle_option,1)
    mouse_click(MouseCord.chemstyle_dropdown,1)

    # Scrolls down the list a number of times to get the desired chemstyle.
    try:
        mouse.position = MouseCord.chemstyle_menu_scroll
        rand_sleep(1)
        mouse_scroll(n=consumable_scroll_dict[chemstyle]*-1)
        rand_sleep(1)
    except KeyError:
        raise Exception("No chemstyle found for that scroll value.")
    mouse_click(MouseCord.first_chemstyle_choice_select, 1)


def set_up_price(price: int, min_undercut: int, consumable: bool = False) -> None:
    """
    Attempts to set up the arguments for the price of an item in the search page and the fut shortcuts screen.

    Args:
        price (int): Selling price of the player.
        min_undercut (int): Amount of undercut to buy the player at.
        consumable (bool, optional): Whether or not the item is a consumable. Defaults to False.
    """
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


def sent_or_tl_item() -> None:
    """
    Either saves an item to the club, or to the transfer list if it is a duplicate.
    """
    rand_sleep(0.5)
    if is_pixel(ImageCord.duplicate_item, (0,0), ImageColour.dark_generic_colour):
        key_press(key_dict['sendToClub'], 1)
    else:
        key_press(key_dict['sendToTL'], 1)


def list_item() -> None:
    """
    Lists item on the transfer market.
    """
    rand_sleep(2)
    key_press(key_dict['listItem'], 4)


def clear_tranfer_list() -> None:
    """
    Clears the transfer list by navigating to the transfer list screen.
    """
    key_press(key_dict['transList'], 4)
    mouse_click(MouseCord.clear_sold_button, 4)    


def ok_logout() -> None:
    """
    Presses on the ok button of an error message block, if that fails it hits enter on the keyboard.
    """
    sleep(2)
    mouse_click(MouseCord.logged_out_ok, 2.5)
    key_press('enter', 0.5)


def search_for_item(delay_length: float = 15, num_cycles: int = 10, send_to_club: bool = False) -> bool:
    """
    Begins the search for an item. Will search for the item 10 x num_cycles number of times.
    If send_to_club is true, then the item will be sent to the club rather than sold.

    Args:
        delay_length (float, optional): Number of seconds delay between certain cycles. Defaults to 15.
        num_cycles (int, optional): Number of cycles to run through. Defaults to 10.
        send_to_club (bool, optional): Will send item to club if True, otherwise item will be sold. Defaults to False.

    Returns:
        bool: True if the logout screen is shown, False if the function finishes on it's own accord.
    """
    
    for c in range(num_cycles):
        sleep(1)
        
        if is_pixel(ImageCord.cannot_authenticate, (0,0), ImageColour.purple_cannot_auth):
            # If error message appears, attempt to logout.
            ok_logout()
            return True 

        key_press(key_dict['rMinBIN'], 0.1)
        counter = 0
        while counter < 8:
            key_press(key_dict['searchBuy'], 0.6)          
            no_results = False
            break_loop_counter = 0
            while True:
                sleep(0.2)
                # Check if any results appeared
                if is_pixel(ImageCord.no_transfers_found, (0,0), ImageColour.white_generic_colour):
                    no_results = True
                    break
                
                # Check if results appeared - if neither, then loop again.
                if is_pixel(ImageCord.transfer_found, (0,0), ImageColour.tranfer_found_box_information_bg_colour):
                    break   
                
                # If loops too many times, hard break it to stop it from infinitely running.
                if break_loop_counter > 10:
                    print("Something went wrong, infinite loop hit.")
                    ok_logout()
                    return True

                break_loop_counter += 1   

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


def find_transfer_price(est_price: int) -> int:
    """
    Attempts to find the true selling price of a player based on the amount of searches left on the market for a given price.

    Args:
        est_price (int): Estimated price of the player in coins.

    Returns:
        int: True selling price of the player in coi
    """
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


def player_sniping(players: List[Tuple[str, int]], min_undercut: int = 500, num_loops: int = 1, random: bool = False, delay_length: float = 10) -> None:
    """
    Runs the sniping bot for players. Takes in a list of players and attempts to buy them at a price to gain a minimum of min_undercut profit.

    Args:
        players (List[Tuple[str, int]]): List of player names and their prices in tuple format: e.g. [('Ziyech', 4000), ...]
        min_undercut (int, optional): Minimum profit to be made on each purchase. Defaults to 500.
        num_loops (int, optional): Number of loops for the algorithm to run. Defaults to 1.
        random (bool, optional): If true, the list of players will get shuffled to always start with a new player. Defaults to False.
        delay_length (float, optional): Number of seconds to sleep when searching for an item. Defaults to 10.
    """
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


def chemstyle_sniping(chemstyles: List[Tuple[str, int]], min_undercut: int = 100, num_loops: int = 1, delay_length: float = 10) -> None:
    """
    Runs the sniping bot for chemstyles. Takes in a list of chemstyles and their selling prices (note not estimate) and attempts to buy 
    them at a price to gain a minimum of min_undercut profit.

    Args:
        chemstyles (List[Tuple[str, int]]): List of chemstyles names and their prices in tuple format: e.g. [('shadow', 3000), ...]
        min_undercut (int, optional): Minimum profit to be made on each purchase. Defaults to 500.
        num_loops (int, optional): Number of loops for the algorithm to run. Defaults to 1.
        delay_length (float, optional): Number of seconds to sleep when searching for an item. Defaults to 10.
    """
    loops = 0
    
    while loops < num_loops:
        
        key_press(key_dict['transSearch'], 2)
        key_press(key_dict['rMinBIN'], 0.2)
        for chemstyle, price in chemstyles:
            set_up_chemstyle(chemstyle)
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


def run(players: List[Tuple[str, int]] = None, consumables: List[Tuple[str, int]] = None, min_undercut: int = 500, num_loops: int = 1, random: bool = False, delay_length: float = 10) -> None:
    """
    Main running function. Will print time stats and choose whether to run the chemstyle bot or player sniping bot.

    Args:
        players (List[Tuple[str, int]], optional): List of player names and their prices in tuple format: e.g. [('Ziyech', 4000), ...]. Defaults to None.
        consumables (List[Tuple[str, int]], optional): List of chemstyles names and their prices in tuple format: e.g. [('shadow', 3000), ...]. Defaults to None.
        min_undercut (int, optional): Minimum profit to be made on each purchase. Defaults to 500.
        num_loops (int, optional): Number of loops for the algorithm to run. Defaults to 1.
        random (bool, optional): If true, the list of players will get shuffled to always start with a new player. Defaults to False.
        delay_length (float, optional): Number of seconds to sleep when searching for an item. Defaults to 10.
    """

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


# def ryan(delay_length, num_cycles):

#     start_time = time.time()
    
#     cut_early = search_for_item(delay_length, num_cycles)

#     elapsed_time = time.time() - start_time
#     hours = elapsed_time // 3600
#     minutes = (elapsed_time - hours*3600)//60
#     seconds = elapsed_time - hours*3600 - minutes*60

#     print(f"{'Operation Halted Early. ' if cut_early else ''}Time taken for operation: {hours:02.0f}h {minutes:02.0f}m {seconds:02.0f}s")


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
    chemstyles = [('anchor', 1200), ('hunter', 1800), ('shadow', 3000)]
    run(consumables=chemstyles, min_undercut=100, num_loops=6, delay_length=20)