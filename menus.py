import tcod

from init_constants import *

from yaml_functions import read_yaml
from batchim import 받침

SYS_LOG = read_yaml("system_log.yaml")
ITEM_LOG = read_yaml("item_log.yaml")

def menu(root, con, header, options, line_up=True):
    """
    a,b,c 등으로 정렬해줌
    """

    if len(options) > 26: raise ValueError('Cannot have a menu with more than 26 options.')

    # calculate root height for the header (after auto-wrap) and one line per option
    header_height = tcod.console_get_height_rect(con, 0, 0, MESSAGE_WIDTH, SCREEN_HEIGHT, header)
    height = len(options) + header_height

    # create an off-screen console that represents the menu's window
    window = tcod.Console(MESSAGE_WIDTH, height)

    # print the header, with auto-wrap
    window.print_box(0, 0, MESSAGE_WIDTH, height, header, alignment=tcod.LEFT)

    # print all the options
    y = header_height
    letter_index = ord('a')

    for option_text in options:
        if line_up:
            text = F"({chr(letter_index)}) {option_text}"
        else:
            text = option_text
        window.print(0, y, text, alignment=tcod.LEFT, fg=tcod.white)
        y += 1
        letter_index += 1

    # blit the contents of "window" to the root console
    x = int(SCREEN_WIDTH / 2 - MESSAGE_WIDTH / 2)
    y = int(MAP_HEIGHT / 2 - height / 2)
    window.blit(root, x, y, 0, 0, MESSAGE_WIDTH, height, fg_alpha=1.0, bg_alpha=0.7)

def inventory_menu(root, con, header, inventory):
    # show a menu with each item of the inventory as an option
    if len(inventory.items) == 0:
        options = ['Inventory is empty.']
    else:
        options = []
        for item in inventory.items:
            if item._Equippable:
                if item._Equippable.equipped:
                    log = ITEM_LOG['equipping_log']
                    log = f' ({log})'
                else:
                    log = ""
                options.append(f'{item.name}{log}')
            else:
                options.append(item.name if item._Item.quantity == 1 else F"{item.name} x {item._Item.quantity}")

    menu(root, con, header, options, line_up=True)

def character_screen(root, con, header, **kw_locations):

    def handle_attr(target_object, route): #단일 경로 정보 하나를 찾음. 중첩 경로 지원
        if len(route) == 1: #단일 정보
            return getattr(target_object, route)
        elif len(route) == 2: #이중 정보
            return getattr(getattr(target_object, route[0]), route[1])
        else:
            print("The hell you put in?")

    def find_location(target_object, **kwargs): #kwargs에서 필요한 객체를 찾아줌.
        for name, objects in kwargs.items():
            if name == target_object:
                answer = objects
                break
        return answer

    infos = []
    kinds = SYS_LOG['character_info_log']['showing']
    #print(f'kinds:{kinds}')
    for key, value in kinds.items():
        #print(f'value:{value}')
        location = find_location(value['owner'], **kw_locations) #찾는 객체 이름.
        name = value['name']
        route = value['route']
        load_type = value['type']

        if load_type == 'value':
            #print(f'location{location}, route {route}')
            total_attr = handle_attr(location, route)

        elif load_type == 'ratio':
            total_attr = f'{handle_attr(location, route[0])}/{handle_attr(location, route[1])}'

        infos.append(f'{name}: {total_attr}')

    menu(root, con, header, infos, line_up=False)