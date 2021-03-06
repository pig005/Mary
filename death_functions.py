import tcod

from map_objects.game_map import GameMap

from enums.game_states import GameStates
from renderer.render_functions import RenderOrder
from game_messages import Message

from yaml_functions import read_yaml, cout
from batchim import 받침

SYS_LOG = read_yaml("system_log.yaml")

def kill_player(player):
    player.color = tcod.darker_gray
    return Message(SYS_LOG['dead_player'], tcod.red), GameStates.PLAYER_DEAD

def insane_player(player):
    player.color = tcod.darker_violet
    return Message(SYS_LOG['insane_player'], tcod.red), GameStates.PLAYER_DEAD

def kill_monster(monster, game_map):
    game_map.monsters -= 1
    capped = monster.name.capitalize()
    death_message = Message(cout(SYS_LOG['death_log'],받침(capped)), tcod.orange)
    monster.name = cout(SYS_LOG['dead_entity'],받침(capped,'(이었','(였'))
    monster.char = '%'
    monster.color = tcod.dark_red
    monster.blocks = False
    monster.render_order = RenderOrder.CORPSE
    monster._Fighter = None
    monster._Ai = None

    return death_message