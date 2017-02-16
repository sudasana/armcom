#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Python 2.7.8
##########################################################################################
#                                  Armoured Commander                                    #
#                       The World War II Tank Commander Roguelike                        #
##########################################################################################

##########################################################################################
#
#    Copyright 2015-2017 Gregory Adam Scott (sudasana@gmail.com)
#
#    This file is part of Armoured Commander.
#
#    Armoured Commander is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Armoured Commander is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with Armoured Commander, in the form of a file named "LICENSE".
#    If not, see <http://www.gnu.org/licenses/>.
#
#    xp_loader.py is covered under a MIT License (MIT) and is Copyright (c) 2015 Sean Hagar
#    see XpLoader_LICENSE.txt for more info.
#
##########################################################################################

##### Libraries #####
from datetime import datetime           # for recording date and time in campaign journal
from encodings import ascii, utf_8      # needed for Py2EXE version
from encodings import hex_codec         # needed for Py2EXE version
from math import atan2, degrees         # more "
from math import pi, floor, ceil, sqrt  # math functions
from operator import attrgetter         # for list sorting
from pygame.locals import *
from textwrap import wrap               # for breaking up game messages
import csv                              # for loading campaign info
import dbhash, anydbm                   # need this for py2exe
import libtcodpy as libtcod             # The Doryen Library
import os                               # for SDL window instruction, other OS-related stuff
import pygame, pygame.mixer             # for sound effects
import random                           # for randomly selecting items from a list
import shelve                           # for saving and loading games
import sys                              # for command line functions
import time                             # for wait function
import xml.etree.ElementTree as xml     # ElementTree library for xml
import xp_loader                        # for loading image files
import gzip                             # for loading image files
import zipfile, io                      # for loading from zip archive

from armcom_defs import *               # general definitions
from armcom_vehicle_defs import *       # vehicle stat definitions

##### Constants #####
DEBUG = False                           # enable in-game debug commands

NAME = 'Armoured Commander'
VERSION = '1.0'                         # determines saved game compatability
SUBVERSION = '4'                        # descriptive only, no effect on compatability

COMPATIBLE_VERSIONS = ['Beta 3.0']      # list of older versions for which the savegame
                                        #  is compatible with this version

DATAPATH = 'data' + os.sep        # path to data files

PI = pi

SCREEN_WIDTH = 149            # width of game window in characters
SCREEN_HEIGHT = 61            # height "
SCREEN_XM = int(SCREEN_WIDTH/2)        # horizontal center "
SCREEN_YM = int(SCREEN_HEIGHT/2)    # vertical "

TANK_CON_WIDTH = 73    # width of tank info console in characters
TANK_CON_HEIGHT = 37    # height "

MSG_CON_WIDTH = TANK_CON_WIDTH    # width of message console in characters
MSG_CON_HEIGHT = 19        # height "

MAP_CON_WIDTH = 73    # width of encounter map console in characters
MAP_CON_HEIGHT = 51    # height "
MAP_CON_X = MSG_CON_WIDTH + 2    # x position of encounter map console
MAP_CON_Y = 2            # y "
MAP_X0 = int(MAP_CON_WIDTH/2)    # centre of encounter map console
MAP_Y0 = int(MAP_CON_HEIGHT/2)

MAP_INFO_CON_WIDTH = MAP_CON_WIDTH    # width of map info console in characters
MAP_INFO_CON_HEIGHT = 7            # height "

DATE_CON_WIDTH = TANK_CON_WIDTH        # date, scenario type, etc. console
DATE_CON_HEIGHT = 1

MENU_CON_WIDTH = 139            # width of in-game menu console
MENU_CON_HEIGHT = 42            # height "
MENU_CON_XM = int(MENU_CON_WIDTH/2)    # horizontal center of "
MENU_CON_YM = int(MENU_CON_HEIGHT/2)    # vertical center of "
MENU_CON_X = SCREEN_XM - MENU_CON_XM                # x and y location to draw
MENU_CON_Y = int(SCREEN_HEIGHT/2) - int(MENU_CON_HEIGHT/2)    # menu console on screen

# text console, displays 84 x 50 characters
TEXT_CON_WIDTH = 86            # width of text display console (campaign journal, messages, etc.)
TEXT_CON_HEIGHT = 57            # height "
TEXT_CON_XM = int(TEXT_CON_WIDTH/2)    # horizontal center "
TEXT_CON_X = SCREEN_XM - TEXT_CON_XM    # x/y location to draw window
TEXT_CON_Y = 2

C_MAP_CON_WIDTH = 90        # width of campaign map console
C_MAP_CON_HEIGHT = 90        # height "
C_MAP_CON_WINDOW_W = 90        # width of how much of the campaign map is displayed on screen
C_MAP_CON_WINDOW_H = 57        # height "
C_MAP_CON_X = SCREEN_WIDTH - C_MAP_CON_WINDOW_W - 1    # x position of campaign map console

C_ACTION_CON_W = SCREEN_WIDTH - C_MAP_CON_WINDOW_W - 3        # width of campaign action console
C_ACTION_CON_H = 30                        # height "

C_INFO_CON_W = SCREEN_WIDTH - C_MAP_CON_WINDOW_W - 3        # width of campaign info console
C_INFO_CON_H = SCREEN_HEIGHT - C_ACTION_CON_H - 4        # height "
C_INFO_CON_X = int(C_INFO_CON_W/2)

MAX_HS = 40        # maximum number of highscore entries to save
NAME_MAX_LEN = 17    # maximum length of crew names in characters
NICKNAME_MAX_LEN = 15    # maximum length of crew nicknames in characters

LIMIT_FPS = 50        # maximum screen refreshes per second

# Game defintions
EXTRA_AMMO = 30        # player tank can carry up to this many extra main gun shells
BASE_EXP_REQ = 30    # exp required to advance from level 1 to 2
LVL_INFLATION = 10    # extra exp required per additional level

STONE_ROAD_MOVE_TIME = 30    # minutes required to move into a new area via an improved road
DIRT_ROAD_MOVE_TIME = 45    # " dirt road
NO_ROAD_MOVE_TIME = 60        # " no road
GROUND_MOVE_TIME_MODIFIER = 15    # additional time required if ground is muddy / rain / snow

# Colour Defintions
KEY_COLOR = libtcod.Color(255, 0, 255)            # key color for transparency

# campaign map base colours
MAP_B_COLOR = libtcod.Color(100, 120, 100)        # fields
MAP_D_COLOR = libtcod.Color(70, 90, 70)            # woods

OPEN_GROUND_COLOR = libtcod.Color(100, 140, 100)
MUD_COLOR = libtcod.Color(80, 50, 30)
HEX_EDGE_COLOR = libtcod.Color(60, 100, 60)
ROAD_COLOR = libtcod.Color(160, 140, 100)
DIRT_COLOR = libtcod.Color(80, 50, 30)
CLEAR_SKY_COLOR = libtcod.Color(16, 180, 240)
OVERCAST_COLOR = libtcod.Color(150, 150, 150)
STONE_ROAD_COLOR = libtcod.darker_grey

FRONTLINE_COLOR = libtcod.red                # highlight for hostile map areas

PLAYER_COLOR = libtcod.Color(10, 64, 10)
ENEMY_COLOR = libtcod.Color(80, 80, 80)
ROW_COLOR = libtcod.Color(30, 30, 30)            # to highlight a line in a console
ROW_COLOR2 = libtcod.Color(20, 20, 20)            # to highlight a line in a console
SELECTED_COLOR = libtcod.blue                # selected option background
HIGHLIGHT_COLOR = libtcod.light_blue            # to highlight important text
GREYED_COLOR = libtcod.Color(60, 60, 60)        # greyed-out option

SKILL_ACTIVATE_COLOR = libtcod.Color(0, 255, 255)    # skill activated message
MENU_TITLE_COLOR = libtcod.lighter_blue            # title of menu console
KEY_HIGHLIGHT_COLOR = libtcod.Color(0, 200, 255)    # highlight for key commands
HIGHLIGHT = (libtcod.COLCTRL_1, libtcod.COLCTRL_STOP)    # constant for highlight pair

TITLE_GROUND_COLOR = libtcod.Color(26, 79, 5)        # color of ground in main menu

SOUNDS = {}                        # sound effects

##########################################################################################
#                                       Classes                                          #
##########################################################################################

# Bones Class
# records high scores and other info between play sessions
class Bones:
    def __init__(self):
        self.score_list = []
        self.graveyard = []

        # tribute to David Bowie
        self.graveyard.append(['Major', 'Jack Celliers', 'Brixton', 'January 10', ''])

        # flags for having displayed help text windows
        self.tutorial_message_flags = {}
        for key in TUTORIAL_TEXT:
            self.tutorial_message_flags[key] = False


# Saved Game Info Class
# holds basic information about a saved game, only read by main menu and only written to
# by SaveGame, doesn't impact gameplay otherwise
class SavedGameInfo:
    def __init__(self, game_version, campaign_name, commander_name, tank_name, current_date):
        self.game_version = game_version
        self.campaign_name = campaign_name
        self.commander_name = commander_name
        self.tank_name = tank_name
        self.current_date = current_date


# Campaign Day Map Class
# holds information about the campaign map used for in an action day
class CampaignDayMap:
    def __init__(self):
        self.seed = 0            # seed used for map painting, set during map
                        #  generation
        self.nodes = []            # list of map nodes
        self.blocked_nodes = set()    # set of impassible map nodes
        self.char_locations = dict()    # dictionary for character location parent nodes
        self.player_node = None        # pointer to player location


# Map Node Class
# holds information about a single location on the campaign map
class MapNode:
    def __init__(self, x, y):
        self.x = x            # x coordinate of the area centre
        self.y = y            # y "
        self.edges = set()        # set of edge locations w/in the area
        self.links = []            # list of adjacent nodes

        self.node_type = ''        # node terrain type
        self.village_radius = 0        # radius of village buildings if village node

        self.dirt_road_links = []    # list of nodes linked to this one by a dirt road
        self.stone_road_links = []    # " an improved road

        self.road_end = False        # any roads should be extended to the edge
                        #   of the map
        self.extended = False        # flag to note that this node has had its
                        #   road extended to edge of map

        self.top_edge = False        # this area is on the top edge of the map
        self.bottom_edge = False    # " bottom "
        self.left_edge = False        # " left "
        self.right_edge = False        # " right "

        self.start = False        # start node
        self.exit = False        # exit node

        self.resistance = None        # area resistance level
        self.res_known = False        # resistance level is known to the player
        self.friendly_control = False    # area is controlled by player forces

        self.arty_strike = False    # friendly artillery has hit this area
        self.air_strike = False        # friendly air forces have hit this area
        self.advancing_fire = False    # player used advancing fire moving into this area

        # Pathfinding stuff
        self.parent = None
        self.g = 0
        self.h = 0
        self.f = 0

        # quest stuff
        self.quest_type = None        # type of active quest for this node
        self.quest_time_limit = None    # time limit to complete quest
        self.quest_vp_bonus = None    # VP bonus awarded for completing quest

    # reset pathfinding info for this node
    def ClearPathInfo(self):
        self.parent = None
        self.g = 0
        self.h = 0
        self.f = 0


# Skill Record Class
# holds information about a crewman's skill and its activation level
class SkillRecord:
    def __init__(self, name, level):
        self.name = name
        self.level = level


# Hit Class
# holds information about a hit on an enemy unit with the player's main gun
class MainGunHit:
    def __init__(self, gun_calibre, ammo_type, critical, area_fire):
        self.gun_calibre = gun_calibre
        self.ammo_type = ammo_type
        self.critical = critical
        self.area_fire = area_fire


# Weather Class
# holds information about weather conditions
class Weather:
    def __init__(self):
        self.clouds = 'Clear'
        self.fog = False
        self.precip = 'None'
        self.ground = 'Dry'

        # record of precip accumilation
        self.rain_time = 0
        self.snow_time = 0
        self.dry_time = 0

    # generate a totally new set of weather conditions upon moving to a new area
    def GenerateNew(self):
        self.clouds = 'Clear'
        self.fog = False
        self.precip = 'None'
        self.ground = 'Dry'

        self.rain_time = 0
        self.snow_time = 0
        self.dry_time = 0

        # cloud cover
        d1, d2, roll = Roll2D6()

        month = campaign.current_date[1]

        if 3 <= month <= 11:
            roll -= 1
        if 5 <= month <= 8:
            roll -= 1
        if roll > 6:
            self.clouds = 'Overcast'

        # precipitation and/or fog
        if self.clouds == 'Overcast':
            d1, d2, roll = Roll2D6()

            if roll <= 4:
                if month <= 2 or month == 12:
                    self.precip = 'Snow'
                elif 5 <= month <= 9:
                    self.precip = 'Rain'
                else:
                    # small chance of snow in march/april, oct/nov
                    d1, d2, roll = Roll2D6()
                    if roll >= 11:
                        self.precip = 'Snow'
                    else:
                        self.precip = 'Rain'

            # fog
            d1, d2, roll = Roll2D6()
            if self.precip != 'None':
                roll -= 2
            if roll >= 10:
                self.fog = True

        # ground cover
        d1, d2, roll = Roll2D6()

        if self.precip == 'Snow':
            if roll >= 11:
                self.ground = 'Deep Snow'
            elif roll >= 5:
                self.ground = 'Snow'
        elif self.precip == 'Rain':
            if roll >= 8:
                self.ground = 'Mud'
        else:
            # deep winter
            if month <= 2 or month == 12:
                if roll == 12:
                    self.ground = 'Deep Snow'
                elif roll >= 8:
                    self.ground = 'Snow'

            # warmer months
            elif 5 <= month <= 9:
                if roll >= 10:
                    self.ground = 'Mud'

            # spring/autumn
            else:
                if roll == 12:
                    self.ground = 'Snow'
                elif roll >= 8:
                    self.ground = 'Mud'

    # check to see if weather changes, and apply effects if so
    def CheckChange(self):
        d1, d2, roll = Roll2D6()
        month = campaign.current_date[1]

        # check to see if precip stops; if so, this will be only change
        # this cycle
        if self.precip != 'None':
            if roll <= 3:
                if self.precip == 'Rain':
                    PopUp('The rain stops.')
                else:
                    PopUp('The snow stops falling.')
                self.precip = 'None'
                return

        # otherwise, if overcast, see if precip starts
        elif self.clouds == 'Overcast':
            if roll <= 3:
                if month <= 2 or month == 12:
                    self.precip = 'Snow'
                    PopUp('Snow starts falling')
                elif 5 <= month <= 9:
                    self.precip = 'Rain'
                    PopUp('Rain starts falling')
                else:
                    # small chance of snow in march/april, oct/nov
                    d1, d2, roll = Roll2D6()
                    if roll >= 11:
                        self.precip = 'Snow'
                        PopUp('Snow starts falling')
                    else:
                        self.precip = 'Rain'
                        PopUp('Rain starts falling')
                return

        # if no precip change, check to see if cloud cover / fog changes
        d1, d2, roll = Roll2D6()

        if self.clouds == 'Clear':
            if roll <= 3:
                self.clouds = 'Overcast'
                PopUp('Clouds roll in and the weather turns overcast')
                return
        else:
            if roll <= 5:
                # if foggy, fog lifts instead
                if self.fog:
                    self.fog = False
                    PopUp('The fog lifts.')
                    return

                # otherwise, the sky clears, stopping any precip
                self.clouds = 'Clear'
                self.precip = 'None'
                PopUp('The sky clears.')
                return

            # chance of fog rolling in
            d1, d2, roll = Roll2D6()
            if roll <= 3 and not self.fog:
                self.fog = True
                PopUp('Fog rolls in.')

    # check for a change in ground cover based on accumilated precip
    # or lack thereof
    def CheckGround(self, minutes_passed):
        change = False
        if self.precip == 'Rain':
            if self.ground != 'Mud':
                self.rain_time += minutes_passed
                if self.rain_time >= 120:
                    PopUp('The rain has turned to ground to mud.')
                    self.ground = 'Mud'
                    self.dry_time = 0
                    change = True
        elif self.precip == 'Snow':
            if self.ground != 'Deep Snow':
                self.snow_time += minutes_passed
                if self.snow_time >= 120:
                    if self.ground == 'Snow':
                        PopUp('The snow on the ground has become deep.')
                        self.ground = 'Deep Snow'
                        change = True
                    elif self.ground in ['Dry', 'Mud']:
                        PopUp('The ground is covered in snow.')
                        self.ground = 'Snow'
                        change = True
        else:
            if self.ground == 'Mud':
                self.dry_time += minutes_passed
                if self.dry_time >= 120:
                    PopUp('The muddy ground dries out.')
                    self.ground = 'Dry'
                    self.rain_time = 0
                    change = True

        # if there was a change, update consoles
        if change:
            if battle is not None:
                UpdateMapOverlay()
            else:
                campaign.BuildActionList()
                UpdateCActionCon()
                UpdateCInfoCon(mouse.cx, mouse.cy)


# Hex Class
# holds information on a hex location in the battle encounter map
class MapHex:
    def __init__(self, hx, hy, rng, sector):
        self.hx = hx
        self.hy = hy
        self.rng = rng
        self.sector = sector
        self.smoke_factors = 0            # current number of smoke factors
        self.x, self.y = Hex2Screen(hx, hy)    # set x and y location to draw on screen


# smoke factor class
# holds information about a smoke factor on the battle encounter map
class SmokeFactor:
    def __init__(self, hx, hy, num_factors):
        self.hx = hx
        self.hy = hy
        self.num_factors = num_factors

    # change position as a result of tank rotating
    def RotatePosition(self, clockwise):
        # convert present coordinate from axial to cube
        x = self.hx
        z = self.hy
        y = -x-z

        # do the rotation
        if clockwise:
            new_x = -y
            new_z = -x
        else:
            new_x = -z
            new_z = -y

        # set the new hex location
        self.hx = new_x
        self.hy = new_z

    # change position based on player tank moving forward or backward
    def YMove(self, y_change):
        # two special cases, if unit would end up in player hex
        if self.hx == 0 and self.hy + y_change == 0:
            if y_change == -1:
                y_change = -2
            else:
                y_change = 2
        self.hy = self.hy + y_change


# Campaign Class
# holds information on an ongoing campaign
class Campaign:
    def __init__(self):

        # Info set by the campaign xml file: defines the parameters of the campaign
        # selected by the player

        self.campaign_name = ''            # name of the campaign (eg. Patton's Best)
        self.campaign_file = ''            # filename of the campaign xml file
        self.player_nation = ''            # three-letter code for player's nation
        self.enemy_nation = ''            # " for enemy nation
        self.map_file = ''            # XP file of campaign map
        self.player_veh_list = []        # list of permitted player vehicle types

        self.mission_activations = []        # list of activation chance dictionaries
                            # for advance, battle, counterattack
                            # missions
        self.activation_modifiers = []        # list of activation modifiers
        self.class_activations = []        # list of unit type and activation chance
                            # tuples for each unit class
                            # first item is always unit class name
        self.ranks = None            # list of ranks for current nation
        self.decorations = None            # list of decorations "

        self.days = []                # list of calendar days: each one is
                            #  a dictionary with keys and values

        self.over = False            # flag set when campaign has finished

        (self.fs_res_x, self.fs_res_y) = FS_RES_LIST[0]    # full screen resolution
        self.fullscreen = False            # full screen preference

        self.exiting = False            # flag for exiting out to main menu
        self.mouseover = (-1, -1)        # keeps track of mouse position

        self.color_scheme = None        # campaign map colour scheme, set at
                            #   map generation

        # campaign options
        self.unlimited_tank_selection = False    # freedom to select any available tank model
        self.casual_commander = False        # can replace commander and continue playing
        self.start_date = 0            # index of date in the calendar to start campaign

        # game settings
        self.animations = True        # in-game animations
        self.sounds = True        # in-game sound effects
        self.pause_labels = True    # wait for enter after displaying a label
        self.tutorial_message = True    # display tutorial message windows

        self.current_date = [0,0,0]    # current year, month, date

        self.day_vp = 0            # vp gained this campaign day
        self.vp = 0            # current total player victory points
        self.action_day = False        # flag if player sees action today
        self.saw_action = False        # flag if player saw action already today
        self.day_in_progress = False    # flag if player is in the campaign map interface

        self.scen_res = ''        # string description of expected resistance for this day
        self.scen_type = ''        # " mission type

        self.tank_on_offer = ''        # new sherman model available during refitting
        self.selected_crew = None    # selected crew member
        self.weather = Weather()    # set up a new weather object
        self.ClearAmmo()        # clear rare ammo supplies\

        self.gyro_skill_avail = False    # gyrostabilier skill is available

        self.stats = {}            # campaign statistics, for display at end of campaign
        self.campaign_journal = []    # list of text descriptions of campaign
        self.record_day_vp = 0        # highest one-day VP score this month


    def ResetForNewDay(self):
        # Following are reset for each new campaign day where player sees action

        self.day_map = None        # day map, will be generated later

        self.weather.GenerateNew()    # reset weather for a new day

        self.hour = 0            # current hour in 24-hour format
        self.minute = 0            # current minute

        self.c_map_y = 0        # offset for displaying campaign map on screen

        self.selected_crew = None    # pointer to currently selected crewmember
        self.resupply = False        # currently in resupply mode

        self.input_mode = 'None'    # current input mode in campaign
        self.selected_node = None    # selected node on the day map
        self.adjacent_nodes = []    # list of adjacent nodes for moving, checking
        self.free_check = False        # player gets a free check adjacent area action

        self.messages = []        # list of campaign messages

        self.sunset = False        # flag that the combat day is over
        self.exiting = False        # flag to exit to main menu

        self.arty_chance = 9        # chance of calling in artillery
        self.air_chance = 7        # chance of calling in air strike

        self.time_of_last_event = (0,0)    # hour, minute of last triggered event;
                        #  0,0 if no event has occured today
        self.quest_active = False    # campaign quest currently active

        self.action_list = []
        self.BuildActionList()

    # check for enemy advances during a counterattack mission day
    def DoEnemyAdvance(self):

        # build list of candidate nodes
        nodes = []
        for node in self.day_map.nodes:
            if node == campaign.day_map.player_node: continue
            if not node.friendly_control: continue
            if node in self.day_map.blocked_nodes: continue
            if node.top_edge:
                nodes.append(node)
                continue

            # check if adjacent to an enemy-held node
            for link_node in node.links:
                if not link_node.friendly_control:
                    nodes.append(node)
                    break

        # if no candidate nodes, return
        if len(nodes) == 0:
            return

        # run through candidate nodes and see if they get taken over
        for node in nodes:

            chance = 0
            for link_node in node.links:
                if not link_node.friendly_control:
                    if link_node.resistance == 'Light' and chance < 3:
                        chance = 3
                    elif link_node.resistance == 'Medium' and chance < 5:
                        chance = 5
                    elif link_node.resistance == 'Heavy' and chance < 7:
                        chance = 7

            # at beginning of day, top-edge nodes won't have any enemy-held
            #  nodes adjacent, so we need to generate random chances for
            #  these ones
            if chance == 0:
                chance = random.choice([3, 5, 7])

            # do advance roll
            d1, d2, roll = Roll2D6()

            # control is lost
            if roll <= chance:
                node.friendly_control = False
                node.res_known = True
                campaign.MoveViewTo(node)
                UpdateCOverlay(highlight_node=node)
                RenderCampaign()
                Wait(500)
                PopUp('A map area has been captured by an enemy advance.')
                UpdateCOverlay()
                RenderCampaign()

        # if no possible path to 'exit' node, player is moved to nearest
        #   friendly node, spends 1-20 HE shells
        if not campaign.day_map.player_node.exit:
            for node in campaign.day_map.nodes:
                if node.exit:
                    if len(GetPath(campaign.day_map.player_node, node, enemy_blocks=True)) > 0:
                        return
                    break

        # HE shells expended during move
        ammo_expended = Roll1D10() * 2
        if tank.general_ammo['HE'] < ammo_expended:
            ammo_expended = tank.general_ammo['HE']
        tank.general_ammo['HE'] -= ammo_expended

        # time required for move
        time_req = 60
        if campaign.weather.ground != 'Dry' or campaign.weather.precip != 'None' or campaign.weather.fog:
            time_req += 15
        campaign.SpendTime(0, time_req)

        PopUp('You have been cut off from your allies and must reposition. You travel' +
            ' off-road to the nearest friendly map area, expending ' + str(ammo_expended) +
            ' HE shells to cover your withdrawl. This takes ' + str(time_req) +
            ' minutes.')

        # player node captured by enemy
        campaign.day_map.player_node.friendly_control = False
        campaign.day_map.player_node.res_known = True

        # find the target node
        closest = None
        closest_dist = 9000
        for node in campaign.day_map.nodes:
            if node.friendly_control:
                dist = GetDistance(campaign.day_map.player_node.x,
                    campaign.day_map.player_node.y, node.x,
                    node.y)
                if dist < closest_dist:
                    closest = node
                    closest_dist = dist

        if closest is None:
            print 'ERROR: Could not find a friendly node to move to'
            return

        # do the move
        campaign.day_map.player_node = closest
        campaign.MoveViewTo(closest)
        UpdateCOverlay()
        RenderCampaign()
        Wait(500)

        # check for sunset
        campaign.CheckSunset()


    # check to see if a random campaign event is triggered
    def RandomCampaignEvent(self):

        # highlight and move player view to event node
        def ShowNode(node):
            campaign.MoveViewTo(node)
            UpdateCOverlay(highlight_node=node)
            RenderCampaign()
            Wait(1000)

        # if current day mission is Counterattack, don't trigger any campaign events
        if campaign.scen_type == 'Counterattack': return

        # if sunset has already happened
        if campaign.sunset: return

        roll = Roll1D100()

        # if no event yet today, set current time as 'time of last event' and return
        if self.time_of_last_event == (0,0):
            self.time_of_last_event = (self.hour, self.minute)
            return
        else:
            h1, m1 = self.time_of_last_event
            h, m = GetTimeUntil(h1, m1, self.hour, self.minute)
            if h == 0:
                # No event
                return
            elif h == 1:
                if m <= 15:
                    roll -= 30
                elif m <= 30:
                    roll -= 25
                elif m <= 45:
                    roll -= 10

        # No event
        if roll <= 50:
            return

        # Ammo supply Discovered
        elif roll <= 55:
            WriteJournal('Friendly supply truck discovered.')
            if PopUp('You have encountered a friendly supply truck. Restock ' +
                'your ammunition? (15 mins.)', confirm=True):
                self.SpendTime(0, 15)
                tank.smoke_grenades = 6
                tank.smoke_bombs = 15
                self.resupply = True
                MainGunAmmoMenu()
                self.resupply = False
                RenderCampaign()
            self.time_of_last_event = (self.hour, self.minute)
            return

        # Quest Triggered
        if roll <= 75:

            # don't trigger another one if there's currently one in progress
            if self.quest_active:
                return

            # determine quest type
            d1, d2, roll = Roll2D6()

            if roll <= 3:
                # like CAPTURE but with a time limit
                quest_type = 'RESCUE'
                vp_bonus = 15
            elif roll <= 7:
                # enter an enemy-held area, automatic battle encounter
                quest_type = 'CAPTURE'
                vp_bonus = 10
            elif roll <= 10:
                # check an enemy-held area for resistance level
                quest_type = 'RECON'
                vp_bonus = 5
            else:
                # enter a friendly-held area, wait for attack
                quest_type = 'DEFEND'
                vp_bonus = 15

            # find quest map node
            player_y = campaign.day_map.player_node.y
            nodes = []
            for node in campaign.day_map.nodes:
                if node in campaign.day_map.blocked_nodes: continue
                # skip marshland nodes; should have been done by
                #  previous line but still seems to be getting through
                if node.node_type == 'E': continue
                if node == campaign.day_map.player_node: continue
                if node.y > player_y: continue
                if quest_type != 'DEFEND' and node.friendly_control: continue
                if quest_type == 'DEFEND' and not node.friendly_control: continue
                if quest_type == 'RECON' and node.res_known: continue
                # node must be close to player
                if len(GetPath(campaign.day_map.player_node, node)) > 3: continue
                nodes.append(node)

            if len(nodes) == 0:
                return

            WriteJournal(quest_type + ' quest triggered')

            # set quest active flag
            self.quest_active = True

            # add campaign stat
            campaign.AddStat('Quests Assigned', 1)

            # select quest node
            node = random.choice(nodes)

            # set quest node settings
            node.quest_type = quest_type
            node.quest_vp_bonus = vp_bonus

            if quest_type == 'RESCUE':
                # determine time limit for quest
                h = campaign.hour + libtcod.random_get_int(0, 2, 4)
                m = campaign.minute
                node.quest_time_limit = (h, m)
                text = ('Commander, you are requested to head to the highlighted ' +
                    'map location. Allied units are pinned down in the area ' +
                    'and require your help. If completed at or before ' +
                    str(h) + ':' + str(m).zfill(2) + ', you will receive ' +
                    'a bonus of ' +    str(vp_bonus) + ' VP.')

            elif quest_type == 'RECON':
                text = ('Commander, you are requested to head to the highlighted ' +
                    'map location and check it for estimated enemy resistance. ' +
                    'If completed, you will receive a bonus of ' +
                    str(vp_bonus) + ' VP.')

            elif quest_type == 'CAPTURE':
                text = ('Commander, you are requested to head to the highlighted ' +
                    'map location and capture it from enemy forces. ' +
                    'If completed, you will receive a bonus of ' +
                    str(vp_bonus) + ' VP.')

            elif quest_type == 'DEFEND':
                text = ('Commander, you are requested to head to the highlighted ' +
                    'map location and defend it from an anticipated enemy  ' +
                    'counterattack. If completed, you will receive a bonus of ' +
                    str(vp_bonus) + ' VP.')

            ShowNode(node)
            PopUp(text)

        # Exit Area Changed
        elif roll <= 80:

            # don't move if player within 2 nodes of current exit
            for node in campaign.day_map.nodes:
                if node.exit:
                    if len(GetPath(campaign.day_map.player_node, node)) <= 4:
                        return
                    break

            # build list of top edge nodes that are reachable from current player
            #  location, note the pre-existing exit node but don't include it in the list
            nodes = []
            old_exit = None
            for node in campaign.day_map.nodes:
                if node.top_edge:
                    if node.friendly_control: continue
                    if node.exit:
                        old_exit = node
                    elif GetPath(campaign.day_map.player_node, node) != []:
                        nodes.append(node)
            # no candidates found
            if len(nodes) == 0: return

            # select a random node from the list, make it the exit node, and clear the
            #  exit flag of the old exit node
            node = random.choice(nodes)
            node.exit = True
            old_exit.exit = False
            ShowNode(node)
            PopUp('HQ has ordered us to proceed to a different target area.')

        # Reconnaissance Report: Reveals expected resistance level in an adjacent area
        elif roll <= 85:

            # build list of possible nodes
            nodes = []
            for node in campaign.day_map.nodes:
                if node in campaign.day_map.player_node.links and not node.res_known:
                    if not node.friendly_control and node.quest_type is None:
                        nodes.append(node)

            # no candidates found
            if len(nodes) == 0: return

            # select a random node and reveal its resistance level
            node = random.choice(nodes)
            node.res_known = True
            ShowNode(node)
            PopUp('Reconnaissance teams have reported on a nearby area.')

        # Enemy Reinforcements: Previously known resistance level is increased
        elif roll <= 90:

            # build list of possible nodes
            nodes = []
            for node in campaign.day_map.nodes:
                if node in campaign.day_map.player_node.links and node.res_known:
                    if not node.friendly_control and node.resistance != 'Heavy':
                        nodes.append(node)

            # no candidates found
            if len(nodes) == 0: return

            # select a random node and increase its resistance level
            node = random.choice(nodes)
            if node.resistance == 'Light':
                node.resistance = 'Medium'
            else:
                node.resistance = 'Heavy'
            ShowNode(node)
            PopUp('We have received reports of enemy reinforcement in a ' +
                'nearby area.')

        # Enemy Advance: Previously captured area is lost
        elif roll <= 95:

            # build list of possible nodes
            nodes = []
            for node in campaign.day_map.nodes:
                if node.friendly_control and node != campaign.day_map.player_node:
                    if node.quest_type is None:
                        nodes.append(node)

            # no candidates found
            if len(nodes) == 0: return

            # select a random node and revert it to enemy control
            node = random.choice(nodes)
            node.friendly_control = False

            ShowNode(node)
            PopUp('A map area has been recaptured by an enemy advance.')

        # Friendly Advance: Nearby area is captured
        else:
            # build list of possible nodes
            nodes = []
            for node in campaign.day_map.nodes:
                if node in campaign.day_map.player_node.links:
                    if node.exit: continue
                    if not node.friendly_control and node != campaign.day_map.player_node:
                        if node.quest_type is None:
                            nodes.append(node)

            # no candidates found
            if len(nodes) == 0: return

            # select a random node and change it to friendly control
            node = random.choice(nodes)
            node.friendly_control = True
            ShowNode(node)
            PopUp('A nearby area has been captured by friendly forces.')

        # return view to player node and continue
        UpdateCOverlay()
        campaign.MoveViewTo(campaign.day_map.player_node)
        RenderCampaign()

        # record that an event occured
        self.time_of_last_event = (self.hour, self.minute)

    # return a text description of node terrain
    def GetTerrainDesc(self, node):
        if node.node_type == 'A':
            return 'Farms & Fields'
        elif node.node_type == 'B':
            return 'Fields'
        elif node.node_type == 'C':
            return 'Village'
        elif node.node_type == 'D':
            return 'Woods'
        elif node.node_type == 'F':
            return 'Bocage'
        print 'ERROR: unknown node terrain'
        return 'Unknown'

    # return the rarity factor for a given vehicle type for the current date
    # if not historically available for this date, returns 0
    def GetRF(self, vehicle_type):
        for v in VEHICLE_TYPES:
            if v[0] == vehicle_type:
                for (k, value) in v[1:]:
                    if k == 'rarity':
                        CAMPAIGN_MONTHS = [(8,1944), (9,1944), (10,1944), (11,1944), (12,1944),
                            (1,1945), (2,1945), (3,1945), (4,1945)]

                        # new campaign, assume earliest month
                        if self.current_date == [0,0,0]:
                            n = 0
                        else:
                            # no rarity yet for first month, use August instead
                            month = self.current_date[1]
                            year = self.current_date[0]
                            if month == 7 and year == 1944:
                                n = 0
                            else:
                                n = CAMPAIGN_MONTHS.index((month, year))
                        return value[n]
        return 0

    # move the campaign day map y offset to immediately show given node
    def MoveViewTo(self, node):
        if node is None: return
        while self.c_map_y > node.y - 10:
            self.c_map_y -= 10
        while self.c_map_y < node.y - C_MAP_CON_WINDOW_H + 10:
            self.c_map_y += 10
        self.CheckYOffset()
        RenderCampaign()

    # record a campaign stat, either creating a new entry or increasing one already existing
    def AddStat(self, stat_name, value):
        if not self.stats.has_key(stat_name):
            self.stats[stat_name] = value
        else:
            previous_value = self.stats[stat_name]
            self.stats[stat_name] = previous_value + value

    # build list of possible campaign day actions and their time cost
    def BuildActionList(self):

        self.action_list = []

        # calculate time increase for weather
        if self.weather.ground != 'Dry' or self.weather.precip != 'None' or self.weather.fog:
            ti = GROUND_MOVE_TIME_MODIFIER
        else:
            ti = 0

        if self.scen_type == 'Counterattack':
            self.action_list.append(('[%cA%c]wait Enemy Counterattack'%HIGHLIGHT, None))
            self.action_list.append(('[%cE%c]nter adjacent friendly area, Improved Road'%HIGHLIGHT, STONE_ROAD_MOVE_TIME+ti))
            self.action_list.append(('[%cE%c]nter adjacent friendly area, Dirt Road'%HIGHLIGHT, DIRT_ROAD_MOVE_TIME+ti))
            self.action_list.append(('[%cE%c]nter adjacent friendly area, No Road'%HIGHLIGHT, NO_ROAD_MOVE_TIME+ti))
            self.action_list.append(('Attempt [%cR%c]esupply'%HIGHLIGHT, 15))
        else:
            self.action_list.append(('[%cC%c]heck adjacent area'%HIGHLIGHT, 15))
            self.action_list.append(('[%cE%c]nter adjacent area, Improved Road'%HIGHLIGHT, STONE_ROAD_MOVE_TIME+ti))
            self.action_list.append(('[%cE%c]nter adjacent area, Dirt Road'%HIGHLIGHT, DIRT_ROAD_MOVE_TIME+ti))
            self.action_list.append(('[%cE%c]nter adjacent area, No Road'%HIGHLIGHT, NO_ROAD_MOVE_TIME+ti))
            self.action_list.append(('Call for [%cA%c]rtillery or Air Strike'%HIGHLIGHT, 15))
            # air strike conditions
            if self.weather.clouds != 'Overcast' and not self.weather.fog and self.weather.precip != 'Snow':
                self.action_list.append(('Call for [%cA%c]ir Strike on adjacent area'%HIGHLIGHT, 30))
            self.action_list.append(('Attempt [%cR%c]esupply'%HIGHLIGHT, 60))

        # always have this option
        self.action_list.append(('[%cV%c]iew Tank'%HIGHLIGHT, None))

        # option of ending day
        if [i for i in ENDING_DAMAGES if i in tank.damage_list]:
            self.action_list.append(('Return to [%cH%c]Q'%HIGHLIGHT, None))

    # generate amount of limited ammo available during morning briefing
    def GenerateAmmo(self):
        self.hcbi = libtcod.random_get_int(0, 1, 10)
        self.hvap = libtcod.random_get_int(0, 1, 3)

        # ADPS ammo easier to get by start of 1945
        if self.current_date[0] == 1945:
            max_adps = 5
            min_adps = 2
        else:
            max_adps = 3
            min_adps = 1
        self.apds = libtcod.random_get_int(0, min_adps, max_adps)

        # check for scrounger skill
        if GetCrewByPosition('Loader').SkillCheck('Scrounger'):
            self.hcbi += libtcod.random_get_int(0, 1, 3)
            self.hvap += 1
            self.apds += libtcod.random_get_int(0, 1, 2)

    # clear available limited ammo supplies
    def ClearAmmo(self):
        self.hcbi = 0
        self.hvap = 0
        self.apds = 0

    # keeps the campaign map offset within bounds
    def CheckYOffset(self):
        if self.c_map_y < 0:
            self.c_map_y = 0
        elif self.c_map_y > C_MAP_CON_HEIGHT - C_MAP_CON_WINDOW_H:
            self.c_map_y = C_MAP_CON_HEIGHT - C_MAP_CON_WINDOW_H

    # award vp for capturing an area
    def AwardCaptureVP(self, node, counterattack=False):
        if node.node_type in ['A', 'B']:
            vp = 1
        elif node.node_type in ['C', 'F']:
            vp = 3
        elif node.node_type == 'D':
            vp = 2

        # exit area gives extra VP
        if node.exit:
            vp += 20
        # advance mission gives bonus VP if not already increased b/c exit node
        elif self.scen_type == 'Advance':
            vp = vp * 2

        self.day_vp += vp
        text = 'You are awarded ' + str(vp) + ' VP for '
        if counterattack:
            text += 'defending'
        else:
            text += 'capturing'
        text += ' this area.'
        PopUp(text)

    # returns a text description of current date and time, or given date in campaign
    #  calendar
    def GetDate(self, lookup_date=None):
        MONTHS = ['', 'January', 'February', 'March', 'April', 'May',
        'June', 'July', 'August', 'September', 'October',
        'November', 'December'
        ]

        if lookup_date is None:
            lookup_date = self.current_date

        text =  MONTHS[lookup_date[1]]
        date = str(lookup_date[2])
        text += ' ' + date
        if date in ['1', '21', '31']:
            text += 'st'
        elif date in ['2', '22']:
            text += 'nd'
        elif date in ['3', '23']:
            text += 'rd'
        else:
            text += 'th'
        text += ', ' + str(lookup_date[0])
        return text

    # returns the hour and minute of sunrise for current month
    def GetSunrise(self):
        SUNRISE = [(0,0), (7,45), (7,15), (6,15), (5,15),
            (5,0), (5,0), (5,0), (5,0), (5,30),
            (6,30), (7,15), (7,45)
        ]
        return SUNRISE[self.current_date[1]]

    # returns the hour and minute of sunset for current month
    def GetSunset(self):
        SUNSET = [(0,0), (16,30), (17,30), (18,00), (19,00),
            (19,15), (19,15), (19,15), (19,15), (18,15),
            (17,15), (16,15), (16,00)
        ]
        return SUNSET[self.current_date[1]]

    # advances clock by given amount of time
    def SpendTime(self, hours, minutes):
        # add minutes
        self.minute += minutes
        # roll over extra minutes into hours
        while self.minute >= 60:
            self.hour += 1
            self.minute -= 60
        # add hours
        self.hour += hours
        UpdateDateCon()

        # check for rain accumilation for mud, dry weather for dry ground,
        # or snow for snow / deep snow cover
        self.weather.CheckGround(((hours*60) + minutes))

        # check for weather change, 10% per 15 mins
        checks = (hours * 4) + int(ceil(float(minutes) / 15.0))
        for c in range(checks):
            if libtcod.random_get_int(0, 1, 10) == 1:
                self.weather.CheckChange()
                # in case there was a change, update consoles
                if battle is not None:
                    PaintMapCon()
                else:
                    campaign.BuildActionList()
                    UpdateCActionCon()
                    UpdateCInfoCon(mouse.cx, mouse.cy)

        # check for quest time limit, eg. RESCUE
        if self.quest_active:
            for node in self.day_map.nodes:
                if node.quest_time_limit is not None:
                    (h,m) = node.quest_time_limit
                    if self.hour > h or (self.hour == h and self.minute > m):
                        # cancel quest
                        text = ('Time has run out to complete ' +
                            node.quest_type + ' quest.')
                        PopUp(text)
                        WriteJournal(text)
                        node.quest_type = None
                        node.quest_vp_bonus = None
                        node.quest_time_limit = None
                        self.quest_active = False
                        if battle is None:
                            UpdateCOverlay()
                    break

    # check to see if it is at or past sunset, and trigger campaign day end if true
    def CheckSunset(self):
        # don't check if already triggered
        if self.sunset: return
        (h, m) = self.GetSunset()
        if self.hour > h or (self.hour == h and self.minute >= m):
            PopUp('The sun has set and this day of combat is over.')
            WriteJournal('The sun set at ' + str(h) + ':' + str(m).zfill(2) + ' and the action day ended')
            campaign.sunset = True
            RenderCampaign()
            self.EndOfDay()

    # commander chose to head back to HQ because of a damaged tank
    def HeadHome(self):
        RenderCampaign()
        PopUp('You have chosen to head back to HQ, ending your combat day.')
        WriteJournal('The commander chose to return to HQ at ' + str(self.hour) + ':' + str(self.minute) + ' because of tank damage')
        campaign.sunset = True
        RenderCampaign()
        self.EndOfDay()

    # do end of campaign day stuff
    def EndOfDay(self):
        # award exp for the day to crew
        for crew in tank.crew:
            d1, d2, roll = Roll2D6()
            crew.AwardExp(roll)

        # check to see if any crew have gone up one or more levels
        self.CheckCrewLevels()

        # show campaign menu for summary
        CampaignMenu()

    # check to see if any tank crew have gained one or more levels
    def CheckCrewLevels(self):
        for crewman in tank.crew:
            while crewman.level < LEVEL_CAP:
                if crewman.exp >= GetExpReq(crewman.level+1):
                    crewman.level += 1
                    crewman.skill_pts += 1
                    text = crewman.name + ' gained a level, is now level ' + str(crewman.level)
                    PopUp(text)
                    WriteJournal(text)
                else:
                    break


# PlayerTank Class
# holds information about a player and their tank; can specify a model of tank during creation
class PlayerTank:
    def __init__(self, tank_type):

        if tank_type is None:
            self.unit_type = 'M4 Turret A'    # default type of tank
        else:
            self.unit_type = tank_type
        self.unit_class = 'TANK'
        self.crew = []            # list of crewmen in the tank

        self.Setup()

    # set up a new tank
    def Setup(self):

        self.alive = True        # tank is not destroyed or disabled
        self.swiss_cheese = False    # tank is damaged to the point where it
                        #  must be abandoned after encounter is over

        self.name = ''            # tank name

        self.general_ammo = {}        # ammo types and numbers in general stores
        self.rr_ammo = {}        # " ready rack

        self.ammo_load = 'HE'        # current shell in main gun
        self.ammo_reload = 'HE'        # type of shell to use for reload
        self.use_rr = True        # use ready rack to reload

        self.fired_main_gun = False    # tank fired its main gun last turn

        self.smoke_grenades = 6        # current number of smoke grenades, max 6
        self.smoke_bombs = 15        # current number of smoke bombs for mortar
                        # (includes one loaded in mortar itself)

        self.turret_facing = 4        # sector that turret is facing
        self.old_t_facing = 4        # used when rotating the turret
        self.new_facing = 4        # used for pivoting the tank

        self.bogged_down = False    # tank is bogged down
        self.immobilized = False    # tank has thrown a track
        self.hull_down = False        # tank is hull down
        self.moving = False        # tank is moving
        self.lead_tank = False        # tank is lead of column

        # flags for MGs
        self.coax_mg_can_fire = False
        self.bow_mg_can_fire = False
        self.aa_mg_can_fire = False
        self.active_mg = -1

        self.has_rof = False        # tank currently has maintained RoF

        ##### List of Active Minor Damage #####
        self.damage_list = []

    # reset the tank for a new encounter turn
    def Reset(self):
        # record the current turret facing
        self.old_t_facing = self.turret_facing
        # reset MG flags
        self.coax_mg_can_fire = False
        self.bow_mg_can_fire = False
        self.aa_mg_can_fire = False
        self.active_mg = -1

    # reset the tank after an encounter
    def ResetAfterEncounter(self):
        self.Reset()
        self.turret_facing = 4
        self.old_t_facing = 4
        self.bogged_down = False
        self.hull_down = False
        self.moving = False
        self.fired_main_gun = False
        # reset crew: orders for all crew, reset bailed out flag
        for crew_member in self.crew:
            crew_member.ResetOrder(reset_all=True)
            crew_member.bailed_out = False
            crew_member.bail_mod = 0

    # apply a given randomly-determined type of minor damage, or randomly determine
    #  what type of damage to apply
    def TakeDamage(self, damage_type=None, light_weapons=False, large_gun=False):

        if damage_type is None:

            # do damage roll
            d1, d2, roll = Roll2D6()

            # apply any modifiers
            if light_weapons:
                roll += 5
            elif large_gun:
                roll -= 2

            # determine type of damage
            d6roll = Roll1D6()

            if roll <= 2:
                if d6roll <= 3:
                    damage_type = 'Gun Sight Broken'
                else:
                    damage_type = 'Engine Knocked Out'
            elif roll == 3:
                if d6roll == 1:
                    damage_type = 'Main Gun Broken'
                else:
                    damage_type = 'Main Gun Malfunction'
            elif roll == 4:
                if d6roll <= 2:
                    damage_type = 'Turret Traverse Broken'
                else:
                    damage_type = 'Turret Traverse Malfunction'
            elif roll == 5:
                if d6roll <= 3:
                    damage_type = 'Radio Broken'
                else:
                    damage_type = 'Radio Malfunction'
            elif roll == 6:
                if d6roll <= 1:
                    damage_type = 'Intercom Broken'
                else:
                    damage_type = 'Intercom Malfunction'
            elif roll <= 8:
                if d6roll <= 2:
                    if not tank.stats.has_key('aa_mg'):
                        return
                    damage_type = 'AA MG'
                elif d6roll <= 4:
                    if not tank.stats.has_key('co_ax_mg'):
                        return
                    damage_type = 'Co-ax MG'
                else:
                    if not tank.stats.has_key('bow_mg'):
                        return
                    damage_type = 'Bow MG'
                if Roll1D6() <= 2:
                    damage_type += ' Broken'
                else:
                    damage_type += ' Malfunction'
            elif roll <= 10:
                if d6roll == 1:
                    damage_type = 'Commander'
                elif d6roll == 2:
                    damage_type = 'Gunner'
                elif d6roll == 3:
                    damage_type = 'Loader'
                elif d6roll == 4:
                    damage_type = 'Driver'
                elif d6roll == 5:
                    damage_type = 'Asst. Driver'
                else:
                    # no damage
                    return
                damage_type += ' Periscope Broken'
            else:
                # no damage
                return

        # don't apply if tank already has this type of damage
        if damage_type in self.damage_list:
            return

        # don't apply if the worse result is already present
        damage_result = GetDamageType(damage_type)
        if damage_result is not None:
            if damage_result.break_result in self.damage_list:
                return

        # remove less bad result
        mal_result = damage_type.replace('Broken', 'Malfunction')
        if mal_result in self.damage_list:
            self.damage_list.remove(mal_result)

        self.damage_list.append(damage_type)
        PopUp('Your tank has been damaged: ' + damage_type)

        # apply any additional effects
        if damage_type == 'Engine Knocked Out':
            self.immobilized = True

        # rebuild orders list and reset spotting ability
        for crewman in tank.crew:
            crewman.BuildOrdersList(no_reset=True)
            crewman.SetSpotAbility()
        UpdateTankCon()

    # select first mg that can fire
    def SelectFirstMG(self):
        if self.coax_mg_can_fire:
            self.active_mg = 0
        elif self.bow_mg_can_fire:
            self.active_mg = 1
        elif self.aa_mg_can_fire:
            self.active_mg = 2
        else:
            # no MGs can fire
            self.active_mg = -1

    # set a new name for the player tank
    def SetName(self, new_name):
        self.name = new_name

    # show a menu to change the shell load of the main gun
    def ChangeGunLoadMenu(self):

        # determine valid options: any ammo type that has at least one shell
        choice_list = []
        for ammo_type in AMMO_TYPES:
            if ammo_type in tank.general_ammo:
                if tank.general_ammo[ammo_type] > 0:
                    choice_list.append(ammo_type)
                elif tank.rr_ammo[ammo_type] > 0:
                    choice_list.append(ammo_type)

        # no shells available
        if len(choice_list) == 0:
            PopUp("No shells remaining, can't change gun load")
            return

        # show the menu and get the selection
        text = 'Select type of shell to load in main gun'
        choice = GetChoice(text, choice_list)

        if choice is None: return

        # replace any current gun shell in general stores
        if self.ammo_load != 'None':
            tank.general_ammo[self.ammo_load] += 1

        # set the new shell type; try from general first, then rr
        if tank.general_ammo[choice] > 0:
            tank.general_ammo[choice] -= 1
        else:
            tank.rr_ammo[choice] -= 1
        self.ammo_load = choice

    # cycle the selected ammo type to reload
    def CycleReload(self):
        type_list = []
        for ammo_type in AMMO_TYPES:
            if ammo_type in tank.general_ammo:
                type_list.append(ammo_type)

        n = type_list.index(tank.ammo_reload)
        if n >= len(type_list)-1:
            tank.ammo_reload = type_list[0]
        else:
            tank.ammo_reload = type_list[n+1]

    # toggle the hatch status of given crew member if possible, and change their spot
    # ability accordingly
    def ToggleHatch(self, crewman):

        # only allow if a crew member is selected
        if crewman is None: return

        # if crew member has no hatch, return
        if crewman.hatch == 'None':    return

        # otherwise, toggle state
        if crewman.hatch == 'Open':
            crewman.hatch = 'Shut'
            PlaySound('hatch_close')
        else:
            crewman.hatch = 'Open'
            PlaySound('hatch_open')

        # update spotting ability
        crewman.SetSpotAbility()

        # re-build list of possible orders
        crewman.BuildOrdersList(no_reset=True)

    # set lead tank status for the day
    def SetLeadTank(self):

        # fireflies never lead
        if tank.stats['vehicle_type'] == 'Sherman VC':
            return

        if not 'M4A3E2' in tank.stats['vehicle_type']:
            # if not a jumbo and was lead tank last combat day, automatically
            # not lead tank today
            if self.lead_tank:
                self.lead_tank = False
                return
            lead_tank = 11
        else:
            lead_tank = 8
        d1, d2, roll = Roll2D6()

        if roll >= lead_tank:
            self.lead_tank = True
            PopUp('Your tank is the Lead Tank for the day')
            WriteJournal('"' + tank.name + '" is assigned to be Lead Tank for the day')
        else:
            self.lead_tank = False

    # set movement status upon deployment into an encounter
    def SetDeployment(self):

        # counterattack scenario is special, no roll required
        if campaign.scen_type == 'Counterattack' or battle.counterattack:
            self.hull_down = True
            return

        # determine chances of starting hull down and/or stopped
        if tank.stats['vehicle_type'] == 'Sherman VC':
            hull_down = 7
            stopped = 9
        elif 'M4A3E2' in tank.stats['vehicle_type']:
            hull_down = 3
            stopped = 5
        else:
            hull_down = 5
            stopped = 7

        # terrain modifier
        if campaign.day_map.player_node.node_type == 'F':
            hull_down += 2

        # check for 'Cautious Driver' skill activation
        crew_member = GetCrewByPosition('Driver')
        if crew_member.SkillCheck('Cautious Driver'):
            hull_down += 2

        d1, d2, roll = Roll2D6()
        if roll <= hull_down:
            self.hull_down = True
            Message('Your tank is Hull Down')
        elif roll <= stopped:
            Message('Your tank is Stopped')
        else:
            self.moving = True
            Message('Your tank is Moving')

    # tank has suffered a penetrating hit, determine effects
    def Penetrate(self, hit_location, sector, gun_type, critical=False):

        # determine base modifiers
        mod = 0
        if hit_location == 'Hull':
            mod -= 1
        # only handles special cases of 88s or PF for now
        large_gun = False
        if gun_type in ['88L', '88LL', 'Panzerfaust']:
            mod -= 2
            large_gun = True

        # do initial roll
        d1, d2, roll = Roll2D6()

        # if original to-kill roll was less than half of what was required, or
        # a natural 2, then two results are rolled and the worse of the two is applied
        if critical:
            d1, d2, roll2 = Roll2D6()
            if roll2 < roll:
                roll = roll2

        # apply any secondary modifiers
        if roll + mod in [3,4,5,11,12]:
            if not tank.stats.has_key('wet_stowage'):
                mod -= 1

            # extra ammo
            total = 0
            for ammo_type in AMMO_TYPES:
                if ammo_type in tank.general_ammo:
                    total += tank.general_ammo[ammo_type]
            total -= tank.stats['main_gun_rounds']
            if total > 0:
                if libtcod.random_get_int(0, 1, 100) <= total:
                    mod -= 1

        # determine final effect
        roll += mod

        # Explodes
        if roll <= 2:
            PlaySound('tank_knocked_out')
            text = 'Your tank explodes, killing the entire crew!'
            PopUp(text)
            WriteJournal(text)
            campaign.AddStat('Tanks Lost', 1)
            self.alive = False
            battle.result = 'Tank Lost'
            for crewman in tank.crew:
                crewman.ResolveKIA()

        # Knocked Out
        elif roll <= 7:
            PlaySound('tank_knocked_out')
            text = 'Your tank has been knocked out, and the crew must bail out.'
            PopUp(text)
            WriteJournal(text)
            campaign.AddStat('Tanks Lost', 1)
            self.alive = False
            battle.result = 'Tank Lost'
            # work out crew casualties and bailing out
            ResolveCrewFate(hit_location, sector, (gun_type == 'Panzerfaust'))

        # Ricochet
        elif roll <= 8:
            text = ('Fragments of shell and armour ricochet throughout the ' +
                'tank, causing multiple wounds and damage.')
            PopUp(text)
            WriteJournal(text)
            tank.swiss_cheese = True
            # generate 3 minor damage results
            for n in range(3):
                self.TakeDamage(large_gun=large_gun)

            # 2 possible wounds per crewman
            for crewman in tank.crew:
                for n in range(2):
                    text = crewman.TakeWound(hit_location, sector)
                    if text is not None:
                        text = crewman.name + ' is wounded! Result: ' + text
                        PopUp(text)

        # Spalling
        elif roll <= 9:
            text = ("The shell impact causes spalling in the tank's armour, " +
                "sending metal fragments bursting into the crew " +
                "compartment.")
            PopUp(text)
            WriteJournal(text)
            tank.swiss_cheese = True
            # generate 2 minor damage results
            for n in range(2):
                self.TakeDamage(large_gun=large_gun)
            # 1 possible wound per crewman
            for crewman in tank.crew:
                text = crewman.TakeWound(hit_location, sector)
                if text is not None:
                    text = crewman.name + ' is wounded! Result: ' + text
                    PopUp(text)

        # Fire
        elif roll <= 10:
            text = ('The shell does no serious damage, but ignites a fire ' +
                'inside the crew compartment which is quickly extinguished.')
            PopUp(text)
            WriteJournal(text)
            # generate 1 minor damage result
            self.TakeDamage(large_gun=large_gun)
            # one possible crew wound
            crewman = random.choice(tank.crew)
            text = crewman.TakeWound(None, None, collateral=True)
            if text is not None:
                text = crewman.name + ' is wounded! Result: ' + text
                PopUp(text)

        # Minor Damage
        else:
            text = ('The shell impacts a well-protected area, causing only ' +
                'minor damage.')
            PopUp(text)
            WriteJournal(text)
            # generate 1 minor damage result
            self.TakeDamage(large_gun=large_gun)

    # abandon tank
    def AbandonTank(self):
        text = 'Your crew abandons your tank and bails out.'
        PopUp(text)
        WriteJournal(text)
        campaign.AddStat('Tanks Lost', 1)
        self.alive = False
        battle.result = 'Tank Lost'
        # crew get a chance to recover from negative status effects
        for crewman in tank.crew:
            crewman.RecoveryRoll()
        ResolveCrewFate(None, None, False, abandoned=True)

    # take a light weapons attack and apply effects
    def LWAttack(self):
        # check for exposed crew wound
        hit_result = False
        for crewman in tank.crew:
            if crewman.hatch == 'Open':
                text = crewman.TakeWound(None, None, collateral=True)
                if text is not None:
                    hit_result = True
                    text = crewman.name + ' is hit! Result: ' + text
                    PopUp(text)
        if not hit_result:
            ShowLabel(MAP_X0+MAP_CON_X, MAP_Y0+MAP_CON_Y, 'No crewmembers affected.')

        # check for minor damage
        if Roll1D6() == 1:
            self.TakeDamage(light_weapons=True)

    # take a minefield attack
    def MinefieldAttack(self):
        # do D10 roll
        roll = Roll1D10()
        if roll >= 3:
            PopUp('Luckily your tanks do not trigger any mines.')
            return
        elif roll <= 1:
            PopUp('One friendly tank is knocked out by a mine blast.')
            battle.tanks_lost += 1
            return

        # player tank disabled!
        text = 'Your tank triggers a mine which explodes, disabling it!'
        PopUp(text)
        WriteJournal(text)
        tank.moving = False
        tank.immobilized = True
        # rebuild list of orders for driver, reset to Stop
        GetCrewByPosition('Driver').BuildOrdersList()
        UpdateTankCon()

        # roll for effect on crew
        roll = Roll1D10()
        if roll <= 8:
            PopUp('Luckily, none of your crew is injured by the blast.')
            return

        # driver or assistant driver possibly wounded
        if roll == 9:
            crew = GetCrewByPosition('Driver')
        else:
            crew = GetCrewByPosition('Asst. Driver')

        # no crew in this position
        if crew is None:
            result = None
        else:
            result = crew.TakeWound(None, None, minefield=True)

        if result is None:
            PopUp('Luckily, none of your crew is injured by the blast.')
            return

        # otherwise, show the wound result
        text = crew.name + ' is hit by the blast! Result: ' + result
        PopUp(text)
        WriteJournal(text)

    # draw player tank to the map console
    def DrawMe(self):

        # return the x, y location and character to use to draw the tank turret
        # based on turret facing
        def GetTurretChar(facing):
            if facing == 0:        # down and right
                x = MAP_X0 + 1
                y = MAP_Y0 + 1
                char = '\\'
            elif facing == 1:        # down
                x = MAP_X0
                y = MAP_Y0 + 1
                char = '|'
            elif facing == 2:        # down and left
                x = MAP_X0 - 1
                y = MAP_Y0 + 1
                char = '/'
            elif facing == 3:        # up and left
                x = MAP_X0 - 1
                y = MAP_Y0 - 1
                char = '\\'
            elif facing == 4:        # up
                x = MAP_X0
                y = MAP_Y0 - 1
                char = '|'
            else:                    # up and right
                x = MAP_X0 + 1
                y = MAP_Y0 - 1
                char = '/'
            return x, y, char

        libtcod.console_set_default_foreground(overlay_con, libtcod.white)
        libtcod.console_put_char(overlay_con, MAP_X0, MAP_Y0, libtcod.CHAR_RADIO_UNSET, flag=libtcod.BKGND_SET)
        libtcod.console_set_char_background(overlay_con, MAP_X0, MAP_Y0, PLAYER_COLOR, flag=libtcod.BKGND_SET)

        # draw turret based on current facing
        x, y, char = GetTurretChar(self.turret_facing)
        col = libtcod.console_get_char_background(map_con, x, y)
        libtcod.console_put_char_ex(overlay_con, x, y, char, libtcod.white, col)

        # if turret has been rotated and we're rotating the turret or
        # firing main gun or MGs, draw old facing too
        if battle.phase in ['Fire Main Gun', 'Fire MGs', 'Rotate Turret'] and self.old_t_facing != self.turret_facing:
            x, y, char = GetTurretChar(self.old_t_facing)
            col = libtcod.console_get_char_background(map_con, x, y)
            libtcod.console_put_char_ex(overlay_con, x, y, char, libtcod.dark_grey, col)

        # if we're pivoting the tank, display what the new facing would be
        elif battle.phase == 'Pivot Tank':
            if tank.new_facing == 0:
                x = MAP_X0 + 3
                y = MAP_Y0 + 1
                char = 224
                col1 = libtcod.console_get_char_background(map_con, x, y)
                col2 = libtcod.white
            elif tank.new_facing == 1:
                x = MAP_X0
                y = MAP_Y0 + 2
                char = 31
                col1 = libtcod.white
                col2 = libtcod.console_get_char_background(map_con, x, y)
            elif tank.new_facing == 2:
                x = MAP_X0 - 3
                y = MAP_Y0 + 1
                char = 225
                col1 = libtcod.console_get_char_background(map_con, x, y)
                col2 = libtcod.white
            elif tank.new_facing == 3:
                x = MAP_X0 - 3
                y = MAP_Y0 - 1
                char = 224
                col1 = libtcod.white
                col2 = libtcod.console_get_char_background(map_con, x, y)
            elif tank.new_facing == 4:
                x = MAP_X0
                y = MAP_Y0 - 2
                char = 30
                col1 = libtcod.white
                col2 = libtcod.console_get_char_background(map_con, x, y)
            else:
                x = MAP_X0 + 3
                y = MAP_Y0 - 1
                char = 225
                col1 = libtcod.white
                col2 = libtcod.console_get_char_background(map_con, x, y)

            libtcod.console_put_char_ex(overlay_con, x, y, char, col1, col2)


# Crewman Class
# holds information about a single crewman in the tank
class Crewman:
    def __init__(self):
        self.name = ''        # crewman name
        self.nickname = ''    # nickname, set by player
        self.hometown = ''    # crewman's hometown
        self.rank_level = 0    # rank level (private, etc.)
        self.position = ''    # position in the tank normally occupied
        self.order = 'None'    # current order
        self.hatch = 'None'    # hatch status
        self.spot = 'None'    # spot status
        self.spot_sector = 4    # sector spotting in if limited to any one

        self.orders_list = []    # list of possible orders for this crewman

        ### Experience Points (EXP) and skills ###
        self.level = 1        # crew experience level
        self.exp = 0        # current experience points
        self.skill_pts = 1    # current skill points
        self.skills = []    # list of skills (skill name, activation chance)

        # decorations
        self.decorations = []        # medals, etc.

        # injury flags
        self.alive = True        # crewman is alive
        self.light_wound = False    # " has received a light wound
        self.serious_wound = False    # "                serious wound
        self.v_serious_wound = False    # "                very serious wound

        # status flags
        self.stunned = False        # " has been stunned by injury or near miss
        self.unconscious = False    # "          knocked unconscious

        self.bailed_out = False        # has bailed out of tank

        self.next = None        # pointer to next crewman in list
        self.prev = None        # pointer to previous "

    # resolves effects of crewman being killed
    def ResolveKIA(self):
        self.no_bail = True
        self.alive = False
        self.unconscious = False
        self.stunned = False
        self.light_wound = False
        self.serious_wound = False
        self.v_serious_wound = False
        self.SetSpotAbility()
        self.ResetOrder()
        self.AddHeadStone()

    # generates a text report of the crewman's status and history, used when crewman is
    #  KIA, sent home, or at end of campaign
    def GenerateReport(self):
        lines = ['', '****', 'Crewman Report']
        lines.append(self.GetRank())
        lines.append(self.name)
        if self.nickname != '':
            lines.append(self.nickname)
        lines.append(' ' + self.hometown)
        lines.append('')
        if not self.alive:
            lines.append('KIA, ' + campaign.GetDate())
            lines.append('')
        elif self.v_serious_wound:
            lines.append('Sent Home, ' + campaign.GetDate())
            lines.append('')

        # skills
        lines.append('Skills:')
        if len(self.skills) == 0:
            lines.append('None')
        else:
            for skill_record in self.skills:
                string = ' ' + skill_record.name
                if skill_record.level < 100:
                    string += ': ' + str(skill_record.level) + '%'
                lines.append(string)

        lines.append('')

        # decorations
        lines.append('Decorations:')
        if len(self.decorations) == 0:
            lines.append('None')
        else:
            for dec_name in self.decorations:
                lines.append(dec_name)

        return lines

    # add an entry to the bones file recording this crewman's demise
    def AddHeadStone(self):
        # open bones file
        save = shelve.open('bones')
        bones = save['bones']
        save.close()

        # add the entry

        # get most recent decortation
        if len(self.decorations) > 0:
            decoration_text = self.decorations[-1]
        else:
            decoration_text = ''

        bones.graveyard.append([self.GetRank(), self.name, self.hometown, campaign.GetDate(), decoration_text])

        # save the bones file
        save = shelve.open('bones')
        save['bones'] = bones
        save.close()

    # award a decoration to this crewman, and display a window with information about
    #  the decoration
    def AwardDecoration(self, dec_name):

        def UpdateScreen():
            libtcod.console_blit(menu_con, 0, 0, MENU_CON_WIDTH, MENU_CON_HEIGHT, 0, MENU_CON_X, MENU_CON_Y)
            libtcod.console_flush()
            Wait(400)

        WriteJournal(self.name + ' awarded new decoration: ' + dec_name)

        # add to crewman's list of decorations
        self.decorations.append(dec_name)

        # darken screen
        libtcod.console_clear(con)
        libtcod.console_blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0,
            0.0, 0.7)

        # clear console
        libtcod.console_set_default_background(menu_con, libtcod.black)
        libtcod.console_set_default_foreground(menu_con, libtcod.white)
        libtcod.console_clear(menu_con)
        libtcod.console_set_alignment(menu_con, libtcod.CENTER)

        # display frame and title
        libtcod.console_print_frame(menu_con, 0, 0, MENU_CON_WIDTH-1, MENU_CON_HEIGHT-1,
            clear=False, flag=libtcod.BKGND_DEFAULT, fmt=0)
        libtcod.console_set_default_foreground(menu_con, MENU_TITLE_COLOR)
        libtcod.console_print(menu_con, MENU_CON_XM, 2, 'Decoration Award')

        libtcod.console_set_default_foreground(menu_con, libtcod.white)

        # crewman name
        text = self.GetRank() + ' ' + self.name
        libtcod.console_print(menu_con, MENU_CON_XM, 5, text)
        if self.nickname != '':
            libtcod.console_print(menu_con, MENU_CON_XM, 6, '"' + self.nickname + '"')
        UpdateScreen()

        text = 'has been '
        if not self.alive:
            text += 'posthumously '
        text += 'awarded the'
        libtcod.console_print(menu_con, MENU_CON_XM, 7, text)
        UpdateScreen()

        # name of decoration
        libtcod.console_print(menu_con, MENU_CON_XM, 11, dec_name)
        UpdateScreen()

        # decoration description
        # get description from definitions file
        if dec_name == 'Purple Heart':
            text = 'for wounds received in action'
        else:
            for (name, text, vp_req) in campaign.decorations:
                if name == dec_name:
                    break

        libtcod.console_print(menu_con, MENU_CON_XM, 15, text)
        UpdateScreen()

        # date
        text = 'this ' + campaign.GetDate()
        libtcod.console_print(menu_con, MENU_CON_XM, 17, text)

        libtcod.console_print(menu_con, MENU_CON_XM, MENU_CON_HEIGHT-3, '[%cEnter%c] to continue'%HIGHLIGHT)

        UpdateScreen()

        libtcod.console_set_alignment(menu_con, libtcod.LEFT)

        exit_menu = False
        while not exit_menu:
            libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS|libtcod.EVENT_MOUSE, key, mouse)

            # exit right away
            if libtcod.console_is_window_closed():
                sys.exit()

            if key.vk == libtcod.KEY_ENTER:
                exit_menu = True

            # update screen
            libtcod.console_flush()

    # returns true if crewman unable to perform actions
    def NoActions(self):
        return not self.alive or self.stunned or self.unconscious

    # roll to recover from status effects
    def RecoveryRoll(self):
        if self.unconscious:
            d1, d2, roll = Roll2D6()
            if self.SkillCheck('True Grit'):
                roll -= 1
            if roll <= 8:
                self.unconscious = False
                self.stunned = True
                Message(self.name + ' regains consciousness but remains Stunned.')
        elif self.stunned:
            d1, d2, roll = Roll2D6()
            if self.SkillCheck('True Grit'):
                roll -= 1
            if roll <= 8:
                self.stunned = False
                Message(self.name + ' recovers from being Stunned.')

    # immediately set crew's level, granting skill and experience points
    def SetLevel(self, new_level):
        if new_level == self.level: return
        self.skill_pts += new_level - self.level
        self.level = new_level
        self.exp = GetExpReq(new_level)

    # award a given number of exp to the crewman
    def AwardExp(self, exp_gain):
        # don't award EXP to dead or out of action crew
        if not self.alive or self.v_serious_wound:
            return
        self.exp += exp_gain

    # upgrade the given skill to the given level
    def UpgradeSkill(self, skill_name, skill_level):
        for crew_skill in self.skills:
            if crew_skill.name == skill_name:
                crew_skill.level = skill_level
                return

    # display a small box with crew info, used for crew info screen and skill
    # additions / upgrades
    def DisplayCrewInfo(self, console, x, y, highlight):
        if highlight:
            libtcod.console_set_default_foreground(console, SELECTED_COLOR)
        else:
            libtcod.console_set_default_foreground(console, libtcod.light_grey)

        libtcod.console_print_frame(menu_con, x, y, 27, 30,
            clear=False, flag=libtcod.BKGND_DEFAULT, fmt=0)

        libtcod.console_set_default_foreground(console, libtcod.white)
        libtcod.console_print(console, x+1, y+1, self.position)

        libtcod.console_set_default_foreground(console, libtcod.light_grey)
        libtcod.console_print(console, x+1, y+2, self.GetRank())
        libtcod.console_set_default_foreground(console, libtcod.white)
        libtcod.console_print(console, x+1, y+3, self.name)
        text = self.nickname
        if text != '':
            libtcod.console_set_default_foreground(console, libtcod.light_blue)
            text = ' "' + text + '"'
        libtcod.console_print(console, x+1, y+4, text)

        # hometown
        libtcod.console_set_default_foreground(console, libtcod.light_grey)
        libtcod.console_print(console, x+1, y+5, self.hometown)
        libtcod.console_set_default_foreground(console, libtcod.white)

        # status
        if self.NoActions():
            libtcod.console_set_default_foreground(console, libtcod.light_red)
            if not self.alive:
                text = 'Dead'
            elif self.unconscious:
                text = 'Unconscious'
            else:
                text = 'Stunned'
            libtcod.console_print(console, x+2, y+6, text)

        # wounds
        if self.v_serious_wound:
            text = 'Very Serious Wound'
        elif self.serious_wound:
            text = 'Serious Wound'
        elif self.light_wound:
            text = 'Light Wound'
        else:
            text = ''
        libtcod.console_set_default_foreground(console, libtcod.red)
        libtcod.console_print(console, x+2, y+7, text)

        # display decorations
        if len(self.decorations) > 0:
            # starting x position
            x1 = x+1
            for dec_name in self.decorations[:20]:

                # USA decorations

                if dec_name == 'Purple Heart':
                    libtcod.console_put_char_ex(console, x1, y+9,
                        31, libtcod.purple, libtcod.black)
                    libtcod.console_put_char_ex(console, x1, y+10,
                        libtcod.CHAR_HEART, libtcod.purple, libtcod.black)
                elif dec_name == 'Bronze Star':
                    libtcod.console_put_char_ex(console, x1, y+9,
                        31, libtcod.red, libtcod.black)
                    libtcod.console_put_char_ex(console, x1, y+10,
                        15, libtcod.light_yellow, libtcod.black)
                elif dec_name == 'Silver Star':
                    libtcod.console_put_char_ex(console, x1, y+9,
                        31, libtcod.blue, libtcod.black)
                    libtcod.console_put_char_ex(console, x1, y+10,
                        15, libtcod.light_yellow, libtcod.black)
                elif dec_name == 'Distinguished Service Cross':
                    libtcod.console_put_char_ex(console, x1, y+9,
                        31, libtcod.blue, libtcod.black)
                    libtcod.console_put_char_ex(console, x1, y+10,
                        197, libtcod.dark_yellow, libtcod.black)
                elif dec_name == 'Congressional Medal of Honor':
                    libtcod.console_put_char_ex(console, x1, y+9,
                        254, libtcod.light_blue, libtcod.black)
                    libtcod.console_put_char_ex(console, x1, y+10,
                        42, libtcod.yellow, libtcod.black)

                # UKC decorations
                elif dec_name == 'Military Medal':
                    libtcod.console_put_char_ex(console, x1, y+9,
                        186, libtcod.white, libtcod.blue)
                    libtcod.console_put_char_ex(console, x1, y+10,
                        42, libtcod.light_grey, libtcod.black)
                elif dec_name == 'Military Cross':
                    libtcod.console_put_char_ex(console, x1, y+9,
                        179, libtcod.purple, libtcod.white)
                    libtcod.console_put_char_ex(console, x1, y+10,
                        31, libtcod.light_grey, libtcod.black)
                elif dec_name == 'Distinguished Service Order':
                    libtcod.console_put_char_ex(console, x1, y+9,
                        179, libtcod.red, libtcod.blue)
                    libtcod.console_put_char_ex(console, x1, y+10,
                        31, libtcod.white, libtcod.black)
                elif dec_name == 'Victoria Cross':
                    libtcod.console_put_char_ex(console, x1, y+9,
                        178, libtcod.red, libtcod.black)
                    libtcod.console_put_char_ex(console, x1, y+10,
                        31, libtcod.dark_yellow, libtcod.black)

                x1 += 1

        libtcod.console_set_default_foreground(console, libtcod.light_grey)
        libtcod.console_print(console, x+1, y+12, 'Level:')
        libtcod.console_print(console, x+1, y+13, 'Exp:')
        libtcod.console_print(console, x+1, y+14, 'Skill Pts:')

        libtcod.console_set_default_foreground(console, libtcod.white)
        libtcod.console_print(console, x+8, y+12, str(self.level))

        # display current exp and exp required for next level
        libtcod.console_set_default_foreground(console, libtcod.white)
        text = str(self.exp) + '/' + str(GetExpReq(self.level+1))
        libtcod.console_print(console, x+6, y+13, text)

        # display skill points
        if self.skill_pts > 0:
            libtcod.console_set_default_foreground(console, libtcod.light_blue)
        libtcod.console_print(console, x+12, y+14, str(self.skill_pts))
        libtcod.console_set_default_foreground(console, libtcod.white)

    # build a list of possible orders based on crewman status, etc.
    def BuildOrdersList(self, no_reset=False):
        self.orders_list = []

        for order in CREW_ORDERS:

            # skip if this order not allowed to this crew member's position
            if self.position not in order.position_list: continue

            # only show Smoke Mortar order if tank has a smoke mortar
            if order.name == 'Fire Smoke Mortar':
                if not tank.stats.has_key('smoke_mortar'): continue

            # skip movement orders if tank is immobilized
            if tank.immobilized or tank.bogged_down:
                if 'Driver' in order.position_list and order.name not in ['Stop', 'Attempt Unbog', 'Abandon Tank']:
                    continue

            # only allow unbog attempt for driver if bogged
            if order.name == 'Attempt Unbog':
                if not tank.bogged_down: continue

            # only allow throw smoke grenade if has hatch and tank
            # has at least one smoke grenade remaining
            if order.name == 'Throw Smoke Grenade':
                if self.hatch != 'Open': continue
                if tank.smoke_grenades == 0: continue

            # disable reload order if no shell in main gun
            if order.name == 'Reload':
                if tank.ammo_load == 'None': continue

            # AA MG
            if order.name in ['Fire AA MG', 'Repair AA MG']:
                if not tank.stats.has_key('aa_mg'): continue
                if self.position == 'Loader' and tank.stats['loader_hatch'] != 'Split': continue
                if self.hatch != 'Open': continue
            if order.name == 'Fire AA MG':
                if 'AA MG Malfunction' in tank.damage_list or 'AA MG Broken' in tank.damage_list: continue
            if order.name == 'Repair AA MG':
                if 'AA MG Malfunction' not in tank.damage_list: continue

            # Co-ax MG
            if order.name == 'Fire Co-Axial MG':
                if not tank.stats.has_key('co_ax_mg'): continue
                if 'Co-ax MG Malfunction' in tank.damage_list or 'Co-ax MG Broken' in tank.damage_list: continue
            if order.name == 'Repair Co-ax MG':
                if not tank.stats.has_key('co_ax_mg'): continue
                if 'Co-ax MG Malfunction' not in tank.damage_list: continue

            # Bow MG
            if order.name == 'Fire Bow MG':
                if not tank.stats.has_key('bow_mg'): continue
                if tank.hull_down: continue
                if 'Bow MG Malfunction' in tank.damage_list or 'Bow MG Broken' in tank.damage_list: continue
            if order.name == 'Repair Bow MG':
                if not tank.stats.has_key('bow_mg'): continue
                if 'Bow MG Malfunction' not in tank.damage_list: continue

            # Firing Main Gun, Directing Main Gun Fire, or changing gun load
            if order.name in ['Fire Main Gun', 'Direct Main Gun Fire', 'Change Gun Load']:
                if 'Main Gun Malfunction' in tank.damage_list or 'Main Gun Broken' in tank.damage_list: continue
                if 'Gun Sight Broken' in tank.damage_list: continue

            # check turret traverse gear
            if 'Turret Traverse Malfunction' in tank.damage_list or 'Turret Traverse Broken' in tank.damage_list:
                if order.name in ['Rotate Turret']: continue

            # check for tank intercom broken
            if 'Intercom Malfunction' in tank.damage_list or 'Intercom Broken' in tank.damage_list:
                if order.name in ['Direct Movement', 'Direct Bow MG Fire']:
                    continue

            # only allow repairs if the system is malfunctioning
            if order.name == 'Repair Main Gun':
                if 'Main Gun Malfunction' not in tank.damage_list: continue
            elif order.name == 'Repair Turret Traverse':
                if 'Turret Traverse Malfunction' not in tank.damage_list: continue
            elif order.name == 'Repair Radio':
                if 'Radio Malfunction' not in tank.damage_list: continue
            elif order.name == 'Repair Intercom':
                if 'Intercom Malfunction' not in tank.damage_list: continue

            # only allow abandoning the tank if one or more crewmen very
            #  seriously wounded or worse, or tank is immobile
            if order.name == 'Abandon Tank':
                crew_qualify = False
                if tank.immobilized:
                    crew_qualify = True
                elif tank.swiss_cheese:
                    crew_qualify = True
                else:
                    for crewman in tank.crew:
                        if crewman.v_serious_wound or not crewman.alive:
                            crew_qualify = True
                            break
                if not crew_qualify: continue

            self.orders_list.append(order)

        # set None order for inactive crew, default order for Loader and Driver
        if not no_reset:
            self.ResetOrder()
            return

        # otherwise, we still need to check that our current order is allowed
        #  if not, try to set to default
        if not self.CurrentOrderOK():
            self.ResetOrder()

    # see if this crew has the specified skill and, if so, roll to activate it
    def SkillCheck(self, skill_name):

        if not self.alive or self.unconscious or self.stunned:
            return False

        for skill in self.skills:
            if skill.name == skill_name:
                roll = Roll1D100()

                # check for battle leadership effect if in battle
                if battle is not None:
                    if battle.battle_leadership:
                        roll -= 5

                if roll <= skill.level:
                    # only display message if skill is not automatic
                    if skill.level < 100:
                        text = self.name + ' activates ' + skill_name + ' skill!'
                        Message(text, color=SKILL_ACTIVATE_COLOR)
                    return True
                break
        return False

    # return the full or short form of this crewman's rank
    def GetRank(self, short=False):
        a, b, c = campaign.ranks[self.rank_level]
        if short:
            return a
        return b

    # generate a random name for a crewman
    def GenerateName(self):
        good_name = False
        while not good_name:
            name = random.choice(FIRST_NAMES)
            name += ' ' + random.choice(LAST_NAMES)
            # make sure name isn't too long
            if len(name) > NAME_MAX_LEN:
                continue
            # make sure name isn't the same as an already existing one
            for crewman in tank.crew:
                if crewman.name == name:
                    continue
            # set name
            self.name = name
            good_name = True

    # check that this crew's hatch status matches what is possible for this tank
    # used after switching tanks, since it may or may not have a loader hatch
    def CheckHatch(self):
        # if this model has a loader hatch
        if self.position == 'Loader':
            # if no hatch in this tank, crew hatch must be set to none
            if tank.stats['loader_hatch'] == 'None':
                self.hatch = 'None'
            else:
                # otherwise, if hatch used to be none, set it to shut now
                if self.hatch == 'None':
                    self.hatch = 'Shut'

    # return a list of text strings with info on this crewman
    def GetInfo(self):
        info_list = []
        info_list.append(self.name)
        info_list.append(self.position)
        # if we're in a battle, return current order
        if battle is not None:
            info_list.append(self.order)
        else:
            info_list.append('')
        info_list.append(self.hatch)
        info_list.append(self.spot)
        info_list.append(self.nickname)
        return info_list

    # set spotting ability of this crewman based on location, hatch status, and order
    def SetSpotAbility(self):
        if self.NoActions():
            self.spot = 'None'
            return

        # check order spot effects
        for order in CREW_ORDERS:
            if order.name == self.order:
                if not order.spot:
                    self.spot = 'None'
                    return
                break

        if self.position == 'Commander':
            if tank.stats.has_key('vision_cupola'):
                self.spot = 'All'
            elif self.hatch == 'Open':
                self.spot = 'All'
            else:
                if 'Commander Periscope Broken' in tank.damage_list:
                    self.spot = 'None'
                else:
                    self.spot = 'Any One Sector'
        elif self.position == 'Gunner':
            if 'Gunner Periscope Broken' in tank.damage_list:
                self.spot = 'None'
            else:
                self.spot = 'Turret Front'
        elif self.position == 'Loader':
            if tank.fired_main_gun:
                self.spot = 'None'
            else:
                if tank.stats['loader_hatch'] != 'None':
                    if self.hatch == 'Open':
                        self.spot = 'All'
                    else:
                        self.spot = 'Any One Sector'
                else:
                    self.spot = 'Any One Sector'
                if self.spot == 'Any One Sector' and 'Loader Periscope Broken' in tank.damage_list:
                    self.spot = 'None'
        elif self.position in ['Driver', 'Asst. Driver']:
            if self.hatch == 'Open':
                self.spot = 'All Except Rear'
            else:
                if self.position == 'Driver' and 'Driver Periscope Broken' in tank.damage_list:
                    self.spot = 'None'
                elif self.position == 'Asst. Driver' and 'Asst. Driver Periscope Broken' in tank.damage_list:
                    self.spot = 'None'
                else:
                    self.spot = 'Tank Front'
        else:
            self.spot = 'None'        # should not be used

    # check that our current order is allowed
    def CurrentOrderOK(self):
        for order in self.orders_list:
            if order.name == self.order: return True
        return False

    # sets default order for loader and driver, or set to no order if out of action
    # if reset_all, resets order for all crew
    def ResetOrder(self, reset_all=False):
        if not self.alive or self.unconscious or self.stunned:
            self.order = 'None'
        elif reset_all or self.position in ['Loader', 'Driver']:
            self.order = self.default_order

        # check that our default order is possible, otherwise set to none
        if not self.CurrentOrderOK():
            self.order = 'None'

    # test to see if this crewman is stunned as a result of a hit
    # different events will supply different base scores to beat in order to save
    def StunCheck(self, base_score):
        # can't be stunned if already hurt
        if not self.alive or self.stunned or self.unconscious:
            return False

        d1, d2, roll = Roll2D6()

        # 6,6 always fails
        if roll != 12:
            if self.SkillCheck('True Grit'):
                roll -= 1
            if roll <= base_score:
                return False
        self.stunned = True
        return True

    # works out the effect of a wound and returns a string description
    def TakeWound(self, hit_location, sector, collateral=False, minefield=False):

        # can't suffer further wounds if dead
        if not self.alive:
            return None

        # stunned and unconscious crew are not subject to collateral damage
        # idea is that they are not exposed enough to suffer injury
        if (self.stunned or self.unconscious) and collateral:
            return None

        d1, d2, roll = Roll2D6()

        # unmodified 6,6 is crewman killed
        if roll == 12:
            if self.SkillCheck('Pocket Bible'):
                WriteJournal(self.name + ' was saved by Pocket Bible.')
                return 'Saved by Pocket Bible'
            if collateral:
                if self.SkillCheck('Lightning Reflexes'):
                    WriteJournal(self.name + ' was saved by Lightning Reflexes.')
                    return 'Saved by Lightning Reflexes'
            text = 'Killed!'
            self.ResolveKIA()
            UpdateTankCon()
            return text

        # work out any hit location crew wound modifiers
        if hit_location is not None and sector is not None:

            d, a, g, l, c = 0, 0, 0, 0, 0

            # turret hit
            if hit_location == 'turret':
                # all directions
                d -= 2
                a -= 2
                # right side
                if sector in [5, 0]:
                    g += 1
                    l -= 1
                # left side
                elif sector in [2, 3]:
                    g -= 1
                    l += 1
                # rear
                elif sector == 1:
                    c += 1
            # hull hit
            else:
                # front right
                if sector == 5:
                    d -= 1
                    l -= 1
                    a += 1
                    g += 1
                # back center, right, or left
                elif sector in [0, 1, 2]:
                    d -= 3
                    a -= 3
                    g -= 2
                    l -= 2
                    c -= 2
                # front left
                elif sector == 3:
                    d += 1
                    l += 1
                    a -= 1
                    g -= 1

            # apply modifiers based on position in tank
            if self.position == 'Commander':
                roll += c
            elif self.position == 'Gunner':
                roll += g
            elif self.position == 'Loader':
                roll += l
            elif self.position == 'Driver':
                roll += d
            elif self.position == 'Asst. Driver':
                roll += a

        # already wounded
        if self.v_serious_wound:
            roll += 3
        elif self.serious_wound:
            roll += 2
        elif self.light_wound:
            roll += 1

        # minefield damage less likely to be serious
        if minefield:
            roll -= 2

        # collateral damage less likely to be serious
        if collateral:
            roll -= 3

        # if crewman is outside tank, normal damage is much less severe, but
        # collateral damage much more dangerous
        if self.order == 'Fire AA MG':
            if collateral:
                roll += 4
            elif hit_location is not None and sector is not None:
                roll -= 2

        if self.SkillCheck('True Grit'):
            roll -= 1

        ##### Check modified roll for result #####

        # No Effect
        if roll <= 6:
            return None

        # if collateral, crewman might have chance to ignore
        if collateral:
            if self.SkillCheck('Lightning Reflexes'):
                return 'Saved by Lightning Reflexes'

        # Light Wound, chance of being stunned
        if roll == 7:
            text = 'Light Wound'
            self.light_wound = True
            if self.StunCheck(10):
                text += ', Stunned'

        # Light Wound, greater chance of being stunned
        elif roll == 8:
            text = 'Light Wound'
            self.light_wound = True
            if self.StunCheck(7):
                text += ', Stunned'

        # Serious Wound, chance of being stunned
        elif roll == 9:
            text = 'Serious Wound'
            self.serious_wound = True
            if self.StunCheck(5):
                text += ', Stunned'

        # Serious Wound, automatically stunned
        elif roll == 10:
            text = 'Serious Wound, Stunned'
            self.serious_wound = True
            self.stunned = True

        # Very Serious Wound, Unconscious
        elif roll == 11:
            text = 'Very Serious Wound, Unconscious'
            self.v_serious_wound = True
            self.unconscious = True
            # overrides any lesser effects
            self.stunned = False

        # Dead
        else:
            if self.SkillCheck('Pocket Bible'):
                WriteJournal(self.name + ' was saved by Pocket Bible.')
                return 'Saved by Pocket Bible'
            text = 'Killed!'
            self.ResolveKIA()

        # update spot ability
        if self.NoActions():
            self.BuildOrdersList()
            self.SetSpotAbility()
            self.ResetOrder()

        UpdateTankCon()

        WriteJournal(self.name + ' was wounded, result: ' + text)

        return text

    # attempt to bail out of tank, return string description of outcome
    def BailOut(self):

        if self.unconscious:
            return 'Cannot bail out'

        # easy to bail out when you're outside the tank already
        if self.order == 'Fire AA MG':
            self.bailed_out = True
            return 'Passed'

        d1, d2, roll = Roll2D6()

        bail_mod = 0
        if self.hatch == 'None':
            bail_mod += 1
        if self.stunned:
            bail_mod += 1

        if self.SkillCheck('Gymnast'):
            bail_mod -= 2

        roll += bail_mod

        if roll <= 10:
            self.bailed_out = True
            return 'Passed'
        else:
            return 'Failed'



# Battle Class
# holds information relating to an encounter on the battle board
# can make this a counterattack battle and/or change the resistance level of the
#  battle if variables are passed on init
class Battle:
    def __init__(self, counterattack=False, res_level=None):

        self.maphexes = []    # list of hexes on the battle map
        self.smoke_factors = []    # list of active smoke factor hexes
                    # (hx, hy, smoke level)

        self.messages = []    # list of game messages
        self.enemy_units = []    # list of active enemy units
        self.vp_total = 0    # current total player VP for encounter

        self.mouseover = (-1, -1)    # keeps track of mouse position

        # if a unit of a given class has already been spawned, record it here
        self.tank_type = None
        self.spg_type = None
        self.at_gun_type = None

        # special flag: play this encounter as if day were a counterattack mission
        self.counterattack = counterattack

        # friendly ambush flag, for counterattack mission
        self.friendly_ambush = False

        # current phase in encounter turn
        self.phase = 'None'

        self.selected_crew = None    # pointer to currently selected crewmember
        self.orders = []        # list of possible orders for a selected crew member

        # marks index number of selected order, used in Issue Order input mode
        self.selected_order = None

        self.area_fire = False        # area fire mode flag
        self.target = None        # pointer to current target enemy unit

        # used to trigger an end to current player input and move to next
        # phase or sub-phase
        self.trigger_phase = False

        self.battle_leadership = False    # battle leadership skill is in play for this
                        # encounter turn

        ##### Battle Record Stats #####

        # enemy units destroyed by player tank, destroyed by friendly units
        # units forced off board by player movement
        # LW and MG, Truck, APCs and ACs, SPG, PzKw IV H, PzKw V G, PzKw V GI, AT Gun
        self.tank_ko_record = [0, 0, 0, 0, 0, 0, 0, 0]
        self.friendly_ko_record = [0, 0, 0, 0, 0, 0, 0, 0]
        self.left_behind = [0, 0, 0, 0, 0, 0, 0, 0]

        self.tanks_lost = 0    # friendly tanks lost
        self.inf_lost = 0    # friendly infantry squads lost

        self.enemy_reinforcements = 0    # total number of enemy reinforcements
                        #  that have arrived in this battle
        self.rounds_passed = 1        # total number of game rounds that have
                        #  passed in this battle encounter

        # current encounter result
        self.result = 'Undetermined'

        ##### Generate Map Hexes #####
        for (hx, hy, rng, sector) in HEXES:
            self.maphexes.append(MapHex(hx, hy, rng, sector))


# Enemy Units
class EnemyUnit:
    def __init__(self):
        self.alive = True    # set to false if destroyed
        self.map_hex = None    # hex location
        self.x = 0        # x position in map console
        self.y = 0        # y "
        self.animating = False    # we are currently animating this unit's movement, so
                    #  don't draw terrain around it

        self.facing = ''    # unit facing: front, side, or rear
                    # not used for infantry units
        self.moving = False    # movement status
        self.terrain = ''    # terrain

        self.pf = False        # unit is armed with a panzerfaust

        self.spotted = False    # unit has been spotted by player tank
        self.identified = False    # unit has been identified; only required for
                    # Tanks, SPGs, and AT Guns
        self.hidden = False    # unit is hidden
        self.spotted_lr = False    # unit was spotted last round (increased
                    # chance of identifying)
        self.spotted_tr = False    # temp flag for setting spotted_lr for next round

        self.immobile = False    # unit has been immobilized by a track hit

        self.shot_at = False    # unit was fired at by player earlier this turn
        self.fired = False    # unit fired last turn; cleared after spotting phase
        self.acquired = 0    # level of acquired target for player tank
        self.acquired_player = 0    # level that this unit has acquired the
                        # player tank
        self.full_apc = False    # unit is an APC carrying infantry

        self.unit_class = ''    # unit class
        self.unit_type = ''    # unit type

        self.morale = self.SetMorale()        # unit morale level
        self.pinned = False            # morale status flags
        self.stunned = False

        self.hit_record = []    # list of unresolved hits against this unit

    # check to see if we do a panzerfaust attack, returning True if attack happened
    def PFAttack(self):

        if not self.pf or self.map_hex.rng != 0 or self.terrain in ['Building', 'Fortification']:
              return False

        if self.hidden or self.pinned:
            return False

        # see if attack occurs
        roll = Roll1D6()

        year = campaign.current_date[0]
        month = campaign.current_date[1]
        if year >= 1945 or (year == 1944 and month == 12):
            roll -= 1
        if tank.moving: roll -= 1
        if tank.lead_tank: roll -= 1
        if self.map_hex.sector in [0,1,2]: roll -= 1

        if campaign.scen_type == 'Advance':
            target_roll = 2
        elif campaign.scen_type == 'Battle':
            target_roll = 3
        else:
            target_roll = 1

        if roll > target_roll: return False

        # firing a pf means that unit is revealed
        self.spotted = True

        # play sound effect
        PlaySound('panzerfaust_firing')

        text = 'An infantry squad fires a Panzerfaust at you!'
        WriteJournal(text)
        ShowLabel(self.x+MAP_CON_X, self.y+MAP_CON_Y, text)

        # create roll action to hold details about the action
        roll_action = RollAction()

        # input details
        roll_action.attacker_unit_type = 'Light Weapons Infantry'
        roll_action.attacker = 'Infantry Squad'
        roll_action.attack_type = 'Panzerfaust'
        roll_action.target_unit_type = tank.unit_type
        roll_action.target = tank.stats['vehicle_type'] + ' "' + tank.name + '"'
        roll_action.rng = 'Close'
        roll_action.score_req = 6

        # calculate DRM
        drm = []
        if tank.moving:
            drm.append(('Target moving', 2))

        smoke_factors = GetSmokeFactors(0, 0, self.map_hex.hx, self.map_hex.hy)
        if smoke_factors > 0:
            drm.append(('Smoke Factors', smoke_factors*2))

        roll_action.drm = drm
        roll_action.CalculateTotalDRM()
        roll_action.roll_req = roll_action.score_req - roll_action.total_drm

        ##### To-hit Roll #####
        d1, d2, roll = Roll2D6()

        roll_action.d1 = d1
        roll_action.d2 = d2
        roll_action.roll = roll

        hit = False

        # critical miss
        if roll == 12:
            roll_action.result = 'Panzerfaust explodes, squad scattered!'
            self.RecordKO()
            self.alive = False
        elif roll > roll_action.roll_req:
            roll_action.result = 'Attack missed!'
        else:
            # determine hit location
            hit_location = GetHitLocation(tank.hull_down)
            if hit_location == 'Miss':
                roll_action.result = 'The shot misses because your tank is hull down.'
            elif hit_location == 'Track':
                roll_action.result = 'Your tank is hit in the track and is immobilized.'
                tank.moving = False
                tank.immobilized = True
            else:
                # hit in turret or hull
                hit = True
                roll_action.result = 'The panzerfaust hits your tank in the ' + hit_location + '!'

        WriteJournal(roll_action.result)

        # display to-hit result to player
        DisplayRoll(roll_action)
        UpdateMapOverlay()
        RenderEncounter()

        if hit:
            ##### Resolve Hit on Player #####
            if hit_location == 'Turret':
                if tank.turret_facing == self.map_hex.sector:
                    facing = 'Front'
                elif GetSectorDistance(self.map_hex.sector, tank.turret_facing) == 3:
                    facing = 'Rear'
                else:
                    facing = 'Side'
            else:
                if self.map_hex.sector == 4:
                    facing = 'Front'
                elif self.map_hex.sector == 1:
                    facing = 'Rear'
                else:
                    facing = 'Side'

            # get To Kill number and update roll action
            (base_tk, roll_req, drm) = CalcTK(self, tank, facing, 'PF', False, False, hit_location)

            # if no chance to knock out, display that instead
            if roll_req < 2:
                ShowLabel(MAP_X0+MAP_CON_X, MAP_Y0+MAP_CON_Y, 'No chance to destroy.')
                del roll_action
                return

            roll_action.hit_location = hit_location
            roll_action.score_req = base_tk
            roll_action.drm = drm
            roll_action.CalculateTotalDRM()
            roll_action.roll_req = roll_req

            ##### To kill Roll #####
            d1, d2, roll = Roll2D6()
            roll_action.d1 = d1
            roll_action.d2 = d2
            roll_action.roll = roll

            if roll < roll_req:
                roll_action.result = "Your tank's armour is penetrated by the hit!"
            else:
                roll_action.result = 'Your tank is unharmed.'

            # display to-kill result to player
            WriteJournal(roll_action.result)
            DisplayRoll(roll_action, tk_roll=True)
            RenderEncounter()

            # play armour saved sound if appropriate
            if roll >= roll_req:
                PlaySound('armour_save')
            else:
                # determine whether it was a critical penetration
                crit = False
                if roll == 2 or roll < int(roll_req / 2):
                    crit = True
                tank.Penetrate(hit_location, self.map_hex.sector, 'Panzerfaust', critical=crit)
                UpdateTankCon()
                RenderEncounter()

        del roll_action

        return True

    # do a pin test or automatically pin
    def PinTest(self, auto=False, modifier=0):
        if self.MoraleTest(modifier=modifier) and not auto:
            return
        # already pinned: double pin, so must pass a morale check or broken
        if self.pinned:
            if not self.MoraleTest(break_test=True):
                self.RecordKO()
                self.alive = False
        self.pinned = True
        self.moving = False
        return

    # do a morale test
    def MoraleTest(self, modifier=0, break_test=False):
        d1, d2, roll = Roll2D6()

        # apply terrain modifiers if break test
        if break_test:
            if self.unit_class == 'AT_GUN' and self.terrain != 'Fortification':
                roll -= 2
            elif self.terrain == 'Woods':
                roll -= 1
            elif self.terrain == 'Building':
                roll -= 2
            elif self.terrain == 'Fortification':
                roll -= 3

        # natural 12 is always a fail
        if roll != 12 and roll <= self.morale + modifier:
            return True
        return False

    # set morale level, only done at spawn
    def SetMorale(self):
        d1, d2, result = Roll2D6()
        if result <= 3:
            return 10
        elif result <= 5:
            return 9
        elif result <= 8:
            return 8
        return 7

    # reset unit for a new turn
    def Reset(self):
        self.shot_at = False

    # draw this unit on the map overlay
    def DrawMe(self):
        # skip if inactive
        if not self.alive: return

        # set colours based on spotting status

        # hidden
        if self.hidden:
            libtcod.console_set_default_background(overlay_con, libtcod.dark_grey)
            libtcod.console_set_default_foreground(overlay_con, libtcod.black)

        # unknown
        elif not self.spotted:
            libtcod.console_set_default_background(overlay_con, ENEMY_COLOR)
            libtcod.console_set_default_foreground(overlay_con, libtcod.darker_grey)

        # spotted but unidentifed
        elif self.unit_class in ['TANK', 'SPG', 'APC', 'AC'] and not self.identified:
            libtcod.console_set_default_background(overlay_con, ENEMY_COLOR)
            libtcod.console_set_default_foreground(overlay_con, libtcod.lighter_grey)

        # spotted
        else:
            libtcod.console_set_default_background(overlay_con, ENEMY_COLOR)
            libtcod.console_set_default_foreground(overlay_con, libtcod.white)

        # if selected as target, highlight
        if battle.target == self and battle.phase in ['Fire Main Gun', 'Fire MGs']:
            libtcod.console_set_default_background(overlay_con, SELECTED_COLOR)

        # select character to use
        if self.unit_class == 'TANK':
            char = libtcod.CHAR_RADIO_UNSET
        elif self.unit_class == 'SPG':
            char = '#'
        elif self.unit_class == 'APC':
            char = libtcod.CHAR_BULLET_INV
        elif self.unit_class == 'AC':
            char = libtcod.CHAR_RADIO_SET
        elif self.unit_class == 'AT_GUN':
            char = 'X'
        elif self.unit_class == 'MG':
            char = 'x'
        elif self.unit_class == 'LW':
            char = libtcod.CHAR_BLOCK1
        else:
            char = libtcod.CHAR_BULLET_SQUARE    # TRUCK

        # print the character
        libtcod.console_put_char(overlay_con, self.x, self.y, char, flag=libtcod.BKGND_SET)

        if self.hidden or not self.spotted: return

        # skip drawing terrain if animating
        if self.animating: return

        # add terrain indicator if any
        if self.terrain not in ['Hull Down', 'Woods', 'Building']: return
        if self.terrain == 'Hull Down':
            char = libtcod.CHAR_ARROW2_N
        elif self.terrain == 'Woods':
            char = libtcod.CHAR_SPADE
        elif self.terrain == 'Building':
            char = libtcod.CHAR_DVLINE

        bc = libtcod.console_get_char_background(map_con, self.x, self.y)
        fc = bc * libtcod.light_grey
        for x in [-1, 1]:
            libtcod.console_put_char_ex(overlay_con, self.x+x, self.y, char, fc, bc)


    # rotate this unit's hex position around the player, used when player tank pivots
    def RotatePosition(self, clockwise):
        # convert present coordinate from axial to cube
        x = self.map_hex.hx
        z = self.map_hex.hy
        y = -x-z

        # do the rotation
        if clockwise:
            new_x = -y
            new_z = -x
        else:
            new_x = -z
            new_z = -y

        # find the new hex location
        for map_hex in battle.maphexes:
            if map_hex.hx == new_x and map_hex.hy == new_z:
                self.map_hex = map_hex
                (self.x, self.y) = self.GetCharLocation()
                return
        print 'ERROR: could not find hex ' + str(new_x) + ',' + str(new_z)

    # record this unit's destruction in the battle record
    def RecordKO(self, friendly=False, left_behind=False, advance_fire=False):

        if not left_behind and friendly:
            text = self.GetDesc() + ' was destroyed by friendly action'
            WriteJournal(text)

        # determine index number for this unit in list of units destroyed
        index = -1
        if self.unit_class in ['LW', 'MG']:
            index = 0
        elif self.unit_class == 'TRUCK':
            index = 1
        elif self.unit_class in ['APC', 'AC']:
            index = 2
        elif self.unit_class == 'SPG':
            index = 3
        elif self.unit_type == 'PzKw IV H':
            index = 4
        elif self.unit_type == 'PzKw V G':
            index = 5
        elif self.unit_type in ['PzKw VI E', 'PzKw VI B']:
            index = 6
        elif self.unit_class == 'AT_GUN':
            index = 7

        if index < 0:
            print 'RecordKO() error: could not find unit type'
            return

        if friendly:
            battle.friendly_ko_record[index] += 1
        elif left_behind:
            battle.left_behind[index] += 1
        else:
            battle.tank_ko_record[index] += 1

        # award exp if destroyed by player tank or by advancing fire
        if (not friendly and not left_behind) or advance_fire:
            for crew in tank.crew:
                crew.AwardExp(1)

        # add to campaign stats
        if not left_behind:
            if index == 0:
                if not friendly:
                    campaign.AddStat('Infantry Destroyed by Player', 1)
                else:
                    campaign.AddStat('Infantry Destroyed by Allies', 1)
            elif index == 7:
                if not friendly:
                    campaign.AddStat('AT Guns Destroyed by Player', 1)
                else:
                    campaign.AddStat('AT Guns Destroyed by Allies', 1)
            elif index > 2 and index < 7:
                if not friendly:
                    campaign.AddStat('Tanks & SPGs Destroyed by Player', 1)
                else:
                    campaign.AddStat('Tanks & SPGs Destroyed by Allies', 1)
            else:
                if not friendly:
                    campaign.AddStat('Other Vehicles Destroyed by Player', 1)
                else:
                    campaign.AddStat('Other Vehicles Destroyed by Allies', 1)

    # set or redetermine the facing for this unit
    # if facing has changed, return True
    def SetFacing(self):
        result = Roll1D10()
        if self.unit_class in ['SPG', 'AT_GUN']:
            if result <= 6:
                new_facing = 'Front'
            elif result <= 9:
                new_facing = 'Side'
            else:
                new_facing = 'Rear'
        elif self.unit_class == 'TANK':
            if result <= 5:
                new_facing = 'Front'
            elif result <= 9:
                new_facing = 'Side'
            else:
                new_facing = 'Rear'
        elif self.unit_class in ['TRUCK', 'APC', 'AC']:
            if result <= 3:
                new_facing = 'Front'
            elif result <= 7:
                new_facing = 'Side'
            else:
                new_facing = 'Rear'

        # otherwise, don't need to set facing
        else:
            return False

        # set facing if different and report back that it changed
        if new_facing != self.facing:
            self.facing = new_facing
            return True
        return False

    # set or redetermine the terrain for this unit
    def SetTerrain(self):

        # list of terrain types
        TERRAIN_TYPE = [
            'Hull Down', 'Woods', 'Building', 'Open'
        ]

        # infantry unit chart
        INFANTRY_TERRAIN = [
            [0, 2, 8, 10],    # Area A: farm buildings and fields
            [0, 3, 5, 10],    # Area B: fields
            [0, 1, 6, 10],    # Area C: village
            [0, 6, 7, 10],    # Area D: Woods
            [0, 4, 5, 10],    # Area F: Bocage
        ]

        # vehicle unit chart
        VEHICLE_TERRAIN = [
            [4, 6, 0, 10],    # Area A
            [2, 3, 0, 10],    # Area B
            [5, 6, 0, 10],    # Area C
            [2, 7, 0, 10],    # Area D
            [7, 8, 0, 10]    # Area F
        ]

        # determine table row to use
        AREA_TYPES = ['A', 'B', 'C', 'D', 'F']
        table_row = AREA_TYPES.index(campaign.day_map.player_node.node_type)

        # do roll
        result = Roll1D10()

        # modifier for counterattack missions
        if campaign.scen_type == 'Counterattack' or battle.counterattack:
            result += 2
            if result > 10:
                result = 10

        # infantry units
        if self.unit_class in ['LW', 'MG', 'AT_GUN']:
            n = 0
            for value in INFANTRY_TERRAIN[table_row]:
                if result <= value:
                    terrain = TERRAIN_TYPE[n]
                    break
                n += 1

            # fortification case
            if campaign.scen_type == 'Battle' and campaign.day_map.player_node.node_type in ['B', 'D']:
                if n == 2:
                    terrain = 'Fortification'

            # special for LW
            elif self.unit_class == 'LW' and result == 10:
                self.moving = True

        # vehicle units
        else:
            n = 0
            for value in VEHICLE_TERRAIN[table_row]:
                if result <= value:
                    terrain = TERRAIN_TYPE[n]
                    break
                n += 1

            if 9 <= result <= 10:
                self.moving = True    # moving if not already

        # set unit terrain type
        self.terrain = terrain

    # returns a short string of text to describe this unit
    # if just spawned, return a simpler description
    def GetDesc(self, new_spawn=False):

        # return a descriptive string for this unit's class, or type if does
        # not need to be identified
        def GetClassDesc():

            # LW and MG are simple
            if self.unit_class in ['LW', 'MG']:
                return self.unit_type

            # AT Guns are a little more complicated
            elif self.unit_class == 'AT_GUN':
                if not self.identified:
                    return 'Anti-Tank Gun'
                if self.unit_type == '50L':
                    text = 'PaK 38'
                elif self.unit_type == '75L':
                    text = 'PaK 40'
                elif self.unit_type == '88LL':
                    text = 'PaK 43'
                return text + ' Anti-Tank Gun'

            # Tanks
            elif self.unit_class == 'TANK':
                if not self.identified:
                    return 'Tank'
                return self.unit_type + ' Tank'

            # SPGs
            elif self.unit_class == 'SPG':
                if not self.identified:
                    return 'Self-propelled Gun'
                return self.unit_type + ' Self-propelled Gun'

            # Trucks
            elif self.unit_class == 'TRUCK':
                return self.unit_type + ' Truck'

            # APCs
            elif self.unit_class == 'APC':
                return self.unit_type + ' Armoured Personel Carrier'

            # ACs
            elif self.unit_class == 'AC':
                return self.unit_type + ' Armoured Car'

            # should never get as far as this point, but just in case
            return ''

        # just appeared, return a simple description
        if new_spawn:
            return GetClassDesc()

        # unit is hidden
        if self.hidden:
            return 'Hidden ' + GetClassDesc()

        # unit is spotted but needs to be identified
        if self.spotted and self.unit_class in ['TANK', 'SPG', 'AT_GUN'] and not self.identified:
            return 'Unidentified ' + GetClassDesc()

        # unit is not spotted but had been previously identified
        if not self.spotted:
            return 'Unspotted ' + GetClassDesc()

        # unit is spotted, and is either identified or doesn't need to be
        return GetClassDesc()

    # the player tank has moved forward or backward, so shift this enemy unit accordingly
    def YMove(self, y_change):

        # two special cases, if unit would end up in player hex
        if self.map_hex.hx == 0 and self.map_hex.hy + y_change == 0:
            if y_change == -1:
                y_change = -2
            else:
                y_change = 2

        new_hy = self.map_hex.hy + y_change

        for map_hex in battle.maphexes:
            if map_hex.hx == self.map_hex.hx and map_hex.hy == new_hy:

                # move is ok, proceed
                self.map_hex = map_hex
                self.moving = True

                # re-determine draw location
                (self.x, self.y) = self.GetCharLocation()

                # clear any hidden flag
                if self.hidden:
                    self.hidden = False

                # redraw the screen to reflect new position
                UpdateMapOverlay()
                RenderEncounter()

                return

        # unit was moved off board
        Message(self.GetDesc() + ' is no longer in the area')
        self.alive = False
        self.RecordKO(left_behind=True)
        UpdateMapOverlay()
        RenderEncounter()
        return

    # unit moves closer to or further away from the player tank
    def DistMove(self, dist):

        # if immobile, can't move
        if self.immobile: return False

        # if ground conditions are deep snow or mud, chance that action will be re-rolled
        if campaign.weather.ground in ['Mud', 'Deep Snow']:
            if Roll1D6() <= 3: return False

        # if new range is 3, unit will move off map
        if self.map_hex.rng + dist == 3:

            # chance that this action will be re-rolled
            if Roll1D6() <= 3: return False

            self.alive = False
            Message(self.GetDesc() + ' has left the area.')
            UpdateMapOverlay()
            RenderEncounter()
            return True

        # otherwise, find a hex to move into
        move_hexes = []

        # skip over player hex if moving close and in range band 0
        if self.map_hex.rng == 0 and dist == -1:
            for map_hex in battle.maphexes:
                if self.map_hex.rng == map_hex.rng and not IsAdjacent(self.map_hex, map_hex) and self.map_hex != map_hex:
                    move_hexes.append(map_hex)
        else:
            for map_hex in battle.maphexes:
                if self.map_hex.rng + dist == map_hex.rng and IsAdjacent(self.map_hex, map_hex):
                    move_hexes.append(map_hex)

        # couldn't find a good hex to move to
        if len(move_hexes) == 0:
            return False

        # do the move
        old_x, old_y = self.x, self.y
        self.map_hex = random.choice(move_hexes)

        # show the animation
        self.MoveAnimation(old_x, old_y)

        # apply effects of moving
        self.MoveEffects()

        return True

    # unit moves laterally around the player, clockwise or counter clockwise
    def LateralMove(self):

        # if immobile, can't move
        if self.immobile: return False

        # if ground conditions are deep snow or mud, chance that action will be re-rolled
        if campaign.weather.ground in ['Mud', 'Deep Snow']:
            if Roll1D6() <= 3: return False

        move_hexes = []
        for map_hex in battle.maphexes:
            if self.map_hex.rng == map_hex.rng and IsAdjacent(self.map_hex, map_hex):
                move_hexes.append(map_hex)

        # couldn't find a good hex to move to
        if len(move_hexes) == 0:
            return False

        # do the move
        old_x, old_y = self.x, self.y
        self.map_hex = random.choice(move_hexes)

        # show the animation
        self.MoveAnimation(old_x, old_y)

        # apply effects of moving
        self.MoveEffects()

        return True

    # show an animation of the unit moving, also triggers calculation of new character location
    def MoveAnimation(self, old_x, old_y):

        # get the unit's new x and y position
        new_x, new_y = self.GetCharLocation()

        # play movement sound
        if self.unit_class not in ['AT_GUN', 'MG', 'LW']:
            PlaySound('engine_noise')
        elif self.unit_class in ['LW', 'MG']:
            PlaySound('infantry_moving')

        # skip if animations are off
        if not campaign.animations:
            self.x = new_x
            self.y = new_y
            UpdateMapOverlay()
            RenderEncounter()
            return

        # set the animation flag
        self.animating = True

        # do the animation
        line = GetLine(old_x, old_y, new_x, new_y)
        for (x,y) in line:
            self.x = x
            self.y = y
            UpdateMapOverlay()
            RenderEncounter()
            Wait(50)

        self.animating = False
        UpdateMapOverlay()
        RenderEncounter()

    # apply effects of unit movement
    def MoveEffects(self):
        self.moving = True
        self.spotted = False
        self.hidden = False
        self.acquired = 0
        self.acquired_player = 0
        if self.unit_class == 'AC':
            self.spotting_player = False
        self.SetFacing()
        self.SetTerrain()

    # do an attack against friendly infantry
    def AttackInfantry(self):

        x, y = self.x+MAP_CON_X, self.y+MAP_CON_Y

        # if unit is Hidden, can't attack
        if self.hidden: return False

        # if unit is at medium or long range and weather is foggy or falling snow,
        # can't attack
        if self.map_hex.rng > 0 and (campaign.weather.fog or campaign.weather.precip == 'Snow'):
            return False

        # vehicle if unit is not facing player, turn instead
        if self.unit_class not in ['LW', 'MG'] and self.facing != 'Front':
            if self.immobile: return False
            ShowLabel(x, y, self.GetDesc() + ' turns to face you.')
            self.facing = 'Front'
            return True

        ShowLabel(x, y, self.GetDesc() + ' fires at friendly infantry.')
        self.moving = False

        if self.unit_class == 'LW':
            PlaySound('german_rifle_fire')
        elif self.unit_class in ['TANK', 'SPG', 'MG', 'APC', 'AC']:
            PlaySound('german_mg_fire')
        # display firing animation
        MGAnimation(self.x+MAP_CON_X, self.y+MAP_CON_Y,
            MAP_X0 + MAP_CON_X, MAP_Y0 + MAP_CON_Y)

        # reset aquired player as target
        self.acquired_player = 0

        # set flag for spotting
        self.fired = True

        # do roll
        result = Roll1D100()

        # automatic kill
        if result <= 3:
            ShowLabel(self.x+MAP_CON_X, self.y+MAP_CON_Y, self.GetDesc() + ' destroys a friendly infantry squad.')
            battle.inf_lost += 1
            return

        # otherwise, determine tk number
        if self.unit_class in ['TANK', 'SPG']:
            if self.map_hex.rng == 0:
                tk_num = 65    # close range
            elif self.map_hex.rng == 1:
                tk_num = 40    # medium range
            else:
                tk_num = 10    # long range
        elif self.unit_class in ['AC', 'LW']:
            if self.map_hex.rng == 0:
                tk_num = 30
            elif self.map_hex.rng == 1:
                tk_num = 20
            else:
                tk_num = 3
        else:
            # MG / APC
            if self.map_hex.rng == 0:
                tk_num = 55
            elif self.map_hex.rng == 1:
                tk_num = 30
            else:
                tk_num = 3

        # apply smoke modifier
        smoke_factors = GetSmokeFactors(0, 0, self.map_hex.hx, self.map_hex.hy)
        if smoke_factors > 0:
            tk_num = int(ceil(float(tk_num) * float(0.5**smoke_factors)))

        # check roll against tk number
        if result <= tk_num:
            ShowLabel(self.x+MAP_CON_X, self.y+MAP_CON_Y, self.GetDesc() + ' destroys a friendly infantry squad.')
            battle.inf_lost += 1
        else:
            ShowLabel(MAP_X0+MAP_CON_X, MAP_Y0+MAP_CON_Y, 'No effect.')

        return True

    # do an attack against a friendly tank
    def AttackTank(self):

        x, y = self.x+MAP_CON_X, self.y+MAP_CON_Y

        # if unit is Hidden, can't attack
        if self.hidden: return False

        # if unit is at medium or long range and weather is foggy or falling snow,
        # can't attack
        if self.map_hex.rng > 0 and (campaign.weather.fog or campaign.weather.precip == 'Snow'):
            return False

        # only tanks, SPGs, and AT Guns will attack friendly tanks
        if self.unit_class not in ['TANK', 'SPG', 'AT_GUN']:
            return False

        # vehicle if unit is not facing player, turn instead
        if self.facing != 'Front':
            if self.immobile: return False
            ShowLabel(x, y, self.GetDesc() + ' turns to face you.')
            self.facing = 'Front'
            return True

        ShowLabel(x, y, self.GetDesc() + ' fires at a friendly tank.')
        self.moving = False

        # get the main gun type and play firing sound
        gun_type = self.stats['main_gun']
        soundfile = GetFiringSound(gun_type)
        if soundfile is not None:
            PlaySound(soundfile)

        # do firing animation
        MainGunAnimation(self.x + MAP_CON_X, self.y + MAP_CON_Y,
            MAP_X0 + MAP_CON_X, MAP_Y0 + MAP_CON_Y)

        # reset aquired player as target
        self.acquired_player = 0

        # set flag for spotting
        self.fired = True

        # determine tk number
        if gun_type == '50L':
            if self.map_hex.rng == 0:
                tk_num = 15
            elif self.map_hex.rng == 1:
                tk_num = 5
            else:
                tk_num = 1
        elif gun_type == '75L':
            if self.map_hex.rng == 0:
                tk_num = 52
            elif self.map_hex.rng == 1:
                tk_num = 40
            else:
                tk_num = 22
        elif gun_type == '75LL':
            if self.map_hex.rng == 0:
                tk_num = 68
            elif self.map_hex.rng == 1:
                tk_num = 66
            else:
                tk_num = 61
        elif gun_type == '88L':
            if self.map_hex.rng == 0:
                tk_num = 68
            elif self.map_hex.rng == 1:
                tk_num = 63
            else:
                tk_num = 43
        elif gun_type == '88LL':
            if self.map_hex.rng == 0:
                tk_num = 68
            elif self.map_hex.rng == 1:
                tk_num = 66
            else:
                tk_num = 61
        else:
            Message('ERROR: Unrecognized gun type in AttackTank()')
            return

        # apply AT gun rotation modifier
        if self.unit_class == 'AT_GUN':
            if self.facing == 'Side':
                if self.unit_type == '88LL':
                    tk_num -= 10
                else:
                    tk_num -= 20
            elif self.facing == 'Rear':
                if self.unit_type == '88LL':
                    tk_num -= 20
                else:
                    tk_num -= 30
            self.facing = 'Front'

        # apply smoke modifier
        smoke_factors = GetSmokeFactors(0, 0, self.map_hex.hx, self.map_hex.hy)
        if smoke_factors > 0:
            tk_num = int(ceil(float(tk_num) * float(0.5**smoke_factors)))

        # do roll and check against tk number
        result = Roll1D100()

        if result <= tk_num:
            PlaySound('tank_knocked_out')
            ShowLabel(self.x+MAP_CON_X, self.y+MAP_CON_Y, self.GetDesc() + ' destroys a friendly tank.')
            battle.tanks_lost += 1
        else:
            ShowLabel(MAP_X0+MAP_CON_X, MAP_Y0+MAP_CON_Y, 'No effect.')

        # NEW: if unit is unidentified, a crewmember indicates the calibre of gun heard
        if self.hidden or not self.identified:
            CrewTalk('That sounded like a ' + gun_type[:2] + 'mm gun!')

        return True


    # attack the player tank
    def AttackPlayer(self):

        x, y = self.x+MAP_CON_X, self.y+MAP_CON_Y

        # if unit is Hidden, can't attack
        if self.hidden: return False

        # if unit is at medium or long range and weather is foggy or falling snow,
        # can't attack
        if self.map_hex.rng > 0 and (campaign.weather.fog or campaign.weather.precip == 'Snow'):
            return False

        # vehicle if unit is not facing player, turn instead
        if self.unit_class not in ['LW', 'MG'] and self.facing != 'Front':
            if self.immobile: return False
            ShowLabel(x, y, self.GetDesc() + ' turns to face you.')
            self.facing = 'Front'
            return True

        # if LW armed with PF, may do a PF attack
        if self.unit_class == 'LW':
            if self.PFAttack(): return

        ShowLabel(x, y, self.GetDesc() + ' fires at you!')
        self.moving = False

        # flag for type of crew reponse at end
        shot_missed = False
        armour_saved = False

        if self.unit_class in ['TANK', 'SPG', 'AT_GUN']:
            # play firing sound
            soundfile = GetFiringSound(self.stats['main_gun'])
            if soundfile is not None:
                PlaySound(soundfile)
            # do main gun firing animation
            MainGunAnimation(self.x + MAP_CON_X, self.y + MAP_CON_Y,
                MAP_X0 + MAP_CON_X, MAP_Y0 + MAP_CON_Y)

        elif self.unit_class == 'LW':
            PlaySound('german_rifle_fire')
            # display firing animation
            MGAnimation(self.x+MAP_CON_X, self.y+MAP_CON_Y,
                MAP_X0 + MAP_CON_X, MAP_Y0 + MAP_CON_Y)

        elif self.unit_class in ['MG', 'APC', 'AC']:
            PlaySound('german_mg_fire')
            # display firing animation
            MGAnimation(self.x+MAP_CON_X, self.y+MAP_CON_Y,
                MAP_X0 + MAP_CON_X, MAP_Y0 + MAP_CON_Y)

        # set flag for spotting
        self.fired = True

        # if unit is APC, AC, MG, or LW, apply light weapons damage instead
        if self.unit_class not in ['TANK', 'SPG', 'AT_GUN']:
            tank.LWAttack()
            return True

        # calculate modifiers and final DR required
        (base_th, roll_req, drm) = CalcTH(self, tank, False, 'AP')

        # if attacker is AT Gun, turn to face player
        if self.unit_class == 'AT_GUN':
            self.facing = 'Front'

        # if hit not possible
        if roll_req < 2:
            ShowLabel(MAP_X0+MAP_CON_X, MAP_Y0+MAP_CON_Y, 'The attack cannot hit you.')
            return True

        # create roll action to hold details about the action
        roll_action = RollAction()

        # input details
        roll_action.attacker_unit_type = self.unit_type
        # mark if attacker is unspotted or needs to be identified
        if not self.spotted or (self.unit_class in ['TANK', 'SPG', 'AT_GUN'] and not self.identified):
            roll_action.attacker_unidentified = True
        roll_action.attacker = self.GetDesc()
        roll_action.attack_type = self.stats['main_gun'].replace('L', '') + 'mm AP'
        roll_action.target_unit_type = tank.unit_type
        roll_action.target = tank.stats['vehicle_type'] + ' "' + tank.name + '"'
        if self.map_hex.rng == 0:
            roll_action.rng = 'Close'
        elif self.map_hex.rng == 1:
            roll_action.rng = 'Medium'
        else:
            roll_action.rng = 'Long'
        roll_action.score_req = base_th
        roll_action.drm = drm
        roll_action.CalculateTotalDRM()
        roll_action.roll_req = roll_req

        ##### To-hit Roll #####
        d1, d2, roll = Roll2D6()
        roll_action.d1 = d1
        roll_action.d2 = d2
        roll_action.roll = roll

        if roll <= roll_req:

            # determine hit location
            hit_location = GetHitLocation(tank.hull_down)
            if hit_location == 'Miss':
                roll_action.result = 'The shot misses because your tank is hull down.'
            elif hit_location == 'Track':
                roll_action.result = 'Your tank is hit in the track and is immobilized.'
                tank.moving = False
                tank.immobilized = True
                # re-build orders list for Driver to disable movement orders
                GetCrewByPosition('Driver').BuildOrdersList()
            else:
                # hit in turret or hull
                roll_action.result = 'Your tank is hit in the ' + hit_location

                # display to player
                DisplayRoll(roll_action)
                UpdateTankCon()
                RenderEncounter()

                ##### Resolve Hit on Player #####
                # determine side of tank that is hit

                # if hit in turret, facing depends on turret facing
                if hit_location == 'Turret':
                    if tank.turret_facing == self.map_hex.sector:
                        facing = 'Front'
                    elif GetSectorDistance(self.map_hex.sector, tank.turret_facing) == 3:
                        facing = 'Rear'
                    else:
                        facing = 'Side'
                else:
                    if self.map_hex.sector == 4:
                        facing = 'Front'
                    elif self.map_hex.sector == 1:
                        facing = 'Rear'
                    else:
                        facing = 'Side'

                # get To Kill number and update roll action
                (base_tk, roll_req, drm) = CalcTK(self, tank, facing, 'AP', False, False, hit_location)

                # if no chance to knock out, display that instead
                if roll_req < 2:
                    ShowLabel(MAP_X0+MAP_CON_X, MAP_Y0+MAP_CON_Y, 'No chance to destroy.')
                    del roll_action
                    return

                roll_action.hit_location = hit_location
                roll_action.score_req = base_tk
                roll_action.drm = drm
                roll_action.CalculateTotalDRM()
                roll_action.roll_req = roll_req

                ##### To kill Roll #####
                d1, d2, roll = Roll2D6()
                roll_action.d1 = d1
                roll_action.d2 = d2
                roll_action.roll = roll

                if roll < roll_req:
                    roll_action.result = "Your tank's armour is penetrated by the hit!"
                else:
                    roll_action.result = 'Your tank is unharmed.'
                    armour_saved = True
                DisplayRoll(roll_action, tk_roll=True)

                # play armour saved or ap hit sound
                if roll >= roll_req:
                    PlaySound('armour_save')
                else:
                    PlaySound('ap_hit')

                UpdateTankCon()
                RenderEncounter()
                if roll < roll_req:

                    # determine whether it was a critical penetration
                    crit = False
                    if roll == 2 or roll < int(roll_req / 2):
                        crit = True
                    tank.Penetrate(hit_location, self.map_hex.sector, self.stats['main_gun'], critical=crit)
                else:
                    # save vs. stun for crew
                    for crewman in tank.crew:
                        if crewman.StunCheck(10):
                            PopUp(crewman.name + ' is Stunned from the impact!')
                del roll_action
                return True
        else:
            roll_action.result = 'Shot misses!'
            shot_missed = True

        # display to player then delete roll action object
        DisplayRoll(roll_action)
        del roll_action
        UpdateTankCon()
        RenderEncounter()

        if shot_missed:
            PlaySound('main_gun_miss')

            # NEW: if unit is unidentified, a crewmember indicates the calibre of gun heard
            if self.hidden or not self.identified:
                text = self.stats['main_gun']
                CrewTalk('That sounded like a ' + text[:1] + 'mm gun!')

        # possible crew talk
        roll = Roll1D10()
        if armour_saved and roll <= 4:
            CrewTalk(random.choice(CREW_TALK_ARMOUR_SAVED))
        elif shot_missed and roll <= 2:
            CrewTalk(random.choice(CREW_TALK_SHOT_MISSED))

        return True

    # resolve outstanding hits against this unit
    def ResolveHits(self):

        # set flag for infantry/vehicle unit
        if self.unit_class in ['LW', 'MG', 'AT_GUN']:
            vehicle = False
        else:
            vehicle = True

        for gun_hit in self.hit_record:

            # if a previous hit has destroyed us, skip all remaining hit resolution
            if not self.alive: continue

            # WP hits have no effect on vehicles
            if gun_hit.ammo_type == 'WP' and vehicle:
                continue

            text = 'Resolving '
            if gun_hit.critical:
                text += 'critical '
            text += gun_hit.ammo_type + ' hit against ' + self.GetDesc()
            Message(text)

            # resolve WP hit on infantry
            if gun_hit.ammo_type == 'WP':
                self.PinTest()
                if not self.alive:
                    ShowLabel(self.x+MAP_CON_X, self.y+MAP_CON_Y, self.GetDesc() + ' surrenders!')
                elif self.pinned:
                    ShowLabel(self.x+MAP_CON_X, self.y+MAP_CON_Y, self.GetDesc() + ' is pinned!')
                else:
                    ShowLabel(self.x+MAP_CON_X, self.y+MAP_CON_Y, 'WP has no additional effect.')
                continue

            if not vehicle:
                # if ammo was AP type, no effect
                if gun_hit.ammo_type in ['AP', 'HVAP', 'APDS']:
                    ShowLabel(self.x+MAP_CON_X, self.y+MAP_CON_Y, 'AP has no effect against infantry targets.')
                    continue

                # get TK roll info from IFT
                (base_tk, roll_req, drm) = CalcIFT(tank, self, gun_hit.gun_calibre, gun_hit.critical, gun_hit.area_fire)

            # unit is vehicle
            else:
                # determine hit location and check for hull down / immobilized
                hit_location = GetHitLocation((self.terrain == 'Hull Down'))

                if hit_location == 'Miss':
                    PopUp(self.GetDesc() + ' is hulldown and was unharmed by hit.')
                    continue
                elif hit_location == 'Track':
                    PopUp(self.GetDesc() + ' is immobilized.')
                    WriteJournal(self.GetDesc() + ' was immobilized by a ' + gun_hit.ammo_type + ' hit from ' + tank.name)
                    self.immobile = True
                    self.moving = False
                    if self.unit_class == 'APC':
                        if self.full_apc:
                            self.DismountInfantry(under_fire=True)
                    continue

                # get TK roll info
                (base_tk, roll_req, drm) = CalcTK(tank, self, self.facing, gun_hit.ammo_type, gun_hit.critical, gun_hit.area_fire, hit_location)

            # create roll action to hold details about the action
            roll_action = RollAction()

            # input details to roll action object
            roll_action.attacker_unit_type = tank.unit_type
            roll_action.attacker = tank.stats['vehicle_type'] + ' "' + tank.name + '"'
            roll_action.attack_type = gun_hit.gun_calibre + 'mm ' + gun_hit.ammo_type
            # mark if self as target is unspotted or needs to be identified
            if not self.spotted or (self.unit_class in ['TANK', 'SPG', 'AT_GUN'] and not self.identified):
                roll_action.target_unidentified = True
            roll_action.target_unit_type = self.unit_type
            roll_action.target = self.GetDesc()
            if self.map_hex.rng == 0:
                roll_action.rng = 'Close'
            elif self.map_hex.rng == 1:
                roll_action.rng = 'Medium'
            else:
                roll_action.rng = 'Long'
            if vehicle:
                roll_action.hit_location = hit_location
            roll_action.score_req = base_tk
            roll_action.drm = drm
            roll_action.CalculateTotalDRM()
            roll_action.roll_req = roll_req

            # if KO is impossible or auto
            if roll_req <= 2 or roll_req > 12:
                if roll_req <= 2:
                    roll_action.nc = True
                else:
                    roll_action.auto_ko = True
                DisplayRoll(roll_action, tk_roll=True)
                del roll_action
                if roll_req > 12:
                    WriteJournal(self.GetDesc() + ' was destroyed by a ' + gun_hit.ammo_type + ' hit from ' + tank.name)
                    self.RecordKO()
                    self.alive = False
                    if self.unit_class == 'APC':
                        if self.full_apc:
                            self.DismountInfantry(under_fire=True)
                    UpdateMapOverlay()
                else:
                    # play armour save sound if appropriate
                    if gun_hit.ammo_type in ['AP', 'HVAP', 'APDS'] and vehicle:
                        PlaySound('armour_save')
                RenderEncounter()
                continue

            ##### To-Kill Roll #####
            d1, d2, roll = Roll2D6()
            roll_action.d1 = d1
            roll_action.d2 = d2
            roll_action.roll = roll

            # Destroyed
            if roll < roll_req:
                roll_action.result = self.GetDesc() + ' is destroyed!'
                WriteJournal(self.GetDesc() + ' was destroyed by a ' + gun_hit.ammo_type + ' hit from ' + tank.name)
                self.RecordKO()
                self.alive = False
                if self.unit_class == 'APC':
                    if self.full_apc:
                        self.DismountInfantry(under_fire=True)

            # Pinned / Stunned
            elif roll == roll_req:

                # automatic pin for infantry, automatic stun for vehicles
                if not vehicle:
                    self.PinTest(auto=True)
                    if not self.alive:
                        roll_action.result = self.GetDesc() + ' is Broken and destroyed!'
                        WriteJournal(self.GetDesc() + ' was broken and destroyed by a ' + gun_hit.ammo_type + ' hit from ' + tank.name)
                    else:
                        roll_action.result = self.GetDesc() + ' is Pinned.'
                else:
                    # double stun
                    if self.stunned:
                        if not self.MoraleTest(break_test=True):
                            roll_action.result = self.GetDesc() + ' is Stunned again and abandoned!'
                            WriteJournal(self.GetDesc() + ' was Stunned by a ' + gun_hit.ammo_type + ' hit from ' + tank.name + ' and abandoned')
                            self.RecordKO()
                            self.alive = False
                        else:
                            roll_action.result = self.GetDesc() + ' remains Stunned.'
                    else:
                        roll_action.result = self.GetDesc() + ' is Stunned!'
                        self.stunned = True
                        self.moving = False
                        # ACs stop spotting the player tank
                        if self.unit_class == 'AC':
                            if self.spotting_player:
                                self.spotting_player = False

            # did not penetrate; infantry must test to avoid pinning
            else:
                roll_action.result = self.GetDesc() + ' is unharmed'
                if not vehicle:
                    # apply difference in scores as modifier
                    self.PinTest(modifier = roll - roll_req)
                    if self.pinned:
                        roll_action.result += ' but pinned'
                roll_action.result += '.'

            # display results to player then delete attack object
            DisplayRoll(roll_action, tk_roll=True)
            del roll_action

            # play tank knocked out sound if appropriate
            if vehicle and not self.alive:
                PlaySound('tank_knocked_out')

            # play armour save sound if appropriate
            elif vehicle and self.alive and gun_hit.ammo_type in ['AP', 'HVAP', 'APDS']:
                PlaySound('armour_save')

            UpdateMapOverlay()
            RenderEncounter()

        # clear hit record
        self.hit_record = []

    # work out friendly action against this unit
    def FriendlyAction(self, flanking_fire=False, artillery=False, air_strike=False, advance_fire=False):

        # do base dice roll
        d1, d2, roll = Roll2D6()

        # natural 2 always destroys
        if roll == 2:
            if self.unit_class in ['TANK', 'SPG']:
                PlaySound('tank_knocked_out')
            text = self.GetDesc() + ' is destroyed by friendly action!'
            ShowLabel(self.x+MAP_CON_X, self.y+MAP_CON_Y, text)
            self.RecordKO(friendly=True, advance_fire=advance_fire)
            self.alive = False
            UpdateMapOverlay()
            RenderEncounter()
            return True

        # apply modifiers
        mod_roll = roll

        # flanking fire attack from Random Events table
        if flanking_fire:
            mod_roll -= 1

        # artillery attack against infantry unit in woods (air bursts)
        if artillery and self.unit_class in ['LW', 'MG', 'AT_GUN']:
            if self.terrain == 'Woods':
                mod_roll -= 1

        # attack vs. LW or MG if friendly infantry squad have been lost
        if self.unit_class in ['LW', 'MG']:
            if 2 < battle.inf_lost < 4:
                mod_roll += 1
            elif battle.inf_lost >= 4:
                mod_roll += 2

        # attack vs. vehicle if friendly tanks have been lost
        # or air strike modifier
        if self.unit_class in ['TANK', 'SPG', 'APC', 'AC', 'TRUCK']:
            if not air_strike:
                if 1 < battle.tanks_lost < 3:
                    mod_roll += 1
                elif battle.tanks_lost >= 3:
                    mod_roll += 2
            else:
                mod_roll -= 1

        # artillery fire or advancing fire against vehicles, except trucks
        if (artillery or advance_fire) and self.unit_class in ['TANK', 'SPG', 'APC', 'AC']:
            mod_roll += 2

        # advancing fire is less effective, especially at longer ranges
        if advance_fire:
            if self.map_hex.rng == 0:
                mod_roll += 1
            elif self.map_hex.rng == 1:
                mod_roll += 2
            else:
                mod_roll += 4

        # smoke factors in target's zone unless air strike or artillery
        if not air_strike and not artillery:
            total_smoke = 0
            for map_hex in battle.maphexes:
                if self.map_hex.rng == map_hex.rng and self.map_hex.sector == map_hex.sector:
                    total_smoke += map_hex.smoke_factors

            if total_smoke > 0:
                mod_roll += total_smoke

        # air strikes less effective than targeted fire
        if air_strike:
            mod_roll += 2

        # turret radio broken
        if 'Radio Malfunction' in tank.damage_list or 'Radio Broken' in tank.damage_list:
            mod_roll += 2

        # British and Commonwealth forces get a bonus to arty attacks
        if artillery and campaign.player_nation in ['CAN', 'UK']:
            mod_roll -= 2

        # calculate TK number required
        if self.unit_class == 'TRUCK':
            tk_num = 7
        elif self.unit_class == 'APC':
            tk_num = 6
        elif self.unit_class in ['AC', 'LW', 'MG']:
            tk_num = 5
        elif self.unit_class == 'AT_GUN':
            tk_num = 4

        elif self.unit_type in ['Marder II', 'Marder III H']:
            tk_num = 6
        elif self.unit_type in ['PzKw IV H', 'STuG III G']:
            tk_num = 5
        elif self.unit_type in ['PzKw V G', 'JgdPzKw IV', 'JgdPz 38(t)']:
            tk_num = 4
        elif self.unit_type in ['PzKw VI E', 'PzKw VI B']:
            tk_num = 3
        else:
            print 'FriendlyAction() Error: Unrecognized unit type'
            return

        # check modified roll against tk number
        if mod_roll <= tk_num:
            if self.unit_class in ['TANK', 'SPG']:
                PlaySound('tank_knocked_out')
            text = self.GetDesc() + ' is destroyed by friendly action!'
            ShowLabel(self.x+MAP_CON_X, self.y+MAP_CON_Y, text)
            self.RecordKO(friendly=True, advance_fire=advance_fire)
            self.alive = False
            UpdateMapOverlay()
            RenderEncounter()
            return True

        # check original roll with new modifiers for smoke placement
        mod_roll = roll

        if self.unit_class in ['TANK', 'SPG', 'AT_GUN']:
            mod_roll += 1

        if artillery:
            mod_roll += 1

        # air strikes and advance fire pin instead of smoke
        if air_strike or advance_fire:
            if mod_roll >= 11 and self.unit_class in ['LW', 'MG', 'AT_GUN']:
                text = self.GetDesc() + ' is pinned.'
                ShowLabel(self.x+MAP_CON_X, self.y+MAP_CON_Y, text)
                self.pinned = True
                RenderEncounter()
                return True

        # place smoke if not already there
        else:

            # movable infantry units less likely to be smoked
            if self.unit_class in ['LW', 'MG']:
                mod_roll -= 2

            if mod_roll >= 11 and self.map_hex.smoke_factors == 0:
                text = self.GetDesc() + ' is hit with smoke from friendly units.'
                ShowLabel(self.x+MAP_CON_X, self.y+MAP_CON_Y, text)
                PlaceSmoke(self.map_hex, 1)
                RenderEncounter()
                return True

        # no effect
        return False

    # dismount infantry from an APC; if under_fire, new unit starts pinned
    def DismountInfantry(self, under_fire=False):
        self.full_apc = False
        ShowLabel(self.x+MAP_CON_X, self.y+MAP_CON_Y, self.GetDesc() + ' dismounts infantry!')
        if Roll1D6() <= 4:
            new_unit = SpawnEnemy('LW', self.map_hex)
        else:
            new_unit = SpawnEnemy('MG', self.map_hex)
        if under_fire:
            # pin the new infantry unit
            new_unit.PinTest(auto=True)

    # find a suitable character location relative to hex centre to draw unit
    def GetCharLocation(self):

        # don't bother with inactive units
        if not self.alive: return (-1, -1)

        # try to find a location within the hex that is not occupied by another enemy unit
        for tries in range(100):
            y_mod = libtcod.random_get_int(0, -2, 2)
            if abs(y_mod) == 2:
                x_limit = 2
            elif abs(y_mod) == 1:
                x_limit = 3
            else:
                x_limit = 4
            x_mod = libtcod.random_get_int(0, -x_limit, x_limit)

            x = self.map_hex.x + x_mod
            y = self.map_hex.y + y_mod

            matched = False
            for unit in battle.enemy_units:
                if unit.y == y and (abs(unit.x + x) <= 2):
                    matched = True
                    break

            # if this spot already occupied, continue with next try
            if matched:
                continue

            return (x, y)

    # do an action for this unit
    def DoAction(self, ambush=False):

        # if pinned or stunned, unit can only recover or do nothing this turn
        if self.pinned:
            if self.MoraleTest():
                text = ' recovers from being Pinned.'
                self.pinned = False
                if self.morale > 2:
                    self.morale -= 1
            else:
                text = ' remains Pinned and does nothing.'
            ShowLabel(self.x+MAP_CON_X, self.y+MAP_CON_Y, self.GetDesc() + text)
            return

        elif self.stunned:
            if self.MoraleTest():
                text = ' recovers from being Stunned.'
                self.stunned = False
                if self.morale > 2:
                    self.morale -= 1
            else:
                text = ' remains Stunned and does nothing.'
            ShowLabel(self.x+MAP_CON_X, self.y+MAP_CON_Y, self.GetDesc() + text)
            return

        # build odds table for this unit:
        # do nothing, move closer, move laterally, move away, attack infantry,
        #  attack friendly tank (player if shot at), attack player tank, attack lead tank
        if self.unit_class in ['TANK', 'SPG']:
            if campaign.scen_type == 'Advance':
                ranges = [10,30,40,60,65,80,85]
            elif campaign.scen_type == 'Battle':
                ranges = [10,20,25,35,40,85,90]
            else:
                ranges = [10,50,60,70,75,95,100]

        # APCs will not normally choose to attack armoured battlegroups. Their main
        # mission is to drop their crew if possible and then retreat to a safe distance
        elif self.unit_class == 'APC':

            # chance to dismount infantry
            if self.full_apc and self.map_hex.rng <= 1:
                if Roll1D6() <= 4:
                    self.moving = False
                    self.DismountInfantry()
                    return

            if campaign.scen_type == 'Advance':
                ranges = [10,20,30,40,60,65,80]
            elif campaign.scen_type == 'Battle':
                ranges = [10,15,20,25,35,40,85]
            else:
                ranges = [10,40,50,60,70,75,80]

        # Trucks move around a lot but don't do very much
        elif self.unit_class == 'TRUCK':
            ranges = [30,40,75,110,0,0,0]

        # Armoured Cars can attack friendly infantry, and can spot the player
        #  tank to help other enemy attacks
        elif self.unit_class == 'AC':

            # if AC is already spotting the player, less chance of acting
            if self.spotting_player:
                if Roll1D6() > 1:
                    ShowLabel(self.x+MAP_CON_X, self.y+MAP_CON_Y, self.GetDesc() + ' continues spotting your tank.')
                    self.moving = False
                    return
                ShowLabel(self.x+MAP_CON_X, self.y+MAP_CON_Y, self.GetDesc() + ' lost sight of your tank!')
                self.spotting_player = False
                self.moving = False
                return

            ranges = [15,25,50,60,75,85,100]

        # Anti-tank Gun
        elif self.unit_class == 'AT_GUN':
            if campaign.scen_type == 'Advance':
                ranges = [30,0,0,0,0,65,70]
            elif campaign.scen_type == 'Battle':
                ranges = [30,0,0,0,0,80,90]

        # Light Weapons or Machine Gun Infantry Squad
        elif self.unit_class in ['LW', 'MG']:
            if campaign.scen_type in ['Advance', 'Battle']:
                ranges = [10,20,40,60,95,0,0]
            else:
                ranges = [10,40,60,70,95,0,100]

        ###################################################################
        #   try to roll an action result that is possible for the unit    #
        ###################################################################
        for i in range(300):

            # do action roll and apply ambush modifier if any
            result = Roll1D100()
            if ambush:
                result += 10
                if self.unit_class in ['LW', 'MG', 'AT_GUN']: result += 10

            # check final result against odds table

            # do nothing
            if result <= ranges[0]:
                ShowLabel(self.x+MAP_CON_X, self.y+MAP_CON_Y, self.GetDesc() + " doesn't appear to do anything.")
                self.moving = False
                return

            # move closer
            elif result <= ranges[1]:
                if self.DistMove(-1):
                    ShowLabel(self.x+MAP_CON_X, self.y+MAP_CON_Y, self.GetDesc() + ' moves towards you.')
                    return

            # move laterally
            elif result <= ranges[2]:
                if self.LateralMove():
                    ShowLabel(self.x+MAP_CON_X, self.y+MAP_CON_Y, self.GetDesc() + ' shifts its position.')
                    return

            # move further away
            elif result <= ranges[3]:
                if self.DistMove(1):
                    ShowLabel(self.x+MAP_CON_X, self.y+MAP_CON_Y, self.GetDesc() + ' moves further away.')
                    return

            # attack friendly infantry
            elif result <= ranges[4]:
                if self.AttackInfantry(): return

            # fire at friendly tank, perhaps fire at player or move
            elif result <= ranges[5]:

                # if unit was fired upon last turn, might act differently
                if self.shot_at:
                    if self.facing == 'Front':
                        if self.AttackPlayer(): return
                    else:
                        if self.DistMove(1): return

                # attack friendly tank
                if self.AttackTank(): return

            # fire - your tank
            elif result <= ranges[6]:
                if self.AttackPlayer(): return

            # fire - lead tank or perhaps player tank
            else:

                # special - some lead tank shots can be redirected to a firefly tank instead
                if tank.stats['vehicle_type'] == 'Sherman VC':
                    if Roll1D6() <= 2:
                        if self.AttackPlayer(): return
                if tank.lead_tank:
                    if self.AttackPlayer(): return
                else:
                    if self.AttackTank(): return


# holds information about a modified roll and its outcomes
class RollAction():
    def __init__(self):
        self.attacker_unit_type = ''    # unit type of attacker
        self.attacker = ''        # description of attacking unit
        self.attack_type = ''        # description of type of attack (HE, AP, etc.)
        self.target_unit_type = ''    # unit type of target
        self.target = ''        # description of target unit

        self.attacker_unidentified = False    # attacking unit is unknown or unidentified
        self.target_unidentified = False    # target unit is unidentified

        self.rng = ''            # range to target
        self.hit_location = ''        # hit location if any
        self.score_req = 0        # base score required on 2D6
        self.auto_ko = False        # target is automatically knocked out
        self.nc = False            # target has no chance of being knocked out

        self.drm = []            # list of dice roll modifiers
        self.total_drm = 0        # sum of all drm

        self.roll_req = 0        # final roll required
        self.roll = 0            # actual roll result
        self.d1 = 0            # d1 result
        self.d2 = 0            # d2 result
        self.result = ''        # description of roll result
        self.rof_result = ''        # rate of fire result if any

    # add up all dice roll modifiers
    def CalculateTotalDRM(self):
        self.total_drm = 0
        for (text, mod) in self.drm:
            self.total_drm += mod


##########################################################################################
#                                     General Functions                                  #
##########################################################################################

# return hours and minutes between two given times
def GetTimeUntil(h1, m1, h2, m2):
    hours = h2 - h1
    if m1 > m2:
        hours -= 1
        m2 += 60
    return (hours, m2-m1)


# add a line to the campaign journal
def WriteJournal(text):
    campaign.campaign_journal.append(text)


# output the completed campaign journal to a text file
def RecordJournal():

    # add final crew reports
    for crewman in tank.crew:
        lines = crewman.GenerateReport()
        for line in lines:
            WriteJournal(line)

    filename = 'Armoured_Commander_Journal_' + datetime.now().strftime("%H_%M_%d-%m-%Y") + '.txt'
    with open(filename, 'a') as f:
        for line in campaign.campaign_journal:
            f.write(line + '\n')


# returns the crew member in the given tank position
def GetCrewByPosition(position):
    for crewman in tank.crew:
        if crewman.position == position:
            return crewman
    return None


# get the required number of exp to be at this level
def GetExpReq(level):
    x = (level-1) * BASE_EXP_REQ
    if level > 2:
        for l in range(3, level+1):
            x += LVL_INFLATION * (l-2)
    return x


# display a window of help text. if help text is disabled in campaign settings, or we have
#  already shown this text before, skip it
def TutorialMessage(key):
    if campaign is not None:
        if not campaign.tutorial_message: return

    save = shelve.open('bones')
    bones = save['bones']

    # check to see if bones file already has key
    if bones.tutorial_message_flags.has_key(key):
        # key is already set to true
        if bones.tutorial_message_flags[key]:
            save.close()
            return

    # mark that this text has been displayed in the bones file
    # will also add the key if bones file did not already have it
    bones.tutorial_message_flags[key] = True
    save['bones'] = bones
    save.close

    # display the text
    for w in range(3, MENU_CON_WIDTH, 6):
        h = int(w/3) - 3
        if h < 3: h = 3
        libtcod.console_rect(0, SCREEN_XM-int(w/2), SCREEN_YM-int(h/2), w, h, False,
            flag=libtcod.BKGND_SET)
        libtcod.console_print_frame(0, SCREEN_XM-int(w/2), SCREEN_YM-int(h/2), w, h,
            clear=True, flag=libtcod.BKGND_DEFAULT, fmt=0)
        libtcod.console_flush()

    libtcod.console_clear(menu_con)
    libtcod.console_set_alignment(menu_con, libtcod.LEFT)
    libtcod.console_print_frame(menu_con, 0, 0, MENU_CON_WIDTH, MENU_CON_HEIGHT,
        clear=False, flag=libtcod.BKGND_DEFAULT, fmt=0)

    libtcod.console_set_default_foreground(menu_con, MENU_TITLE_COLOR)
    libtcod.console_print_ex(menu_con, MENU_CON_XM, 1,
        libtcod.BKGND_NONE, libtcod.CENTER, 'Tutorial Message')
    libtcod.console_set_default_foreground(menu_con, libtcod.white)

    lines = wrap(TUTORIAL_TEXT[key], 60, subsequent_indent = ' ')
    y = int(MENU_CON_HEIGHT / 2) - int(len(lines)/2)
    for line in lines:
        libtcod.console_print(menu_con, 40, y, line)
        y += 1

    libtcod.console_print_ex(menu_con, MENU_CON_XM, MENU_CON_HEIGHT-2, libtcod.BKGND_NONE,
        libtcod.CENTER, '[%cEnter%c] to Continue'%HIGHLIGHT)

    libtcod.console_blit(menu_con, 0, 0, MENU_CON_WIDTH, MENU_CON_HEIGHT, 0, MENU_CON_X, MENU_CON_Y)
    libtcod.console_flush()

    WaitForEnter()

    # re-blit original display console to screen
    libtcod.console_blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)
    libtcod.console_flush()


# display help interface
def ShowHelp():
    # select the first help dictionary item that starts with this character
    # don't change selection if no entry with this character
    def GetEntry(key_code):
        for (topic, text) in help_list:
            # if lower or upper case match
            if topic[0] == chr(key_code) or topic[0] == chr(key_code - 32):
                return (topic, text)
        return None

    # sort the list of help terms alphabetically by keyword
    help_list = sorted(HELP_TEXT, key=lambda tup: tup[0])

    # select first entry by default
    selected = help_list[0]

    x = 30

    # darken screen
    libtcod.console_clear(con)
    libtcod.console_blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0,
        0.0, 0.7)

    exit_view = False
    while not exit_view:

        # generate and display menu
        libtcod.console_clear(menu_con)
        libtcod.console_set_alignment(menu_con, libtcod.LEFT)
        libtcod.console_print_frame(menu_con, 0, 0, MENU_CON_WIDTH, MENU_CON_HEIGHT,
            clear=False, flag=libtcod.BKGND_DEFAULT, fmt=0)

        libtcod.console_set_default_foreground(menu_con, MENU_TITLE_COLOR)
        libtcod.console_print_ex(menu_con, MENU_CON_XM, 1,
            libtcod.BKGND_NONE, libtcod.CENTER, 'Help Topics')
        libtcod.console_set_default_foreground(menu_con, libtcod.white)

        libtcod.console_print_ex(menu_con, MENU_CON_XM, 2, libtcod.BKGND_NONE, libtcod.CENTER, 'Type a letter to jump to its entry, arrow keys to scroll')

        libtcod.console_print_ex(menu_con, MENU_CON_XM, MENU_CON_HEIGHT-2,
            libtcod.BKGND_NONE, libtcod.CENTER, '[%cESC%c] Return'%HIGHLIGHT)

        libtcod.console_hline(menu_con, 1, 3, MENU_CON_WIDTH-2, flag=libtcod.BKGND_DEFAULT)
        libtcod.console_hline(menu_con, 1, MENU_CON_HEIGHT-3, MENU_CON_WIDTH-2, flag=libtcod.BKGND_DEFAULT)
        libtcod.console_vline(menu_con, x, 4, MENU_CON_HEIGHT-7, flag=libtcod.BKGND_DEFAULT)


        # display list of help topics, with selected one at yc
        n = 0
        s = help_list.index(selected)
        yc = int(MENU_CON_HEIGHT/2)
        for (topic, text) in help_list:
            y = yc - (s-n)
            n += 1
            if y < 6 or y > MENU_CON_HEIGHT-9:
                continue
            if (topic, text) == selected:
                libtcod.console_set_default_background(menu_con, SELECTED_COLOR)
                libtcod.console_rect(menu_con, 2, y, x-4, 1, False, flag=libtcod.BKGND_SET)
                libtcod.console_set_default_background(menu_con, libtcod.black)
            libtcod.console_print(menu_con, 2, y, topic)

        # display explanational text of selected item, double spaced
        (topic, text) = selected

        lines = wrap(text, MENU_CON_WIDTH-50-x, subsequent_indent = ' ')
        y = yc - int(len(lines)/2)
        for line in lines:
            libtcod.console_print(menu_con, x+4, y, line)
            y += 1

        libtcod.console_blit(menu_con, 0, 0, MENU_CON_WIDTH, MENU_CON_HEIGHT, 0, MENU_CON_X, MENU_CON_Y)
        libtcod.console_flush()

        refresh = False
        while not refresh:

            # get input from user
            libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS|libtcod.EVENT_MOUSE, key, mouse)

            # exit right away
            if libtcod.console_is_window_closed(): sys.exit()

            if key.vk == libtcod.KEY_ESCAPE:
                exit_view = True
                break

            elif key.vk == libtcod.KEY_UP or key.vk == libtcod.KEY_DOWN:

                n = help_list.index(selected)
                if key.vk == libtcod.KEY_UP:
                    if n > 0:
                        selected = help_list[n-1]
                        refresh = True
                else:
                    if n < len(help_list)-1:
                        selected = help_list[n+1]
                        refresh = True

            # lowercase alphabetical character
            if 92 <= key.c <= 122:
                # pass code to function
                result = GetEntry(key.c)
                if result is not None:
                    selected = result
                    refresh = True

            libtcod.console_flush()

    # re-draw screen if needed
    if campaign.day_in_progress:
        if battle is None:
            RenderCampaign()
        else:
            RenderEncounter()


# display player tank info; if select_tank is True, we can scroll through all available
# tank models and choose one
def ShowTankInfo(select_tank = False):

    # check list of permitted player vehicle types, and only select those that are
    # available in the current calendar month
    if select_tank:
        tank_list = []
        for vehicle_name in campaign.player_veh_list:
            if campaign.GetRF(vehicle_name) > 0:
                tank_list.append(vehicle_name)
        selected_tank = tank_list[0]

    # darken screen
    libtcod.console_clear(con)
    libtcod.console_blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0,
        0.0, 0.7)

    exit_menu = False
    while not exit_menu:

        # generate and display menu
        libtcod.console_clear(menu_con)
        libtcod.console_print_frame(menu_con, 0, 0, MENU_CON_WIDTH, MENU_CON_HEIGHT,
            clear=False, flag=libtcod.BKGND_DEFAULT, fmt=0)

        libtcod.console_set_default_foreground(menu_con, MENU_TITLE_COLOR)

        if select_tank:
            text = 'Select a Tank Model'
        else:
            text = 'Player Tank Info'

        libtcod.console_print_ex(menu_con, MENU_CON_XM, 2,
            libtcod.BKGND_NONE, libtcod.CENTER, text)
        libtcod.console_set_default_foreground(menu_con, libtcod.white)

        # display tank info
        if select_tank:
            show_tank = selected_tank
        else:
            show_tank = tank.unit_type
        ShowVehicleTypeInfo(show_tank, menu_con, 34, 8)

        # display possible actions
        if select_tank:
            text = '[%cA/D/Left/Right%c] Scroll '%HIGHLIGHT
            text += '[%cEnter%c] Select Tank'%HIGHLIGHT
        else:
            text = '[%cESC%c] Return'%HIGHLIGHT
        libtcod.console_print_ex(menu_con, MENU_CON_XM, MENU_CON_HEIGHT-2,
            libtcod.BKGND_NONE, libtcod.CENTER, text)

        libtcod.console_blit(menu_con, 0, 0, MENU_CON_WIDTH, MENU_CON_HEIGHT, 0, MENU_CON_X, MENU_CON_Y)
        libtcod.console_flush()

        refresh = False
        while not refresh:
            # get input from user
            libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS|libtcod.EVENT_MOUSE, key, mouse)

            if key.vk == libtcod.KEY_ESCAPE and not select_tank:
                exit_menu = True
                break

            elif key.vk == libtcod.KEY_ENTER and select_tank:
                exit_menu = True
                break

            # exit right away
            if libtcod.console_is_window_closed():
                sys.exit()

            # input for selecting a tank model
            if select_tank:

                # get pressed key
                key_char = chr(key.c)


                if key_char in ['a', 'A'] or key.vk == libtcod.KEY_LEFT:
                    i = tank_list.index(selected_tank)
                    if i > 0:
                        selected_tank = tank_list[i-1]
                    else:
                        selected_tank = tank_list[-1]
                    refresh = True

                elif key_char in ['d', 'D'] or key.vk == libtcod.KEY_RIGHT:
                    i = tank_list.index(selected_tank)
                    if i < len(tank_list)-1:
                        selected_tank = tank_list[i+1]
                    else:
                        selected_tank = tank_list[0]
                    refresh = True

            libtcod.console_flush()

    # re-draw screen if needed
    if campaign.day_in_progress:
        if battle is None:
            RenderCampaign()
        else:
            RenderEncounter()

    # return tank selection if we're doing that
    if select_tank:
        return selected_tank


# display crew info and allow player to select crew to view/add/upgrade skills
def ShowCrewInfo():

    # darken screen
    libtcod.console_clear(con)
    libtcod.console_blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0,
        0.0, 0.7)

    # select first crew member by default
    selected_crew = tank.crew[0]

    exit_menu = False
    while not exit_menu:

        # clear console
        libtcod.console_set_default_background(menu_con, libtcod.black)
        libtcod.console_set_default_foreground(menu_con, libtcod.white)
        libtcod.console_clear(menu_con)

        # display frame, title, and commands
        libtcod.console_print_frame(menu_con, 0, 0, MENU_CON_WIDTH-1, MENU_CON_HEIGHT-1,
            clear=False, flag=libtcod.BKGND_DEFAULT, fmt=0)

        libtcod.console_set_default_foreground(menu_con, MENU_TITLE_COLOR)
        libtcod.console_print_ex(menu_con, MENU_CON_XM, 2,
            libtcod.BKGND_NONE, libtcod.CENTER, 'Tank Crew Info')

        libtcod.console_set_default_foreground(menu_con, libtcod.white)
        libtcod.console_print_ex(menu_con, MENU_CON_XM, MENU_CON_HEIGHT-7,
            libtcod.BKGND_NONE, libtcod.CENTER,
            '[%cA/D/Left/Right%c] Change Crew Selection'%HIGHLIGHT)
        libtcod.console_print_ex(menu_con, MENU_CON_XM, MENU_CON_HEIGHT-6,
            libtcod.BKGND_NONE, libtcod.CENTER,
            '[%cEnter%c] View/Add/Upgrade Skills'%HIGHLIGHT)
        libtcod.console_print_ex(menu_con, MENU_CON_XM, MENU_CON_HEIGHT-5,
            libtcod.BKGND_NONE, libtcod.CENTER,
            'Change [%cN%c]ame'%HIGHLIGHT)
        libtcod.console_print_ex(menu_con, MENU_CON_XM, MENU_CON_HEIGHT-4,
            libtcod.BKGND_NONE, libtcod.CENTER,
            '[%cK%c] Set/Reset Nickname'%HIGHLIGHT)
        libtcod.console_print_ex(menu_con, MENU_CON_XM, MENU_CON_HEIGHT-3,
            libtcod.BKGND_NONE, libtcod.CENTER,
            '[%cESC%c] Return'%HIGHLIGHT)

        # display crew info
        libtcod.console_set_alignment(menu_con, libtcod.LEFT)
        x = 2
        for crew_member in tank.crew:
            highlight=False
            if selected_crew.position == crew_member.position:
                highlight=True
            crew_member.DisplayCrewInfo(menu_con, x, 4, highlight)
            x += 27

        libtcod.console_blit(menu_con, 0, 0, MENU_CON_WIDTH, MENU_CON_HEIGHT, 0, MENU_CON_X, MENU_CON_Y)
        libtcod.console_flush()

        refresh = False
        while not refresh:

            libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS|libtcod.EVENT_MOUSE, key, mouse)

            # exit right away
            if libtcod.console_is_window_closed():
                sys.exit()

            # exit view
            if key.vk == libtcod.KEY_ESCAPE:
                exit_menu = True
                break

            elif key.vk == libtcod.KEY_ENTER:
                ShowSkills(selected_crew)
                refresh = True

            key_char = chr(key.c)

            if key_char in ['d', 'D'] or key.vk == libtcod.KEY_RIGHT:
                selected_crew = selected_crew.next
                refresh = True

            elif key_char in ['a', 'A'] or key.vk == libtcod.KEY_LEFT:
                selected_crew = selected_crew.prev
                refresh = True

            elif key_char in ['k', 'K']:
                libtcod.console_clear(menu_con)
                libtcod.console_print_frame(menu_con, 0, 0, MENU_CON_WIDTH, MENU_CON_HEIGHT,
                    clear=False, flag=libtcod.BKGND_DEFAULT, fmt=0)
                libtcod.console_blit(menu_con, 0, 0, MENU_CON_WIDTH, MENU_CON_HEIGHT, con, MENU_CON_X, MENU_CON_Y)

                text = 'Enter new nickname for ' + selected_crew.name
                selected_crew.nickname = GetInput(0, text, 25, NICKNAME_MAX_LEN)
                refresh = True

            elif key_char in ['n', 'N']:

                libtcod.console_clear(menu_con)
                libtcod.console_print_frame(menu_con, 0, 0, MENU_CON_WIDTH, MENU_CON_HEIGHT,
                    clear=False, flag=libtcod.BKGND_DEFAULT, fmt=0)
                libtcod.console_blit(menu_con, 0, 0, MENU_CON_WIDTH, MENU_CON_HEIGHT, con, MENU_CON_X, MENU_CON_Y)

                text = 'Enter new name for ' + selected_crew.name
                selected_crew.name = GetInput(0, text, 25, NAME_MAX_LEN, get_name=True)
                refresh = True


            libtcod.console_flush()

    # re-draw screen if needed
    if campaign.day_in_progress:
        if battle is None:
            RenderCampaign()
        else:
            RenderEncounter()


# allow player to view skills and spend skill points for a crew member
def ShowSkills(crew_member):

    if not crew_member.alive: return

    # select first skill as default
    selected_skill = 0

    exit_menu = False
    while not exit_menu:

        # build a list of possible skills for this crewman
        # if crewman already has a level in this skill, record it, otherwise record as 0
        skill_list = []
        for skill in SKILLS:
            if len(skill.restrictions) > 0:
                if crew_member.position not in skill.restrictions:
                    continue

            # only allow stabilizer skill to US forces
            if skill.name == 'Gyrostabilizer' and campaign.player_nation != 'USA':
                continue

            level = 0

            for crew_skill in crew_member.skills:
                if crew_skill.name == skill.name:
                    level = crew_skill.level
                    break

            skill_list.append((skill, level))

        # clear console
        libtcod.console_set_default_background(menu_con, libtcod.black)
        libtcod.console_set_default_foreground(menu_con, libtcod.white)
        libtcod.console_clear(menu_con)

        # display frame, title, and commands
        libtcod.console_print_frame(menu_con, 0, 0, MENU_CON_WIDTH-1, MENU_CON_HEIGHT-1,
            clear=False, flag=libtcod.BKGND_DEFAULT, fmt=0)

        libtcod.console_set_default_foreground(menu_con, MENU_TITLE_COLOR)
        libtcod.console_print_ex(menu_con, MENU_CON_XM, 2,
            libtcod.BKGND_NONE, libtcod.CENTER, 'Crew Skills')

        libtcod.console_set_default_foreground(menu_con, libtcod.white)
        libtcod.console_print_ex(menu_con, MENU_CON_XM, MENU_CON_HEIGHT-5,
            libtcod.BKGND_NONE, libtcod.CENTER,
            '[%cW/S/Up/Down%c] Change Skill Selection'%HIGHLIGHT)
        libtcod.console_print_ex(menu_con, MENU_CON_XM, MENU_CON_HEIGHT-4,
            libtcod.BKGND_NONE, libtcod.CENTER,
            '[%cEnter%c] Add/Upgrade Skill'%HIGHLIGHT)
        libtcod.console_print_ex(menu_con, MENU_CON_XM, MENU_CON_HEIGHT-3,
            libtcod.BKGND_NONE, libtcod.CENTER,
            '[%cESC%c] Return/Continue'%HIGHLIGHT)

        # display crew info
        crew_member.DisplayCrewInfo(menu_con, 29, 4, False)

        # draw selected skill info box
        libtcod.console_set_default_foreground(menu_con, libtcod.light_grey)
        libtcod.console_print_frame(menu_con, 83, 4, 40, 30,
            clear=False, flag=libtcod.BKGND_DEFAULT, fmt=0)
        libtcod.console_print(menu_con, 86, 9, 'Description')
        libtcod.console_print(menu_con, 86, 25, 'Activation Levels')
        libtcod.console_set_default_foreground(menu_con, libtcod.white)

        # now display list of all possible skills, highlighting ones the crew
        # member already has at least one level of
        # also display detailed info about selected skill
        libtcod.console_set_default_foreground(menu_con, libtcod.light_grey)
        libtcod.console_print_frame(menu_con, 56, 4, 27, 30,
            clear=False, flag=libtcod.BKGND_DEFAULT, fmt=0)
        libtcod.console_print(menu_con, 59, 5, 'Skills')
        libtcod.console_set_default_foreground(menu_con, libtcod.white)

        y = 7
        n = 0
        for (skill, level) in skill_list:

            if n == selected_skill:
                libtcod.console_set_default_background(menu_con, libtcod.darker_grey)
                libtcod.console_rect(menu_con, 57, y, 25, 1, False, flag=libtcod.BKGND_SET)
                libtcod.console_set_default_background(menu_con, libtcod.black)

                # description of selected skill
                libtcod.console_set_default_foreground(menu_con, libtcod.white)

                lines = wrap(skill.desc, 30, subsequent_indent = ' ')
                y2 = 11
                for line in lines:
                    libtcod.console_print(menu_con, 86, y2, line)
                    y2 += 1

                # activation levels
                if skill.levels[0] == 100:
                    libtcod.console_print(menu_con, 86, 27, 'Always active')
                else:
                    x2 = 86
                    for skill_level in skill.levels:
                        # crew has this activation level or greater
                        if skill_level <= level:
                            libtcod.console_set_default_foreground(menu_con, libtcod.light_blue)
                        else:
                            libtcod.console_set_default_foreground(menu_con, libtcod.white)
                        libtcod.console_print(menu_con, x2, 27, str(skill_level)+'%%')
                        x2 += len(str(skill_level)) + 2

            # gyro skill not available yet
            if skill.name == 'Gyrostabilizer' and not campaign.gyro_skill_avail:
                libtcod.console_set_default_foreground(menu_con, GREYED_COLOR)
            elif level > 0:
                libtcod.console_set_default_foreground(menu_con, libtcod.light_blue)
            else:
                libtcod.console_set_default_foreground(menu_con, libtcod.white)

            libtcod.console_print(menu_con, 58, y, skill.name)
            y += 1
            n += 1

        libtcod.console_blit(menu_con, 0, 0, MENU_CON_WIDTH, MENU_CON_HEIGHT, 0, MENU_CON_X, MENU_CON_Y)
        libtcod.console_flush()

        refresh = False
        while not refresh:

            libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS|libtcod.EVENT_MOUSE, key, mouse)

            # exit right away
            if libtcod.console_is_window_closed(): sys.exit()

            # exit view
            if key.vk == libtcod.KEY_ESCAPE:
                exit_menu = True
                break

            key_char = chr(key.c)

            # skill selection up
            if key.vk == libtcod.KEY_UP or key_char in ['w', 'W']:
                if selected_skill == 0:
                    selected_skill = len(skill_list)-1
                else:
                    selected_skill -= 1
                refresh = True

            # skill selection down
            elif key.vk == libtcod.KEY_DOWN or key_char in ['s', 'S']:
                if selected_skill == len(skill_list)-1:
                    selected_skill = 0
                else:
                    selected_skill += 1
                refresh = True

            # add / upgrade skill
            elif key.vk == libtcod.KEY_ENTER:

                # needs to be alive, active, and have at least one skill point
                if not crew_member.NoActions() and crew_member.skill_pts > 0:

                    n = 0
                    for (skill, level) in skill_list:
                        if n == selected_skill:

                            # gyro skill not available yet
                            if skill.name == 'Gyrostabilizer' and not campaign.gyro_skill_avail:
                                break

                            # check to see if we can add / upgrade this skill
                            # add new skill
                            if level == 0:
                                text = 'Spend a skill point to add skill "' + skill.name + '"'
                                if PopUp(text, confirm=True):
                                    crew_member.skill_pts -= 1
                                    crew_member.skills.append(SkillRecord(skill.name, skill.levels[0]))
                                    WriteJournal(crew_member.name + ' added a new skill: ' + skill.name + ', now at '+ str(skill.levels[0]) + '%% activation')
                                    PlaySound('new_skill')

                            # upgrade skill
                            else:
                                for skill_level in skill.levels:
                                    # we're not at this level yet, so we can upgrade
                                    if level < skill_level:

                                        text = 'Spend a skill point to upgrade skill "' + skill.name + '"'
                                        if PopUp(text, confirm=True):
                                            crew_member.skill_pts -= 1
                                            crew_member.UpgradeSkill(skill.name, skill_level)
                                            WriteJournal(crew_member.name + ' upgraded a skill: ' + skill.name + ', now at ' + str(skill_level) + '%% activation')
                                            PlaySound('new_skill')

                                        # we found the right skill level
                                        break

                            # we found the selected skill, so we can break out of for loop
                            break

                        n += 1

                    refresh = True

            libtcod.console_flush()


# display campaign stats, can be accessed during the campaign also shown at the end of a campaign
def ShowCampaignStats():
    # darken screen
    libtcod.console_clear(con)
    libtcod.console_blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0,
        0.0, 0.7)

    exit_menu = False
    while not exit_menu:

        # generate and display menu
        libtcod.console_clear(menu_con)
        libtcod.console_set_alignment(menu_con, libtcod.LEFT)
        libtcod.console_print_frame(menu_con, 0, 0, MENU_CON_WIDTH, MENU_CON_HEIGHT,
            clear=False, flag=libtcod.BKGND_DEFAULT, fmt=0)

        libtcod.console_set_default_foreground(menu_con, MENU_TITLE_COLOR)
        libtcod.console_print_ex(menu_con, MENU_CON_XM, 2,
            libtcod.BKGND_NONE, libtcod.CENTER, 'Campaign Stats')
        libtcod.console_set_default_foreground(menu_con, libtcod.white)

        # display current day of campaign calendar
        libtcod.console_set_default_background(menu_con, ROW_COLOR)
        libtcod.console_rect(menu_con, MENU_CON_XM-20, 5, 40, 1, False, flag=libtcod.BKGND_SET)
        if not campaign.stats.has_key('Days of Combat'):
            d1 = '0'
        else:
            d1 = campaign.stats['Days of Combat']
        d2 = len(campaign.days) - campaign.start_date
        text = 'Campaign Day ' + str(d1) + '/' + str(d2)
        libtcod.console_print_ex(menu_con, MENU_CON_XM, 5, libtcod.BKGND_NONE,
            libtcod.CENTER, text)
        w = int(ceil(float(d1) / float(d2) * 40.0))
        libtcod.console_set_default_background(menu_con, HIGHLIGHT_COLOR)
        libtcod.console_rect(menu_con, MENU_CON_XM-20, 5, w, 1, False, flag=libtcod.BKGND_SET)
        libtcod.console_set_default_background(menu_con, libtcod.black)

        # display current VP total
        text = 'Total Victory Points: ' + str(campaign.vp + campaign.day_vp)
        libtcod.console_print(menu_con, 53, 7, text)

        # display rest of campaign stats
        y = 9
        for stat_name in C_STATS:
            text = stat_name + ': '
            if not campaign.stats.has_key(stat_name):
                text += '0'
            else:
                text += str(campaign.stats[stat_name])
            libtcod.console_print(menu_con, 53, y, text)
            y += 1

        libtcod.console_print_ex(menu_con, MENU_CON_XM, MENU_CON_HEIGHT-4,
            libtcod.BKGND_NONE, libtcod.CENTER,
            'Display Campaign [%cJ%c]ournal'%HIGHLIGHT)

        libtcod.console_print_ex(menu_con, MENU_CON_XM, MENU_CON_HEIGHT-2,
            libtcod.BKGND_NONE, libtcod.CENTER,
            '[%cESC%c] Return'%HIGHLIGHT)

        libtcod.console_blit(menu_con, 0, 0, MENU_CON_WIDTH, MENU_CON_HEIGHT, 0, MENU_CON_X, MENU_CON_Y)
        libtcod.console_flush()

        refresh = False
        while not refresh:

            # get input from user
            libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS|libtcod.EVENT_MOUSE, key, mouse)

            if key.vk == libtcod.KEY_ESCAPE:
                exit_menu = True
                break

            key_char = chr(key.c)

            if key_char in ['j', 'J']:
                ShowTextWindow('Campaign Journal', campaign.campaign_journal)

            # exit right away
            if libtcod.console_is_window_closed():
                sys.exit()

            libtcod.console_flush()

    # re-draw screen
    if battle is None:
        if campaign.day_in_progress:
            RenderCampaign()
    else:
        RenderEncounter()


# display a window of text lines, allow player to scroll up and down
def ShowTextWindow(title, text_lines):

    # copy existing screen to con
    libtcod.console_blit(0, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, con, 0, 0)

    # generate list of lines to display
    lines = []
    for line in text_lines:
        if len(line) <= 84:
            lines.append(line)
            continue
        # split original line
        split_lines = wrap(line, 84, subsequent_indent = ' ')
        lines.extend(split_lines)

    # starting y scroll position: bottom of list
    y2 = len(lines) - 1

    exit_menu = False
    while not exit_menu:

        # generate and display window
        libtcod.console_clear(text_con)
        libtcod.console_print_frame(text_con, 0, 0, TEXT_CON_WIDTH, TEXT_CON_HEIGHT,
            clear=False, flag=libtcod.BKGND_DEFAULT, fmt=0)

        # window title
        libtcod.console_set_default_foreground(text_con, MENU_TITLE_COLOR)
        libtcod.console_print_ex(text_con, TEXT_CON_XM, 1,
            libtcod.BKGND_NONE, libtcod.CENTER,
            title)
        libtcod.console_set_default_foreground(text_con, libtcod.white)

        # commands
        libtcod.console_print_ex(text_con, TEXT_CON_XM, TEXT_CON_HEIGHT-3,
            libtcod.BKGND_NONE, libtcod.CENTER,
            '[%cUp/Down/PgUp/PgDn/Home/End%c] Scroll'%HIGHLIGHT)
        libtcod.console_print_ex(text_con, TEXT_CON_XM, TEXT_CON_HEIGHT-2,
            libtcod.BKGND_NONE, libtcod.CENTER,
            '[%cESC%c] Return'%HIGHLIGHT)

        # text content
        if len(lines) <= 48:
            y1 = 0
        else:
            y1 = y2 - 48

        y = 3
        for n in range(y1, y2+1):
            if n > len(lines) - 1: break
            libtcod.console_print(text_con, 2, y, lines[n])
            y += 1

        libtcod.console_blit(text_con, 0, 0, TEXT_CON_WIDTH, TEXT_CON_HEIGHT, 0, TEXT_CON_X, TEXT_CON_Y)
        libtcod.console_flush()

        refresh = False
        while not refresh:
            # get input from user
            libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS|libtcod.EVENT_MOUSE, key, mouse)

            if key.vk == libtcod.KEY_ESCAPE:
                exit_menu = True
                break

            elif key.vk == libtcod.KEY_UP:
                if y2 > 48:
                    y2 -= 1
                    refresh = True

            elif key.vk == libtcod.KEY_DOWN:
                if y2 < len(lines) - 1:
                    y2 += 1
                    refresh = True

            elif key.vk == libtcod.KEY_HOME:
                y2 = 48
                refresh = True

            elif key.vk == libtcod.KEY_END:
                y2 = len(lines) - 1
                refresh = True

            elif key.vk == libtcod.KEY_PAGEUP:
                y2 -= 10
                if y2 < 48: y2 = 48
                refresh = True

            elif key.vk == libtcod.KEY_PAGEDOWN:
                y2 += 10
                if y2 > len(lines) - 1: y2 = len(lines) - 1
                refresh = True

            # exit right away
            if libtcod.console_is_window_closed():
                sys.exit()

            key_char = chr(key.c)

            libtcod.console_flush()

    # copy con back to screen
    libtcod.console_blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)
    libtcod.console_flush()


# display a window allowing the player to change game settings, which are saved in the campaign
# object
def ShowSettings():

    # darken screen
    libtcod.console_clear(con)
    libtcod.console_blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0,
        0.0, 0.7)

    exit_menu = False
    while not exit_menu:

        # generate and display menu
        libtcod.console_clear(menu_con)
        libtcod.console_set_alignment(menu_con, libtcod.LEFT)
        libtcod.console_print_frame(menu_con, 0, 0, MENU_CON_WIDTH, MENU_CON_HEIGHT,
            clear=False, flag=libtcod.BKGND_DEFAULT, fmt=0)

        libtcod.console_set_default_foreground(menu_con, MENU_TITLE_COLOR)
        libtcod.console_print_ex(menu_con, MENU_CON_XM, 2,
            libtcod.BKGND_NONE, libtcod.CENTER, 'Game Settings Menu')
        libtcod.console_set_default_foreground(menu_con, libtcod.white)
        libtcod.console_print_ex(menu_con, MENU_CON_XM, 3,
            libtcod.BKGND_NONE, libtcod.CENTER, VERSION + SUBVERSION)

        # Campaign Settings
        libtcod.console_print_frame(menu_con, 50, 5, 40, 6, clear=False,
            flag=libtcod.BKGND_DEFAULT, fmt=0)
        libtcod.console_set_default_foreground(menu_con, MENU_TITLE_COLOR)
        libtcod.console_print(menu_con, 52, 6, 'Campaign Settings')
        libtcod.console_set_default_foreground(menu_con, libtcod.white)

        text = 'Tank Selection: '
        if campaign.unlimited_tank_selection:
            text += 'Unlimited'
        else:
            text += 'Strict'
        libtcod.console_print(menu_con, 52, 8, text)

        text = 'Commander Replacement: '
        if campaign.casual_commander:
            text += 'Casual'
        else:
            text += 'Realistic'
        libtcod.console_print(menu_con, 52, 9, text)

        # Display Settings
        libtcod.console_print_frame(menu_con, 50, 12, 58, 13, clear=False,
            flag=libtcod.BKGND_DEFAULT, fmt=0)
        libtcod.console_set_default_foreground(menu_con, MENU_TITLE_COLOR)
        libtcod.console_print(menu_con, 52, 13, 'Display Settings')
        libtcod.console_set_default_foreground(menu_con, libtcod.white)

        text = '[%cA%c]nimations: '%HIGHLIGHT
        if campaign.animations:
            text += 'On'
        else:
            text += 'Off'
        libtcod.console_print(menu_con, 52, 15, text)

        text = '[%cS%c]ounds: '%HIGHLIGHT
        if campaign.sounds:
            text += 'On'
        else:
            text += 'Off'
        libtcod.console_print(menu_con, 52, 16, text)

        text = '[%cD%c]isplay Tutorial Messages: '%HIGHLIGHT
        if campaign.tutorial_message:
            text += 'On'
        else:
            text += 'Off'
        libtcod.console_print(menu_con, 52, 17, text)

        text = '[%cW%c]ait for Enter before clearing on-screen labels: '%HIGHLIGHT
        if campaign.pause_labels:
            text += 'On'
        else:
            text += 'Off'
        libtcod.console_print(menu_con, 52, 18, text)

        text = '[%cF%c]ull Screen: '%HIGHLIGHT
        # display based on actual fullscreen status, not campaign setting
        if libtcod.console_is_fullscreen():
            text += 'On'
        else:
            text += 'Off'
        libtcod.console_print(menu_con, 52, 20, text)

        text = '[%cR%c]esolution for Full Screen: '%HIGHLIGHT
        text += str(campaign.fs_res_x) + ' x ' + str(campaign.fs_res_y)
        libtcod.console_print(menu_con, 52, 21, text)

        libtcod.console_set_default_foreground(menu_con, libtcod.lighter_blue)
        libtcod.console_print(menu_con, 53, 22, 'Changing either of these two settings may')
        libtcod.console_print(menu_con, 53, 23, 'pause your computer for a few seconds')
        libtcod.console_set_default_foreground(menu_con, libtcod.white)

        libtcod.console_print_ex(menu_con, MENU_CON_XM, MENU_CON_HEIGHT-3,
            libtcod.BKGND_NONE, libtcod.CENTER, 'Press highlighted letter to change setting')

        libtcod.console_print_ex(menu_con, MENU_CON_XM, MENU_CON_HEIGHT-2,
            libtcod.BKGND_NONE, libtcod.CENTER,
            '[%cESC%c] Return'%HIGHLIGHT)

        libtcod.console_blit(menu_con, 0, 0, MENU_CON_WIDTH, MENU_CON_HEIGHT, 0, MENU_CON_X, MENU_CON_Y)
        libtcod.console_flush()

        refresh = False
        while not refresh:
            # get input from user
            libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS|libtcod.EVENT_MOUSE, key, mouse)

            if key.vk == libtcod.KEY_ESCAPE:
                exit_menu = True
                break

            # exit right away
            if libtcod.console_is_window_closed():
                sys.exit()

            key_char = chr(key.c)

            if key_char in ['a', 'A']:
                campaign.animations = not campaign.animations
                refresh = True

            elif key_char in ['s', 'S']:
                campaign.sounds = not campaign.sounds
                refresh = True

            elif key_char in ['w', 'W']:
                campaign.pause_labels = not campaign.pause_labels
                refresh = True

            elif key_char in ['d', 'D']:
                campaign.tutorial_message = not campaign.tutorial_message
                refresh = True

            elif key_char in ['f', 'F']:
                # switch FS mode and update campaign setting if required
                libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())
                campaign.fullscreen = libtcod.console_is_fullscreen()
                refresh = True

            elif key_char in ['r', 'R']:
                n = 0
                for (x, y) in FS_RES_LIST:
                    if x == campaign.fs_res_x and y == campaign.fs_res_y:
                        if n == len(FS_RES_LIST) - 1:
                            (campaign.fs_res_x, campaign.fs_res_y) = FS_RES_LIST[0]
                        else:
                            (campaign.fs_res_x, campaign.fs_res_y) = FS_RES_LIST[n+1]
                        break
                    n += 1
                libtcod.sys_force_fullscreen_resolution(campaign.fs_res_x, campaign.fs_res_y)

                # toggle FS to force an update into the new resolution
                if libtcod.console_is_fullscreen():
                    libtcod.console_set_fullscreen(False)
                    libtcod.console_set_fullscreen(True)
                refresh = True

            libtcod.console_flush()

    # re-draw screen
    if battle is None:
        if campaign.day_in_progress:
            RenderCampaign()
    else:
        RenderEncounter()


# display information on the campaign or encounter map; no input possible while it's
# being displayed
# x, y is highlighted object or location; label appears centered under this
# if crewman is not none, label is being spoken by that crewman
def ShowLabel(x, y, original_text, crewman=None):

    libtcod.console_set_default_background(0, GREYED_COLOR)

    # build text string
    text = ''

    # add crewman position to front of string
    if crewman is not None:
        text += crewman.position + ': '
    text += original_text

    # if wait for enter is on in campaign settings, add to text to display
    if campaign.pause_labels:
        text += ' [Enter to continue]'

    # divide text to be shown into lines
    lines = wrap(text, 28)

    n = 1
    for line in lines:
        # don't try to draw outside the screen
        if y+n >= SCREEN_HEIGHT:
            break
        if x + int((len(line)+1)/2) >= SCREEN_WIDTH:
            x = SCREEN_WIDTH - int((len(line)+1)/2)

        # make sure label falls within map console
        if battle is not None:
            if x - int((len(line)+1)/2) <= MAP_CON_X:
                x = MAP_CON_X + int((len(line)+1)/2)
        else:
            if x - int((len(line)+1)/2) <= C_MAP_CON_X:
                x = C_MAP_CON_X + int((len(line)+1)/2)

        # if animations are off, display labels all at once
        if not campaign.animations:
            libtcod.console_print_ex(0, x, y+n, libtcod.BKGND_SET, libtcod.CENTER, line)
            libtcod.console_flush()

        # otherwise, reveal label two characters at a time
        else:
            for i in xrange(0, len(line)+1, 2):
                libtcod.console_print_ex(0, x, y+n, libtcod.BKGND_SET, libtcod.CENTER, line[:i])
                libtcod.console_flush()
                Wait(1)
            else:
                # if there's an odd character left
                if len(line)+1 > i:
                    libtcod.console_print_ex(0, x, y+n, libtcod.BKGND_SET, libtcod.CENTER, line)
                    libtcod.console_flush()
                    Wait(1)
        n += 1

    if campaign.pause_labels:
        WaitForEnter()
    else:
        Wait(1100)
    libtcod.console_set_default_background(0, libtcod.black)

    # if in an encounter, add the label to the message queue, and re-render the screen
    if battle is not None:
        Message(original_text, color=libtcod.light_grey)
        RenderEncounter()


# wait for a specified amount of miliseconds, refreshing the screen in the meantime
def Wait(wait_time):
    # added this to avoid the spinning wheel of death in Windows
    libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS|libtcod.EVENT_MOUSE, key, mouse)
    libtcod.sys_sleep_milli(wait_time)


# returns true if number is odd
def IsOdd(num):
    return num & 1 and True or False


# returns center of given hex
# hex 0, 0 always center of map console
def Hex2Screen(hx, hy):
    x = (MAP_CON_WIDTH/2) + (hx*9)
    y = (MAP_CON_HEIGHT/2) + (hy*6) + (hx*3)
    return x, y


# returns hex at given coordinate
# can return hex 0,0
def Screen2Hex(x, y):
    for map_hex in battle.maphexes:
        if GetDistance(x, y, map_hex.x, map_hex.y) <= 3:
            return map_hex
    return None


# draws a single ascii hex
def DrawHex(console, x, y):
    libtcod.console_print_ex(console, x-3, y-3, libtcod.BKGND_SET, libtcod.LEFT, '|-----|')
    libtcod.console_print_ex(console, x-4, y-2, libtcod.BKGND_SET, libtcod.LEFT, '/       \\')
    libtcod.console_print_ex(console, x-5, y-1, libtcod.BKGND_SET, libtcod.LEFT, '/         \\')
    libtcod.console_print_ex(console, x-6, y, libtcod.BKGND_SET, libtcod.LEFT, '|           |')
    libtcod.console_print_ex(console, x-5, y+1, libtcod.BKGND_SET, libtcod.LEFT, '\\         /')
    libtcod.console_print_ex(console, x-4, y+2, libtcod.BKGND_SET, libtcod.LEFT, '\\       /')
    libtcod.console_print_ex(console, x-3, y+3, libtcod.BKGND_SET, libtcod.LEFT, '|-----|')


# returns true if two given hexes are adjacent
def IsAdjacent(hex1, hex2):
    if hex1 == hex2: return False    # same hex!
    DIRECTIONS = [(1,0), (1,-1), (0,-1), (-1,0), (-1,1), (0,1)]
    for (x_mod, y_mod) in DIRECTIONS:
        if hex1.hx + x_mod == hex2.hx and hex1.hy + y_mod == hex2.hy:
            return True
    return False


# returns the rounded distance between two points
def GetDistance(x1, y1, x2, y2):
    return int(sqrt((x1-x2)**2 + (y1-y2)**2))


# Bresenham's Line Algorithm
# returns a series of x, y points along a line
# based on an implementation on the roguebasin wiki
def GetLine(x1, y1, x2, y2):
    points = []
    issteep = abs(y2-y1) > abs(x2-x1)
    if issteep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2
    rev = False
    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1
        rev = True
    deltax = x2 - x1
    deltay = abs(y2-y1)
    error = int(deltax / 2)
    y = y1

    if y1 < y2:
        ystep = 1
    else:
        ystep = -1
    for x in range(x1, x2 + 1):
        if issteep:
            points.append((y, x))
        else:
            points.append((x, y))
        error -= deltay
        if error < 0:
            y += ystep
            error += deltax

    # Reverse the list if the coordinates were reversed
    if rev:
        points.reverse()
    return points


# get this difference in sectors between two facings / directions
def GetSectorDistance(new_f, old_f):
    diff = abs(new_f - old_f)
    if diff == 4:
        diff = 2
    elif diff == 5:
        diff = 1
    return diff


# return just the total result of a percentile 2D10 roll
def Roll1D100():
    return libtcod.random_get_int(0, 1, 100)


# return the result of a 1d10 roll
def Roll1D10():
    return libtcod.random_get_int(0, 1, 10)


# return the result of a 1D6 roll
def Roll1D6():
    return libtcod.random_get_int(0, 1, 6)


# return the result of a 2D6 roll
def Roll2D6():
    d1 = libtcod.random_get_int(0, 1, 6)
    d2 = libtcod.random_get_int(0, 1, 6)
    return d1, d2, (d1+d2)


# returns true if all enemy units in an encounter are dead
def AllEnemiesDead():
    for unit in battle.enemy_units:
        if unit.alive: return False
    return True


# add a new message to the encounter or campaign message queue and delete oldest one
# if required
def Message(new_msg, color=libtcod.white):

    # don't show if not in an encounter
    if battle is None: return

    # split the message if necessary, among multiple lines
    new_msg_lines = wrap(new_msg, MSG_CON_WIDTH-4, subsequent_indent = ' ')

    for line in new_msg_lines:
        #if the buffer is full, remove the first line to make room for the new one
        if len(battle.messages) == MSG_CON_HEIGHT:
            del battle.messages[0]

        #add the new line as a tuple, with the text and the color
        battle.messages.append( (line, color) )

    # update the message console
    UpdateMsgCon()
    RenderEncounter()


# roll on the activation table and spawn enemy units on the battle map
def ActivateEnemies():

    # if counterattack, use day resistance, otherwise use player location level
    if campaign.scen_type == 'Counterattack' or battle.counterattack:
        res_level = campaign.scen_res
    else:
        res_level = campaign.day_map.player_node.resistance

    # determine initial number of enemy units
    if res_level == 'Light':
        n = 2
    elif res_level == 'Medium':
        n = 3
    else:
        n = 4

    # spawn enemies
    for rolls in range(0, n):
        SpawnEnemy()
        UpdateMapOverlay()
        RenderEncounter()

        # pause for a bit
        Wait(300)


# spawn an enemy unit, can specify a unit class and spawn hex
def SpawnEnemy(unit_class=None, map_hex=None):

    # check to see if a date modifier applies
    def CheckModifer(mod):
        if mod['year'] > campaign.current_date[0]: return False        # wrong year
        if mod['month'] > campaign.current_date[1]: return False     # not late enough in the year
        if mod['date'] > campaign.current_date[2]: return False     # not late enough in the month

        # apply the modifier
        return True

    new_unit = EnemyUnit()

    if unit_class is None:

        # roll for unit class based on mission type
        # counterattack battle overrides day mission
        if battle.counterattack:
            column = 2
        else:
            if campaign.scen_type == 'Advance':
                column = 0
            elif campaign.scen_type == 'Battle':
                column = 1
            else:
                column = 2

        # activation list is a list of tuples: unit class followed by spawn chance
        # make a copy so we can apply date modifiers if any
        activation_list = list(campaign.mission_activations[column])

        # apply date modifier if any
        if len(campaign.activation_modifiers) > 0:
            for mod in campaign.activation_modifiers:
                if CheckModifer(mod):
                    for (k,v) in activation_list:
                        if k == mod['class_name']:
                            # apply the modifier
                            v += mod['mod']
                            if v < 0: v = 0
                            break

        # get sum of activation chances, might be modified beyond total of 100
        total = 0
        for (k,v) in activation_list:
            total += v

        random.shuffle(activation_list)
        unit_class = ''
        roll = libtcod.random_get_int(0, 0, total)
        for (k,v) in activation_list:
            if v == 0: continue        # skip if no chance to spawn
            if roll <= v:
                unit_class = k
                break
            roll -= v

    if unit_class == '':
        print 'ERROR: Could not generate a random unit class'
        return

    # determine unit type
    unit_type = ''

    # if unit is TANK, SPG, or AT Gun, check to see if there's already a unit
    # type set
    if unit_class == 'TANK' and battle.tank_type is not None:
        unit_type = battle.tank_type
    elif unit_class == 'SPG' and battle.spg_type is not None:
        unit_type = battle.spg_type
    elif unit_class == 'AT_GUN' and battle.at_gun_type is not None:
        unit_type = battle.at_gun_type

    # MG and LW only have one unit type each
    if unit_class == 'MG':
        unit_type = 'MG Team'
    elif unit_class == 'LW':
        unit_type = 'Light Weapons Infantry'

    # if unit type not set, generate it now
    if unit_type == '':
        result = libtcod.random_get_int(0, 1, 1000)
        for class_list in campaign.class_activations:
            if class_list[0] == unit_class:
                # copy list of possible unit types (skipping first element)
                type_list = class_list[1:]
                # shuffle list and run through, finding result
                random.shuffle(type_list)
                for (k,v) in type_list:
                    if v == 0: continue    # skip if no chance to spawn
                    if result <= v:
                        unit_type = k
                        break
                    result -= v
                break

    if unit_type == '':
        print 'ERROR: Could not generate a random unit type for class: ' + unit_class
        return

    # apply morale modifier for certain unit classes / types
    if unit_type in ['PzKw V G', 'PzKw VI E', 'PzKw VI B']:
        if new_unit.morale < 10: new_unit.morale += 1

    # set AT Gun main gun info
    if unit_class == 'AT_GUN':
        # set up unit gun type
        new_unit.stats = {}
        new_unit.stats['main_gun'] = unit_type

    # set encounter vehicle type if required
    if unit_class == 'TANK' and battle.tank_type is None:
        battle.tank_type = unit_type
    elif unit_class == 'SPG' and battle.spg_type is None:
        battle.spg_type = unit_type
    elif unit_class == 'AT_GUN' and battle.at_gun_type is None:
        battle.at_gun_type = unit_type

    # set up the stats of the new unit
    new_unit.unit_type = unit_type
    new_unit.unit_class = unit_class

    # set vehicle stats for vehicles
    if new_unit.unit_class in ['TANK', 'SPG', 'APC', 'AC', 'TRUCK']:
        SetVehicleStats(new_unit)

    # if unit is LW, check to see if armed with a panzerfaust
    if new_unit.unit_class == 'LW':
        roll = Roll1D6()
        if campaign.current_date[0] == 1945:
            roll -= 1
        if roll <= 3:
            new_unit.pf = True

    # if unit is an APC, see if it is carrying infantry
    elif new_unit.unit_class == 'APC':
        if Roll1D6() <= 4:
            new_unit.full_apc = True

    # if unit is an AC, set its spot flag
    elif new_unit.unit_class == 'AC':
        new_unit.spotting_player = False

    # determine spawn hex if not specified
    if map_hex is None:

        # roll for spawn sector
        d1, d2, roll = Roll2D6()
        if campaign.scen_type == 'Counterattack':
            roll += 1

        if roll <= 6:
            sector = 4
        elif roll <= 9:
            sector = random.choice([3,5])
        elif roll <= 11:
            sector = random.choice([2,0])
        else:
            sector = 1

        # now that we have the sector, determine the spawn range
        result = Roll1D10()

        # apply area type drm
        if campaign.day_map.player_node.node_type == 'C':
            result -= 3
        elif campaign.day_map.player_node.node_type == 'D':
            result -= 2
        elif campaign.day_map.player_node.node_type == 'F':
            result -= 5

        # apply firefly drm
        if tank.stats['vehicle_type'] == 'Sherman VC':
            result += 3

        if unit_class == 'LW':
            if result <= 6:
                rng = 0        # close
            else:
                rng = 1        # medium
        elif unit_class == 'MG':
            if result <= 3:
                rng = 0        # close
            elif result <= 8:
                rng = 1        # medium
            else:
                rng = 2        # long
        elif unit_class == 'AT':
            if result <= 2:
                rng = 0        # close
            elif result <= 7:
                rng = 1        # medium
            else:
                rng = 2        # long
        elif unit_class == 'SPG':
            if result <= 2:
                rng = 0        # close
            elif result <= 6:
                rng = 1        # medium
            else:
                rng = 2        # long
        else:
            if result <= 3:
                rng = 0        # close
            elif result <= 7:
                rng = 1        # medium
            else:
                rng = 2        # long

        # we have the sector and range, now determine the hex location
        # build list of possible spawn hexes
        spawn_hexes = []
        for map_hex in battle.maphexes:
            if rng == map_hex.rng and sector == map_hex.sector:
                spawn_hexes.append(map_hex)

        new_unit.map_hex = random.choice(spawn_hexes)
    else:
        new_unit.map_hex = map_hex

    # determine draw location within hex
    (new_unit.x, new_unit.y) = new_unit.GetCharLocation()

    # determine unit facing
    new_unit.SetFacing()

    # determine initial unit terrain and movement status
    new_unit.SetTerrain()

    battle.enemy_units.append(new_unit)

    # report message
    text = new_unit.GetDesc(new_spawn=True) + ' reported at '
    if new_unit.map_hex.sector == 0:
        text += "four o'clock"
    elif new_unit.map_hex.sector == 1:
        text += "six o'clock"
    elif new_unit.map_hex.sector == 2:
        text += "eight o'clock"
    elif new_unit.map_hex.sector == 3:
        text += "ten o'clock"
    elif new_unit.map_hex.sector == 4:
        text += "twelve o'clock"
    elif new_unit.map_hex.sector == 5:
        text += "two o'clock"
    text += ', '
    if new_unit.map_hex.rng == 0:
        text += 'close range!'
    elif new_unit.map_hex.rng == 1:
        text += 'medium range.'
    else:
        text += 'long range.'

    # play sound effect
    PlaySound('radio')

    # show information as a flash label on the map
    ShowLabel(new_unit.x+MAP_CON_X, new_unit.y+MAP_CON_Y, text)

    return new_unit


# create a new crewmember for the player tank
def SpawnCrewMember(name, position, rank_level, replacement=False, old_member=None):

    # if tank model does not have an asst driver, skip
    if position == 'Asst. Driver' and tank.stats.has_key('no_asst_driver'):
        return None

    new_crew = Crewman()

    if name is None:
        new_crew.GenerateName()
    else:
        new_crew.name = name
    new_crew.position = position
    new_crew.rank_level = rank_level

    # choose a random hometown
    if campaign.player_nation == 'USA':
        new_crew.hometown = random.choice(USA_HOMETOWNS)
    elif campaign.player_nation == 'CAN':
        new_crew.hometown = random.choice(CAN_HOMETOWNS)
    # NEW: transcode to handle accented characters
    new_crew.hometown = new_crew.hometown.decode('utf8').encode('cp850')

    # set default order and initial hatch state
    if position == 'Commander':
        new_crew.default_order = 'None'
        new_crew.hatch = 'Open'
    elif position == 'Gunner':
        new_crew.default_order = 'None'
        new_crew.hatch = 'None'
    elif position == 'Loader':
        new_crew.default_order = 'Reload'
        # set hatch based on tank
        if tank.stats['loader_hatch'] != 'None':
            new_crew.hatch = 'Open'
        else:
            new_crew.hatch = 'None'
    elif position == 'Driver':
        new_crew.default_order = 'Stop'
        new_crew.hatch = 'Open'
    elif position == 'Asst. Driver':
        new_crew.default_order = 'None'
        new_crew.hatch = 'Open'

    # set current order to default
    new_crew.order = new_crew.default_order

    # set initial spot ability; this will change later on
    new_crew.SetSpotAbility()

    # set up next and previous pointers unless this is a replacement crew member
    if not replacement:
        # if there's already at least one crew in tank list, set prev and next pointers
        if len(tank.crew) > 0:
            tank.crew[-1].next = new_crew
            new_crew.prev = tank.crew[-1]
            new_crew.next = tank.crew[0]
            tank.crew[0].prev = new_crew
        # otherwise, just set own next pointer to self
        else:
            new_crew.next = new_crew
            new_crew.prev = new_crew

    tank.crew.append(new_crew)

    # record to journal
    WriteJournal(new_crew.position + ' assigned as: ' + new_crew.GetRank(short=True) + ' ' + new_crew.name)

    return new_crew


# set up stats for a unit based on its vehicle type
def SetVehicleStats(obj):
    # get the right vehicle type entry
    for vehicle_type in VEHICLE_TYPES:
        if vehicle_type[0] == obj.unit_type:
            break
    else:
        print 'ERROR: Vehicle type not found: ' + obj.unit_type
        return

    obj.stats = {}

    # go through keys and values, skipping first item in list
    for (k, value) in vehicle_type[1:]:
        if k == 'HVSS':
            # random chance of actually having HVSS if on or after Nov. '44
            # if we're started a new campaign, date has not been set, so
            # assume earliest date in calendar
            if campaign.current_date == [0,0,0]:
                date = campaign.days[0]
                year = int(date['year'])
                month = int(date['month'])
            else:
                year = campaign.current_date[0]
                month = campaign.current_date[1]
            if year >= 1945 or (year == 1944 and month >= 11):
                if libtcod.random_get_int(0, 1, 10) <= value:
                    obj.stats['HVSS'] = True
        elif value == '':
            obj.stats[k] = True
        else:
            obj.stats[k] = value

    # if object is player tank, set up the ammo types as well
    if obj == tank:
        obj.general_ammo['HE'] = 0
        obj.general_ammo['AP'] = 0
        obj.rr_ammo['HE'] = 0
        obj.rr_ammo['AP'] = 0

        if obj.stats['main_gun'] == '75':
            obj.general_ammo['WP'] = 0
            obj.general_ammo['HCBI'] = 0
            obj.rr_ammo['WP'] = 0
            obj.rr_ammo['HCBI'] = 0

        elif obj.stats['main_gun'] == '76L':
            obj.general_ammo['HVAP'] = 0
            obj.rr_ammo['HVAP'] = 0

        elif obj.stats['main_gun'] == '76LL':
            obj.general_ammo['APDS'] = 0
            obj.rr_ammo['APDS'] = 0


# determine hit location on vehicles
def GetHitLocation(hull_down):
    result = Roll1D10()
    if hull_down:
        if result <= 5:
            return 'Turret'
        else:
            return 'Miss'
    else:
        if result <= 4:
            return 'Turret'
        elif result <= 9:
            return 'Hull'
        else:
            return 'Track'


# calculate base to-hit number, drm, and final roll required for an ordinance to-hit attack
def CalcTH(attacker, target, area_fire, ammo_type):

    # determine range of attack
    # different calculation depending on whether player is attacker or target
    if attacker == tank:
        rng = target.map_hex.rng
    else:
        rng = attacker.map_hex.rng

    ##### Determine base to-hit score required #####
    # direct fire
    if not area_fire:
        # infantry targets
        if target.unit_class in ['AT_GUN', 'MG', 'LW']:
            if rng == 0:
                base_th = 8
            elif rng == 1:
                base_th = 5
            else:
                base_th = 2
        # vehicle targets
        else:
            if rng == 0:
                base_th = 10
            elif rng == 1:
                base_th = 7
            else:
                base_th = 5
    # area fire
    else:
        if rng == 0:
            base_th = 7
        elif rng == 1:
            base_th = 8
        else:
            base_th = 6

    # to-hit score modifiers
    # long-range guns
    if 'LL' in attacker.stats['main_gun']:
        if rng == 1:
            base_th += 1
        elif rng == 2:
            base_th += 2
    elif 'L' in attacker.stats['main_gun']:
        if rng > 0:
            base_th += 1
    else:
        if rng > 0:
            base_th -= 1

    # firing smoke at close range
    if ammo_type in ['WP', 'HCBI'] and rng == 0:
        base_th += 2

    # smaller caliber guns
    if attacker.stats['main_gun'] == '20L':
        if rng == 1:
            base_th -= 1
        elif rng == 2:
            base_th -= 3

    ##### Dice Roll Modifiers #####

    drm = []
    # if turret has been rotated; doesn't apply to RoF shots
    # only applies to player tank
    if attacker == tank:
        if not tank.has_rof:
            diff = GetSectorDistance(tank.turret_facing, tank.old_t_facing)
            if diff != 0:
                # apply penalty, +1 per sector
                drm.append(('Turret has been rotated', diff))

        # commander buttoned up
        crew_member = GetCrewByPosition('Commander')
        if crew_member.hatch == 'Shut' and not tank.stats.has_key('vision_cupola'):
            drm.append(('Commander buttoned up', 1))

        # tank moving, firing with gyrostabilizer
        if tank.moving:
            if not GetCrewByPosition('Gunner').SkillCheck('Gyrostabilizer'):
                drm.append(('Firing on the move - Gyrostabilizer skill failed', 4))
            else:
                drm.append(('Firing on the move', 2))

        # acquired target
        if target.acquired == 1:
            drm.append(('Target acquired 1', -1))
        elif target.acquired == 2:
            drm.append(('Target acquired 2', -2))
        # increase acquired target number for next shot
        if target.acquired < 2:
            target.acquired += 1

    # some different modifiers used for enemy units
    else:

        # take advantage of AC spotting player
        spotter = False
        if attacker.acquired_player == 0:
            for unit in battle.enemy_units:
                if unit == attacker: continue
                if unit.unit_class == 'AC':
                    if unit.spotting_player:
                        spotter = True
                        break

        if spotter:
            drm.append(('Target acquired 1 via Spotter', -1))
        else:
            if attacker.acquired_player == 1:
                drm.append(('Target acquired 1', -1))
            elif attacker.acquired_player == 2:
                drm.append(('Target acquired 2', -2))

        # increase acquired target level for next shot
        if attacker.acquired_player < 2:
            attacker.acquired_player += 1

        # AT Guns rotating to fire
        if attacker.unit_class == 'AT_GUN':
            if attacker.facing == 'Side':
                if attacker.unit_type == '88LL':
                    drm.append(('Rotated Facing - 360' + chr(248) + ' mount', 1))
                else:
                    drm.append(('Rotated Facing', 2))
            elif attacker.facing == 'Rear':
                if attacker.unit_type == '88LL':
                    drm.append(('Rotated Facing - 360' + chr(248) + ' mount', 2))
                else:
                    drm.append(('Rotated Facing', 3))

    # vehicle target is moving
    if target.unit_class not in ['LW', 'MG', 'AT_GUN']:
        if target.moving:
            if not GetCrewByPosition('Gunner').SkillCheck('Target Tracking'):
                drm.append(('Vehicle target is moving', 2))

    # vehicle target size
    if target.unit_class not in ['LW', 'MG', 'AT_GUN']:
        target_size = target.stats['target_size']
        if target_size == 'Small':
            drm.append(('Small vehicle target', 1))
        elif target_size == 'Large':
            drm.append(('Large vehicle target', -1))
        elif target_size == 'Very Large':
            drm.append(('Very Large vehicle target', -2))

    # target terrain, direct fire only
    if attacker == tank and not area_fire:

        # all AT guns are assumed to be emplaced, no moving around
        if target.unit_class == 'AT_GUN' and target.terrain != 'Fortification':
            drm.append(('Emplaced gun target', 2))
        else:
            if target.terrain == 'Woods':
                drm.append(('Target in Woods', 1))
            elif target.terrain == 'Building':
                drm.append(('Target in Building', 2))
            elif target.terrain == 'Fortification':
                drm.append(('Target in Fortification', 3))

    # LoS hinderance (smoke)
    if attacker == tank:
        smoke_factors = GetSmokeFactors(0, 0, target.map_hex.hx, target.map_hex.hy)
    else:
        smoke_factors = GetSmokeFactors(0, 0, attacker.map_hex.hx, attacker.map_hex.hy)
    if smoke_factors > 0:
        drm.append(('Smoke Factors', smoke_factors*2))

    # firing through fog or falling snow
    if not area_fire and (campaign.weather.fog or campaign.weather.precip == 'Snow'):
        drm.append(('Fog or Falling Snow', 2))

    # commander directing fire
    if attacker == tank:
        crew_member = GetCrewByPosition('Commander')
        if crew_member.order == 'Direct Main Gun Fire':
            if crew_member.hatch == 'Open':
                if crew_member.SkillCheck('Fire Direction'):
                    mod = -3
                else:
                    mod = -2
                drm.append(('Commander Directing Fire', mod))
            elif tank.stats.has_key('vision_cupola'):
                if crew_member.SkillCheck('Fire Direction'):
                    mod = -2
                else:
                    mod = -1
                drm.append(('Commander Directing Fire', mod))
    total_drm = 0
    for (text, mod) in drm:
        total_drm += mod
    roll_req = base_th - total_drm

    return (base_th, roll_req, drm)


# return an armour value modified to be x steps higher/lower
def GetArmourStep(base_armour, modifier):
    ARMOUR_VALUES = [0,1,2,3,4,6,8,11,14,18,26]
    index = ARMOUR_VALUES.index(base_armour)
    new_index = index + modifier
    if new_index < 0 or new_index > 10:
        return base_armour
    return ARMOUR_VALUES[new_index]


# calculate base to-kill number, drm, and final roll required for a hit on a vehicle
def CalcTK(attacker, target, target_facing, ammo_type, critical, area_fire, hit_location):

    # determine range of attack
    # different calculation depending on whether player is attacker or target
    if attacker == tank:
        rng = target.map_hex.rng
    else:
        rng = attacker.map_hex.rng
    if rng == 0:
        rng_text = 'Close'
    elif rng == 1:
        rng_text = 'Medium'
    else:
        rng_text = 'Long'
    rng_text += ' Range'

    # get armour modifier, or set unarmoured target location flag
    unarmoured = False
    if hit_location == 'Hull':
        if target_facing in ['Rear', 'Side']:
            if 'hull_side_armour' in target.stats:
                armour_text = 'Hull Side'
                armour_mod = target.stats['hull_side_armour']
            else:
                unarmoured = True
        else:
            if 'hull_front_armour' in target.stats:
                armour_text = 'Hull Front'
                armour_mod = target.stats['hull_front_armour']
            else:
                unarmoured = True

    # turret hit
    else:
        if target_facing in ['Rear', 'Side']:
            if 'turret_side_armour' in target.stats:
                armour_text = 'Turret Side'
                armour_mod = target.stats['turret_side_armour']
            else:
                unarmoured = True
        else:
            if 'turret_front_armour' in target.stats:
                armour_text = 'Turret Front'
                armour_mod = target.stats['turret_front_armour']
            else:
                unarmoured = True
    # rear armour is always one step lower
    if not unarmoured and target_facing == 'Rear':
        if hit_location == 'Hull':
            armour_text = 'Hull Rear'
        else:
            armour_text = 'Turret Rear'
        armour_mod = GetArmourStep(armour_mod, -1)

    if not unarmoured:
        armour_text += ' Armour'
    drm = []

    ##### Panzerfaust #####
    if ammo_type == 'PF':
        base_tk = 31
        drm.append((armour_text, -armour_mod))

    ##### HE ammo #####
    elif ammo_type == 'HE':

        if attacker.stats['main_gun'] == '20L':
            if unarmoured:
                base_tk = 6
            else:
                base_tk = 3
                drm.append((armour_text, -armour_mod))
        elif attacker.stats['main_gun'] in ['88L', '88LL']:
            if unarmoured:
                base_tk = 14
            else:
                base_tk = 8
                drm.append((armour_text, -armour_mod))
        else:
            if unarmoured:
                base_tk = 12
            else:
                base_tk = 7
                drm.append((armour_text, -armour_mod))
        if unarmoured and critical:
            base_tk = base_tk * 2

        if not critical and area_fire:
            if target.terrain == 'Woods':
                drm.append(('Target in Woods', 1))

    ##### HVAP / APDS ammo #####
    # unarmoured targets use AP procedure instead
    elif ammo_type in ['HVAP', 'APDS'] and not unarmoured:
        if attacker.stats['main_gun'] == '76L':
            base_tk = 20
            if campaign.player_nation == 'USA':
                base_tk += 2
            range_mods = [2,-2,-5]
        elif attacker.stats['main_gun'] == '76LL':
            base_tk = 25
            range_mods = [0,0,-2]

        # apply range modifier
        drm.append((rng_text, range_mods[rng]))

        # apply armour modifier
        drm.append((armour_text, -armour_mod))

    ##### AP ammo #####
    elif ammo_type == 'AP':

        # hit location is unarmoured
        if unarmoured:
            if attacker.stats['main_gun'] == '20L':
                base_tk = 7
            elif attacker.stats['main_gun'] in ['88L', '88LL']:
                base_tk = 10
            else:
                base_tk = 9
            if critical:
                base_tk = base_tk * 2
        else:

            # start with gun type to get base TK number, also set range modifiers
            if attacker.stats['main_gun'] == '20L':
                base_tk = 6
            elif attacker.stats['main_gun'] == '50L':
                base_tk = 13
            elif attacker.stats['main_gun'] == '75':
                base_tk = 14
            elif attacker.stats['main_gun'] in ['75L', '76L']:
                base_tk = 17
            elif attacker.stats['main_gun'] == '88L':
                base_tk = 20
            elif attacker.stats['main_gun'] in ['75LL', '76LL']:
                base_tk = 23
            elif attacker.stats['main_gun'] == '88LL':
                base_tk = 27
            else:
                print 'ERROR: Gun Type not found!'
                return (2, 2, [])

            # double if critical
            if critical:
                base_tk = base_tk * 2

            # apply range modifier
            if attacker.stats['main_gun'] == '20L':
                range_mods = [1,-1,-3]
            else:
                range_mods = [0,-1,-2]

            # apply range modifier
            drm.append((rng_text, range_mods[rng]))

            # apply armour modifier
            drm.append((armour_text, -armour_mod))

    # calculate roll required
    total_drm = 0
    for (text, mod) in drm:
        total_drm += mod
    roll_req = base_tk + total_drm

    return (base_tk, roll_req, drm)


# calculate base to-kill number, drm, and final tk number for a player attack on the IFT
def CalcIFT(attacker, target, attack_weapon, critical, area_fire, fp=0, rng=0):

    # determine base roll to get a kill result
    if attack_weapon == 'MG':
        # bow MG - penalty for medium range
        if rng == 8 and target.map_hex.rng == 1:
            fp = int(fp/2)
        # infantry targets
        if target.unit_class in ['AT_GUN', 'MG', 'LW']:
            if fp == 1:
                base_tk = 4
            elif fp == 2:
                base_tk = 5
            elif fp == 4:
                base_tk = 6
        # unarmoured truck
        else:
            if fp == 1:
                base_tk = 3
            elif fp == 2:
                base_tk = 4
            elif fp == 4:
                base_tk = 5

    elif attack_weapon == '20L':
        if critical:
            base_tk = 5
        else:
            base_tk = 4
    elif attack_weapon == '88L':
        if critical:
            base_tk = 13
        else:
            base_tk = 9
    else:
        if critical:
            base_tk = 12
        else:
            base_tk = 8

    # calculate DRM
    drm = []

    # if critical, subtract TEM as DRM
    if critical:

        # special: AT Guns automatically destroyed with a critical hit
        # DRM are not displayed so don't bother listing them
        if target.unit_class == 'AT_GUN':
            return (base_tk, 13, drm)

        if target.terrain == 'Woods':
            drm.append(('Target in Woods', -1))
        elif target.terrain == 'Building':
            drm.append(('Target in Building', -2))
        elif target.terrain == 'Fortification':
            drm.append(('Target in Fortification', -3))

    # if non-critical area fire hit, add TEM as positive modifier instead
    elif area_fire:

        # all AT guns are assumed to be emplaced, no moving around
        if target.unit_class == 'AT_GUN' and target.terrain != 'Fortification':
            drm.append(('Emplaced gun target', 2))
        else:
            if target.terrain == 'Woods':
                drm.append(('Target in Woods', 1))
            elif target.terrain == 'Building':
                drm.append(('Target in Building', 2))
            elif target.terrain == 'Fortification':
                drm.append(('Target in Fortification', 3))

    # target moving in open
    if target.terrain == 'Open' and target.moving:
        drm.append(('Target moving in open', -1))

    # HE in mud or deep snow
    if campaign.weather.ground in ['Mud', 'Deep Snow'] and attack_weapon != 'MG':
        drm.append(('HE in Mud or Deep Snow', 1))

    # MG attack modifiers
    if attack_weapon == 'MG':
        if attacker.moving:
            drm.append(('Attacker Moving or Pivoting', 1))
        # coax fired and turret was rotated
        elif rng == 12 and tank.turret_facing != tank.old_t_facing:
            drm.append(('Turret has been rotated', 1))

        # target in fortification
        if target.terrain == 'Fortification':
            drm.append(('Target in fortification', 3))
        # target in woods
        elif target.terrain == 'Woods':
            drm.append(('Target in woods', 1))
        # target in building
        elif target.terrain == 'Building':
            drm.append(('Target in building', 2))
        # attack vs. emplaced gun
        elif target.unit_class == 'AT_GUN':
            drm.append(('Emplaced gun target', 2))

        # commander directing MG fire
        crew_member = GetCrewByPosition('Commander')
        if (rng == 12 and crew_member.order == 'Direct Co-ax MG Fire') or (rng == 8 and crew_member.order == 'Direct Bow MG Fire'):
            if crew_member.SkillCheck('Fire Direction'):
                mod = -2
            else:
                mod = -1
            drm.append(('Commander Directing Fire', mod))

        # skill check for asst driver
        if rng == 8:
            crew_member = GetCrewByPosition('Asst. Driver')
            if crew_member.order == 'Fire Bow MG':
                if crew_member.SkillCheck('Apprentice Gunner'):
                    drm.append(('Asst. Driver Skill', -1))

        # LoS hinderance (smoke)
        if attacker == tank:
            smoke_factors = GetSmokeFactors(0, 0, target.map_hex.hx, target.map_hex.hy)
        else:
            smoke_factors = GetSmokeFactors(0, 0, attacker.map_hex.hx, attacker.map_hex.hy)
        if smoke_factors > 0:
            drm.append(('Smoke Factors', smoke_factors*2))

    # calculate roll required
    total_drm = 0
    for (text, mod) in drm:
        total_drm += mod
    roll_req = base_tk - total_drm

    return (base_tk, roll_req, drm)


##########################################################################################
#                            Encounter Windows and Animations                            #
##########################################################################################

# display information about a vehicle
def ShowVehicleTypeInfo(unit_type, console, x, y, no_image=False):

    def PrintInfo(px, py, text):
        libtcod.console_print_ex(console, px, py, libtcod.BKGND_NONE, libtcod.LEFT, text)

    # get the right vehicle type entry
    for vt in VEHICLE_TYPES:
        if vt[0] == unit_type:
            break
    else:
        print 'ERROR: Vehicle type not found: ' + unit_type
        return
    stats = {}
    for (k, value) in vt[1:]:
        stats[k] = value

    # display the info
    text = stats['vehicle_type']
    if stats.has_key('sub_type'):
        text += ' (' + stats['sub_type'] + ')'
    if stats.has_key('nickname'):
        text += ' "' + stats['nickname'] + '"'
    PrintInfo(x, y, text)
    PrintInfo(x, y+1, stats['vehicle_class'])

    libtcod.console_set_default_foreground(console, libtcod.light_grey)
    PrintInfo(x, y+3, 'Main Gun:')
    libtcod.console_set_default_foreground(console, libtcod.white)
    if stats.has_key('main_gun'):
        text = stats['main_gun']
        if text != 'MG':
            text.replace('L', '') + 'mm'
    else:
        text = 'None'
    PrintInfo(x+10, y+3, text)

    libtcod.console_set_default_foreground(console, libtcod.light_grey)
    PrintInfo(x, y+5, 'Armour:  Front  Side')
    PrintInfo(x, y+6, 'Turret')
    PrintInfo(x, y+7, 'Hull')
    libtcod.console_set_default_foreground(console, libtcod.white)

    if stats.has_key('turret_front_armour'):
        text = str(stats['turret_front_armour'])
    else:
        text = '-'
    PrintInfo(x+11, y+6, text)
    if stats.has_key('turret_side_armour'):
        text = str(stats['turret_side_armour'])
    else:
        text = '-'
    PrintInfo(x+17, y+6, text)
    if stats.has_key('hull_front_armour'):
        text = str(stats['hull_front_armour'])
    else:
        text = '-'
    PrintInfo(x+11, y+7, text)
    if stats.has_key('hull_side_armour'):
        text = str(stats['hull_side_armour'])
    else:
        text = '-'
    PrintInfo(x+17, y+7, text)

    if stats.has_key('loader_hatch'):
        libtcod.console_set_default_foreground(console, libtcod.light_grey)
        PrintInfo(x, y+9, 'Loader Hatch:')
        libtcod.console_set_default_foreground(console, libtcod.white)
        PrintInfo(x+14, y+9, stats['loader_hatch'])

    ys = 1
    if stats.has_key('vision_cupola'):
        PrintInfo(x, y+9+ys, 'Vision Cupola')
        ys += 1
    if stats.has_key('smoke_mortar'):
        PrintInfo(x, y+9+ys, 'Smoke Mortar')
        ys += 1
    if stats.has_key('wet_stowage'):
        PrintInfo(x, y+9+ys, 'Wet Stowage')
        ys += 1
    if stats.has_key('HVSS'):
        PrintInfo(x, y+9+ys, 'Possible HVSS')
        ys += 1

    # show vehicle info text if any
    if stats.has_key('info_text'):
        ys += 2
        lines = wrap(stats['info_text'], 34, subsequent_indent = ' ')
        for line in lines:
            PrintInfo(x, y+9+ys, line)
            ys += 1

    # skip drawing overhead image of tank
    if no_image: return

    # show vehicle overhead image if any
    if stats.has_key('overhead_view'):
        temp_console = LoadXP(stats['overhead_view'])
        libtcod.console_blit(temp_console, 0, 0, 0, 0, console, x+46, y)


# show info about an enemy unit
def UnitInfo(mx, my):

    # make sure mouse cursor is over map window
    if mx < MAP_CON_X or my > MAP_CON_HEIGHT: return

    # adjust for offset
    mx -= MAP_CON_X
    my -= 2

    # see if there is a unit here
    for unit in battle.enemy_units:
        if not unit.alive: continue
        if unit.x == mx and unit.y == my:

            # if unit needs to be unidentified and isn't, don't display info for it
            if unit.unit_class in ['TANK', 'SPG', 'AT_GUN'] and not unit.identified:
                return

            # darken screen
            libtcod.console_clear(con)
            libtcod.console_blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0,
                0.0, 0.7)

            # generate display
            libtcod.console_clear(menu_con)
            libtcod.console_print_frame(menu_con, 0, 0, MENU_CON_WIDTH, MENU_CON_HEIGHT,
                clear=False, flag=libtcod.BKGND_DEFAULT, fmt=0)
            libtcod.console_set_alignment(menu_con, libtcod.LEFT)

            libtcod.console_set_default_foreground(menu_con, MENU_TITLE_COLOR)
            libtcod.console_print_ex(menu_con, MENU_CON_XM, 2,
                libtcod.BKGND_NONE, libtcod.CENTER, 'Unit Info')
            libtcod.console_set_default_foreground(menu_con, libtcod.white)
            libtcod.console_print_ex(menu_con, MENU_CON_XM, 4,
                libtcod.BKGND_NONE, libtcod.CENTER, unit.GetDesc())

            # grab description from UNIT_INFO if not vehicle
            if unit.unit_class in ['LW', 'MG', 'AT_GUN']:
                text = UNIT_INFO[unit.unit_type]
                lines = wrap(text, 56, subsequent_indent = ' ')
                y = 6
                for line in lines:
                    libtcod.console_print(menu_con, MENU_CON_XM-28, y, line)
                    y += 1
            else:
                # show vehicle info
                ShowVehicleTypeInfo(unit.unit_type, menu_con, 58, 7)

            libtcod.console_print_ex(menu_con, MENU_CON_XM, MENU_CON_HEIGHT-4,
                libtcod.BKGND_NONE, libtcod.CENTER, 'Press Enter to continue')
            libtcod.console_blit(menu_con, 0, 0, MENU_CON_WIDTH, MENU_CON_HEIGHT, 0, MENU_CON_X, MENU_CON_Y)
            libtcod.console_flush()

            WaitForEnter()
            return


# show a pop-up window describing an attack or a to kill roll and its results
def DisplayRoll(roll_action, tk_roll=False):

    # display the menu as it is being drawn, pausing for animation effect
    def UpdateMenu(wait_time):
        if not campaign.animations: return
        libtcod.console_blit(menu_con, 0, 0, MENU_CON_WIDTH, MENU_CON_HEIGHT, 0, MENU_CON_X, MENU_CON_Y)
        libtcod.console_flush()
        Wait(wait_time)

    # darken screen
    libtcod.console_clear(con)
    libtcod.console_blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0,
        0.0, 0.7)

    libtcod.console_clear(menu_con)
    libtcod.console_print_frame(menu_con, 0, 0, MENU_CON_WIDTH, MENU_CON_HEIGHT,
        clear=False, flag=libtcod.BKGND_DEFAULT, fmt=0)
    libtcod.console_set_alignment(menu_con, libtcod.CENTER)

    # window title
    libtcod.console_set_default_foreground(menu_con, MENU_TITLE_COLOR)
    if tk_roll:
        text = 'To Kill Roll'
    else:
        text = 'To Hit Roll'
    libtcod.console_print(menu_con, MENU_CON_XM, 2, text)
    libtcod.console_set_default_foreground(menu_con, libtcod.white)

    # attack/hit description
    if tk_roll:
        text = roll_action.target + ' hit by ' + roll_action.attack_type + ' fired from ' + roll_action.attacker
    else:
        text = roll_action.attacker + ' firing ' + roll_action.attack_type + ' at ' + roll_action.target

    # text might be long, so split up into lines
    lines = wrap(text, 60)
    libtcod.console_print(menu_con, MENU_CON_XM, 4, lines[0])
    if len(lines) > 1:
        libtcod.console_print(menu_con, MENU_CON_XM, 5, lines[1])

    # hit location if any
    if roll_action.hit_location is not '':
        libtcod.console_print(menu_con, MENU_CON_XM, 6, 'Target hit in ' + roll_action.hit_location)

    # display roll required
    if tk_roll:
        # check auto_ko
        if roll_action.auto_ko:
            text = 'Target automatically destroyed!'
        # check no chance
        elif roll_action.nc:
            text = 'No chance to kill target with this attack'
        else:
            text = 'Base to kill number: ' + str(roll_action.score_req)
    else:
        text = roll_action.rng + ' range, base to hit number: ' + str(roll_action.score_req)
    libtcod.console_print(menu_con, MENU_CON_XM, 7, text)

    # display DRM and required roll to hit if any
    if not roll_action.auto_ko and not roll_action.nc:

        libtcod.console_print_frame(menu_con, 38, 9, 63, 16,
            clear=False, flag=libtcod.BKGND_DEFAULT, fmt=0)
        libtcod.console_print(menu_con, MENU_CON_XM, 10, 'Dice Roll Modifiers')
        y = 12

        if len(roll_action.drm) == 0:
            libtcod.console_print(menu_con, MENU_CON_XM, y, 'None')
        else:
            for (text, num) in roll_action.drm:
                libtcod.console_set_alignment(menu_con, libtcod.LEFT)
                libtcod.console_print(menu_con, 40, y, text)
                libtcod.console_set_alignment(menu_con, libtcod.RIGHT)
                text = str(num)
                if num > 0:
                    text = '+' + text
                libtcod.console_print(menu_con, 94, y, text)
                UpdateMenu(200)
                y += 1

            # display total modifier
            libtcod.console_set_alignment(menu_con, libtcod.LEFT)
            libtcod.console_print(menu_con, 40, 23, 'Total:')
            libtcod.console_set_alignment(menu_con, libtcod.RIGHT)
            text = str(roll_action.total_drm)
            if roll_action.total_drm > 0:
                    text = '+' + text
            libtcod.console_print(menu_con, 94, 23, text)
            UpdateMenu(400)

        libtcod.console_set_alignment(menu_con, libtcod.CENTER)
        if tk_roll:
            libtcod.console_print(menu_con, MENU_CON_XM, 26, 'Required to kill: Less than ' + str(roll_action.roll_req))
            libtcod.console_print(menu_con, MENU_CON_XM, 28, 'To Kill roll (2D6):')
        else:
            libtcod.console_print(menu_con, MENU_CON_XM, 26, 'Required to hit: ' + str(roll_action.roll_req) + ' or less')
            libtcod.console_print(menu_con, MENU_CON_XM, 28, 'To Hit roll (2D6):')
        UpdateMenu(900)

    # dice roll animation and sound
    skip_roll = False
    # skip roll if auto kill or no chance to kill, unless weapon was MG and roll
    # was a malfunction
    if roll_action.auto_ko or roll_action.nc:
        skip_roll = True
        if 'MG' in roll_action.attack_type and roll_action.roll == 12:
            skip_roll = False

    if not skip_roll:
        for n in range(20):
            libtcod.console_print(menu_con, MENU_CON_XM, 29, '     ')
            text = str(libtcod.random_get_int(0, 1, 6)) + '+' + str(libtcod.random_get_int(0, 1, 6))
            libtcod.console_print(menu_con, MENU_CON_XM, 29, text)
            PlaySound('dice_roll')
            UpdateMenu(45)

        # display real to hit roll result
        libtcod.console_print(menu_con, MENU_CON_XM, 29, '  +  ')
        text = str(roll_action.d1) + '+' + str(roll_action.d2)
        libtcod.console_print(menu_con, MENU_CON_XM, 29, text)
        libtcod.console_print(menu_con, MENU_CON_XM, 30, 'Total: ' + str(roll_action.roll))
        libtcod.console_print(menu_con, MENU_CON_XM, 32, roll_action.result)

    # display RoF result if any
    if roll_action.rof_result is not '':
        libtcod.console_print(menu_con, MENU_CON_XM, 34, roll_action.rof_result)

    libtcod.console_print(menu_con, MENU_CON_XM, MENU_CON_HEIGHT-2, 'Press Enter to continue')

    libtcod.console_set_alignment(menu_con, libtcod.LEFT)
    libtcod.console_blit(menu_con, 0, 0, MENU_CON_WIDTH, MENU_CON_HEIGHT, 0, MENU_CON_X, MENU_CON_Y)
    libtcod.console_flush()

    WaitForEnter()


# work out the fate of a crew of a destroyed sherman that didn't explode
def ResolveCrewFate(hit_location, sector, pf, abandoned=False):

    # darken screen
    libtcod.console_clear(con)
    libtcod.console_blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0,
        0.0, 0.7)

    # use the menu console
    libtcod.console_clear(menu_con)
    libtcod.console_set_alignment(menu_con, libtcod.CENTER)
    libtcod.console_set_default_foreground(menu_con, libtcod.white)
    libtcod.console_print_frame(menu_con, 0, 0, MENU_CON_WIDTH, MENU_CON_HEIGHT,
        clear=False, flag=libtcod.BKGND_DEFAULT, fmt=0)

    libtcod.console_set_default_foreground(menu_con, MENU_TITLE_COLOR)
    libtcod.console_print(menu_con, MENU_CON_XM, 1, 'Tank Knocked Out')
    libtcod.console_print(menu_con, MENU_CON_XM, 2, 'Crew Wounds and Bail-Out Results')
    libtcod.console_set_default_foreground(menu_con, libtcod.white)
    libtcod.console_set_alignment(menu_con, libtcod.LEFT)

    # column titles
    libtcod.console_set_default_foreground(menu_con, libtcod.light_grey)
    libtcod.console_print(menu_con, 26, 11, 'Crewman')
    libtcod.console_print(menu_con, 52, 11, 'Initial Wound')
    libtcod.console_print(menu_con, 74, 11, 'Bail Out')
    libtcod.console_print(menu_con, 92, 11, 'Final Wound')
    libtcod.console_hline(menu_con, 25, 12, 97, flag=libtcod.BKGND_DEFAULT)
    libtcod.console_set_default_foreground(menu_con, libtcod.white)

    # list crew, highlighting every other row
    y = 13
    for crewman in tank.crew:
        text = crewman.GetRank(short=True) + ' ' + crewman.name
        libtcod.console_print(menu_con, 26, y, text)
        if crewman.nickname != '':
            libtcod.console_print(menu_con, 27, y+1, '"' + crewman.nickname + '"')

        # status
        if crewman.NoActions():
            libtcod.console_set_default_foreground(menu_con, libtcod.light_red)
            if not crewman.alive:
                text = 'Dead'
            elif crewman.unconscious:
                text = 'Unconscious'
            else:
                text = 'Stunned'
            libtcod.console_print(menu_con, 27, y+2, text)

        # wounds
        if crewman.v_serious_wound:
            text = 'Very Serious Wound'
        elif crewman.serious_wound:
            text = 'Serious Wound'
        elif crewman.light_wound:
            text = 'Light Wound'
        else:
            text = ''
        libtcod.console_set_default_foreground(menu_con, libtcod.red)
        libtcod.console_print(menu_con, 27, y+3, text)

        libtcod.console_set_default_foreground(menu_con, libtcod.white)

        if IsOdd(y):
            libtcod.console_set_default_background(menu_con, ROW_COLOR)
            libtcod.console_rect(menu_con, 25, y, 97, 3, False, flag=libtcod.BKGND_SET)
            libtcod.console_set_default_background(menu_con, libtcod.black)
        y += 3

    libtcod.console_print_ex(menu_con, MENU_CON_XM, MENU_CON_HEIGHT-2,
        libtcod.BKGND_NONE, libtcod.CENTER, '[%cEnter%c] to proceed'%HIGHLIGHT)
    libtcod.console_blit(menu_con, 0, 0, MENU_CON_WIDTH, MENU_CON_HEIGHT, 0, MENU_CON_X, MENU_CON_Y)
    libtcod.console_flush()
    WaitForEnter()

    # clear press enter display
    libtcod.console_print_ex(menu_con, MENU_CON_XM, MENU_CON_HEIGHT-2,
        libtcod.BKGND_NONE, libtcod.CENTER, '                  ')

    # Initial wound rolls
    # only possibility of an initial wound if tank was not abandoned
    if not abandoned:
        y = 13
        for crewman in tank.crew:
            if crewman.alive:
                text = crewman.TakeWound(hit_location, sector)
                if text is not None:
                    libtcod.console_set_default_foreground(menu_con, libtcod.red)
                    # split long strings
                    lines = wrap(text, 18)
                    n = 0
                    for line in lines:
                        libtcod.console_print(menu_con, 52, y+n, line)
                        n+=1
                    libtcod.console_set_default_foreground(menu_con, libtcod.white)
                else:
                    libtcod.console_print(menu_con, 52, y, 'Not wounded.')
            libtcod.console_blit(menu_con, 0, 0, MENU_CON_WIDTH, MENU_CON_HEIGHT, 0, MENU_CON_X, MENU_CON_Y)
            libtcod.console_flush()
            Wait(300)
            y += 3
        Wait(300)

    # Surviving and conscious crewmen roll to bail out
    y = 13
    for crewman in tank.crew:
        if crewman.alive:
            text = crewman.BailOut()

            if text == 'Passed':
                WriteJournal(crewman.name + ' bailed out successfully.')
            else:
                WriteJournal(crewman.name + ' failed to bail out!')

            if text != 'Passed':
                libtcod.console_set_default_foreground(menu_con, libtcod.red)
            libtcod.console_print(menu_con, 74, y, text)
            libtcod.console_set_default_foreground(menu_con, libtcod.white)
            libtcod.console_blit(menu_con, 0, 0, MENU_CON_WIDTH, MENU_CON_HEIGHT, 0, MENU_CON_X, MENU_CON_Y)
            libtcod.console_flush()
            Wait(300)
        y += 3

    # Crewmen who bailed out roll again for wound
    crewman_inside = False
    y = 13
    for crewman in tank.crew:
        if crewman.bailed_out:
            text = crewman.TakeWound(None, None)
            if text is not None:
                libtcod.console_set_default_foreground(menu_con, libtcod.red)
                # split long strings
                lines = wrap(text, 24)
                n = 0
                for line in lines:
                    libtcod.console_print(menu_con, 92, y+n, line)
                    n+=1
                libtcod.console_set_default_foreground(menu_con, libtcod.white)
            else:
                libtcod.console_print(menu_con, 92, y, 'Not wounded.')
            libtcod.console_blit(menu_con, 0, 0, MENU_CON_WIDTH, MENU_CON_HEIGHT, 0, MENU_CON_X, MENU_CON_Y)
            libtcod.console_flush()
            Wait(300)
        elif crewman.alive:
            # set flag - might be killed if tank burns up
            crewman_inside = True
        y += 3

    # brew up roll
    if not abandoned:
        roll = Roll1D100()
        if tank.stats.has_key('wet_stowage'):
            target_score = 15
        elif 'M4A1' in tank.stats['vehicle_type']:
            target_score = 75
        elif 'M4A3' in tank.stats['vehicle_type']:
            target_score = 70
        else:
            target_score = 80

        if pf: target_score += 5

        if roll <= target_score and not crewman_inside:
            libtcod.console_print_ex(menu_con, MENU_CON_XM, MENU_CON_HEIGHT-7,
                libtcod.BKGND_NONE, libtcod.CENTER, 'Your tank burns up, but ' +
                'luckily everyone managed to bail out.')

        else:
            if roll <= target_score:
                text = 'Your tank burns up, killing anyone trapped inside.'
                result_text = 'Burns to death'
            else:
                text = 'Luckily your tank does not burn up. Any surviving crewmen still inside are rescued.'
                result_text = 'Rescued'
            libtcod.console_print_ex(menu_con, MENU_CON_XM, MENU_CON_HEIGHT-7,
                libtcod.BKGND_NONE, libtcod.CENTER, text)
            y = 13
            for crewman in tank.crew:
                if not crewman.bailed_out and crewman.alive:
                    # apply result
                    if roll <= target_score:
                        crewman.alive = False
                        libtcod.console_set_default_foreground(menu_con, libtcod.red)
                    else:
                        crewman.bailed_out = True
                    # display text description of result
                    libtcod.console_print(menu_con, 92, y, result_text)
                    libtcod.console_set_default_foreground(menu_con, libtcod.white)
                    libtcod.console_blit(menu_con, 0, 0, MENU_CON_WIDTH, MENU_CON_HEIGHT, 0, MENU_CON_X, MENU_CON_Y)
                    libtcod.console_flush()
                    Wait(300)
                y += 3

    libtcod.console_set_alignment(menu_con, libtcod.CENTER)
    libtcod.console_print(menu_con, MENU_CON_XM, MENU_CON_HEIGHT-5, 'Your combat is over')
    libtcod.console_print(menu_con, MENU_CON_XM, MENU_CON_HEIGHT-3, '[%cEnter%c] to continue'%HIGHLIGHT)

    libtcod.console_blit(menu_con, 0, 0, MENU_CON_WIDTH, MENU_CON_HEIGHT, 0, MENU_CON_X, MENU_CON_Y)
    libtcod.console_flush()
    WaitForEnter()

    libtcod.console_set_alignment(menu_con, libtcod.LEFT)

    # check to see if we're ending the campaign because commander is dead or sent home
    if CheckCommander():
        campaign.exiting = True



##########################################################################################
#                             Encounter Actions and Phases                               #
##########################################################################################

# deplete smoke factors on map
def DepleteSmoke():
    for smoke_factor in battle.smoke_factors:
        # rain depletes smoke faster
        if campaign.weather.precip == 'Rain':
            smoke_factor.num_factors -= 0.75
        else:
            smoke_factor.num_factors -= 0.5
    for smoke_factor in battle.smoke_factors:
        if smoke_factor.num_factors <= 0.0:
            battle.smoke_factors.remove(smoke_factor)


# do spotting and identification checks for each crewmember that is able to do so
def DoSpotting():

    # flag if anything results from spotting attempts
    spot_result = False
    for crewman in tank.crew:

        # skip if this crew member cannot spot
        if crewman.spot == 'None': continue

        sectors = []

        # determine sectors in which crew member can spot
        if crewman.spot == 'All':
            sectors = [0, 1, 2, 3, 4, 5]
        elif crewman.spot == 'Any One Sector':
            sectors = [crewman.spot_sector]
        elif crewman.spot == 'Turret Front':
            # set according to turret facing
            sectors = [tank.turret_facing]
        elif crewman.spot == 'All Except Rear':
            sectors = [0, 2, 3, 4, 5]
        elif crewman.spot == 'Tank Front':
            sectors = [4]

        # test to spot and/or identify each enemy unit
        for unit in battle.enemy_units:

            # skip if unit not alive
            if not unit.alive: continue

            # skip if unit is outside of spotting area for this crew member
            if unit.map_hex.sector not in sectors: continue

            # skip if unit is already hidden
            if unit.hidden: continue

            # skip if unit is spotted and identified
            if unit.spotted and unit.identified: continue

            # skip if unit is spotted and doesn't need to be identified
            if unit.spotted and unit.unit_class not in ['TANK', 'SPG', 'AT_GUN']: continue

            # skip if foggy or falling snow and target is at medium and long range
            if unit.map_hex.rng > 0 and (campaign.weather.fog or campaign.weather.precip == 'Snow'):
                continue

            # do roll
            d1, d2, roll = Roll2D6()

            mod_roll = roll

            # apply modifiers
            if crewman.hatch in ['Shut', 'None']:
                mod_roll += 2
            else:
                # Eagle Eyed Skill Test
                if crewman.SkillCheck('Eagle Eyed'):
                    mod_roll -= 2
            if tank.moving:
                mod_roll += 2
            if unit.terrain in ['Woods', 'Building', 'Fortification', 'Hull Down']:
                mod_roll += 2
            if unit.unit_class not in ['LW', 'MG', 'AT_GUN']:
                if unit.stats['target_size'] == 'Small':
                    mod_roll += 1
                elif unit.stats['target_size'] == 'Large':
                    mod_roll -= 1
                elif unit.stats['target_size'] == 'Very Large':
                    mod_roll -= 2
            if unit.map_hex.rng == 1:
                mod_roll -= 1
            elif unit.map_hex.rng == 0:
                mod_roll -= 2
            if unit.fired:
                mod_roll -= 2
            if unit.moving:
                mod_roll -= 2
            if unit.spotted_lr:
                mod_roll -= 1
            mod_roll += (GetSmokeFactors(0, 0, unit.map_hex.hx, unit.map_hex.hy) * 2)

            # natural 12, or modified roll is 12 or more
            if roll == 12 or mod_roll >= 12:
                # target becomes hidden if not already spotted
                if unit.spotted or unit.hidden: continue
                text = unit.GetDesc() + ' is now hidden.'
                unit.hidden = True
                ShowLabel(unit.x+MAP_CON_X, unit.y+MAP_CON_Y, text)
                spot_result = True

            # natural 2, or modified roll is equal to or less than 4
            elif roll == 2 or mod_roll <= 4:
                # target is spotted and, if required, identified
                unit.spotted = True
                if unit.unit_class in ['TANK', 'SPG', 'AT_GUN']:
                    unit.identified = True
                text = unit.GetDesc() + ' spotted!'
                ShowLabel(unit.x+MAP_CON_X, unit.y+MAP_CON_Y, text, crewman=crewman)
                spot_result = True

            # modified result equal to or less than score required
            elif mod_roll <= 8:

                # mark that unit was spotted this round
                unit.spotted_tr = True

                # if already spotted, no additional benefit
                if unit.spotted: continue
                unit.spotted = True
                text = unit.GetDesc() + ' spotted!'
                ShowLabel(unit.x+MAP_CON_X, unit.y+MAP_CON_Y, text, crewman=crewman)

                spot_result = True

            UpdateMapOverlay()
            RenderEncounter()

    if not spot_result:
        Message('No results from spotting attempts.')

    # clear old flags and set new flags
    for unit in battle.enemy_units:
        unit.spotted_lr = False
        unit.fired = False
        if unit.spotted_tr:
            unit.spotted_tr = False
            unit.spotted_lr = True
    tank.fired_main_gun = False

    # redraw units on map to reflect new spotting status
    UpdateMapOverlay()


# try to set up firing MG(s)
def SetupFireMGs():
    # set MG flags
    if GetCrewByPosition('Commander').order == 'Fire AA MG' or GetCrewByPosition('Loader').order == 'Fire AA MG':
        tank.aa_mg_can_fire = True
    if GetCrewByPosition('Gunner').order == 'Fire Co-Axial MG':
        tank.coax_mg_can_fire = True
    if not tank.stats.has_key('no_asst_driver'):
        if GetCrewByPosition('Asst. Driver').order == 'Fire Bow MG' and not tank.hull_down:
            tank.bow_mg_can_fire = True

    # activate first available MG
    tank.SelectFirstMG()
    if tank.active_mg == -1: return False

    # set phase now so SelectNextTarget knows what to do
    NewPhase('Fire MGs')

    # get first target
    SelectNextTarget()
    return True


# fire an MG
def FireMG():

    if battle.target is None: return

    # set MG type used and play sound effect
    if tank.active_mg == 0:
        choice = 'Co-ax'
        PlaySound('coax_mg_firing')
    elif tank.active_mg == 1:
        choice = 'Bow'
        PlaySound('bow_mg_firing')
    elif tank.active_mg == 2:
        choice = 'AA'
        PlaySound('aa_mg_firing')
    else:
        return

    # display firing animation
    MGAnimation(MAP_X0 + MAP_CON_X, MAP_Y0 + MAP_CON_Y, battle.target.x + MAP_CON_X,
        battle.target.y + MAP_CON_Y)

    # now there's only one MG selected, so fire it at the target!
    # mark that this MG has fired, also record mg firepower and normal range
    if choice == 'Co-ax':
        tank.coax_mg_can_fire = False
        mg_fp = tank.stats['co_ax_mg']
        mg_rng = 12
    elif choice == 'Bow':
        tank.bow_mg_can_fire = False
        mg_fp = tank.stats['bow_mg']
        mg_rng = 8
    else:
        tank.aa_mg_can_fire = False
        mg_fp = tank.stats['aa_mg']
        mg_rng = 8

    # select the next MG that can fire
    tank.SelectFirstMG()

    # calculate modifiers and final DR required
    (base_tk, roll_req, drm) = CalcIFT(tank, battle.target, 'MG', False, False, fp=mg_fp, rng=mg_rng)

    # create roll action object to hold details about the action
    roll_action = RollAction()

    # input details
    roll_action.attacker_unit_type = tank.unit_type
    roll_action.attacker = tank.stats['vehicle_type'] + ' "' + tank.name + '"'
    roll_action.attack_type = choice + ' MG'
    # mark if target is unspotted or needs to be identified
    if not battle.target.spotted or (battle.target.unit_class in ['TANK', 'SPG', 'AT_GUN'] and not battle.target.identified):
        roll_action.target_unidentified = True
    roll_action.target_unit_type = battle.target.unit_type
    roll_action.target = battle.target.GetDesc()
    if battle.target.map_hex.rng == 0:
        roll_action.rng = 'Close'
    elif battle.target.map_hex.rng == 1:
        roll_action.rng = 'Medium'
    else:
        roll_action.rng = 'Long'
    roll_action.score_req = base_tk
    roll_action.drm = drm
    roll_action.CalculateTotalDRM()
    roll_action.roll_req = roll_req

    # record if KO is impossible
    if roll_req <= 2: roll_action.nc = True

    ##### To-Kill Roll #####
    d1, d2, roll = Roll2D6()
    roll_action.d1 = d1
    roll_action.d2 = d2
    roll_action.roll = roll

    # malfunction
    if d1 == 6 and d2 == 6:
        roll_action.result = 'The MG has malfunctioned!'

    # Target Destroyed
    elif roll < roll_req:
        roll_action.result = battle.target.GetDesc() + ' is destroyed!'
        WriteJournal(battle.target.GetDesc() + ' was destroyed by MG fire from ' + tank.name)
        battle.target.RecordKO()
        battle.target.alive = False

    # Infantry are automatically Pinned
    elif roll == roll_req:
        if battle.target.unit_class in ['LW', 'MG', 'AT_GUN']:
            battle.target.PinTest(auto=True)
            if not battle.target.alive:
                roll_action.result = battle.target.GetDesc() + ' is Broken and destroyed!'
                WriteJournal(battle.target.GetDesc() + ' was broken and destroyed by MG fire from ' + tank.name)
            else:
                roll_action.result = battle.target.GetDesc() + ' is Pinned.'

        # no effect on vehicles
        else:
            roll_action.result = battle.target.GetDesc() + ' is unharmed.'

    # No effect
    else:
        roll_action.result = battle.target.GetDesc() + ' is unharmed.'

    # display results to player then delete roll object
    DisplayRoll(roll_action, tk_roll=True)
    del roll_action

    # apply effects of MG malfunction if any
    if d1 == 6 and d2 == 6:
        if choice == 'Co-ax':
            tank.TakeDamage(damage_type='Co-ax MG Malfunction')
        elif choice == 'Bow':
            tank.TakeDamage(damage_type='Bow MG Malfunction')
        else:
            tank.TakeDamage(damage_type='AA MG Malfunction')

    # try to select another target
    SelectNextTarget()

    UpdateMapOverlay()
    RenderEncounter()


# attempt to repair a tank malfunction
# if post encounter, has different requirements and possible effects
def AttemptRepairs(post_encounter=False):

    # skip if tank was destroyed or severely damaged
    if not tank.alive or tank.swiss_cheese: return

    # step through in reverse so we can pop out old entries and add new ones
    for damage in reversed(tank.damage_list):

        # if broken periscope, replace if after combat, otherwise can't fix
        if 'Periscope Broken' in damage:
            if post_encounter:
                PopUp('The ' + damage + ' has been replaced!')
                tank.damage_list.remove(damage)
            continue

        damage_type = GetDamageType(damage)

        # not found; can't be repaired
        if damage_type is None: continue

        # no repair allowed
        if damage_type.repair_score == 0: continue

        # see if we can attempt this repair now
        active_crewman = None
        repair_ok = False
        if (damage_type.auto_repair and post_encounter):
            repair_ok = True
        else:
            for crewman in tank.crew:
                if crewman.order == damage_type.order:
                    repair_ok = True
                    active_crewman = crewman
                    break
        if not repair_ok: continue

        # do repair roll
        d1, d2, roll = Roll2D6()

        # check for skill activation
        if not post_encounter:
            if active_crewman.SkillCheck('Mechanic'):
                roll -= 1

        # bonus automatically applied if repair attempt is after an encounter
        if not post_encounter:
            if GetCrewByPosition('Gunner').order == 'Help Repair':
                roll -= 1
        else:
            roll -= 1

        if (d1 == 6 and d2 == 2 and damage_type.break_score != 0) or roll >= damage_type.break_score:
            PopUp('The repair attempt failed! ' + damage_type.break_result + '.')
            tank.damage_list.remove(damage)
            tank.damage_list.append(damage_type.break_result)

        elif roll > damage_type.repair_score and not (damage_type.auto_repair and post_encounter):
            PopUp('The ' + damage_type.name + ' repair was not successful.')

        else:
            PopUp('The ' + damage_type.name + ' has been repaired!')
            tank.damage_list.remove(damage)

        if battle is not None: UpdateTankCon()


# try to set up main gun to fire
# returns True if target selection can proceed, False if not
def SetupMainGun():

    # check for malfunctioning, broken main gun or gun sight
    if 'Main Gun Malfunction' in tank.damage_list or 'Main Gun Broken' in tank.damage_list:
        return False
    if 'Gun Sight Broken' in tank.damage_list:
        return False

    # if gunner is out of action or not ordered to fire, return
    if GetCrewByPosition('Gunner').order != 'Fire Main Gun':
        return False

    # if tank is moving, cannot fire main gun unless gunner has gyrostabilizer training
    if tank.moving:
        gyro = False
        for skill in GetCrewByPosition('Gunner').skills:
            if skill.name == 'Gyrostabilizer':
                gyro = True
                break
        if not gyro:
            PopUp('Tank is moving and cannot fire main gun.')
            return False

    # need to have a shell in the gun
    if tank.ammo_load == 'None':
        PopUp('No shell loaded - order Loader to Change Gun Load.')
        return False

    # if WP or HCBI loaded, switch to Area Fire automatically
    if tank.ammo_load in ['WP', 'HCBI']:
        battle.area_fire = True

    # if AP loaded, switch to direct fire automatically
    elif tank.ammo_load in ['AP', 'HVAP', 'APDS']:
        battle.area_fire = False

    # set this now so SelectNextTarget knows how to select the inital target
    NewPhase('Fire Main Gun')

    # grab first possible target
    SelectNextTarget()

    return True


# selects the next valid target for active weapon
def SelectNextTarget():

    # build a list of valid targets
    # build list differently based on whether main gun or MGs are firing
    targets = []
    for unit in battle.enemy_units:
        if not unit.alive: continue
        if unit.hidden or not unit.spotted: continue

        # skip if target is beyond close range and it's foggy or falling snow
        if unit.map_hex.rng > 0:
            if campaign.weather.fog or campaign.weather.precip == 'Snow':
                continue

        # main gun target
        if battle.phase == 'Fire Main Gun':
            if tank.turret_facing != unit.map_hex.sector:
                continue
            targets.append(unit)    # target is good

        # MG target
        elif battle.phase == 'Fire MGs':
            # must not be in long range
            if unit.map_hex.rng == 2: continue
            # must be unarmoured target
            if unit.unit_class not in ['AT_GUN', 'MG', 'LW', 'TRUCK']: continue

            # try to add target based on active MG
            # coax
            if tank.active_mg == 0:
                if tank.turret_facing != unit.map_hex.sector: continue
                targets.append(unit)
            # bow
            elif tank.active_mg == 1:
                if unit.map_hex.sector != 4: continue
                if tank.hull_down: continue
                targets.append(unit)
            # AA
            elif tank.active_mg == 2:
                targets.append(unit)

    # if no targets possible, return
    if len(targets) == 0:
        battle.target = None
        return

    # if no target is already set, then return the first in the list
    if battle.target is None:
        battle.target = targets[0]
        return

    # otherwise, skip to the already selected target
    for target in targets:
        if target == battle.target: break

    # if there's a next one, return that, otherwise return the first one in the list
    index_num = targets.index(target)
    if index_num < len(targets) - 1:
        battle.target = targets[index_num + 1]
    else:
        battle.target = targets[0]


# fire the player tank's main gun at the selected target
def FireMainGun():

    if battle.target is None: return

    # random callout
    if Roll1D10() == 1:
        ShowLabel(MAP_X0+MAP_CON_X, MAP_Y0+MAP_CON_Y, 'Firing!',
            GetCrewByPosition('Gunner'))
    if Roll1D10() == 2:
        ShowLabel(MAP_X0+MAP_CON_X, MAP_Y0+MAP_CON_Y, 'On the way!',
            GetCrewByPosition('Gunner'))

    # play firing sound
    soundfile = GetFiringSound(tank.stats['main_gun'])
    if soundfile is not None:
        PlaySound(soundfile)

    # do firing animation
    MainGunAnimation(MAP_X0 + MAP_CON_X, MAP_Y0 + MAP_CON_Y, battle.target.x + MAP_CON_X,
        battle.target.y + MAP_CON_Y)

    # calculate modifiers and final DR required
    (base_th, roll_req, drm) = CalcTH(tank, battle.target, battle.area_fire, tank.ammo_load)

    # set the tank fired main gun flag
    tank.fired_main_gun = True

    # lose any other acquired target
    for unit in battle.enemy_units:
        if unit == battle.target: continue
        unit.acquired = 0

    # create roll action to hold details about the action
    roll_action = RollAction()

    # input details
    roll_action.attacker_unit_type = tank.unit_type
    roll_action.attacker = tank.stats['vehicle_type'] + ' "' + tank.name + '"'

    # record description of main gun and ammo used
    roll_action.attack_type = tank.stats['main_gun'].replace('L', '') + 'mm ' + tank.ammo_load

    # mark if target is unspotted or needs to be identified
    if not battle.target.spotted or (battle.target.unit_class in ['TANK', 'SPG', 'AT_GUN'] and not battle.target.identified):
        roll_action.target_unidentified = True
    roll_action.target_unit_type = battle.target.unit_type
    roll_action.target = battle.target.GetDesc()
    if battle.target.map_hex.rng == 0:
        roll_action.rng = 'Close'
    elif battle.target.map_hex.rng == 1:
        roll_action.rng = 'Medium'
    else:
        roll_action.rng = 'Long'
    roll_action.score_req = base_th
    roll_action.drm = drm
    roll_action.CalculateTotalDRM()
    roll_action.roll_req = roll_req

    ##### To-hit Roll #####
    d1, d2, roll = Roll2D6()

    roll_action.d1 = d1
    roll_action.d2 = d2
    roll_action.roll = roll

    # flag to record what kind of animation / effect to show later
    hit_result = None

    # handle smoke attacks differently
    if tank.ammo_load in ['WP', 'HCBI']:

        # double sixes: main gun malfunction
        if roll == 12:
            roll_action.result = 'Main Gun Malfunction!'
            tank.damage_list.append('Main Gun Malfunction')

        elif roll <= roll_req:
            roll_action.result = 'Shot hit target area!'
            hit_result = 'smoke_hit'

            # add smoke factors
            if tank.ammo_load == 'WP':
                n = 1.0
            else:
                n = 2.0
            PlaceSmoke(battle.target.map_hex, n)
            PaintMapCon()

            # if WP, record hit on target for pin check
            if tank.ammo_load == 'WP':
                battle.target.hit_record.append(MainGunHit(tank.stats['main_gun'],
                    tank.ammo_load, False, battle.area_fire))

        else:
            roll_action.result = 'Shot missed target area!'
            hit_result = 'miss'

    else:

        # tell target it's been fired at
        battle.target.shot_at = True

        # record hits to apply after final shot

        # check for Knows Weak Spots skill activation
        weak_spot = False
        if roll == 3:
            crew_member = GetCrewByPosition('Gunner')
            if crew_member.SkillCheck('Knows Weak Spots'):
                weak_spot = True

        # critical hit, automatically hits
        # if original to-hit roll was 2+
        if roll_action.roll_req >= 2 and (roll == 2 or weak_spot):
            roll_action.result = 'Critical Hit!'
            battle.target.hit_record.append(MainGunHit(tank.stats['main_gun'],
                tank.ammo_load, True, battle.area_fire))

        # double sixes: main gun malfunction
        elif roll == 12:
            roll_action.result = 'Automatic Miss, Main Gun Malfunction!'
            tank.damage_list.append('Main Gun Malfunction')

        elif roll <= roll_req:
            roll_action.result = 'Shot hit!'
            battle.target.hit_record.append(MainGunHit(tank.stats['main_gun'],
                tank.ammo_load, False, battle.area_fire))
            if tank.ammo_load == 'HE':
                hit_result = 'he_hit'
            else:
                hit_result = 'ap_hit'
        else:
            roll_action.result = 'Shot missed.'
            hit_result = 'miss'

    # clear the fired shell, record last shell type
    old_load = tank.ammo_load
    tank.ammo_load = 'None'

    # if main gun malfunctioned, cannot reload or maintain RoF
    if 'Main Gun Malfunction' in tank.damage_list:
        roll_action.rof_result = 'Cannot reload or maintain RoF'
        UpdateTankCon()
        # go to next phase
        battle.trigger_phase = True
    else:

        # try to load a new shell into the main gun if loader is on correct order
        crew_member = GetCrewByPosition('Loader')
        if crew_member.order in ['Reload', 'Change Gun Load']:

            # check for possibility of Shell Juggler skill activation first
            skill_used = False
            if tank.use_rr and tank.general_ammo[tank.ammo_reload] > 0:
                if crew_member.SkillCheck('Shell Juggler'):
                    tank.ammo_load = tank.ammo_reload
                    tank.general_ammo[tank.ammo_reload] -= 1
                    UpdateTankCon()
                    skill_used = True

            if not skill_used:
                if tank.use_rr:
                    if tank.rr_ammo[tank.ammo_reload] > 0:
                        tank.ammo_load = tank.ammo_reload
                        tank.rr_ammo[tank.ammo_reload] -= 1
                        UpdateTankCon()
                    else:
                        # wasn't able to use rr
                        tank.use_rr = False

                if not tank.use_rr:
                    if tank.general_ammo[tank.ammo_reload] > 0:
                        tank.ammo_load = tank.ammo_reload
                        tank.general_ammo[tank.ammo_reload] -= 1
                        UpdateTankCon()

        # if changed gun load, cannot maintain RoF
        if GetCrewByPosition('Loader').order == 'Change Gun Load':
            roll_action.rof_result = 'Loader changed gun load this round, cannot maintain RoF'
            battle.trigger_phase = True

        # if no shell is loaded, cannot maintain RoF
        elif tank.ammo_load == 'None':
            if crew_member.order != 'Reload':
                roll_action.rof_result = 'No shell in main gun, cannot maintain RoF'
            else:
                roll_action.rof_result = 'No shells of reload type available, cannot reload!'
            battle.trigger_phase = True

        else:
            # determine if RoF is maintained

            # switch fire mode if required for reloaded shell type
            if battle.area_fire and tank.ammo_load in ['AP', 'HVAP', 'APDS']:
                battle.area_fire = False
                UpdateTankCon()
            elif not battle.area_fire and tank.ammo_load in ['WP', 'HCBI']:
                battle.area_fire = True
                UpdateTankCon()

            # see if RoF is maintained: use unmodified to-hit roll plus new modifiers
            # only best modifier will apply in case of skill mods
            skill_mod = 0

            # Ready Rack use or Asst. Driver passing ammo
            if tank.use_rr:
                roll -= 2
            else:
                if not tank.stats.has_key('no_asst_driver'):
                    crew_member = GetCrewByPosition('Asst. Driver')
                    if crew_member.order == 'Pass Ammo':
                        mod = -1
                        if crew_member.SkillCheck('Shell Tosser'):
                            skill_mod = -2
                            mod = 0
                        roll += mod

            crew_member = GetCrewByPosition('Gunner')
            if crew_member.SkillCheck('Quick Trigger'):
                if skill_mod > -1: skill_mod = -1

            crew_member = GetCrewByPosition('Loader')
            if crew_member.SkillCheck('Fast Hands'):
                if skill_mod > -1: skill_mod = -1

            roll += skill_mod

            if roll <= tank.stats['rof_num']:
                roll_action.rof_result = 'RoF maintained!'
                tank.has_rof = True
            else:
                roll_action.rof_result = "RoF wasn't maintained, end of main gun fire."
                # go to hit resolution
                battle.trigger_phase = True

    # show all this to the player!
    DisplayRoll(roll_action)

    # reset turret facing since can't rotate again
    tank.old_t_facing = tank.turret_facing

    # show shot result animation and/or sound
    RenderEncounter()
    if hit_result is not None:
        HitAnimation(hit_result)

    # redraw the map overlay
    UpdateMapOverlay()

    # delete the roll action object
    del roll_action

    # call out new ammo load if any
    if tank.ammo_load != 'None' and old_load != tank.ammo_load:
        ShowLabel(MAP_X0+MAP_CON_X, MAP_Y0+MAP_CON_Y,
            tank.ammo_load + ' up!', GetCrewByPosition('Loader'))

    RenderEncounter()


##########################################################################################
#                                   Encounter Animations                                 #
##########################################################################################

# display an animation of a main gun firing from x1,y1 to x2,y2
# displayed on root console
def MainGunAnimation(x1, y1, x2, y2):

    if not campaign.animations: return

    # get the line to display the animation
    line = GetLine(x1, y1, x2, y2)

    # don't animate if too short
    if len(line) < 3: return

    for (x, y) in line[2:]:
        # record the foreground color and character of the cell
        col = libtcod.console_get_char_foreground(0, x, y)
        char = libtcod.console_get_char(0, x, y)

        # now set to white, main gun round character
        libtcod.console_set_char_foreground(0, x, y, libtcod.white)
        libtcod.console_set_char(0, x, y, libtcod.CHAR_BULLET)

        # refresh screen and wait
        libtcod.console_flush()
        Wait(70)

        # reset character
        libtcod.console_set_char_foreground(0, x, y, col)
        libtcod.console_set_char(0, x, y, char)

    libtcod.console_flush()


# display an animation of MG fire
def MGAnimation(x1, y1, x2, y2):

    if not campaign.animations: return

    # get the line to display the animation
    line = GetLine(x1, y1, x2, y2)

    # don't animate if too short
    if len(line) < 3: return

    # erase the los line and render the screen
    UpdateMapOverlay(skip_los=True)
    RenderEncounter()

    for n in range(20):
        # pick a random point along the line
        (x, y) = random.choice(line[2:-1])

        # record the original foreground color and character of the cell
        col = libtcod.console_get_char_foreground(0, x, y)
        char = libtcod.console_get_char(0, x, y)

        # pick random display color
        c = libtcod.random_get_int(0, 0, 30)
        libtcod.console_set_char_foreground(0, x, y, libtcod.Color(220, 145+c, 30))

        # set character to mg bullet
        libtcod.console_set_char(0, x, y, 249)

        # refresh screen and wait
        libtcod.console_flush()
        Wait(70)

        # reset character
        libtcod.console_set_char_foreground(0, x, y, col)
        libtcod.console_set_char(0, x, y, char)

    # reset los display and re-render screen
    UpdateMapOverlay()
    RenderEncounter()


# display an animation of an artilery or air strike on an area centered on x,y
# displayed on root console
def ArtyStrikeAnimation(x, y):

    if not campaign.animations: return

    # wait for latter part of sound effect
    if campaign.sounds:
        Wait(400)

    for n in range(10):

        x1 = x + libtcod.random_get_int(0, -7, 7)
        y1 = y + libtcod.random_get_int(0, -4, 4)

        # skip if off map
        if x1 < C_MAP_CON_X or x1 >= SCREEN_WIDTH - 1 or y1 < 4 or y1 >= SCREEN_HEIGHT:
            continue

        # cycle through animation characters, ending with grey smoke
        libtcod.console_set_char_foreground(0, x1, y1, libtcod.red)
        libtcod.console_set_char(0, x1, y1, 249)
        libtcod.console_flush()
        Wait(40)

        libtcod.console_set_char(0, x1, y1, libtcod.CHAR_BULLET)
        libtcod.console_flush()
        Wait(40)

        libtcod.console_set_char(0, x1, y1, libtcod.CHAR_RADIO_UNSET)
        libtcod.console_flush()
        Wait(40)

        libtcod.console_set_char_foreground(0, x1, y1, libtcod.light_grey)
        libtcod.console_set_char(0, x1, y1, libtcod.CHAR_BLOCK1)
        libtcod.console_flush()
        Wait(40)

    # blit display console to screen to clear animation and update screen
    libtcod.console_blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)
    libtcod.console_flush()


# animation of a hit from a main gun
def HitAnimation(hit_result):

    # shot missed, no animation just sound effect
    if hit_result == 'miss':
        PlaySound('main_gun_miss')
        return

    # smoke hit
    if hit_result == 'smoke_hit':
        PlaySound('smoke_hit')
        return

    # AP or HE hit
    PlaySound(hit_result)
    if not campaign.animations: return

    if hit_result == 'he_hit':
        animations = HE_HIT_ANIMATION
    else:
        animations = AP_HIT_ANIMATION
    x = MAP_CON_X + battle.target.x
    y = MAP_CON_Y + battle.target.y
    col = libtcod.console_get_char_background(map_con, battle.target.x, battle.target.y)
    libtcod.console_set_char_background(0, x, y, col)
    for (char, color, pause) in animations:
        libtcod.console_set_char(0, x, y, char)
        libtcod.console_set_char_foreground(0, x, y, color)
        libtcod.console_flush()
        Wait(pause)

    libtcod.console_flush()


# add one or more smoke factors into a map hex
def PlaceSmoke(target_hex, num_factors):
    battle.smoke_factors.append(SmokeFactor(target_hex.hx, target_hex.hy, num_factors))
    CalculateSmokeFactors()


# calculate active smokes factors for each hex
def CalculateSmokeFactors():
    # clear any existing smoke factors
    for map_hex in battle.maphexes:
        map_hex.smoke_factors = 0
    # recalculate
    for map_hex in battle.maphexes:
        for smoke_factor in battle.smoke_factors:
            if map_hex.hx == smoke_factor.hx and map_hex.hy == smoke_factor.hy:
                map_hex.smoke_factors += int(ceil(smoke_factor.num_factors))
    # redraw battle map
    PaintMapCon()


# handles a crew member in the turret throwing a smoke grenade out of an open hatch
def HandleSmokeGrenades():
    for crew_member in tank.crew:
        if crew_member.order == 'Throw Smoke Grenade':
            if crew_member.hatch != 'Open':
                PopUp(crew_member.name + " must have an open hatch to throw a smoke grenade.")
            elif tank.smoke_grenades == 0:
                PopUp('No smoke grenades remaining!')
            else:
                # throw the grenade!
                tank.smoke_grenades -= 1
                UpdateTankCon()
                Message(crew_member.name + ' throws a smoke grenade!')
                for map_hex in battle.maphexes:
                    if map_hex.hx == 0 and map_hex.hy == 0:
                        PlaceSmoke(map_hex, 0.5)
                        break


# handles firing the smoke mortar
def HandleSmokeMortar():
    for crew_member in tank.crew:
        if crew_member.order == 'Fire Smoke Mortar':
            if tank.smoke_bombs == 0:
                PopUp('No ammo remaining for smoke mortar!')
            else:
                tank.smoke_bombs -= 1
                UpdateTankCon()
                Message(crew_member.name + ' fires smoke from the mortar!')
                for map_hex in battle.maphexes:
                    if map_hex.rng == 0 and tank.turret_facing == map_hex.sector:
                        PlaceSmoke(map_hex, 1)
                        break


# returns total number of smoke factors between hexes
def GetSmokeFactors(hx1, hy1, hx2, hy2):

    # build list of hexes in line to target
    x1, y1 = Hex2Screen(hx1, hy1)
    x2, y2 = Hex2Screen(hx2, hy2)
    line = GetLine(x1, y1, x2, y2)

    hex_list = []
    for (x,y) in line:
        map_hex = Screen2Hex(x,y)
        if map_hex is not None:
            if map_hex not in hex_list:
                hex_list.append(map_hex)

    smoke_factors = 0
    for map_hex in hex_list:
        smoke_factors += map_hex.smoke_factors
    return smoke_factors


# set up restock ready rack interface
def SetupReadyRack():
    # only possible if loader is on correct order
    if GetCrewByPosition('Loader').order != 'Restock Ready Rack':
        return False
    return True


# attempt to set up tank to pivot
def SetupPivot():
    if GetCrewByPosition('Driver').order != 'Pivot Tank':
        return False
    # make sure tank can move
    if tank.bogged_down or tank.immobilized:
        PopUp('Tank is immobile and unable to pivot')
        return False
    # pivot can proceed - reset variable
    tank.new_facing = 4
    return True


# commits a pivot of the player tank, and rotates enemies and sector control around the
# player tank
def PivotTank():

    # apply effects of pivot
    # can still throw a track, but only on natural 12 followed by 5+ on D6
    # check for maintaining HD
    d1, d2, roll = Roll2D6()
    if roll == 12:
        if libtcod.random_get_int(0, 1, 6) >= 5:
            # thrown track
            PopUp('Your tank has thrown a track and is immobilized!')
            tank.moving = False
            tank.new_facing = 4
            tank.immobilized = True
            UpdateTankCon()
            RenderEncounter()
            return

    if tank.hull_down:
        # chance to maintain HD
        if roll <= 6:
            PopUp('Your tank pivots and maintains a Hull Down position.')
        else:
            PopUp('Your tank pivots but has lost its Hull Down position.')
            tank.hull_down = False

    tank.moving = True

    # determine number of sectors pivoted and direction to pivot
    # not strictly the most efficent system here: always assumes a clockwise rotation
    if tank.new_facing == 5:
        sector_distance = 1
        clockwise = True
    elif tank.new_facing == 0:
        sector_distance = 2
        clockwise = True
    elif tank.new_facing == 1:
        sector_distance = 3
        clockwise = True
    elif tank.new_facing == 2:
        sector_distance = 2
        clockwise = False
    else:
        sector_distance = 1
        clockwise = False

    for n in range(sector_distance):

        # rotate enemy units
        for unit in battle.enemy_units:
            unit.RotatePosition(clockwise)

        # rotate smoke factors if any on map
        if len(battle.smoke_factors) > 0:
            for obj in battle.smoke_factors:
                obj.RotatePosition(clockwise)

    # recalculate hex smoke factors
    CalculateSmokeFactors()

    # reset tank variable
    tank.new_facing = 4

    # redraw consoles and update screen
    UpdateTankCon()
    UpdateMapOverlay()
    RenderEncounter()


# resolve a movement order for the player tank
def MoveTank():

    crew = GetCrewByPosition('Driver')

    # if already pivoted, return
    if crew.order == 'Pivot Tank':
        return

    # if driver is dead, stunned, or unconscious, can't move tank
    # if tank is already moving, it stops
    if crew.NoActions():
        if tank.moving:
            PopUp('Your driver is incapacitated, and your tank rolls to a stop')
            tank.moving = False
            UpdateTankCon()
            RenderEncounter()
        return

    # if stopped and driver is on stop orders, don't check anything
    if crew.order == 'Stop' and not tank.moving: return

    # stop order is simple
    if crew.order == 'Stop':
        if tank.moving:
            PopUp('Your tank comes to a stop')
            tank.moving = False
        UpdateTankCon()
        RenderEncounter()
        return

    # unbog attempt
    if crew.order == 'Attempt Unbog' and tank.bogged_down:
        d1, d2, roll = Roll2D6()
        mod_roll = roll

        # skill check
        if crew.hatch == 'Open':
            if crew.SkillCheck('Tough Mudder'):
                mod_roll -= 2

        # driver buttoned up
        else:
            mod_roll += 2

        # HVSS
        if tank.stats.has_key('HVSS'):
            mod_roll -= 1

        # Commander Directing Movement from Open Hatch: -2
        # Commander Directing Movement from Vision Cupola: -1
        crew_member = GetCrewByPosition('Commander')
        if crew_member.order == 'Direct Movement':
            if crew_member.hatch == 'Open':
                if crew_member.SkillCheck('Driver Direction'):
                    mod = -3
                else:
                    mod = -2
                mod_roll += mod
            elif tank.stats.has_key('vision_cupola'):
                if crew_member.SkillCheck('Driver Direction'):
                    mod = -2
                else:
                    mod = -1
                mod_roll += mod

        if roll == 12 or mod_roll >= 11:
            PopUp('You have thrown a track trying to unbog your tank!')
            tank.bogged_down = False
            tank.immobilized = True
            UpdateTankCon()
            CrewTalk(random.choice(CREW_TALK_THROWN_TRACK), position_list='Driver')
        elif mod_roll <= 4:
            PopUp('Your tank is no longer bogged down')
            tank.bogged_down = False
            UpdateTankCon()
        else:
            PopUp('Driver is unable to unbog tank.')
        return

    # make sure tank can move
    # this shouldn't happen, since driver has to be on Stop or Attempt Unbog
    # order in these two cases
    if tank.bogged_down or tank.immobilized:
        Message('Tank is unable to move.')
        return

    # play sound effect
    PlaySound('sherman_movement')

    # check for move from stop
    move_from_stop = False
    if not tank.moving:
        move_from_stop = True

    # tank gets moving status for this turn at least
    # and loses hull down if it had it
    tank.moving = True
    tank.hull_down = False
    UpdateTankCon()
    RenderEncounter()

    # lose all acquired targets, ACs stop spotting player
    for unit in battle.enemy_units:
        unit.acquired = 0
        unit.acquired_player = 0
        if unit.unit_class == 'AC':
            unit.spotting_player = False

    # do movement roll
    d1, d2, roll = Roll2D6()

    # determine modifiers to roll
    mod_roll = roll

    # Commander Directing Movement from Open Hatch: -2
    # Commander Directing Movement from Vision Cupola: -1
    crew_member = GetCrewByPosition('Commander')
    if crew_member.order == 'Direct Movement':
        if crew_member.hatch == 'Open':
            if crew_member.SkillCheck('Driver Direction'):
                mod = -3
            else:
                mod = -2
            mod_roll += mod
        elif tank.stats.has_key('vision_cupola'):
            if crew_member.SkillCheck('Driver Direction'):
                mod = -2
            else:
                mod = -1
            mod_roll += mod

    # HVSS: -1
    if tank.stats.has_key('HVSS'):
        mod_roll -= 1

    # Driver Buttoned up: +2
    crew_member = GetCrewByPosition('Driver')
    if crew_member.hatch != 'Open':
        mod_roll += 2

    # check Drag Racer skill
    if move_from_stop:
        if crew_member.SkillCheck('Drag Racer'):
            mod_roll -= 1

    # weather effects
    if campaign.weather.ground == 'Snow':
        mod_roll += 1
    elif campaign.weather.ground in ['Mud', 'Deep Snow']:
        mod_roll += 2

    # if unmodified roll is 12, or if modified roll is 12 or more, tank has
    # possibility of throwing a track or bogging down
    if roll == 12 or mod_roll >= 12:
        d6_roll = libtcod.random_get_int(0, 1, 6)

        if d6_roll >= 5:
            # thrown track
            PopUp('Your tank has thrown a track and is immobilized!')
            tank.moving = False
            tank.immobilized = True
            UpdateTankCon()
            RenderEncounter()
            return
        elif d6_roll >= 3:
            # bogged down
            PopUp('Your tank becomes bogged down!')
            tank.moving = False
            tank.bogged_down = True
            UpdateTankCon()
            RenderEncounter()
            return

    # Check modified roll for Hull Down:
    if crew_member.order == 'Forward to Hull Down':

        # skill check
        if crew_member.SkillCheck('Eye for Cover'):
            mod_roll -= 2

        if campaign.day_map.player_node.node_type == 'F':
            mod_roll -= 2

        if mod_roll <= 4:
            PopUp('Your tank moves forward into a hull down position.')
            tank.hull_down = True
            UpdateTankCon()
            RenderEncounter()
        else:
            PopUp('Your tank moves forward but is unable to move into a hull down position.')

    elif crew_member.order == 'Reverse to Hull Down':

        # skill check
        if crew_member.SkillCheck('Eye for Cover'):
            mod_roll -= 1

        if campaign.day_map.player_node.node_type == 'F':
            mod_roll -= 2

        if mod_roll <= 3:
            PopUp('Your tank moves backward into a hull down position.')
            tank.hull_down = True
            UpdateTankCon()
            RenderEncounter()
        else:
            PopUp('Your tank moves backward but is unable to move into a hull down position.')

    # Effect on enemy units: Do a new 2D6 roll plus new modifiers
    d1, d2, roll = Roll2D6()

    # high-powered engine or light tank
    if 'M4A3' in tank.stats['vehicle_type']:
        roll -= 2
    elif tank.stats['vehicle_class'] == 'Light Tank':
        roll -= 2

    # duckbills
    if tank.stats.has_key('duckbills'):
        roll += 2

    # weather effects
    if campaign.weather.ground == 'Mud':
        roll += 4
    elif campaign.weather.ground in ['Snow', 'Deep Snow']:
        roll += 2

    # if equal to target number, enemy facings are recalculated, less than, enemy units and
    # smoke are moved
    if crew_member.order == 'Reverse to Hull Down':
        target_score = 5
        move_dist = -1
    elif crew_member.order == 'Forward to Hull Down':
        target_score = 6
        move_dist = 1
    elif crew_member.order == 'Reverse':
        target_score = 7
        move_dist = -1
    else:
        # forward
        target_score = 8
        move_dist = 1

    if roll < target_score:
        PopUp('Your tank has moved far enough that enemies are in new positions.')
        for unit in battle.enemy_units:
            if not unit.alive: continue
            unit.YMove(move_dist)
            # reset spotting, hidden, and target acquired
            unit.spotted = False
            unit.hidden = False
            unit.acquired = 0
            unit.acquired_player = 0
            if unit.unit_class == 'AC':
                unit.spotting_player = False

        for obj in battle.smoke_factors:
            obj.YMove(move_dist)
        CalculateSmokeFactors()
        # re-draw enemy units and smoke in new positions
        UpdateMapOverlay()

        # check for changed facings
        for unit in battle.enemy_units:
            if not unit.alive: continue
            if unit.SetFacing():
                text = unit.GetDesc() + ' now on ' + unit.facing + ' facing'
                ShowLabel(unit.x+MAP_CON_X, unit.y+MAP_CON_Y, text)

    elif roll == target_score:
        for unit in battle.enemy_units:
            if not unit.alive: continue
            if unit.SetFacing():
                text = unit.GetDesc() + ' now on ' + unit.facing + ' facing'
                ShowLabel(unit.x+MAP_CON_X, unit.y+MAP_CON_Y, text)
    else:
        PopUp('Your tank does not move far enough to affect enemy positions.')


# see if we are just rotating the tank's turret (not firing main gun)
def SetupRotateTurret():
    crew_member = GetCrewByPosition('Gunner')
    if crew_member.order != 'Rotate Turret':
        return False
    tank.old_t_facing = tank.turret_facing        # record current turret facing
    return True


# rotate the main gun turret one sector
def RotateTurret(clockwise):

    # check for turret traverse gear broken
    if 'Turret Traverse Malfunction' in tank.damage_list: return
    if 'Turret Traverse Broken' in tank.damage_list: return

    if clockwise:
        tank.turret_facing += 1
        if tank.turret_facing > 5:
            tank.turret_facing = 0
    else:
        tank.turret_facing -= 1
        if tank.turret_facing < 0:
            tank.turret_facing = 5

    # if current target is no longer valid, choose a new one
    if battle.target is not None:
        if battle.phase == 'Fire Main Gun':
            if tank.turret_facing != battle.target.map_hex.sector:
                SelectNextTarget()
        elif battle.phase == 'Fire MGs' and tank.active_mg == 0:
                SelectNextTarget()

    # otherwise, try to get a new target
    else:
        SelectNextTarget()

    UpdateMapOverlay()
    RenderEncounter()


# display menu in tank console to set order for a crew member
def DisplayCrewOrders():

    # get selected crew member
    crewman = battle.selected_crew

    # if no order selected yet, select current order by default
    if battle.selected_order == None:
        n = 0
        for order in crewman.orders_list:
            if order.name == crewman.order:
                battle.selected_order = n
                break
            n += 1
        # can't find current order, select first one instead
        if battle.selected_order == None:
            battle.selected_order = 0

    # display menu
    libtcod.console_print(tank_con, 1, 1, 'Set Crew Order for:')

    # display current crew member info
    libtcod.console_set_default_background(tank_con, ROW_COLOR)
    libtcod.console_rect(tank_con, 1, 3, TANK_CON_WIDTH-2, 2, False, flag=libtcod.BKGND_SET)
    libtcod.console_set_default_background(tank_con, libtcod.black)
    libtcod.console_print(tank_con, 1, 2, 'Crewman             Position     Order        Hatch  Spot')
    info_list = crewman.GetInfo()
    libtcod.console_print(tank_con, 1, 3, info_list[0])
    libtcod.console_print(tank_con, 21, 3, info_list[1])

    # order might be long, so split it up
    lines = wrap(info_list[2], 11)
    libtcod.console_print(tank_con, 34, 3, lines[0])
    if len(lines) > 1:
        libtcod.console_print(tank_con, 34, 4, lines[1])

    libtcod.console_print(tank_con, 47, 3, info_list[3])

    # spot might be long too
    lines = wrap(info_list[4], 11)
    libtcod.console_print(tank_con, 54, 3, lines[0])
    if len(lines) > 1:
        libtcod.console_print(tank_con, 54, 4, lines[1])

    # nickname
    if info_list[5] != '':
        libtcod.console_print(tank_con, 2, 4, '"' + info_list[5] + '"')

    # display list of order names
    y = 6
    n = 0
    dy = 15
    for order in crewman.orders_list:
        # if order is selected then highlight
        if battle.selected_order == n:
            libtcod.console_set_default_background(tank_con, SELECTED_COLOR)
        libtcod.console_print_ex(tank_con, 1, y, libtcod.BKGND_SET, libtcod.LEFT, order.name)
        libtcod.console_set_default_background(tank_con, libtcod.black)

        # if order is selected then display order description
        # and spot effects
        if battle.selected_order == n:
            # split up the description string
            lines = wrap(order.desc, TANK_CON_WIDTH-23, subsequent_indent = ' ')
            for line in lines:
                libtcod.console_print(tank_con, 1, dy, line)
                dy += 1
            if order.spot:
                text = 'May spot'
            else:
                text = 'May not spot'
            text += ' next turn'
            libtcod.console_print(tank_con, 1, dy, text)
        y += 1
        n += 1

    # display instructions for selecting and issuing orders
    dy += 2
    for line in ORDER_INFO:
        libtcod.console_print(tank_con, 1, dy, line)
        dy+=1


################################################################################
#                          Console Drawing and Updating                        #
################################################################################

# display weather conditions to given console
def DisplayWeather(console, x, y):
    # cloud cover
    if campaign.weather.clouds == 'Clear':
        libtcod.console_set_default_background(console, CLEAR_SKY_COLOR)
        libtcod.console_set_default_foreground(console, libtcod.white)
    else:
        libtcod.console_set_default_background(console, OVERCAST_COLOR)
        libtcod.console_set_default_foreground(console, libtcod.dark_grey)
    libtcod.console_rect(console, x, y, 10, 3, False, flag=libtcod.BKGND_SET)
    libtcod.console_print_ex(console, x+5, y, libtcod.BKGND_SET, libtcod.CENTER, campaign.weather.clouds)

    # precipitation
    if campaign.weather.precip in ['Rain', 'Snow']:
        libtcod.console_set_default_foreground(console, libtcod.white)
        libtcod.console_print_ex(console, x+5, y+1, libtcod.BKGND_SET, libtcod.CENTER, campaign.weather.precip)

    # fog
    if campaign.weather.fog:
        libtcod.console_set_default_background(console, libtcod.light_grey)
        libtcod.console_set_default_foreground(console, libtcod.white)
        libtcod.console_rect(console, x, y+2, 10, 1, False, flag=libtcod.BKGND_SET)
        libtcod.console_print_ex(console, x+5, y+2, libtcod.BKGND_SET, libtcod.CENTER, 'Fog')

    # ground cover
    libtcod.console_set_default_foreground(console, libtcod.black)
    if campaign.weather.ground == 'Dry':
        libtcod.console_set_default_background(console, OPEN_GROUND_COLOR)
    elif campaign.weather.ground == 'Mud':
        libtcod.console_set_default_background(console, MUD_COLOR)
    else:
        libtcod.console_set_default_background(console, libtcod.white)
    libtcod.console_rect(console, x, y+3, 10, 1, False, flag=libtcod.BKGND_SET)
    libtcod.console_print_ex(console, x+5, y+3, libtcod.BKGND_SET, libtcod.CENTER, campaign.weather.ground)


# paint the encounter map console
def PaintMapCon():
    libtcod.console_set_default_background(map_con, libtcod.black)
    libtcod.console_clear(map_con)

    # draw map hexes, including player hex 0,0
    libtcod.console_set_default_foreground(map_con, HEX_EDGE_COLOR)
    for map_hex in battle.maphexes:
        if map_hex.rng == 2:
            libtcod.console_set_default_background(map_con, libtcod.Color(80, 120, 80))
        elif map_hex.rng == 1:
            libtcod.console_set_default_background(map_con, libtcod.Color(90, 130, 90))
        else:
            libtcod.console_set_default_background(map_con, libtcod.Color(100, 140, 100))
        if map_hex.hx == 0 and map_hex.hy == 0:
            libtcod.console_set_default_foreground(map_con, libtcod.black)
        DrawHex(map_con, map_hex.x, map_hex.y)

    libtcod.console_set_default_background(map_con, libtcod.black)

    # if fog or falling snow, display lack of sight for medium and long range hexes
    if campaign.weather.fog or campaign.weather.precip == 'Snow':

        for map_hex in battle.maphexes:
            if map_hex.rng > 0:
                libtcod.console_set_default_background(map_con, libtcod.Color(180, 180, 180))
                libtcod.console_set_default_foreground(map_con, HEX_EDGE_COLOR)
                DrawHex(map_con, map_hex.x, map_hex.y)
                libtcod.console_set_default_background(map_con, libtcod.black)

    # draw smoke hexes overtop
    for map_hex in battle.maphexes:

        # skip if not visible anyway
        if campaign.weather.fog or campaign.weather.precip == 'Snow':
            if map_hex.rng > 0: continue

        if map_hex.smoke_factors > 0:
            # calculate background colour to use
            c = 120 + (map_hex.smoke_factors*20)
            # limit to light grey!
            if c > 220:
                c = 220
            col = libtcod.Color(c, c, c)
            libtcod.console_set_default_background(map_con, col)

            if map_hex.hx == 0 and map_hex.hy == 0:
                libtcod.console_set_default_foreground(map_con, libtcod.black)
            else:
                libtcod.console_set_default_foreground(map_con, HEX_EDGE_COLOR)

            # paint smoke hex
            DrawHex(map_con, map_hex.x, map_hex.y)

            libtcod.console_set_default_background(map_con, libtcod.black)

    libtcod.console_set_default_foreground(map_con, libtcod.black)

    # draw zone boundaries
    def DrawBoundaryLine(x1, y1, x2, y2):
        char = '/'
        if y1 == y2:
            char = '-'
        elif y1 < y2:
            if x1 < x2:
                char = '\\'
        else:
            if x1 > x2:
                char = '\\'
        line = GetLine(x1, y1, x2, y2)
        # skip first and last location
        for (x, y) in line[1:-1]:
            libtcod.console_put_char(map_con, x, y, char, flag=libtcod.BKGND_DEFAULT)
        (x,y) = line[-1]
        libtcod.console_put_char(map_con, x, y, '|', flag=libtcod.BKGND_DEFAULT)

    # sectors 5 and 0
    DrawBoundaryLine(MAP_X0+6, MAP_Y0, MAP_X0+12, MAP_Y0)
    DrawBoundaryLine(MAP_X0+12, MAP_Y0, MAP_X0+15, MAP_Y0+3)
    DrawBoundaryLine(MAP_X0+15, MAP_Y0+3, MAP_X0+21, MAP_Y0+3)
    DrawBoundaryLine(MAP_X0+21, MAP_Y0+3, MAP_X0+24, MAP_Y0)
    DrawBoundaryLine(MAP_X0+24, MAP_Y0, MAP_X0+30, MAP_Y0)

    # sectors 0 and 1
    DrawBoundaryLine(MAP_X0+3, MAP_Y0+3, MAP_X0+6, MAP_Y0+6)
    DrawBoundaryLine(MAP_X0+6, MAP_Y0+6, MAP_X0+3, MAP_Y0+9)
    DrawBoundaryLine(MAP_X0+3, MAP_Y0+9, MAP_X0+6, MAP_Y0+12)
    DrawBoundaryLine(MAP_X0+6, MAP_Y0+12, MAP_X0+12, MAP_Y0+12)
    DrawBoundaryLine(MAP_X0+12, MAP_Y0+12, MAP_X0+15, MAP_Y0+15)

    # sectors 1 and 2
    DrawBoundaryLine(MAP_X0-3, MAP_Y0+3, MAP_X0-6, MAP_Y0+6)
    DrawBoundaryLine(MAP_X0-6, MAP_Y0+6, MAP_X0-3, MAP_Y0+9)
    DrawBoundaryLine(MAP_X0-3, MAP_Y0+9, MAP_X0-6, MAP_Y0+12)
    DrawBoundaryLine(MAP_X0-6, MAP_Y0+12, MAP_X0-12, MAP_Y0+12)
    DrawBoundaryLine(MAP_X0-12, MAP_Y0+12, MAP_X0-15, MAP_Y0+15)

    # sectors 2 and 3
    DrawBoundaryLine(MAP_X0-6, MAP_Y0, MAP_X0-12, MAP_Y0)
    DrawBoundaryLine(MAP_X0-12, MAP_Y0, MAP_X0-15, MAP_Y0+3)
    DrawBoundaryLine(MAP_X0-15, MAP_Y0+3, MAP_X0-21, MAP_Y0+3)
    DrawBoundaryLine(MAP_X0-21, MAP_Y0+3, MAP_X0-24, MAP_Y0)
    DrawBoundaryLine(MAP_X0-24, MAP_Y0, MAP_X0-30, MAP_Y0)

    # sectors 3 and 4
    DrawBoundaryLine(MAP_X0-3, MAP_Y0-3, MAP_X0-6, MAP_Y0-6)
    DrawBoundaryLine(MAP_X0-6, MAP_Y0-6, MAP_X0-12, MAP_Y0-6)
    DrawBoundaryLine(MAP_X0-12, MAP_Y0-6, MAP_X0-15, MAP_Y0-9)
    DrawBoundaryLine(MAP_X0-15, MAP_Y0-9, MAP_X0-12, MAP_Y0-12)
    DrawBoundaryLine(MAP_X0-12, MAP_Y0-12, MAP_X0-15, MAP_Y0-15)

    # sectors 4 and 5
    DrawBoundaryLine(MAP_X0+3, MAP_Y0-3, MAP_X0+6, MAP_Y0-6)
    DrawBoundaryLine(MAP_X0+6, MAP_Y0-6, MAP_X0+12, MAP_Y0-6)
    DrawBoundaryLine(MAP_X0+12, MAP_Y0-6, MAP_X0+15, MAP_Y0-9)
    DrawBoundaryLine(MAP_X0+15, MAP_Y0-9, MAP_X0+12, MAP_Y0-12)
    DrawBoundaryLine(MAP_X0+12, MAP_Y0-12, MAP_X0+15, MAP_Y0-15)


# draw the encounter map overlay console
def UpdateMapOverlay(skip_los=False):

    # reset console colors and clear
    libtcod.console_set_default_foreground(overlay_con, libtcod.black)
    libtcod.console_set_default_background(overlay_con, KEY_COLOR)
    libtcod.console_clear(overlay_con)

    # draw player tank
    tank.DrawMe()

    # draw enemy units
    for unit in battle.enemy_units:
        unit.DrawMe()

    libtcod.console_set_default_foreground(overlay_con, libtcod.white)
    libtcod.console_set_default_background(overlay_con, libtcod.black)

    # highlight spotting sector if in set spot sector phase
    if battle.phase == 'Set Spot Sectors' and battle.selected_crew is not None:
        if battle.selected_crew.spot_sector == 0:
            for (x, y) in GetLine(MAP_X0+2, MAP_Y0+1, 67, 35):
                col = libtcod.console_get_char_background(map_con, x, y)
                libtcod.console_put_char_ex(overlay_con, x, y, 250, libtcod.white, col)
        elif battle.selected_crew.spot_sector == 1:
            for (x, y) in GetLine(MAP_X0, MAP_Y0+2, 36, 46):
                col = libtcod.console_get_char_background(map_con, x, y)
                libtcod.console_put_char_ex(overlay_con, x, y, 250, libtcod.white, col)
        elif battle.selected_crew.spot_sector == 2:
            for (x, y) in GetLine(MAP_X0-2, MAP_Y0+1, 5, 35):
                col = libtcod.console_get_char_background(map_con, x, y)
                libtcod.console_put_char_ex(overlay_con, x, y, 250, libtcod.white, col)
        elif battle.selected_crew.spot_sector == 3:
            for (x, y) in GetLine(MAP_X0-2, MAP_Y0-1, 5, 15):
                col = libtcod.console_get_char_background(map_con, x, y)
                libtcod.console_put_char_ex(overlay_con, x, y, 250, libtcod.white, col)
        elif battle.selected_crew.spot_sector == 4:
            for (x, y) in GetLine(MAP_X0, MAP_Y0-2, 36, 4):
                col = libtcod.console_get_char_background(map_con, x, y)
                libtcod.console_put_char_ex(overlay_con, x, y, 250, libtcod.white, col)
        elif battle.selected_crew.spot_sector == 5:
            for (x, y) in GetLine(MAP_X0+2, MAP_Y0-1, 67, 15):
                col = libtcod.console_get_char_background(map_con, x, y)
                libtcod.console_put_char_ex(overlay_con, x, y, 250, libtcod.white, col)

    # draw LoS if in Fire Main Gun or Fire MGs phase
    if battle.phase in ['Fire Main Gun', 'Fire MGs'] and battle.target is not None and not skip_los:
        line = GetLine(MAP_X0, MAP_Y0, battle.target.x, battle.target.y)
        for (x,y) in line[2:-1]:
            col = libtcod.console_get_char_background(map_con, x, y)
            libtcod.console_put_char_ex(overlay_con, x, y, 250, libtcod.white, col)

    # draw weather conditions display in top right corner
    DisplayWeather(overlay_con, MAP_CON_WIDTH-10, 1)

    libtcod.console_set_default_foreground(overlay_con, libtcod.white)
    libtcod.console_set_default_background(overlay_con, libtcod.black)

    # TODO
    # display symbol legend on map

    # Units
    libtcod.console_print_ex(overlay_con, 1, 41, libtcod.BKGND_SET, libtcod.LEFT, 'Unit type:')
    libtcod.console_print_ex(overlay_con, 1, 42, libtcod.BKGND_SET, libtcod.LEFT, '----------')

    libtcod.console_put_char(overlay_con, 1, 43, libtcod.CHAR_RADIO_UNSET, flag=libtcod.BKGND_SET)
    libtcod.console_print_ex(overlay_con, 4, 43, libtcod.BKGND_SET, libtcod.LEFT, 'Tank')

    libtcod.console_put_char(overlay_con, 1, 44, 'X', flag=libtcod.BKGND_SET)
    libtcod.console_print_ex(overlay_con, 4, 44, libtcod.BKGND_SET, libtcod.LEFT, 'Anti Tank Gun')

    libtcod.console_put_char(overlay_con, 1, 45, "#", flag=libtcod.BKGND_SET)
    libtcod.console_print_ex(overlay_con, 4, 45, libtcod.BKGND_SET, libtcod.LEFT, 'Self Propelled Gun')

    libtcod.console_put_char(overlay_con, 1, 46, libtcod.CHAR_BULLET_INV, flag=libtcod.BKGND_SET)
    libtcod.console_print_ex(overlay_con, 4, 46, libtcod.BKGND_SET, libtcod.LEFT, 'Armoured Personel Carrier')

    libtcod.console_put_char(overlay_con, 1, 47, libtcod.CHAR_RADIO_SET, flag=libtcod.BKGND_SET)
    libtcod.console_print_ex(overlay_con, 4, 47, libtcod.BKGND_SET, libtcod.LEFT, 'Armoured Carrier')

    libtcod.console_put_char(overlay_con, 1, 48, libtcod.CHAR_BLOCK1, flag=libtcod.BKGND_SET)
    libtcod.console_print_ex(overlay_con, 4, 48, libtcod.BKGND_SET, libtcod.LEFT, 'Light Infantry')

    libtcod.console_put_char(overlay_con, 1, 49, 'x', flag=libtcod.BKGND_SET)
    libtcod.console_print_ex(overlay_con, 4, 49, libtcod.BKGND_SET, libtcod.LEFT, 'Machine Gun')

    libtcod.console_put_char(overlay_con, 1, 50, libtcod.CHAR_BULLET_SQUARE, flag=libtcod.BKGND_SET)
    libtcod.console_print_ex(overlay_con, 4, 50, libtcod.BKGND_SET, libtcod.LEFT, 'Truck')

    # Tactical situation
    #if self.terrain == 'Hull Down':
    #    char = libtcod.CHAR_ARROW2_N
    #elif self.terrain == 'Building':
    #    char = libtcod.CHAR_DVLINE
    #elif self.terrain == 'Woods':
    #    char = libtcod.CHAR_SPADE

    libtcod.console_print_ex(overlay_con, 60, 41, libtcod.BKGND_SET, libtcod.LEFT, 'Situation:')
    libtcod.console_print_ex(overlay_con, 60, 42, libtcod.BKGND_SET, libtcod.LEFT, '----------')

    libtcod.console_put_char(overlay_con, 60, 43, libtcod.CHAR_ARROW2_N, flag=libtcod.BKGND_SET)
    libtcod.console_put_char(overlay_con, 61, 43, ' ', flag=libtcod.BKGND_SET)
    libtcod.console_put_char(overlay_con, 62, 43, libtcod.CHAR_ARROW2_N, flag=libtcod.BKGND_SET)
    libtcod.console_print_ex(overlay_con, 64, 43, libtcod.BKGND_SET, libtcod.LEFT, 'Hull Down')

    libtcod.console_put_char(overlay_con, 60, 44, libtcod.CHAR_DVLINE, flag=libtcod.BKGND_SET)
    libtcod.console_put_char(overlay_con, 61, 44, ' ', flag=libtcod.BKGND_SET)
    libtcod.console_put_char(overlay_con, 62, 44, libtcod.CHAR_DVLINE, flag=libtcod.BKGND_SET)
    libtcod.console_print_ex(overlay_con, 64, 44, libtcod.BKGND_SET, libtcod.LEFT, 'Building')

    libtcod.console_put_char(overlay_con, 60, 45, libtcod.CHAR_SPADE, flag=libtcod.BKGND_SET)
    libtcod.console_put_char(overlay_con, 61, 45, ' ', flag=libtcod.BKGND_SET)
    libtcod.console_put_char(overlay_con, 62, 45, libtcod.CHAR_SPADE, flag=libtcod.BKGND_SET)
    libtcod.console_print_ex(overlay_con, 64, 45, libtcod.BKGND_SET, libtcod.LEFT, 'Woods')

    # display current round number
    libtcod.console_print_ex(overlay_con, int(MAP_CON_WIDTH/2), 0, libtcod.BKGND_SET,
        libtcod.CENTER, 'Round ' + str(battle.rounds_passed))

    # display current turn phase if any
    if battle.phase != 'None':
        libtcod.console_print_ex(overlay_con, int(MAP_CON_WIDTH/2), 1, libtcod.BKGND_SET, libtcod.CENTER, battle.phase + ' Phase')

    # display MG selections if firing MGs
    if battle.phase == 'Fire MGs':
        libtcod.console_set_default_foreground(overlay_con, GREYED_COLOR)
        if tank.coax_mg_can_fire:
            if tank.active_mg == 0:
                libtcod.console_set_default_foreground(overlay_con, SELECTED_COLOR)
            else:
                libtcod.console_set_default_foreground(overlay_con, libtcod.white)
        libtcod.console_print_ex(overlay_con, 2, 1, libtcod.BKGND_SET, libtcod.LEFT, 'Co-ax MG')
        libtcod.console_set_default_foreground(overlay_con, GREYED_COLOR)
        if tank.bow_mg_can_fire:
            if tank.active_mg == 1:
                libtcod.console_set_default_foreground(overlay_con, SELECTED_COLOR)
            else:
                libtcod.console_set_default_foreground(overlay_con, libtcod.white)
        libtcod.console_print_ex(overlay_con, 2, 2, libtcod.BKGND_SET, libtcod.LEFT, 'Bow MG')
        libtcod.console_set_default_foreground(overlay_con, GREYED_COLOR)
        if tank.aa_mg_can_fire:
            if tank.active_mg == 2:
                libtcod.console_set_default_foreground(overlay_con, SELECTED_COLOR)
            else:
                libtcod.console_set_default_foreground(overlay_con, libtcod.white)
        libtcod.console_print_ex(overlay_con, 2, 3, libtcod.BKGND_SET, libtcod.LEFT, 'AA MG')

    # display reminder if spotting/combat restricted
    if campaign.weather.fog or campaign.weather.precip == 'Snow':
        libtcod.console_print_ex(overlay_con, int(MAP_CON_WIDTH/2), MAP_CON_HEIGHT-1, libtcod.BKGND_SET, libtcod.CENTER, 'Fog/Snow: Spotting/Combat at close range only')


# draw or update the map info console
def UpdateMapInfoCon(mx, my):
    libtcod.console_clear(map_info_con)

    # make sure mouse cursor is over map window
    if mx < MAP_CON_X or my > MAP_CON_HEIGHT:
        libtcod.console_print_ex(map_info_con, int(MAP_INFO_CON_WIDTH/2), 1,
            libtcod.BKGND_NONE, libtcod.CENTER, 'Mouseover a unit for information')
        return

    # adjust for offset
    mx -= MAP_CON_X
    my -= 2

    # if we're over ourself
    if mx == MAP_X0 and my == MAP_Y0:
        text = 'M4 Sherman "' + tank.name + '"'
        libtcod.console_print_ex(map_info_con, int(MAP_INFO_CON_WIDTH/2), 1, libtcod.BKGND_NONE, libtcod.CENTER, text)
        return

    # check for enemy unit under cursor
    for unit in battle.enemy_units:
        if not unit.alive: continue
        if unit.x == mx and unit.y == my:

            # print info on this unit
            x = int(MAP_INFO_CON_WIDTH/2)
            y = 0

            # basic description
            text = unit.GetDesc()
            libtcod.console_print(map_info_con, x, y, text)
            y += 1

            # morale status
            text = ''
            if unit.pinned:
                text = 'Pinned'
            elif unit.stunned:
                text = 'Stunned'
            libtcod.console_set_default_foreground(map_info_con, libtcod.light_red)
            libtcod.console_print(map_info_con, x, y, text)
            libtcod.console_set_default_foreground(map_info_con, libtcod.white)
            y += 1

            # range and sector
            rng = unit.map_hex.rng
            if rng == 2:
                text = 'Long'
            elif rng == 1:
                text = 'Medium'
            else:
                text = 'Short'
            text += ' Range, '

            if unit.map_hex.sector == 0:
                text = 'Rear Right '
            elif unit.map_hex.sector == 1:
                text = 'Rear '
            elif unit.map_hex.sector == 2:
                text = 'Rear Left '
            elif unit.map_hex.sector == 3:
                text = 'Front Left '
            elif unit.map_hex.sector == 4:
                text = 'Front '
            elif unit.map_hex.sector == 5:
                text = 'Front Right '
            text += 'Sector'
            libtcod.console_print(map_info_con, x, y, text)
            y += 1

            # if hidden or not spotted, no more info displayed
            if unit.hidden or not unit.spotted:
                return

            # emplaced, movement, or immobile status
            if unit.unit_class == 'AT_GUN':
                text = 'Emplaced'
            elif unit.moving:
                text = 'Moving'
            else:
                if unit.immobile:
                    text = 'Immobile'
                else:
                    text = 'Stationary'

            # terrain
            text += ' in ' + unit.terrain
            libtcod.console_print(map_info_con, x, y, text)
            y+=1

            # facing if applicable
            if unit.facing != '':
                text = unit.facing + ' Facing'
                libtcod.console_print(map_info_con, x, y, text)
                y+=1

            # acquired target / acquired player target
            text = ''
            if unit.acquired > 0:
                text += 'Acquired Target: ' + str(unit.acquired)
            if unit.acquired > 0 and unit.acquired_player > 0:
                text += ' ; '
            if unit.acquired_player > 0:
                text += 'Acquired Player: ' + str(unit.acquired_player)
            if unit.unit_class == 'AC':
                if unit.spotting_player:
                    text += 'Spotting Player'
            if text != '':
                libtcod.console_print(map_info_con, x, y, text)
                y+=1

            # display unit info reminder if doesn't need to be identified first
            if not (unit.unit_class in ['TANK', 'SPG', 'AT_GUN'] and not unit.identified):
                libtcod.console_print(map_info_con, x, MAP_INFO_CON_HEIGHT-1, 'Right-click for more info')

            # unit info displayed, so return
            return

    # no unit found, display instruction text
    libtcod.console_print_ex(map_info_con, int(MAP_INFO_CON_WIDTH/2), 1,
        libtcod.BKGND_NONE, libtcod.CENTER, 'Mouseover a unit for information')


# write current messages to message console
def UpdateMsgCon():
    libtcod.console_clear(msg_con)
    y=0
    for (line, color) in battle.messages:
        libtcod.console_set_default_foreground(msg_con, color)
        libtcod.console_print(msg_con, 0, y, line)
        y += 1


# draw tank info to tank info console
# used in encounters as well as in the campaign day view
def UpdateTankCon():
    libtcod.console_clear(tank_con)

    # if we're currently in issue orders input mode, show selected crew member
    # and possible orders instead
    if battle is not None:
        if battle.phase == 'Issue Order':
            DisplayCrewOrders()
            return

    ##### Tank Name #####
    libtcod.console_set_default_foreground(tank_con, HIGHLIGHT_COLOR)
    libtcod.console_print(tank_con, 1, 1, tank.name)

    ##### Tank Model Name, and Nickname if any #####
    libtcod.console_set_default_foreground(tank_con, libtcod.white)
    text = tank.stats['vehicle_type']
    if 'nickname' in tank.stats:
        text += ' "' + tank.stats['nickname'] + '"'
    # note if current tank has HVSS
    if tank.stats.has_key('HVSS'):
        text += ' (HVSS)'
    libtcod.console_print(tank_con, 1, 2, text)

    ##### Tank Status if in Battle Encounter #####
    if battle is not None:
        libtcod.console_set_default_foreground(tank_con, libtcod.light_grey)
        text = ''
        if tank.lead_tank:
            text += 'Lead Tank, '
        if tank.moving:
            text += 'Moving'
        else:
            text += 'Stopped'
        if tank.hull_down:
            libtcod.console_set_default_foreground(tank_con, libtcod.light_green)
            text += ', Hull Down'
        if tank.bogged_down:
            libtcod.console_set_default_foreground(tank_con, libtcod.red)
            text += ', Bogged Down'
        if tank.immobilized:
            libtcod.console_set_default_foreground(tank_con, libtcod.red)
            text += ', Immobilized'
        libtcod.console_print(tank_con, 1, 3, text)
        libtcod.console_set_default_foreground(tank_con, libtcod.white)

    ##### Ammo Load Info - Displayed at Top Right of Console #####
    libtcod.console_set_alignment(tank_con, libtcod.RIGHT)
    x = TANK_CON_WIDTH - 10
    total_g = 0
    total_rr = 0
    for ammo_type in reversed(AMMO_TYPES):
        if ammo_type in tank.general_ammo:
            libtcod.console_set_default_foreground(tank_con, libtcod.light_grey)
            libtcod.console_print(tank_con, x, 1, ammo_type)
            libtcod.console_set_default_foreground(tank_con, libtcod.white)
            text = str(tank.general_ammo[ammo_type])
            libtcod.console_print(tank_con, x, 2, text)
            total_g += tank.general_ammo[ammo_type]
            text = str(tank.rr_ammo[ammo_type])
            libtcod.console_print(tank_con, x, 3, text)
            total_rr += tank.rr_ammo[ammo_type]

            # check for rare ammo supplies
            if campaign.resupply:
                text = ''
                if ammo_type == 'HCBI' and campaign.hcbi > 0:
                    text = str(campaign.hcbi)
                elif ammo_type == 'HVAP' and campaign.hvap > 0:
                    text = str(campaign.hvap)
                elif ammo_type == 'APDS' and campaign.apds > 0:
                    text = str(campaign.apds)
                if text != '':
                    text = '(' + text + ')'
                    libtcod.console_print(tank_con, x+1, 0, text)
            x -= (len(ammo_type)+2)
    libtcod.console_set_default_background(tank_con, ROW_COLOR)
    libtcod.console_rect(tank_con, x-4, 1, TANK_CON_WIDTH-x+3, 1, False, flag=libtcod.BKGND_SET)
    libtcod.console_set_default_background(tank_con, libtcod.black)
    libtcod.console_set_default_foreground(tank_con, libtcod.light_grey)
    libtcod.console_print(tank_con, x, 1, 'Ammo')
    libtcod.console_print(tank_con, x, 2, 'General')
    libtcod.console_print(tank_con, x, 3, 'Ready Rack')
    if campaign.resupply and battle is None:
        libtcod.console_print(tank_con, x-5, 1, 'Resupplying')

    # display current total and maximum ammo load
    x = TANK_CON_WIDTH-2
    libtcod.console_print(tank_con, x, 1, 'Max')
    libtcod.console_set_default_foreground(tank_con, libtcod.white)
    text = str(total_g) + '/' + str(tank.stats['main_gun_rounds'])
    libtcod.console_print(tank_con, x, 2, text)
    text = str(total_rr) + '/' + str(tank.stats['rr_size'])
    libtcod.console_print(tank_con, x, 3, text)
    libtcod.console_set_alignment(tank_con, libtcod.LEFT)

    ##### Main Gun Info #####
    libtcod.console_set_default_background(tank_con, ROW_COLOR)
    libtcod.console_rect(tank_con, 1, 5, TANK_CON_WIDTH-2, 2, False, flag=libtcod.BKGND_SET)
    libtcod.console_set_default_background(tank_con, libtcod.black)

    libtcod.console_set_default_foreground(tank_con, libtcod.light_grey)
    libtcod.console_print(tank_con, 1, 5, 'Main Gun:')
    libtcod.console_set_default_foreground(tank_con, libtcod.white)

    # generate display text for gun
    text = tank.stats['main_gun'].replace('L', '') + 'mm'
    libtcod.console_print(tank_con, 11, 5, text)

    libtcod.console_set_default_foreground(tank_con, libtcod.light_grey)
    libtcod.console_print(tank_con, 18, 5, 'Gun Load:')
    libtcod.console_set_default_foreground(tank_con, libtcod.white)
    if tank.ammo_load == 'None':
        libtcod.console_set_default_foreground(tank_con, libtcod.red)
    libtcod.console_print(tank_con, 28, 5, tank.ammo_load)
    libtcod.console_set_default_foreground(tank_con, libtcod.white)

    libtcod.console_set_default_foreground(tank_con, libtcod.light_grey)
    libtcod.console_print(tank_con, 35, 5, 'Ammo Reload:')
    libtcod.console_set_default_foreground(tank_con, libtcod.white)
    libtcod.console_print(tank_con, 48, 5, tank.ammo_reload)

    libtcod.console_set_default_foreground(tank_con, libtcod.light_grey)
    libtcod.console_print(tank_con, 55, 5, 'From:')
    libtcod.console_set_default_foreground(tank_con, libtcod.white)
    if tank.use_rr:
        text = 'Ready Rack'
    else:
        text = 'General'
    libtcod.console_print(tank_con, 61, 5, text)

    ##### Misc Stats #####
    libtcod.console_set_default_foreground(tank_con, libtcod.light_grey)
    libtcod.console_print(tank_con, 1, 6, 'Smoke Grenades:')
    libtcod.console_set_default_foreground(tank_con, libtcod.white)
    libtcod.console_print(tank_con, 17, 6, str(tank.smoke_grenades))
    if tank.stats.has_key('smoke_mortar'):
        libtcod.console_set_default_foreground(tank_con, libtcod.light_grey)
        libtcod.console_print(tank_con, 20, 6, 'Smoke Bombs:')
        libtcod.console_set_default_foreground(tank_con, libtcod.white)
        libtcod.console_print(tank_con, 33, 6, str(tank.smoke_bombs))

    ##### Damage Info #####
    text = ''

    # display if took a penetrating hit
    if tank.swiss_cheese:
        text += 'Suffered Penetrating Hit! '

    for d in tank.damage_list:
        if text != '':
            text += '; '
        text += d
    if text == '':
        libtcod.console_set_default_foreground(tank_con, libtcod.light_grey)
        libtcod.console_print(tank_con, 1, 8, 'No damage')
    else:
        libtcod.console_set_default_foreground(tank_con, libtcod.red)
        lines = wrap(text, TANK_CON_WIDTH-2)
        y = 7
        for line in lines:
            libtcod.console_print(tank_con, 1, y, line)
            y += 1
            if y == 11: break

    ##### Crew Info #####
    y = 12
    libtcod.console_set_default_foreground(tank_con, libtcod.light_grey)
    libtcod.console_set_default_background(tank_con, ROW_COLOR)
    libtcod.console_rect(tank_con, 1, y-1, TANK_CON_WIDTH-2, 1, False, flag=libtcod.BKGND_SET)
    libtcod.console_print(tank_con, 1, y-1, 'Crewman                 Position      Order         Hatch   Spot')
    libtcod.console_set_default_foreground(tank_con, libtcod.white)
    libtcod.console_set_default_background(tank_con, libtcod.black)
    n = 0
    for crew_member in tank.crew:

        # determine basic foreground color for display
        fc = libtcod.white

        # if crewmember is having trouble, grey out their info
        if crew_member.NoActions():
            fc = GREYED_COLOR

        # highlight if selected
        selected = False
        if battle is not None:
            if battle.selected_crew is not None:
                if crew_member.position == battle.selected_crew.position:
                    selected = True
            if battle.phase not in ['Set Spot Sectors', 'Orders']:
                selected = False
        else:
            if campaign.selected_crew is not None:
                if crew_member.position == campaign.selected_crew.position:
                    selected = True
        if selected:
            fc = HIGHLIGHT_COLOR

        # set foreground color
        libtcod.console_set_default_foreground(tank_con, fc)

        # shade every other slot
        if IsOdd(n):
            libtcod.console_set_default_background(tank_con, ROW_COLOR)
        else:
            libtcod.console_set_default_background(tank_con, ROW_COLOR2)
        libtcod.console_rect(tank_con, 1, (n*3)+y, TANK_CON_WIDTH-2, 3, False, flag=libtcod.BKGND_SET)
        libtcod.console_set_default_background(tank_con, libtcod.black)

        # go through list of info text and display
        info_list = crew_member.GetInfo()
        # short rank and name
        text = crew_member.GetRank(short=True) + ' ' + info_list[0]
        libtcod.console_print(tank_con, 1, (n*3)+y, text)

        # position
        libtcod.console_print(tank_con, 25, (n*3)+y, info_list[1])

        # order
        # if not in battle, don't display anything
        if info_list[2] != '':
            lines = wrap(info_list[2], 11)
            libtcod.console_print(tank_con, 39, (n*3)+y, lines[0])
            if len(lines) > 1:
                libtcod.console_print(tank_con, 39, (n*3)+y+1, lines[1])

        # hatch
        libtcod.console_print(tank_con, 53, (n*3)+y, info_list[3])

        # spot
        lines = wrap(info_list[4], 11)
        libtcod.console_print(tank_con, 61, (n*3)+y, lines[0])
        if len(lines) > 1:
            libtcod.console_print(tank_con, 61, (n*3)+y+1, lines[1])

        # nickname
        if info_list[5] != '':
            libtcod.console_print(tank_con, 2, (n*3)+y+1, '"' + info_list[5] + '"')

        # wounds and/or status
        libtcod.console_set_default_foreground(tank_con, libtcod.red)
        if not crew_member.alive:
            text = 'Dead'
        else:
            if crew_member.v_serious_wound:
                text = 'Very Serious Wound'
            elif crew_member.serious_wound:
                text = 'Serious Wound'
            elif crew_member.light_wound:
                text = 'Light Wound'
            else:
                text = ''
            if crew_member.unconscious:
                if text != '':
                    text += ', '
                text += 'Unconscious'
            elif crew_member.stunned:
                if text != '':
                    text += ', '
                text += 'Stunned'
        libtcod.console_print(tank_con, 2, (n*3)+y+2, text)

        libtcod.console_set_default_foreground(tank_con, libtcod.white)
        n += 1

    libtcod.console_hline(tank_con, 1, 27, TANK_CON_WIDTH-2, flag=libtcod.BKGND_DEFAULT)

    # display target mode if firing main gun
    if battle is not None:
        if battle.phase == 'Fire Main Gun':
            libtcod.console_set_default_foreground(tank_con, HIGHLIGHT_COLOR)
            if battle.area_fire:
                text = 'Area Fire Mode'
            else:
                text = 'Direct Fire Mode'
            libtcod.console_print(tank_con, 1, 28, text)
            libtcod.console_set_default_foreground(tank_con, libtcod.white)

        # display instructions based on current input mode
        lines = []
        if battle.phase == 'Set Spot Sectors':
            lines = SPOT_SECTOR_INFO
        elif battle.phase == 'Orders':
            lines = ORDERS_PHASE_INFO
        elif battle.phase == 'Pivot Tank':
            lines = PIVOT_INFO
        elif battle.phase == 'Rotate Turret':
            lines = ROTATE_INFO
        elif battle.phase == 'Fire Main Gun':
            lines = FIRE_GUN_INFO
        elif battle.phase == 'Fire MGs':
            lines = FIRE_MGS_INFO

        y = 29
        for line in lines:
            libtcod.console_print(tank_con, 1, y, line)
            y += 1
    else:
        # list possible actions in campaign view
        libtcod.console_print(tank_con, 1, TANK_CON_HEIGHT-8,
            'Change [%cG%c]un load, '%HIGHLIGHT +
            'Ammo [%cR%c]eload, '%HIGHLIGHT +
            '[%cT%c]oggle Ready Rack use'%HIGHLIGHT)
        libtcod.console_print(tank_con, 1, TANK_CON_HEIGHT-7,
            '[%cW/S%c] '%HIGHLIGHT +
            'or [%cUp/Down%c]: move crew selection, '%HIGHLIGHT +
            '[%cH%c] toggle their hatch'%HIGHLIGHT)
        libtcod.console_print(tank_con, 1, TANK_CON_HEIGHT-6,
            'Open [%cM%c]ain Gun Ammunition Menu'%HIGHLIGHT)
        libtcod.console_print(tank_con, 1, TANK_CON_HEIGHT-2,
            '[%cENTER%c] to confirm this loadout'%HIGHLIGHT)


# date, time, etc. console
def UpdateDateCon():

    libtcod.console_clear(date_con)

    text = campaign.GetDate()
    libtcod.console_print(date_con, 0, 0, text)

    text = str(campaign.hour) + ':' + str(campaign.minute).zfill(2)
    libtcod.console_print(date_con, 23, 0, text)

    # mission for the day
    text = campaign.scen_type
    # special: counterattack battle
    if battle is not None:
        if battle.counterattack:
            text = 'Counterattack'
    libtcod.console_print(date_con, 31, 0, text)

    # if we're not in a battle, display expected resistance level for the day
    if battle is None:
        libtcod.console_print(date_con, 50, 0, 'Day Resistance: ' + campaign.scen_res)

    # otherwise, display area terrain
    else:
        text = campaign.GetTerrainDesc(campaign.day_map.player_node)
        libtcod.console_print(date_con, 50, 0, text)


# request input from the player, displayed on con
# can supply a list of random strings
# if get_name is true, select random string from FIRST_NAMES and LAST_NAMES instead
def GetInput(console, prompt_text, y, max_length, random_list=[], get_name=False):
    input_text = ''
    exit_prompt = False
    x = SCREEN_XM - int(max_length/2)

    W = 84
    libtcod.console_print_frame(console, SCREEN_XM - int(W/2), y-5, W, 13,
        clear=True, flag=libtcod.BKGND_DEFAULT, fmt=0)

    while not exit_prompt:
        # display prompt text
        libtcod.console_print_ex(console, SCREEN_XM, y-3, libtcod.BKGND_NONE, libtcod.CENTER, prompt_text)
        # display input area
        libtcod.console_set_default_background(con, PLAYER_COLOR)
        libtcod.console_rect(console, x, y, max_length, 1, False, flag=libtcod.BKGND_SET)

        # clear any old string, then display current string
        libtcod.console_rect(console, x, y, max_length, 1, True, flag=libtcod.BKGND_SET)
        libtcod.console_print_ex(console, SCREEN_XM, y, libtcod.BKGND_NONE, libtcod.CENTER, input_text)
        # if list of random possible strings is provided, add instruction
        if len(random_list) > 0 or get_name:
            text = 'Press Ctrl+R to randomly select an entry, replacing anything already inputted'
            libtcod.console_print_ex(console, SCREEN_XM, y+4, libtcod.BKGND_NONE, libtcod.CENTER, text)
        # display instructions
        text = '[%cEnter%c] to continue'%HIGHLIGHT
        libtcod.console_print_ex(console, SCREEN_XM, y+5, libtcod.BKGND_NONE, libtcod.CENTER, text)

        libtcod.console_blit(console, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)

        refresh = False
        while not refresh:

            # exit right away
            if libtcod.console_is_window_closed():
                sys.exit()

            libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS|libtcod.EVENT_MOUSE, key, mouse)

            if key.vk == libtcod.KEY_ENTER:
                refresh = True
                exit_prompt = True
                PlaySound('menu_select')

            elif key.vk == libtcod.KEY_BACKSPACE:
                if len(input_text) > 0:
                    input_text = input_text[:-1]
                    refresh = True

            # if any valid character is entered
            if 32 <= key.c <= 126:

                # if control-r, choose a random string
                if key.c == 114 and (key.lctrl or key.rctrl):

                    # if selecting a name
                    if get_name:
                        input_text = random.choice(FIRST_NAMES) + ' ' + random.choice(LAST_NAMES)
                        refresh = True

                    elif len(random_list) > 0:

                        # keep doing this many times until a result is found that
                        # is different than the current one
                        for n in range(99):
                            random_string = random.choice(random_list)
                            if len(random_string) > max_length:
                                random_string = random_string[:max_length]
                            if random_string != input_text:
                                input_text = random_string
                                break
                        refresh = True

                # otherwise, try to add it to the string
                else:
                    if len(input_text) < max_length:
                        input_text = input_text + chr(key.c)
                        refresh = True

            libtcod.console_flush()

    # reset console color
    libtcod.console_set_default_background(con, libtcod.black)
    return input_text


# ask the player to choose between several options
# only used for changing gun load at the moment
# can use ESC to cancel and not choose any option
def GetChoice(prompt_text, choice_list):

    # darken screen if in battle
    if battle is not None:
        libtcod.console_clear(con)
        libtcod.console_blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0,
            0.0, 0.7)
    exit_prompt = False
    libtcod.console_set_alignment(menu_con, libtcod.CENTER)
    # select first choice by default
    selected = choice_list[0]
    while not exit_prompt:

        # display menu of choices
        libtcod.console_clear(menu_con)
        libtcod.console_print_frame(menu_con, 0, 0, MENU_CON_WIDTH, MENU_CON_HEIGHT,
            clear=False, flag=libtcod.BKGND_DEFAULT, fmt=0)
        libtcod.console_print(menu_con, MENU_CON_XM, 3, prompt_text)

        y = 8
        for choice in choice_list:
            if choice == selected:
                libtcod.console_set_default_background(menu_con, SELECTED_COLOR)
                w = len(choice) + 2
                libtcod.console_rect(menu_con, MENU_CON_XM-int(w/2), y, w, 1, False, flag=libtcod.BKGND_SET)
                libtcod.console_set_default_background(menu_con, libtcod.black)
            libtcod.console_print(menu_con, MENU_CON_XM, y, choice)
            y += 2

        libtcod.console_print(menu_con, MENU_CON_XM, MENU_CON_HEIGHT-4, '[%cW/S/Up/Down%c] to move selection'%HIGHLIGHT)
        libtcod.console_print(menu_con, MENU_CON_XM, MENU_CON_HEIGHT-3, '[Enter] to choose, [ESC] to cancel')

        libtcod.console_blit(menu_con, 0, 0, MENU_CON_WIDTH, MENU_CON_HEIGHT, 0, MENU_CON_X, MENU_CON_Y)
        libtcod.console_flush()

        refresh = False
        while not refresh:
            libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS|libtcod.EVENT_MOUSE, key, mouse)

            if key.vk == libtcod.KEY_ENTER:
                refresh = True
                exit_prompt = True
            elif key.vk == libtcod.KEY_ESCAPE:
                selected = None
                refresh = True
                exit_prompt = True

            key_char = chr(key.c)

            if key_char in ['w', 'W'] or key.vk == libtcod.KEY_UP:
                if choice_list.index(selected) == 0:
                    selected = choice_list[-1]
                else:
                    selected = choice_list[choice_list.index(selected)-1]
                refresh = True

            elif key_char in ['s', 'S'] or key.vk == libtcod.KEY_DOWN:
                if choice_list.index(selected) == len(choice_list) - 1:
                    selected = choice_list[0]
                else:
                    selected = choice_list[choice_list.index(selected)+1]
                refresh = True

            libtcod.console_flush()

    libtcod.console_set_alignment(menu_con, libtcod.CENTER)

    return selected


# handle random encounter event
def RandomEvent():

    # chance of no event this round
    if Roll1D6() <= 2:
        Message('No Random Event this round.')
        return

    # retermine roll result ranges
    # Flanking Fire, Friendly Arty, Time Passes, Harrasing Fire, Enemy Arty, Enemy Reinforcement
    #  Mines
    if campaign.scen_type == 'Advance':
        RANGES = [3,4,5,7,8,9,12]
    elif campaign.scen_type == 'Battle':
        RANGES = [3,4,5,7,9,10,12]
    else:
        RANGES = [3,5,6,7,9,12,0]

    roll = Roll2D6()

    # flanking fire
    if roll <= RANGES[0]:
        # skip if no enemies
        if AllEnemiesDead():
            Message('No Random Event this round.')
            return

        PopUp('Friendly forces conduct Flanking Fire against the enemy.')
        RenderEncounter()
        result = False
        for unit in battle.enemy_units:
            if not unit.alive: continue
            if unit.FriendlyAction(flanking_fire=True):
                result = True
            UpdateMapOverlay()
            RenderEncounter()

        if not result:
            PopUp('No results from Flanking Fire.')

    # friendly artillery
    elif roll <= RANGES[1]:

        # skip if no enemies
        if AllEnemiesDead():
            Message('No Random Event this round.')
            return

        PopUp('Friendly forces conduct artillery fire against the enemy.')
        PlaySound('arty_firing')
        result = False
        for unit in battle.enemy_units:
            if not unit.alive: continue
            if unit.FriendlyAction(artillery=True):
                result = True
            UpdateMapOverlay()
            RenderEncounter()

        if not result:
            PopUp('No results from Friendly Artillery.')

    # time passes
    elif roll <= RANGES[2]:
        PopUp('15 minutes of time has passed.')
        campaign.SpendTime(0, 15)
        WriteJournal('Time is now ' + str(campaign.hour) + ':' + str(campaign.minute).zfill(2))
        RenderEncounter()

    # harrasing fire
    elif roll <= RANGES[3]:
        PlaySound('german_rifle_fire')
        PopUp('Small-arms fire peppers your tank, threatening any crew member not buttoned up.')
        tank.LWAttack()

    # enemy artillery
    elif roll <= RANGES[4]:
        PopUp('Enemy artillery fire rains down on your position.')
        PlaySound('arty_firing')
        ArtyStrikeAnimation(MAP_X0+MAP_CON_X, MAP_Y0+MAP_CON_Y)
        result = Roll1D10()
        if result <= 6:
            num_ko = 1
        elif result <= 9:
            num_ko = 2
        else:
            num_ko = 3
        PopUp(str(num_ko) + ' friendly infantry squads are destroyed.')
        battle.inf_lost += num_ko
        tank.LWAttack()

    # enemy reinforcement
    elif roll <= RANGES[5]:
        # check for reinforcement roll
        if battle.enemy_reinforcements > 0:
            roll = Roll1D6()
            if roll != 1 and roll + battle.enemy_reinforcements >= 7:
                Message('No Random Event this round.')
                return
        battle.enemy_reinforcements += 1
        Message('Enemy reinforcements have arrived.')
        RenderEncounter()
        SpawnEnemy()
        UpdateMapOverlay()
        RenderEncounter()

    # mines
    elif roll <= RANGES[6]:
        if not tank.moving:
            Message('No Random Event this round.')
        else:
            PopUp('Your battle group has moved into a minefield!')
            tank.MinefieldAttack()


# display the menu bar on the main console
def DisplayMenuBar():
    libtcod.console_set_default_foreground(con, libtcod.light_grey)
    libtcod.console_set_alignment(con, libtcod.LEFT)
    if campaign.day_in_progress:
        libtcod.console_print(con, 1, 0, MENU_BAR1)
    libtcod.console_print(con, 14, 0, MENU_BAR2)
    libtcod.console_set_default_foreground(con, libtcod.white)


# screen rendering function for encounters, draws everything to the main console
#  if zoom_in is True, game will display an animation effect zooming in on the encounter
#  location
def RenderEncounter(no_flush=False, zoom_in=False):

    # clear the display console
    libtcod.console_clear(con)

    # display menu bar
    DisplayMenuBar()

    # blit consoles to display console
    libtcod.console_blit(date_con, 0, 0, DATE_CON_WIDTH, DATE_CON_HEIGHT, con, 1, 2)
    libtcod.console_blit(tank_con, 0, 0, TANK_CON_WIDTH, TANK_CON_HEIGHT, con, 1, 4)
    libtcod.console_blit(msg_con, 0, 0, MSG_CON_WIDTH, MSG_CON_HEIGHT, con, 1, TANK_CON_HEIGHT+5)
    libtcod.console_blit(map_con, 0, 0, MAP_CON_WIDTH, MAP_CON_HEIGHT, con, MAP_CON_X, MAP_CON_Y)

    # blit map overlay
    libtcod.console_blit(overlay_con, 0, 0, MAP_CON_WIDTH, MAP_CON_HEIGHT, con,
        MAP_CON_X, MAP_CON_Y)

    libtcod.console_blit(map_info_con, 0, 0, MAP_INFO_CON_WIDTH, MAP_INFO_CON_HEIGHT,
        con, MAP_CON_X, SCREEN_HEIGHT-MAP_INFO_CON_HEIGHT)

    # lines between console displays
    libtcod.console_hline(con, 1, 1, SCREEN_WIDTH-2, flag=libtcod.BKGND_DEFAULT)
    libtcod.console_hline(con, 1, 3, TANK_CON_WIDTH, flag=libtcod.BKGND_DEFAULT)
    libtcod.console_hline(con, 1, TANK_CON_HEIGHT+4, TANK_CON_WIDTH, flag=libtcod.BKGND_DEFAULT)
    libtcod.console_hline(con, MAP_CON_X, MAP_CON_HEIGHT+2, MAP_CON_WIDTH, flag=libtcod.BKGND_DEFAULT)
    libtcod.console_vline(con, MAP_CON_X-1, 2, SCREEN_HEIGHT-2, flag=libtcod.BKGND_DEFAULT)

    # zoom in effect
    if zoom_in and campaign.animations:
        x = campaign.day_map.player_node.x+C_MAP_CON_X
        y = campaign.day_map.player_node.y+4-campaign.c_map_y

        for w in range(3, SCREEN_WIDTH, 2):
            libtcod.console_blit(con, x-w, y-w, w*2, w*2, 0, x-w, y-w)
            libtcod.console_print_frame(0, x-w, y-w, w*2, w*2,
                clear=False, flag=libtcod.BKGND_DEFAULT, fmt=0)
            libtcod.console_flush()
            if x-w < 0 and x+w >= SCREEN_WIDTH: break

    # blit full display console to screen and update screen
    libtcod.console_blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)
    if not no_flush:
        libtcod.console_flush()


# wait for player to press enter before continuing
def WaitForEnter():
    end_pause = False
    while not end_pause:
        # get input from user
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS|libtcod.EVENT_MOUSE, key, mouse)

        # exit right away
        if libtcod.console_is_window_closed():
            sys.exit()

        elif key.vk == libtcod.KEY_ENTER:
            end_pause = True

        # screenshot
        elif key.vk == libtcod.KEY_F12:
            SaveScreenshot()

        # refresh the screen
        libtcod.console_flush()

    # wait for enter to be released
    while libtcod.console_is_key_pressed(libtcod.KEY_ENTER):
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS|libtcod.EVENT_MOUSE, key, mouse)
        libtcod.console_flush()

# wait for player to press space before continuing
def WaitForSpace():
    end_pause = False
    while not end_pause:
        # get input from user
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS|libtcod.EVENT_MOUSE, key, mouse)

        # exit right away
        if libtcod.console_is_window_closed():
            sys.exit()

        elif key.vk == libtcod.KEY_SPACE:
            end_pause = True

        # screenshot
        elif key.vk == libtcod.KEY_F12:
            SaveScreenshot()

        # refresh the screen
        libtcod.console_flush()

    # wait for enter to be released
    while libtcod.console_is_key_pressed(libtcod.KEY_SPACE):
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS|libtcod.EVENT_MOUSE, key, mouse)
        libtcod.console_flush()


# save the game in progress
def SaveGame():

    # don't save if campaign is over@
    if campaign.over: return

    # create a new SavedGameInfo class
    name = ''
    for crewman in tank.crew:
        if crewman.position == 'Commander':
            name = crewman.name
            break
    info = SavedGameInfo(VERSION, campaign.campaign_name, name, tank.name, campaign.GetDate())

    save = shelve.open('savegame')
    save['info'] = info
    save['campaign'] = campaign
    save['tank'] = tank
    save['battle'] = battle
    save.close


# load a saved game
def LoadGame():
    global campaign, tank, battle
    save = shelve.open('savegame')
    campaign = save['campaign']
    tank = save['tank']
    battle = save['battle']
    save.close()

    # reset campaign calendar info from xml file
    LoadCampaignInfo()


# load campaign info from xml file
def LoadCampaignInfo():

    root = xml.parse(DATAPATH + campaign.campaign_file)
    campaign.campaign_name = root.find('name').text
    campaign.player_nation = root.find('player_nation').text
    campaign.enemy_nation = root.find('enemy_nation').text

    # set campaign variables for ranks and awards based on player nation
    if campaign.player_nation == 'USA':
        campaign.ranks = USA_RANKS
        campaign.decorations = USA_DECORATIONS
    elif campaign.player_nation == 'CAN':
        campaign.ranks = UKC_RANKS
        campaign.decorations = UKC_DECORATIONS

    # load campaign map file info from campaign file
    if root.find('campaign_map_file') is not None:
        campaign.map_file = root.find('campaign_map_file').text

    # build list of permitted player vehicle types
    campaign.player_veh_list = []
    veh_list = root.find('player_tanks').findall('player_tank_type')
    for item in veh_list:
        campaign.player_veh_list.append(item.text)

    # load unit class activation chance info for each type of mission
    campaign.mission_activations = []
    CLASSES = ['TANK','SPG','AT_GUN','LW','MG','TRUCK','APC','AC']
    item = root.find('activation_table')
    for tag_name in ['advance', 'battle', 'counterattack']:
        item2 = item.find(tag_name)
        tuple_list = []
        for class_name in CLASSES:
            value = int(item2.find(class_name).text)
            tuple_list.append((class_name, value))
        campaign.mission_activations.append(tuple_list)

    # load activation modifiers as list of dictionaries
    item = root.find('activation_modifiers')
    if item is not None:
        for child in item.findall('modifier'):
            dictionary = {}
            dictionary['year'] = int(child.find('year').text)
            dictionary['month'] = int(child.find('month').text)
            dictionary['date'] = int(child.find('date').text)
            dictionary['class_name'] = child.find('class_name').text
            dictionary['mod'] = int(child.find('mod').text)
            campaign.activation_modifiers.append(dictionary)

    # load activation chance info for each unit class (out of 1000)
    campaign.class_activations = []
    item = root.find('unit_class_activations')
    for tag_name in CLASSES:
        unit_list = [tag_name]
        item_list = item.findall(tag_name)
        for unit_type in item_list:
            reader = csv.reader([unit_type.text], delimiter=';', skipinitialspace=True, strict=True)
            for row in reader:
                unit_list.append((row[0], int(row[1])))
        campaign.class_activations.append(unit_list)

    # load calendar day info into campaign object
    REQUIRED_KEYS = ['month', 'date', 'year', 'comment']
    OPTIONAL_KEYS = ['resistance_level', 'mission', 'description', 'terrain',
        'map_x', 'map_y']

    campaign.days = []
    item_list = root.find('calendar').findall('day')
    for item in item_list:
        day = {}
        # go through required keys and get their values
        for key in REQUIRED_KEYS:
            value = item.find(key).text
            # some need to be cast to integer values
            if key in ['month', 'date', 'year']:
                value = int(value)

            # add the key and value
            day[key] = value

        # do the same for optional key/value pairs
        for key in OPTIONAL_KEYS:
            if item.find(key) is not None:
                value = item.find(key).text
                day[key] = value

        # add the completed day entry to the campaign calendar
        campaign.days.append(day)

    # delete the parsed xml data; we've saved everything we need
    del root


# load a console image from an .xp file
def LoadXP(filename):
    filename = DATAPATH + filename
    xp_file = gzip.open(filename)
    raw_data = xp_file.read()
    xp_file.close()
    xp_data = xp_loader.load_xp_string(raw_data)
    console = libtcod.console_new(xp_data['width'], xp_data['height'])
    xp_loader.load_layer_to_console(console, xp_data['layer_data'][0])
    return console


# open the highscores file and try to add this campaign's outcome
def AddHighScore():
    # load the existing highscores object from the bones file
    save = shelve.open('bones')
    bones = save['bones']
    save.close()

    # compose the outcome text to be added
    for crew_member in tank.crew:
        if crew_member.position == 'Commander':
            break
    if not crew_member.alive:
        outcome = 'KIA on ' + campaign.GetDate()
    elif crew_member.v_serious_wound:
        outcome = 'Sent Home on ' + campaign.GetDate()
    else:
        outcome = 'Survived'

    # add the new entry to the list of highscores
    vp = campaign.vp + campaign.day_vp
    bones.score_list.append((tank.name, crew_member.name, vp, outcome,
        campaign.unlimited_tank_selection,
        campaign.casual_commander,
        campaign.campaign_name))

    # sort the new list
    bones.score_list.sort(key=lambda tup: tup[2], reverse=True)

    # limit to max length
    if len(bones.score_list) > MAX_HS:
        del bones.score_list[-1]

    # save the new bones file
    save = shelve.open('bones')
    save['bones'] = bones
    save.close()


# save a screenshot of the current main console
def SaveScreenshot():
    img = libtcod.image_from_console(0)
    filename = 'screenshot_' + time.strftime("%Y_%m_%d_%H_%M_%S") + '.bmp'
    libtcod.image_save(img, filename)
    PlaySound('screenshot')
    PopUp("Screenshot saved as: " + filename)


# display a crew speech box, either on the encounter or the campaign day map
def CrewTalk(message, position_list=None):

    # build a list of possible crew members to speak; commander never speaks
    crew_list = []
    for crewman in tank.crew:
        if crewman.position == 'Commander': continue
        if not crewman.alive or crewman.stunned or crewman.unconscious:
            continue
        if position_list is not None:
            if crewman.position not in position_list: continue
        crew_list.append(crewman)

    if len(crew_list) == 0:
        return

    # select the crewman to speak
    crewman = random.choice(crew_list)

    # determine draw location,
    if battle is None:
        x = campaign.day_map.player_node.x+C_MAP_CON_X
        y = campaign.day_map.player_node.y+3-campaign.c_map_y
    else:
        x = MAP_X0 + MAP_CON_X
        y = MAP_Y0 + MAP_CON_Y

    ShowLabel(x, y, message, crewman=crewman)

    # re-draw original console to screen
    libtcod.console_blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)


# display a pop-up info window
# if confirm, we want a confirmation from the player
def PopUp(message, confirm=False, skip_update=False):

    # darken screen
    libtcod.console_clear(con)
    libtcod.console_blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0,
        0.0, 0.7)

    # draw message window to screen
    lines = wrap(message, 30)

    y = 25

    # draw background box
    libtcod.console_print_frame(0, SCREEN_XM-17, y-2, 34, len(lines)+6,
        clear=True, flag=libtcod.BKGND_SET, fmt=0)

    for line in lines:
        libtcod.console_print_ex(0, SCREEN_XM, y, libtcod.BKGND_NONE, libtcod.CENTER, line)
        y += 1

    if confirm:
        text = '[%cy%c] or [%cN%c]'%(libtcod.COLCTRL_1, libtcod.COLCTRL_STOP, libtcod.COLCTRL_1, libtcod.COLCTRL_STOP)
    else:

        text = '[%cEnter%c] to continue'%HIGHLIGHT
    libtcod.console_print_ex(0, SCREEN_XM, y+1, libtcod.BKGND_NONE, libtcod.CENTER, text)

    # wait for input
    choice = False
    exit_menu = False
    while not exit_menu:
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS|libtcod.EVENT_MOUSE, key, mouse)

        key_char = chr(key.c)

        # exit right away
        if libtcod.console_is_window_closed():
            sys.exit()

        if confirm:
            if key.vk == libtcod.KEY_ENTER or key.vk == libtcod.KEY_ESCAPE or key_char in ['n', 'N']:
                exit_menu = True
            elif key_char in ['y', 'Y']:
                choice = True
                exit_menu = True
        else:
            if key.vk == libtcod.KEY_ENTER:
                exit_menu = True

        # update screen
        libtcod.console_flush()

    # play menu sound
    #PlaySound('menu_select')

    # if we don't want to redraw the battle or campaign screen
    if skip_update: return choice

    # redraw the console but don't refresh screen, in case we will show another pop-up
    if battle is not None:
        RenderEncounter(no_flush=True)
    elif campaign.day_in_progress:
        RenderCampaign(no_flush=True)

    return choice

# checks if we need to set spot sectors for one or more crewmen
def CheckSpotSectors():

    # first check that there are one or more enemy units that could be spotted or
    # identified
    none_to_spot = True
    for unit in battle.enemy_units:
        if not unit.alive: continue
        if unit.hidden: continue
        if unit.spotted and unit.identified: continue
        if unit.spotted and unit.unit_class not in ['TANK', 'SPG', 'AT_GUN']: continue
        if unit.map_hex.rng > 0 and (campaign.weather.fog or campaign.weather.precip == 'Snow'): continue
        none_to_spot = False
        break

    if none_to_spot: return False

    # spotting could happen, so check to see if any crew need to set a spot sector
    for crew_member in tank.crew:
        if crew_member.spot == 'Any One Sector':
            return True

    # spotting could happen, but no crew members need to have their sector set
    return False


################################################################################
#                             Encounter Handling                               #
################################################################################

# display encounter menu
def EncounterMenu():

    # darken screen
    libtcod.console_clear(con)
    libtcod.console_blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0,
        0.0, 0.7)

    # generate and display menu
    libtcod.console_clear(menu_con)
    libtcod.console_print_frame(menu_con, 0, 0, MENU_CON_WIDTH, MENU_CON_HEIGHT,
        clear=False, flag=libtcod.BKGND_DEFAULT, fmt=0)
    libtcod.console_set_default_foreground(menu_con, MENU_TITLE_COLOR)
    libtcod.console_print_ex(menu_con, MENU_CON_XM, 1,
        libtcod.BKGND_NONE, libtcod.CENTER, 'Encounter Menu')
    libtcod.console_set_default_foreground(menu_con, libtcod.white)

    # campaign is over
    if campaign.exiting:
        libtcod.console_print_ex(menu_con, MENU_CON_XM, 3,
            libtcod.BKGND_NONE, libtcod.CENTER, '[%cEnter%c] Return to Main Menu'%HIGHLIGHT)

    # scenario is resolved
    elif battle.result != 'Undetermined':
        libtcod.console_print_ex(menu_con, MENU_CON_XM, 3,
            libtcod.BKGND_NONE, libtcod.CENTER, '[%cEnter%c] Return to Campaign Map'%HIGHLIGHT)

    # scenario continues
    else:
        libtcod.console_print_ex(menu_con, MENU_CON_XM, 3,
            libtcod.BKGND_NONE, libtcod.CENTER, '[%cEnter%c] Return to Game'%HIGHLIGHT)
        libtcod.console_print_ex(menu_con, MENU_CON_XM, 4,
            libtcod.BKGND_NONE, libtcod.CENTER, '[%cQ%c] Save Game and Quit'%HIGHLIGHT)

    # display enemy units destroyed
    x = 36
    libtcod.console_set_alignment(menu_con, libtcod.LEFT)
    libtcod.console_set_default_foreground(menu_con, libtcod.light_grey)
    libtcod.console_print(menu_con, x, 7, '                                         Destroyed by               Forced off')
    libtcod.console_print(menu_con, x, 8, 'Enemy Forces              VP Value    Player    Friendly Forces    Encounter Map')
    libtcod.console_print(menu_con, x, 9, '-----------------------------------------------------------------------------------')
    libtcod.console_set_default_foreground(menu_con, libtcod.white)
    libtcod.console_print(menu_con, x, 10, 'LW and MG Squads             1')
    libtcod.console_print(menu_con, x, 11, 'Trucks                       1')
    libtcod.console_print(menu_con, x, 12, 'APC or Armoured Car          2')
    libtcod.console_print(menu_con, x, 13, 'Self-Propelled Guns          6')
    libtcod.console_print(menu_con, x, 14, 'Panzer IV                    7')
    libtcod.console_print(menu_con, x, 15, 'Panzer V (Panther)           9')
    libtcod.console_print(menu_con, x, 16, 'Panzer VI (Tiger)           12')
    libtcod.console_print(menu_con, x, 17, 'Anti-Tank Gun                4')

    libtcod.console_set_alignment(menu_con, libtcod.RIGHT)
    VP_SCORES = [1, 1, 2, 6, 7, 9, 12, 4]

    # destroyed by player
    y = 10
    player_vp = 0
    n = 0
    for num in battle.tank_ko_record:
        libtcod.console_print(menu_con, x+40, y, str(num))
        player_vp += (num * VP_SCORES[n])
        y += 1
        n += 1

    # destroyed by friendly forces
    y = 10
    friendly_vp = 0
    n = 0
    for num in battle.friendly_ko_record:
        libtcod.console_print(menu_con, x+54, y, str(num))
        friendly_vp += (num * VP_SCORES[n])
        y += 1
        n += 1

    # left behind by player movement
    y = 10
    left_behind_vp = 0
    n = 0
    for num in battle.left_behind:
        libtcod.console_print(menu_con, x+72, y, str(num))
        left_behind_vp -= int(num * VP_SCORES[n] / 2)
        y += 1
        n += 1

    # Victory Point Totals
    libtcod.console_print(menu_con, x+40, 19, str(player_vp))
    libtcod.console_print(menu_con, x+54, 19, str(friendly_vp))
    libtcod.console_print(menu_con, x+72, 19, str(left_behind_vp))
    libtcod.console_set_alignment(menu_con, libtcod.LEFT)
    libtcod.console_print(menu_con, x, 19, 'Totals:')

    # display friendly forces lost
    libtcod.console_set_default_foreground(menu_con, libtcod.light_grey)
    libtcod.console_print(menu_con, x, 22, 'Friendly Forces         VP Value      Lost')
    libtcod.console_print(menu_con, x, 23, '------------------------------------------')
    libtcod.console_set_default_foreground(menu_con, libtcod.white)
    libtcod.console_print(menu_con, x, 24, 'Tanks                      -5')
    libtcod.console_print(menu_con, x, 25, 'Infantry Squads            -3')

    libtcod.console_set_alignment(menu_con, libtcod.RIGHT)
    libtcod.console_print(menu_con, x+40, 24, str(battle.tanks_lost))
    libtcod.console_print(menu_con, x+40, 25, str(battle.inf_lost))

    libtcod.console_set_alignment(menu_con, libtcod.CENTER)

    # display present VP total
    vp_total = player_vp + friendly_vp + left_behind_vp - (battle.tanks_lost * 5) - (battle.inf_lost * 3)
    libtcod.console_print(menu_con, MENU_CON_XM, 28, 'Encounter VP Total: ' + str(vp_total))

    # also display campaign day and overall VP
    text = 'Campaign Day VP: ' + str(campaign.day_vp)
    libtcod.console_print(menu_con, MENU_CON_XM, 30, text)
    text = 'Total Campaign VP: ' + str(campaign.vp)
    libtcod.console_print(menu_con, MENU_CON_XM, 31, text)

    # record in case we are leaving encounter
    battle.vp_total = vp_total

    # Encounter Result: Undetermined / Victory / Tank Lost
    libtcod.console_print(menu_con, MENU_CON_XM, 35, 'Encounter Result: ' + battle.result)

    libtcod.console_set_alignment(menu_con, libtcod.LEFT)

    libtcod.console_blit(menu_con, 0, 0, MENU_CON_WIDTH, MENU_CON_HEIGHT, 0, MENU_CON_X, MENU_CON_Y)
    libtcod.console_flush()

    exit_menu = False
    while not exit_menu:
        # get input from user
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS|libtcod.EVENT_MOUSE, key, mouse)

        if key.vk == libtcod.KEY_ENTER: break

        # get pressed key
        key_char = chr(key.c)

        if battle.result == 'Undetermined' and key_char in ['q', 'Q']:
            SaveGame()
            campaign.exiting = True
            libtcod.console_clear(con)
            return

        # exit right away
        if libtcod.console_is_window_closed():
            sys.exit()

        libtcod.console_flush()

    # re-draw screen
    RenderEncounter()


# set a new phase for the encounter, update phase display title on encounter map,
# and update tank console to reflect new phase
def NewPhase(new_phase):
    battle.phase = new_phase
    UpdateMapOverlay()
    UpdateTankCon()
    RenderEncounter()


# main loop for battle encounter
def DoEncounter():

    global battle, key, mouse

    # get input and perform events
    exit_encounter = False
    while not exit_encounter:

        # trigger encounter end
        if battle.result != 'Undetermined':
            # display scenario menu for battle overview if campaign is not over
            if not campaign.over:
                EncounterMenu()

            break

        # exit right away
        if libtcod.console_is_window_closed():
            sys.exit()

        # check to see if player is exiting out of the campaign
        elif campaign.exiting:
            battle = None
            return

        libtcod.console_flush()

        GetEncounterInput()

    # award or subtract VP
    campaign.day_vp += battle.vp_total
    if battle.vp_total < 0:
        text = 'You have lost ' + str(abs(battle.vp_total))
    elif battle.vp_total == 0:
        text = 'You gain no'
    else:
        text = 'You are awarded ' + str(battle.vp_total)
    text += ' VP for this encounter.'

    battle = None

    Message(text)


# get input and do encounter actions
def GetEncounterInput():
    # check for keyboard or mouse input
    libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS|libtcod.EVENT_MOUSE, key, mouse)

    # mouse stuff first
    mx, my = mouse.cx, mouse.cy

    # check mouse position against last recorded one
    if (mx, my) != battle.mouseover:
        battle.mouseover = (mx, my)

        # update map info console
        UpdateMapInfoCon(mx, my)
        RenderEncounter()

    # see if right mouse button was clicked
    if mouse.rbutton:
        UnitInfo(mx, my)
        RenderEncounter()

    # if ESCAPE key is pressed, open encounter menu
    if key.vk == libtcod.KEY_ESCAPE:
        EncounterMenu()

    # help display
    elif key.vk == libtcod.KEY_F1 or key.vk == libtcod.KEY_1:
        ShowHelp()

    # tank info display
    elif key.vk == libtcod.KEY_F2 or key.vk == libtcod.KEY_2:
        ShowTankInfo()

    # crew info display
    elif key.vk == libtcod.KEY_F3 or key.vk == libtcod.KEY_3:
        ShowCrewInfo()

    # settings
    elif key.vk == libtcod.KEY_F4 or key.vk == libtcod.KEY_4:
        ShowSettings()

    # campaign stats
    elif key.vk == libtcod.KEY_F5 or key.vk == libtcod.KEY_5:
        ShowCampaignStats()

    # screenshot
    elif key.vk == libtcod.KEY_F6 or key.vk == libtcod.KEY_6:
        SaveScreenshot()

    # backspace key can cancel issue order input mode
    elif key.vk == libtcod.KEY_BACKSPACE:
        if battle.phase == 'Issue Order':
            battle.selected_order = None    # clear any selected order
            NewPhase('Orders')

    # if the END or SPACE BAR keys are pressed, the game shifts to the next phase
    # can also be trigged by game
    if key.vk == libtcod.KEY_END or key.vk == libtcod.KEY_SPACE or battle.trigger_phase:

        battle.trigger_phase = False

        # end of set spot sectors sub-phase, do spotting then orders phase
        if battle.phase == 'Set Spot Sectors':
            NewPhase('Spotting')
            DoSpotting()
            NewPhase('Orders')
            SaveGame()
            return

        # end of Orders phase, start of Crew Action phase
        if battle.phase == 'Orders':

            # check for abandoning the tank
            for crewman in tank.crew:
                if crewman.order == 'Abandon Tank':
                    text = ('You are about to abandon your tank. It ' +
                        'will be destroyed. Are you certain?')
                    if PopUp(text, confirm=True):
                        tank.AbandonTank()
                        return

            # Change Gun Load
            crew_member = GetCrewByPosition('Loader')
            if crew_member.order == 'Change Gun Load':
                tank.ChangeGunLoadMenu()
                UpdateTankCon()
                RenderEncounter()
                SaveGame()

            if SetupPivot():
                NewPhase('Pivot Tank')
                SaveGame()
                return
            else:
                # set this but only so that the next if statement is
                # immediately triggered
                battle.phase = 'Pivot Tank'

        if battle.phase == 'Pivot Tank':

            # check for pivot order
            crew_member = GetCrewByPosition('Driver')
            if crew_member.order == 'Pivot Tank':
                if tank.new_facing != 4:
                    PivotTank()
                else:
                    # if pivot order was given but tank did not pivot,
                    # any moving status from a previous turn is lost
                    if tank.moving:
                        tank.moving = False
                        UpdateTankCon()

            # check for player tank movement
            NewPhase('Tank Movement')
            MoveTank()

            # check for rotating turret
            if SetupRotateTurret():
                NewPhase('Rotate Turret')
                SaveGame()
                return
            else:
                battle.phase = 'Rotate Turret'

        if battle.phase == 'Rotate Turret':

            # clear old facing for turret
            tank.old_t_facing = tank.turret_facing
            UpdateMapOverlay()

            # check for firing main gun, or attempt repairing it
            if SetupMainGun():
                UpdateMapOverlay()
                RenderEncounter()
                SaveGame()
                return
            else:
                battle.phase = 'Fire Main Gun'

        if battle.phase == 'Fire Main Gun':

            # finish up main gun sub-phase
            # clear any target, clear RoF flag
            battle.target = None
            tank.has_rof = False
            UpdateMapOverlay()
            RenderEncounter()

            # resolve any outstanding hits on alive enemy units
            for unit in battle.enemy_units:
                if not unit.alive: continue
                if len(unit.hit_record) > 0:
                    unit.ResolveHits()

            # check for firing MGs
            if SetupFireMGs():
                SaveGame()
                return
            else:
                battle.phase = 'Fire MGs'

        if battle.phase == 'Fire MGs':

            # clear any target
            battle.target = None

            # throw smoke grenade phase
            NewPhase('Smoke Grenades')
            HandleSmokeGrenades()

            # fire smoke mortar
            NewPhase('Smoke Mortar')
            HandleSmokeMortar()

            # check for restocking ready rack
            if SetupReadyRack():
                PopUp('Loader may move shells into or out of the Ready Rack')
                MainGunAmmoMenu()
                RenderEncounter()

            ##### End of Action Phase, crew has chance to recover #####
            NewPhase('Crew Recovery')
            for crewman in tank.crew:
                crewman.RecoveryRoll()

            # if we got an ambush, skip this section but reset flag
            if battle.friendly_ambush:
                battle.friendly_ambush = False
            else:
                ##### Enemy Action #####
                NewPhase('Enemy Action')

                # do an action for each active enemy unit on the board
                for unit in battle.enemy_units:
                    if not unit.alive: continue
                    unit.DoAction()
                    UpdateMapOverlay()
                    RenderEncounter()
                    # check to see if tank has been knocked out by enemy action
                    if battle.result != 'Undetermined':
                        return

            ##### Friendly Action #####
            # Skip if no alive enemy units
            if not AllEnemiesDead():
                NewPhase('Friendly Action')

                # do an action for each active enemy unit on the board
                result = False
                for unit in battle.enemy_units:
                    if not unit.alive: continue
                    if unit.FriendlyAction():
                        result = True
                    UpdateMapOverlay()
                    RenderEncounter()

                if not result:
                    PopUp('No results from Friendly Action.')

            ##### Random Events #####
            NewPhase('Random Events')
            RandomEvent()

            ##### Repair Attempts #####
            NewPhase('Attempt Repairs')
            AttemptRepairs()

            # check to trigger scenario loss
            if not tank.alive:
                return

            # check to trigger scenario victory
            if AllEnemiesDead():
                Message('You have won the encounter!')
                RenderEncounter()
                battle.result = 'Victory'
                return

            ##### Start of New Encounter Turn #####

            battle.rounds_passed += 1

            # reset the player tank for a new turn
            tank.Reset()

            # reset enemy units for new turn
            for unit in battle.enemy_units:
                if not unit.alive: continue
                unit.Reset()

            # reset Battle Leadership effect
            if battle.battle_leadership:
                Message('Battle Leadership no longer in effect.')
                battle.battle_leadership = False

            # test for new battle leadership effect
            if GetCrewByPosition('Commander').SkillCheck('Battle Leadership'):
                Message('Battle Leadership now in effect.')
                battle.battle_leadership = True

            # deplete smoke
            NewPhase('Smoke Depletion')
            DepleteSmoke()
            CalculateSmokeFactors()

            # rebuild list of orders and set spot ability for crew
            for crewman in tank.crew:
                crewman.BuildOrdersList()
                crewman.SetSpotAbility()

            # see if spot sectors need to be selected
            if CheckSpotSectors():
                # select first crew that can choose one spot sector
                for crewman in tank.crew:
                    if crewman.spot == 'Any One Sector':
                        battle.selected_crew = crewman
                        break
                NewPhase('Set Spot Sectors')
            else:
                # do spotting phase, then orders
                DoSpotting()
                NewPhase('Orders')

            SaveGame()

    # get pressed key
    key_char = chr(key.c)

    # debug commands
    if DEBUG:
        # knock out player tank
        if key_char == 'k' and (key.lctrl or key.rctrl):
            tank.alive = False
            battle.result = 'Tank Lost'
            RenderEncounter()
            return

        # win encounter
        elif key_char == 'v' and (key.lctrl or key.rctrl):
            PopUp('You have won the encounter!')
            RenderEncounter()
            battle.result = 'Victory'
            return

        # immobilize tank
        elif key_char == 'i' and (key.lctrl or key.rctrl):
            PopUp('Your tank is immobilized!')
            tank.moving = False
            tank.immobilized = True
            UpdateTankCon()
            RenderEncounter()
            return

        # apply a minor damage result
        elif key_char == 'd' and (key.lctrl or key.rctrl):
            tank.TakeDamage()
            RenderEncounter()
            return

    # select spot sector mode
    if battle.phase == 'Set Spot Sectors':
        # select next crew member that can select a spot sector
        if key_char in ['s', 'S'] or key.vk == libtcod.KEY_DOWN:
            battle.selected_crew = battle.selected_crew.next
            while battle.selected_crew.spot != 'Any One Sector':
                battle.selected_crew = battle.selected_crew.next
            UpdateTankCon()
            UpdateMapOverlay()
            RenderEncounter()

        # select previous crew member that can select a spot sector
        elif key_char in ['w', 'W'] or key.vk == libtcod.KEY_UP:
            battle.selected_crew = battle.selected_crew.prev
            while battle.selected_crew.spot != 'Any One Sector':
                battle.selected_crew = battle.selected_crew.prev
            UpdateTankCon()
            UpdateMapOverlay()
            RenderEncounter()

        # rotate selected sector clockwise
        elif key_char in ['d', 'D'] or key.vk == libtcod.KEY_RIGHT:
            battle.selected_crew.spot_sector += 1
            if battle.selected_crew.spot_sector > 5:
                battle.selected_crew.spot_sector = 0
            UpdateMapOverlay()
            RenderEncounter()

        # rotate selected sector counter clockwise
        elif key_char in ['a', 'A'] or key.vk == libtcod.KEY_LEFT:
            battle.selected_crew.spot_sector -= 1
            if battle.selected_crew.spot_sector < 0:
                battle.selected_crew.spot_sector = 5
            UpdateMapOverlay()
            RenderEncounter()

    # orders input mode - can select crew, toggle hatch state, change ammo options,
    # and switch to 'Issue Order' input mode
    elif battle.phase == 'Orders':

        # select next crew member
        if key_char in ['s', 'S'] or key.vk == libtcod.KEY_DOWN:
            battle.selected_crew = battle.selected_crew.next
            UpdateTankCon()
            RenderEncounter()

        # select previous crew member
        elif key_char in ['w', 'W'] or key.vk == libtcod.KEY_UP:
            battle.selected_crew = battle.selected_crew.prev
            UpdateTankCon()
            RenderEncounter()

        # toggle hatch status for selected crew member
        elif key_char in ['h', 'H']:
            tank.ToggleHatch(battle.selected_crew)
            UpdateTankCon()
            RenderEncounter()

        # issue an order to selected crew member from a menu
        elif key_char in ['o', 'O']:
            # only allow if a valid crew member is selected
            if battle.selected_crew is None: return
            if battle.selected_crew.NoActions(): return
            NewPhase('Issue Order')

        # cycle through ammo reload selections
        elif key_char in ['r', 'R']:
            tank.CycleReload()
            UpdateTankCon()
            RenderEncounter()

        # toggle use of ready rack
        elif key_char in ['t', 'T']:
            tank.use_rr = not tank.use_rr
            UpdateTankCon()
            RenderEncounter()

        # switch to another order for selected crewman
        elif key_char in ['a', 'd'] or key.vk in [libtcod.KEY_LEFT, libtcod.KEY_RIGHT]:

            # only allow if a valid crew member is selected
            if battle.selected_crew is None: return
            if battle.selected_crew.NoActions(): return

            # find current order in order list
            n = 0
            for order in battle.selected_crew.orders_list:
                if order.name == battle.selected_crew.order:
                    break
                n += 1
            # find the previous or next one
            if key_char in ['d', 'D'] or key.vk == libtcod.KEY_RIGHT:
                if n == len(battle.selected_crew.orders_list) - 1:
                    battle.selected_crew.order = battle.selected_crew.orders_list[0].name
                else:
                    battle.selected_crew.order = battle.selected_crew.orders_list[n+1].name
            else:
                if n == 0:
                    battle.selected_crew.order = battle.selected_crew.orders_list[len(battle.selected_crew.orders_list) - 1].name
                else:
                    battle.selected_crew.order = battle.selected_crew.orders_list[n-1].name

            # reset spot ability to reflect new order
            battle.selected_crew.SetSpotAbility()
            UpdateTankCon()
            RenderEncounter()

        # debug: wound selected crew member
        if DEBUG:
            if key_char == 'w' and (key.lctrl or key.rctrl):
                if battle.selected_crew is None: return
                text = battle.selected_crew.TakeWound(None, None)
                UpdateTankCon()
                RenderEncounter()
                if text is not None:
                    PopUp(battle.selected_crew.name + ' is wounded! Result: ' + text)

            # generate crew report
            elif key_char == 'c' and (key.lctrl or key.rctrl):
                if battle.selected_crew is None: return
                text = battle.selected_crew.GenerateReport()
                for line in text:
                    WriteJournal(line)
                Message('DEBUG: Report added to campaign journal')

    # issue order input mode
    elif battle.phase == 'Issue Order':

        # select previous order in list
        if key_char in ['w', 'W'] or key.vk == libtcod.KEY_UP:
            if battle.selected_order > 0:
                battle.selected_order -= 1
            else:
                battle.selected_order = len(battle.selected_crew.orders_list)-1
            UpdateTankCon()
            RenderEncounter()

        # select next order in list
        elif key_char in ['s', 'S'] or key.vk == libtcod.KEY_DOWN:
            if len(battle.selected_crew.orders_list) > battle.selected_order + 1:
                battle.selected_order += 1
            else:
                battle.selected_order = 0
            UpdateTankCon()
            RenderEncounter()

        # issue selected order
        elif key_char in ['o', 'O']:
            battle.selected_crew.order = battle.selected_crew.orders_list[battle.selected_order].name
            # reset spot ability to reflect new order
            battle.selected_crew.SetSpotAbility()
            Message(battle.selected_crew.name + ' now on ' + battle.selected_crew.order + ' order.')
            battle.selected_order = None    # clear any selected order
            NewPhase('Orders')

    # pivot tank mode
    elif battle.phase == 'Pivot Tank':
        if key_char in ['d', 'D'] or key.vk == libtcod.KEY_RIGHT:    # pivot clockwise
            if tank.new_facing == 5:
                tank.new_facing = 0
            else:
                tank.new_facing += 1
            UpdateMapOverlay()
            RenderEncounter()
        elif key_char in ['a', 'A'] or key.vk == libtcod.KEY_LEFT:    # pivot counter clockwise
            if tank.new_facing == 0:
                tank.new_facing = 5
            else:

                tank.new_facing -= 1
            UpdateMapOverlay()
            RenderEncounter()
        elif key.vk == libtcod.KEY_ENTER:    # commit pivot
            battle.trigger_phase = True

    # rotate turret mode
    elif battle.phase == 'Rotate Turret':
        if key_char in ['d', 'D'] or key.vk == libtcod.KEY_RIGHT:    # rotate clockwise
            RotateTurret(True)
        elif key_char in ['a', 'A'] or key.vk == libtcod.KEY_LEFT:    # rotate counter clockwise
            RotateTurret(False)
        elif key.vk == libtcod.KEY_ENTER:    # commit rotation
            battle.trigger_phase = True

    # main gun firing mode
    elif battle.phase == 'Fire Main Gun':

        # if not holding RoF, can rotate turret or select a different target
        if not tank.has_rof:

            if key_char in ['d', 'D'] or key.vk == libtcod.KEY_RIGHT:    # rotate clockwise
                RotateTurret(True)
            elif key_char in ['a', 'A'] or key.vk == libtcod.KEY_LEFT:    # rotate counter clockwise
                RotateTurret(False)

            # switch firing mode if HE loaded
            elif key_char in ['f', 'F'] and tank.ammo_load == 'HE':
                battle.area_fire = not battle.area_fire
                UpdateTankCon()
                RenderEncounter()

            # select next target
            if key.vk == libtcod.KEY_TAB:
                SelectNextTarget()
                UpdateMapOverlay()
                RenderEncounter()

        # fire gun!
        if key.vk == libtcod.KEY_ENTER:
            FireMainGun()

        # cycle through ammo reload selections
        elif key_char in ['r', 'R']:
            tank.CycleReload()
            UpdateTankCon()
            RenderEncounter()

        # toggle use of ready rack
        elif key_char in ['t', 'T']:
            tank.use_rr = not tank.use_rr
            UpdateTankCon()
            RenderEncounter()

    # firing MGs
    elif battle.phase == 'Fire MGs':

        # if co-ax can fire, can rotate turret
        if tank.coax_mg_can_fire:
            if key_char in ['d', 'D'] or key.vk == libtcod.KEY_RIGHT:    # rotate clockwise
                RotateTurret(True)
            elif key_char in ['a', 'A'] or key.vk == libtcod.KEY_LEFT:    # rotate counter clockwise
                RotateTurret(False)

        # activate a different MG
        if tank.coax_mg_can_fire or tank.bow_mg_can_fire or tank.aa_mg_can_fire:
            if key_char in ['m', 'M']:
                if tank.active_mg == 0:
                    if tank.bow_mg_can_fire:
                        tank.active_mg = 1
                    elif tank.aa_mg_can_fire:
                        tank.active_mg = 2
                elif tank.active_mg == 1:
                    if tank.aa_mg_can_fire:
                        tank.active_mg = 2
                    elif tank.coax_mg_can_fire:
                        tank.active_mg = 0
                elif tank.active_mg == 2:
                    if tank.coax_mg_can_fire:
                        tank.active_mg = 0
                    elif tank.bow_mg_can_fire:
                        tank.active_mg = 1
                UpdateMapOverlay()
                RenderEncounter()
                SelectNextTarget()

        # select next target
        if key.vk == libtcod.KEY_TAB:
            SelectNextTarget()
            UpdateMapOverlay()
            RenderEncounter()

        # fire an MG
        elif key.vk == libtcod.KEY_ENTER:
            FireMG()
            # no more MGs can fire
            if tank.active_mg == -1:
                battle.trigger_phase = True

    libtcod.console_flush()


################################################################################
#                       Set up and Handle an Encounter                         #
################################################################################

# starts up or loads and continues a battle encounter
def InitEncounter(load=False, counterattack=False, res_level=None):

    global battle

    # loading a battle in progress
    if load:

        # find the selected crewman: since pointer is saved, it's pointing to a
        # now non-existing object
        for crew_member in tank.crew:
            if crew_member.name == battle.selected_crew.name:
                battle.selected_crew = crew_member
                break

        # draw consoles for first time
        UpdateDateCon()
        UpdateTankCon()
        UpdateMsgCon()
        PaintMapCon()
        UpdateMapOverlay()
        UpdateMapInfoCon(0,0)        # give 0, 0 for mouse position
        RenderEncounter()

    else:

        # set up battle object
        battle = Battle(counterattack=counterattack, res_level=res_level)

        # roll on deployment table for player tank status
        tank.SetDeployment()

        # set up initial list of orders for crew, also set their initial spot ability
        for crewman in tank.crew:
            crewman.BuildOrdersList()
            crewman.SetSpotAbility()

        # draw encounter consoles for first time
        PaintMapCon()
        UpdateMapOverlay()
        UpdateMapInfoCon(0,0)        # give 0, 0 for mouse position
        UpdateTankCon()
        UpdateMsgCon()
        UpdateDateCon()

        # first time we're showing the encounter console, so use a zoom-in effect
        RenderEncounter(zoom_in=True)

        Message('Encounter begins!')

        # activate enemy units and draw screen
        ActivateEnemies()
        RenderEncounter()

        # do artillery / air strike if any
        if campaign.day_map.player_node.arty_strike:
            # reset flag
            campaign.day_map.player_node.arty_strike = False

            PopUp('Friendly forces conduct artillery fire against the enemy.')
            result = False

            # play sound effects
            PlaySound('arty_firing')

            for unit in battle.enemy_units:
                if not unit.alive: continue
                if unit.FriendlyAction(artillery=True):
                    result = True
                UpdateMapOverlay()
                RenderEncounter()

            if not result:
                PopUp('No results from Friendly Artillery.')

        elif campaign.day_map.player_node.air_strike:
            # reset flag
            campaign.day_map.player_node.air_strike = False

            PopUp('Friendly forces conduct an air strike against the enemy.')
            result = False

            for unit in battle.enemy_units:
                if not unit.alive: continue
                if unit.FriendlyAction(air_strike=True):
                    result = True
                UpdateMapOverlay()
                RenderEncounter()

            if not result:
                PopUp('No results from air strike.')

        # advancing fire results
        if campaign.day_map.player_node.advancing_fire:
            # reset flag
            campaign.day_map.player_node.advancing_fire = False

            PopUp('You use advancing fire to attack the enemy.')
            result = False

            # sound effects played before advancing fire resolution
            soundfile = GetFiringSound(tank.stats['main_gun'])
            if soundfile is not None:
                PlaySound(soundfile)
                Wait(300)
                PlaySound(soundfile)
                Wait(300)
                PlaySound(soundfile)

            for unit in battle.enemy_units:
                if not unit.alive:
                    continue
                if unit.FriendlyAction(advance_fire=True):
                    result = True
                    # TODO bug
                    # Add actual result from advancing fire, like the enemy
                    # unit being destroyed

                UpdateMapOverlay()
                RenderEncounter()

            if not result:
                PopUp('No results from advancing fire.')

        # select first crew by default
        battle.selected_crew = tank.crew[0]

        # check to make sure there's at least one enemy left alive after initial
        #  attacks
        if not AllEnemiesDead():

            # do ambush roll
            roll = Roll1D10()

            # apply weather modifiers
            if campaign.weather.fog or campaign.weather.precip != 'None':
                roll -= 1

            # terrain modifiers
            if campaign.day_map.player_node.node_type == 'F':    # bocage
                roll -= 2

            # check for keen senses skill
            crew_member = GetCrewByPosition('Commander')
            if crew_member.SkillCheck('Keen Senses'):
                if campaign.scen_type != 'Counterattack' and not battle.counterattack:
                    roll += 2
                else:
                    roll -= 2

            # ambush occurs if roll <= 7
            if roll <= 7:

                # counterattack ambush!
                if campaign.scen_type == 'Counterattack' or battle.counterattack:
                    PopUp('Your forces have ambushed the enemy!')
                    battle.friendly_ambush = True
                else:
                    PopUp('Your tank has been ambushed! Enemy gets first attack.')
                    ##### Enemy Action #####
                    NewPhase('Enemy Action')
                    for unit in battle.enemy_units:
                        if not unit.alive: continue
                        unit.DoAction(ambush=True)
                        UpdateMapOverlay()
                        RenderEncounter()
                        # check to see if tank has been knocked out by enemy action
                        # or if commander has been taken out
                        if battle.result != 'Undetermined' or campaign.over:
                            if not campaign.over:
                                EncounterMenu()
                            return
                ##### Random Events #####
                NewPhase('Random Events')
                RandomEvent()
            else:
                PopUp('Enemy units are caught off guard, you have first attack.')

            # set spot ability for crew
            for crew_member in tank.crew:
                crew_member.SetSpotAbility()


            # see if we need to set spot sectors for one or more crewmen
            if CheckSpotSectors():
                # select first crew that can choose one spot sector
                for crew_member in tank.crew:
                    if crew_member.spot == 'Any One Sector':
                        battle.selected_crew = crew_member
                        break

                NewPhase('Set Spot Sectors')
            else:

                # do initial spotting phase
                DoSpotting()

                # next phase is orders
                NewPhase('Orders')

        # if all enemies dead
        else:

            PopUp('Your initial attack has destroyed all enemy forces!')
            # skip right to orders phase
            NewPhase('Orders')

        SaveGame()

    # start the encounter handler
    DoEncounter()



##########################################################################################
#                                  Campaign Functions                                    #
##########################################################################################

# draw the campaign map onto the console
# done when a new map is generated, or a saved game is loaded
def PaintCampaignMap():
    libtcod.console_clear(c_map_con)

    # create the RNG based on the saved seed
    rng = libtcod.random_new_from_seed(campaign.day_map.seed)

    ##### Determine colour scheme to use based on season and current ground cover

    # Field color, Woods ground color, Coniferous tree, Deciduous tree,
    # village ground, marsh ground

    LATE_SUMMER_TO_MID_AUTUMN = [(140,110,16), (16,60,16), (80,110,80), (80,110,80),
        (60,90,60), (60,30,10)]
    MID_TO_LATE_AUTUMN = [(120,90,16), (16,60,16), (80,110,80), (200,80,20),
        (60,90,60), (60,30,10)]
    EDGE_OF_WINTER = [(110,90,45), (70,45,15), (80,110,80), (80,50,30),
        (80,70,45), (60,90,45)]
    WINTER_OR_GROUND_SNOW = [(240,240,240), (240,240,240), (80,110,80), (80,50,30),
        (240,240,240), (240,240,240)]
    SPRING = [(110,170,110), (36,80,36), (80,110,80), (230,135,210),
        (60,90,60), (60,30,10)]
    SUMMER = [(90,150,90), (16,60,16), (80,110,80), (80,110,80),
        (60,90,60), (60,30,10)]

    # snow ground automatically means winter colours
    if campaign.weather.ground in ['Snow', 'Deep Snow']:
        color_scheme = WINTER_OR_GROUND_SNOW
        campaign.color_scheme = 'WINTER_OR_GROUND_SNOW'

    # late autumn, winter with no snow, or early spring
    elif campaign.current_date[1] in [11, 12, 1, 2, 3]:
        color_scheme = EDGE_OF_WINTER
        campaign.color_scheme = 'EDGE_OF_WINTER'

    # spring
    elif campaign.current_date[1] in [4, 5]:
        color_scheme = SPRING
        campaign.color_scheme = 'SPRING'

    # summer
    elif campaign.current_date[1] in [6, 7]:
        color_scheme = SUMMER
        campaign.color_scheme = 'SUMMER'

    # late summer to mid autumn
    elif campaign.current_date[1] in [8, 9]:
        color_scheme = LATE_SUMMER_TO_MID_AUTUMN
        campaign.color_scheme = 'LATE_SUMMER_TO_MID_AUTUMN'

    # autumn
    else:
        color_scheme = MID_TO_LATE_AUTUMN
        campaign.color_scheme = 'MID_TO_LATE_AUTUMN'


    ##### Paint base display characters for each coordinate #####
    for y in range(0, C_MAP_CON_HEIGHT):
        for x in range (0, C_MAP_CON_WIDTH):
            parent_node = campaign.day_map.char_locations[(x,y)]

            # Fields and Farm Buildings, Fields, Bocage base
            if parent_node.node_type in ['A', 'B', 'F']:
                c_mod = libtcod.random_get_int(rng, -3, 7)
                (r,g,b) = color_scheme[0]
                bc = libtcod.Color(r+c_mod, g+c_mod, b+c_mod)
                fc = libtcod.black
                display_char = 0

                # if this is an A area, chance of there being a farm
                # building here instead
                if parent_node.node_type == 'A':
                    if libtcod.random_get_int(rng, 1, 50) == 1:
                        bc = libtcod.grey
                        fc = libtcod.light_grey
                        display_char = 179

            # woods
            elif parent_node.node_type == 'D':
                c_mod = libtcod.random_get_int(rng, -5, 10)
                (r,g,b) = color_scheme[1]
                bc = libtcod.Color(r+c_mod, g+c_mod, b+c_mod)
                fc = libtcod.black
                display_char = 0

                # chance of a tree greeble
                if libtcod.random_get_int(rng, 1, 10) > 6:
                    c_mod = libtcod.random_get_int(rng, -20, 20)
                    if libtcod.random_get_int(rng, 1, 8) == 1:
                        display_char = libtcod.CHAR_ARROW2_N
                        (r,g,b) = color_scheme[2]
                        fc = libtcod.Color(r+c_mod, g+c_mod, b+c_mod)
                    else:
                        display_char = libtcod.CHAR_SPADE
                        (r,g,b) = color_scheme[3]
                        fc = libtcod.Color(r+c_mod, g+c_mod, b+c_mod)

            # villages
            elif parent_node.node_type == 'C':
                c_mod = libtcod.random_get_int(rng, -5, 10)
                (r,g,b) = color_scheme[4]
                bc = libtcod.Color(r+c_mod, g+c_mod, b+c_mod)
                fc = libtcod.black
                display_char = 0

                # if within village building radius, chance of a building here
                dist = GetDistance(x, y, parent_node.x, parent_node.y)
                if dist <= parent_node.village_radius:

                    chance = int(100.0 * (float(dist) / float(parent_node.village_radius)))

                    if libtcod.random_get_int(rng, 1, 120) >= chance:

                        # dirt background
                        c_mod = libtcod.random_get_int(rng, -5, 10)
                        bc = libtcod.Color(80+c_mod, 50+c_mod, 30+c_mod)

                        # possible building building or dirt
                        if libtcod.random_get_int(rng, 1, 3) == 3:
                            fc = libtcod.light_grey
                            display_char = 254

            # marshland
            else:
                if libtcod.random_get_int(rng, 1, 3) <= 2:
                    c_mod = libtcod.random_get_int(rng, -5, 10)
                    bc = libtcod.Color(10+c_mod, 30+c_mod, 60+c_mod)
                else:
                    c_mod = libtcod.random_get_int(rng, -5, 10)
                    (r,g,b) = color_scheme[4]
                    bc = libtcod.Color(r+c_mod, g+c_mod, b+c_mod)

                fc = libtcod.black
                display_char = 0
                # possible greeble
                if libtcod.random_get_int(rng, 1, 8) == 1:
                    if libtcod.random_get_int(rng, 1, 5) == 1:
                        c_mod = libtcod.random_get_int(rng, -20, 20)
                        # use deciduous tree colour
                        (r,g,b) = color_scheme[3]
                        fc = libtcod.Color(r+c_mod, g+c_mod, b+c_mod)
                        if libtcod.random_get_int(rng, 1, 8) == 1:
                            display_char = libtcod.CHAR_ARROW2_N
                        else:
                            display_char = libtcod.CHAR_SPADE
                    else:
                        c_mod = libtcod.random_get_int(rng, -5, 10)
                        fc = libtcod.Color(16, 60+c_mod, 16)
                        display_char = 19

            # if this is an edge coordinate, set a little darker
            if (x,y) in parent_node.edges:
                bc = bc * libtcod.lighter_grey
                fc = fc * libtcod.lighter_grey

            # paint the char
            libtcod.console_put_char_ex(c_map_con, x, y, display_char, fc, bc)

    ##### Build Improved Roads #####

    # attempt to generate an improved road linking two nodes
    def GenerateRoad(node1, node2, dirt=False):
        # get path if possible, and link nodes together
        path = GetPath(node1, node2)
        if path != []:
            lastnode = node1
            for node in path:
                if not dirt:
                    lastnode.stone_road_links.append(node)
                    node.stone_road_links.append(lastnode)
                else:
                    lastnode.dirt_road_links.append(node)
                    node.dirt_road_links.append(lastnode)
                lastnode = node
            # improved roads should be extended to edge of map
            if not dirt:
                node1.road_end = True
                node2.road_end = True

    # 80% chance of a vertical improved road running through area
    if libtcod.random_get_int(rng, 1, 10) <= 8:

        # select start and end nodes
        node1 = None
        node2 = None
        for node in random.sample(campaign.day_map.nodes, len(campaign.day_map.nodes)):
            if node.bottom_edge and node.node_type != 'D' and node not in campaign.day_map.blocked_nodes:
                node1 = node
            elif node.top_edge and node.node_type != 'D' and node not in campaign.day_map.blocked_nodes:
                node2 = node
            if node1 is not None and node2 is not None:
                break

        # attempt to build road
        if node1 is not None and node2 is not None:
            GenerateRoad(node1, node2)

    # 20% chance of a crossroad
    if libtcod.random_get_int(rng, 1, 10) <= 2:

        # select start and end nodes
        node1 = None
        node2 = None
        for node in random.sample(campaign.day_map.nodes, len(campaign.day_map.nodes)):
            if node.top_edge or node.bottom_edge: continue
            if node.left_edge and node.node_type != 'D':
                node1 = node
            elif node.right_edge and node.node_type != 'D':
                node2 = node
            if node1 is not None and node2 is not None:
                break

        # attempt to build road
        if node1 is not None and node2 is not None:
            GenerateRoad(node1, node2)


    ##### Build Dirt Roads #####

    # go through villages nodes, if they are not already connected to an improved road,
    # try to link it via a dirt road to the nearest node that is connected
    for node1 in campaign.day_map.nodes:
        if node1.node_type == 'C':

            if len(node1.stone_road_links) > 0: continue
            if len(node1.dirt_road_links) > 0: continue

            closest = None
            for node2 in campaign.day_map.nodes:

                if node1 == node2: continue

                if len(node2.stone_road_links) > 0 or len(node2.dirt_road_links) > 0:
                    if closest is None:
                        closest = node2
                        continue
                    dist = GetDistance(node1.x, node1.y, node2.x, node2.y)
                    if dist < GetDistance(node1.x, node1.y, closest.x, closest.y):
                        closest = node2
                        continue

            if closest is not None:
                GenerateRoad(node1, closest, dirt=True)
                continue

            # no improved roads on the map, link to closest village or dirt road
            closest = None
            for node2 in campaign.day_map.nodes:
                if node1 == node2: continue
                if node2.node_type == 'C' or len(node2.dirt_road_links) > 0:
                    if closest is None:
                        closest = node2
                        continue
                    dist = GetDistance(node1.x, node1.y, node2.x, node2.y)
                    if dist < GetDistance(node1.x, node1.y, closest.x, closest.y):
                        closest = node2
                        continue

            if closest is not None:
                GenerateRoad(node1, closest, dirt=True)
                continue

    ##### Paint Roads #####

    # draw a road onto map
    def DrawRoad(line, dirt=False):
        # for each char location along this line, re-paint it
        for (x,y) in line:
            c_mod = libtcod.random_get_int(rng, -5, 10)
            if not dirt:
                col = libtcod.Color(60+c_mod, 60+c_mod, 60+c_mod)
            else:
                col = libtcod.Color(80+c_mod, 50+c_mod, 30+c_mod)
            libtcod.console_put_char_ex(c_map_con, x, y, 219, col, col)

    # dirt road links
    skip_nodes = []
    for node1 in campaign.day_map.nodes:
        if len(node1.dirt_road_links) == 0: continue
        skip_nodes.append(node1)
        for node2 in node1.dirt_road_links:
            if node2 in skip_nodes: continue
            line = GetLine(node1.x, node1.y, node2.x, node2.y)
            DrawRoad(line, dirt=True)

    # stone road links
    skip_nodes = []
    for node1 in campaign.day_map.nodes:
        if len(node1.stone_road_links) == 0: continue
        skip_nodes.append(node1)
        for node2 in node1.stone_road_links:
            if node2 in skip_nodes: continue
            line = GetLine(node1.x, node1.y, node2.x, node2.y)
            DrawRoad(line)

    # extend stone road ends to edge of map
    # if adjacent to another road_end, only pick one to extend
    for node in campaign.day_map.nodes:
        if node.road_end:

            # check that it's not adjacent to one that has already been extended
            # produces a "fork" effect at edge of map

            fork = False
            for node2 in node.links:
                if node2.extended:
                    fork = True
                    break
            if fork: continue

            if node.top_edge:
                line = GetLine(node.x, node.y, node.x, 0)
            elif node.bottom_edge:
                line = GetLine(node.x, node.y, node.x, C_MAP_CON_HEIGHT-1)
            elif node.left_edge:
                line = GetLine(node.x, node.y, 0, node.y)
            elif node.right_edge:
                line = GetLine(node.x, node.y, C_MAP_CON_WIDTH-1, node.y)
            else:
                continue

            DrawRoad(line)
            node.extended = True

    # bocage painting method
    for node in campaign.day_map.nodes:
        if node.node_type == 'F':

            def DrawBocage(x,y):
                c_mod = libtcod.random_get_int(rng, -5, 10)
                col = libtcod.Color(20+c_mod, 60+c_mod, 20+c_mod)
                libtcod.console_put_char_ex(c_map_con, x, y, 219, col, col)

            # create list of node locations
            locations = []
            for y in range(0, C_MAP_CON_HEIGHT):
                for x in range (0, C_MAP_CON_WIDTH):
                    if campaign.day_map.char_locations[(x,y)] == node:
                        locations.append((x,y))

            # draw outline
            for (x,y) in node.edges:
                DrawBocage(x,y)

            # fill in squares
            for i in range(4):
                n = libtcod.random_get_int(rng, 0, len(locations)-1)
                (x,y) = locations[n]
                w = libtcod.random_get_int(rng, 3, 9)
                h = libtcod.random_get_int(rng, 3, 9)

                for x1 in range(x-w, x+w+1):
                    if (x1,y-h) in locations and libtcod.console_get_char(c_map_con, x1, y-h) == 0:
                        DrawBocage(x1,y-h)
                    if (x1,y+h) in locations and libtcod.console_get_char(c_map_con, x1, y+h) == 0:
                        DrawBocage(x1,y+h)

                for y1 in range(y-h+1, y+h):
                    if (x-w,y1) in locations and libtcod.console_get_char(c_map_con, x-w, y1) == 0:
                        DrawBocage(x-w,y1)
                    if (x+w,y1) in locations and libtcod.console_get_char(c_map_con, x+w, y1) == 0:
                        DrawBocage(x+w,y1)


# draw and update the campaign map overlay
# used to show things that change on the campaign map: area control, player location, etc.
def UpdateCOverlay(highlight_node=None, anim_x=-1, anim_y=-1):
    # clear to key colour
    libtcod.console_set_default_background(c_overlay_con, KEY_COLOR)
    libtcod.console_clear(c_overlay_con)
    libtcod.console_set_default_background(c_overlay_con, libtcod.black)

    # highlight frontline between friendly and hostile map areas
    libtcod.console_set_default_foreground(c_overlay_con, FRONTLINE_COLOR)
    for node in campaign.day_map.nodes:
        if not node.friendly_control: continue
        # skip impassible nodes too
        if node in campaign.day_map.blocked_nodes: continue
        for (x,y) in node.edges:
            # check adjacent map character locations
            for (x2,y2) in [(x,y-1), (x-1,y), (x+1,y), (x,y+1)]:
                # adjacent character location is outside of map
                if (x2,y2) not in campaign.day_map.char_locations: continue
                node2 = campaign.day_map.char_locations[(x2,y2)]
                if node2 != node and not node2.friendly_control:
                    # draw the character
                    libtcod.console_put_char(c_overlay_con, x2, y2, 178, libtcod.BKGND_SET)

    # set foreground colour based on campaign map colours
    if campaign.color_scheme == 'WINTER_OR_GROUND_SNOW':
        libtcod.console_set_default_foreground(c_overlay_con, libtcod.blue)
    else:
        libtcod.console_set_default_foreground(c_overlay_con, libtcod.white)

    # draw a line to new location if doing campaign action
    # will appear beneath other information drawn below
    if campaign.input_mode != 'None' and campaign.selected_node is not None:
        if campaign.input_mode in ['Move Into Adjacent Area', 'Call in Strike']:
            line = GetLine(campaign.day_map.player_node.x, campaign.day_map.player_node.y,
                campaign.selected_node.x, campaign.selected_node.y)
            for (x, y) in line:
                libtcod.console_put_char(c_overlay_con, x, y, 250, libtcod.BKGND_SET)

    # display start / exit nodes, node center point
    for node in campaign.day_map.nodes:

        if node.start:
            libtcod.console_print_ex(c_overlay_con, node.x, node.y-1,
                libtcod.BKGND_SET, libtcod.CENTER, 'Start')
        elif node.exit:
            libtcod.console_print_ex(c_overlay_con, node.x, node.y-1,
                libtcod.BKGND_SET, libtcod.CENTER, 'Exit')

        # highlight player node or draw node center
        # don't draw player indicator if we are animating it
        if campaign.day_map.player_node == node and anim_x == -1:
            libtcod.console_put_char(c_overlay_con, node.x, node.y, '@', libtcod.BKGND_SET)
            for (x,y) in campaign.day_map.player_node.edges:
                libtcod.console_put_char(c_overlay_con, x, y, libtcod.CHAR_BULLET, libtcod.BKGND_SET)
        else:
            libtcod.console_put_char(c_overlay_con, node.x, node.y, libtcod.CHAR_BULLET,
                libtcod.BKGND_SET)

        if node.friendly_control:
            libtcod.console_print_ex(c_overlay_con, node.x, node.y+1,
                libtcod.BKGND_SET, libtcod.CENTER, campaign.player_nation)
        elif node.res_known and node.resistance is not None:
            libtcod.console_print_ex(c_overlay_con, node.x, node.y+1,
                libtcod.BKGND_SET, libtcod.CENTER, node.resistance)

        # highlighting node (overwrites player node highlight)
        if highlight_node == node:
            col = libtcod.console_get_default_foreground(c_overlay_con)
            libtcod.console_set_default_foreground(c_overlay_con, SELECTED_COLOR)
            for (x,y) in node.edges:
                libtcod.console_put_char(c_overlay_con, x, y, libtcod.CHAR_BULLET, libtcod.BKGND_SET)
            libtcod.console_set_default_foreground(c_overlay_con, col)

        if not node.friendly_control:
            if node.arty_strike or node.air_strike:
                libtcod.console_print_ex(c_overlay_con, node.x, node.y+2,
                    libtcod.BKGND_SET, libtcod.CENTER, 'Area hit by')
                if node.arty_strike:
                    text = 'Artillery'
                else:
                    text = 'Air Strike'
                libtcod.console_print_ex(c_overlay_con, node.x, node.y+3,
                    libtcod.BKGND_SET, libtcod.CENTER, text)

        # active quest node
        if node.quest_type is not None:
            libtcod.console_print_ex(c_overlay_con, node.x, node.y-2,
                libtcod.BKGND_SET, libtcod.CENTER, node.quest_type)

    # highlight selected area if any
    if campaign.input_mode != 'None' and campaign.selected_node is not None:
        libtcod.console_set_default_foreground(c_overlay_con, SELECTED_COLOR)
        for (x,y) in campaign.selected_node.edges:
            libtcod.console_put_char(c_overlay_con, x, y, 219, libtcod.BKGND_SET)

    # draw animated player indicator if any
    if anim_x > -1 and anim_y > -1:
        libtcod.console_set_default_foreground(c_overlay_con, libtcod.white)
        libtcod.console_put_char(c_overlay_con, anim_x, anim_y, '@', libtcod.BKGND_SET)


# draw the campaign action console
def UpdateCActionCon():
    libtcod.console_clear(c_action_con)

    # if we're doing an action
    if campaign.input_mode != 'None':

        # we're checking an adjacent area
        if campaign.input_mode == 'Check Adjacent Area':
            lines = CHECK_AREA
        # we're moving into an area
        elif campaign.input_mode == 'Move Into Adjacent Area':
            lines = MOVE_AREA
        elif campaign.input_mode == 'Call in Strike':
            lines = ['Call in Strike on Adjacent Area', '']
            lines.append('[%cTab%c] Cycle through adjacent areas (Shift to reverse)'%HIGHLIGHT)
            lines.append('Call in [%cA%c]rtillery Strike'%HIGHLIGHT)
            if campaign.weather.clouds != 'Overcast' and not campaign.weather.fog and campaign.weather.precip != 'Snow':
                lines.append('Call in Ai[%cr%c] Strike'%HIGHLIGHT)
            lines.append('[%cBackspace%c] Cancel action'%HIGHLIGHT)
        dy = 1
        for line in lines:
            libtcod.console_print(c_action_con, 0, dy, line)
            dy += 1

    else:
        libtcod.console_print(c_action_con, 0, 1, 'Action')
        libtcod.console_print(c_action_con, 0, 2, '------')
        libtcod.console_print(c_action_con, 41, 1, 'Mins. Required')
        libtcod.console_print(c_action_con, 41, 2, '--------------')
        dy = 4
        for (text, time) in campaign.action_list:
            libtcod.console_print(c_action_con, 0, dy, text)
            if time is not None:
                libtcod.console_print(c_action_con, 47, dy, str(time))
            else:
                libtcod.console_print(c_action_con, 47, dy, 'N/A')
            libtcod.console_set_default_foreground(c_action_con, libtcod.dark_grey)
            libtcod.console_hline(c_action_con, 0, dy+1, 50, flag=libtcod.BKGND_DEFAULT)
            libtcod.console_set_default_foreground(c_action_con, libtcod.white)
            dy += 2

    libtcod.console_print(c_action_con, 1, C_ACTION_CON_H-4, '[%cW/S/up/down%c]: Scroll Map'%HIGHLIGHT)

    # display time remaining until sunset if hasn't happened yet
    (sunset_h, sunset_m) = campaign.GetSunset()
    (h, m) = GetTimeUntil(campaign.hour, campaign.minute, sunset_h, sunset_m)
    if h < 0: return
    text = 'Time until sunset: ' + str(h) + ':' + str(m).zfill(2)
    libtcod.console_print(c_action_con, 1, C_ACTION_CON_H-2, text)


# draw the campaign area info console with info based on mouse position
def UpdateCInfoCon(mx, my):
    libtcod.console_clear(c_info_con)

    # display weather conditions
    DisplayWeather(c_info_con, C_INFO_CON_X-5, 0)
    libtcod.console_set_default_background(c_info_con, libtcod.black)
    libtcod.console_set_default_foreground(c_info_con, libtcod.white)

    # display artillery chance
    libtcod.console_print(c_info_con, 0, 0, 'Artillery Chance')
    libtcod.console_print(c_info_con, 7, 2, '<=' + str(campaign.arty_chance))

    libtcod.console_print(c_info_con, 38, 0, 'Air Strike Chance')
    if campaign.weather.clouds == 'Overcast' or campaign.weather.fog or campaign.weather.precip == 'Snow':
        text = 'N/A'
    else:
        text = '<=' + str(campaign.air_chance)
    libtcod.console_print(c_info_con, 46, 2, text)

    # make sure mouse cursor is over map window
    if mx < C_MAP_CON_X or mx >= C_MAP_CON_X + C_MAP_CON_WIDTH or my < 4:
        libtcod.console_print_ex(c_info_con, C_INFO_CON_X, 5,
            libtcod.BKGND_NONE, libtcod.CENTER, 'Mouseover an area for info')
        return

    # adjust for offset
    mx -= C_MAP_CON_X
    my = my - 4 + campaign.c_map_y

    # check in case of error
    if (mx,my) not in campaign.day_map.char_locations:
        print 'ERROR: Could not find character location under mouse cursor'
        return

    node = campaign.day_map.char_locations[(mx,my)]

    if node.node_type == 'A':
        text = 'Farm Buildings and Fields'
    elif node.node_type == 'B':
        text = 'Fields'
    elif node.node_type == 'C':
        text = 'Village'
    elif node.node_type == 'D':
        text = 'Woods'
    elif node.node_type == 'E':
        text = 'Marshland'
    elif node.node_type == 'F':
        text = 'Bocage'
    else:
        text = ''
    libtcod.console_print_ex(c_info_con, C_INFO_CON_X, 5, libtcod.BKGND_NONE,
        libtcod.CENTER, text)

    if node.friendly_control:
        text = 'Friendly Control'
    elif node.res_known:
        text = node.resistance + ' Enemy Resistance Expected'
    else:
        text = 'Unknown Enemy Resistance Level'
    libtcod.console_print_ex(c_info_con, C_INFO_CON_X, 7, libtcod.BKGND_NONE,
        libtcod.CENTER, text)

    if campaign.quest_active:
        if node.quest_type is not None:
            text = 'Active Quest: ' + node.quest_type
            libtcod.console_print_ex(c_info_con, C_INFO_CON_X, 9,
                libtcod.BKGND_NONE, libtcod.CENTER, text)
            text = 'VP Bonus: ' + str(node.quest_vp_bonus)
            libtcod.console_print_ex(c_info_con, C_INFO_CON_X, 10,
                libtcod.BKGND_NONE, libtcod.CENTER, text)
            if node.quest_time_limit is not None:
                (h, m) = node.quest_time_limit
                text = 'Expires: ' + str(h) + ':' + str(m).zfill(2)
                libtcod.console_print_ex(c_info_con, C_INFO_CON_X, 11,
                    libtcod.BKGND_NONE, libtcod.CENTER, text)


# set up "check adjacent area" action
def SetupCheckArea():
    # if no node selected, select first linked node in list
    if campaign.selected_node is None:
        campaign.selected_node = campaign.day_map.player_node.links[0]
    campaign.input_mode = 'Check Adjacent Area'
    UpdateCActionCon()
    UpdateCOverlay()
    RenderCampaign()


# check the selected area for enemy resistance
def CheckArea():

    # if friendly control, don't do anything
    if campaign.selected_node.friendly_control or campaign.selected_node.resistance is None:
        return

    # if known resistance level, don't do anything
    if campaign.selected_node.res_known:
        return

    # set flag to known resistance level
    campaign.selected_node.res_known = True

    # display results message
    text = campaign.selected_node.resistance + ' enemy resistance reported in this area.'
    ShowLabel(campaign.selected_node.x+C_MAP_CON_X, campaign.selected_node.y+4-campaign.c_map_y, text)

    # spend time if not free action
    if not campaign.free_check:
        campaign.SpendTime(0, 15)
    else:
        # clear the flag
        campaign.free_check = False

    # reset input mode
    campaign.input_mode = 'None'

    # chance of crew reaction
    if campaign.selected_node.resistance == 'Heavy':
        if Roll1D10() <= 2:
            CrewTalk(random.choice(CREW_TALK_HEAVY_RES))

    # might have completed a quest
    if campaign.selected_node.quest_type is not None:
        if campaign.selected_node.quest_type == 'RECON':
            campaign.AddStat('Quests Completed', 1)
            text = ('Congratulations, commander. You have reported your ' +
                'reconnaissance of the requested map area and have earned ' +
                str(campaign.selected_node.quest_vp_bonus) + ' bonus VP.')
            PopUp(text)
            WriteJournal('RECON quest completed')

            # award VP
            campaign.day_vp += campaign.selected_node.quest_vp_bonus

            # reset node and campaign flag
            campaign.selected_node.quest_type = None
            campaign.selected_node.quest_vp_bonus = None
            campaign.quest_active = False

    SaveGame()

    UpdateCActionCon()
    UpdateCOverlay()
    RenderCampaign()


# select the next adjacent area
def SelectNextArea():

    # build list of possible areas

    nodes = []
    if campaign.scen_type == 'Counterattack':
        for node in campaign.day_map.player_node.links:
            if not node.friendly_control: continue
            if node.top_edge:
                nodes.append(node)
                continue
            for link_node in node.links:
                if not link_node.friendly_control:
                    nodes.append(node)
                    continue
    else:
        for node in campaign.day_map.player_node.links:
            nodes.append(node)

    # no nodes could be found
    if len(nodes) == 0:
        campaign.selected_node = None
        return

    if campaign.selected_node is None:
        campaign.selected_node = nodes[0]
        return

    # sort by degree heading to player node
    def GetHeading(node):
        rads = atan2(node.y-campaign.day_map.player_node.y, node.x-campaign.day_map.player_node.x)
        rads %= 2*pi
        degs = degrees(rads) + 90
        if degs >= 360: degs -= 360
        return int(degs)
    node_list = []
    for node in nodes:
        node_list.append((node, GetHeading(node)))
    node_list.sort(key=lambda node: node[1])

    # find the current selected node
    n = 0
    for (node, heading) in node_list:
        if node == campaign.selected_node: break
        n += 1

    # reverse if shift is down
    if key.shift:
        # at start of list
        if n == 0:
            new_node = node_list[-1]
        else:
            new_node = node_list[n-1]
    else:
        # not at end of list
        if n < len(node_list) - 1:
            new_node = node_list[n+1]
        else:
            new_node = node_list[0]

    # set new selected node (heading is not used here)
    (campaign.selected_node, heading) = new_node

    UpdateCOverlay()
    RenderCampaign()


# set up "move to adjacent area" action
def SetupMoveArea():
    if campaign.selected_node is None:
        SelectNextArea()

    # if no areas could be selected, return
    if campaign.selected_node is None:
        return

    campaign.input_mode = 'Move Into Adjacent Area'
    UpdateCActionCon()
    UpdateCOverlay()
    RenderCampaign()


# move into selected area
def MoveArea():

    # determine how much time to spend
    text = 'You move into a new area'
    if campaign.selected_node in campaign.day_map.player_node.stone_road_links:
        time_req = STONE_ROAD_MOVE_TIME
        text += ' along an improved road'
    elif campaign.selected_node in campaign.day_map.player_node.dirt_road_links:
        time_req = DIRT_ROAD_MOVE_TIME
        text += ' along a dirt road'
    else:
        time_req = NO_ROAD_MOVE_TIME

    if campaign.weather.ground != 'Dry' or campaign.weather.precip != 'None' or campaign.weather.fog:
        time_req += GROUND_MOVE_TIME_MODIFIER

    text += ' which takes ' + str(time_req) + ' minutes.'

    # if target area is enemy controlled, see if can use advancing fire
    # must have at least 6 HE shells
    # NEW: main gun must also be operational
    gun_malfunction = 'Main Gun Malfunction' in tank.damage_list or 'Main Gun Broken' in tank.damage_list
    total_he = tank.general_ammo['HE'] + tank.rr_ammo['HE']

    # NEW: handle situations when there is no node selected
    friendly_control = False
    if campaign.selected_node is not None:
        if campaign.selected_node.friendly_control:
            friendly_control = True

    if not gun_malfunction and not friendly_control and total_he >= 6:

        text += ' Use advancing fire (requires 1-6 HE rounds; currently have '
        text += str(total_he) + ' rounds)?'
        if PopUp(text, confirm=True):
            # determine number of rounds required and expend shells, pulling
            # from general stores first, then ready rack
            rounds_req = Roll1D6()
            for r in range(rounds_req):
                if tank.general_ammo['HE'] > 0:
                    tank.general_ammo['HE'] -= 1
                elif tank.rr_ammo['HE'] > 0:
                    tank.rr_ammo['HE'] -= 1

            # set flag
            campaign.selected_node.advancing_fire = True

            # show result
            text = 'You expend ' + str(rounds_req) + ' HE round'
            if rounds_req > 1: text += 's'
            text += ' entering the area.'
            PopUp(text)
    else:
        PopUp(text)

    campaign.SpendTime(0, time_req)

    # play sound effect
    PlaySound('sherman_movement')

    # movement animation
    if campaign.animations:
        line = GetLine(campaign.day_map.player_node.x, campaign.day_map.player_node.y,
            campaign.selected_node.x, campaign.selected_node.y)
        for (x,y) in line:
            UpdateCOverlay(anim_x=x, anim_y=y)
            RenderCampaign()
            Wait(100)

    # move player to target node
    campaign.day_map.player_node = campaign.selected_node

    # clean up and reset input mode
    campaign.selected_node = None
    campaign.input_mode = 'None'

    UpdateCOverlay()
    UpdateCActionCon()
    RenderCampaign()

    # if not under friendly control, possibly trigger a combat encounter
    #  if we moved during a counterattack, battle is automatic
    if campaign.scen_type == 'Counterattack' or not campaign.day_map.player_node.friendly_control:

        # battle roll
        roll = Roll1D10()

        if campaign.day_map.player_node.node_type == 'A':
            roll += 1
        elif campaign.day_map.player_node.node_type in ['C', 'F']:
            roll += 2

        if campaign.day_map.player_node.resistance == 'Light':
            target_score = 8
        elif campaign.day_map.player_node.resistance == 'Medium':
            target_score = 6
        else:
            target_score = 4

        # check for capture quest: automatic battle
        if campaign.day_map.player_node.quest_type is not None:
            if campaign.day_map.player_node.quest_type in ['CAPTURE', 'RESCUE']:
                target_score = 1

        # counterattack: automatic battle
        elif campaign.scen_type == 'Counterattack':
            target_score = 1

        if roll < target_score:
            PopUp('You meet no resistance in this area.')
            no_combat = True

            # award exp to crew
            for crew in tank.crew:
                crew.AwardExp(1)

            # chance of crew reaction
            if Roll1D10() == 1:
                CrewTalk(random.choice(CREW_TALK_NO_RES))

        else:
            PopUp('A battle encounter is triggered!')
            WriteJournal('')
            text = 'Battle encounter triggered at ' + str(campaign.hour) + ':' + str(campaign.minute).zfill(2)
            text += ', ' + campaign.GetTerrainDesc(campaign.day_map.player_node) + ' terrain'
            WriteJournal(text)

            campaign.SpendTime(0, 15)

            # enter encounter
            InitEncounter()

            # if we're exiting, don't bother re-drawing the screen
            if campaign.exiting:
                return

            no_combat = False

        # do post-encounter stuff and return
        PostEncounter(no_combat)

    else:

        # possible DEFEND mission
        if campaign.day_map.player_node.quest_type is not None:
            if campaign.day_map.player_node.quest_type == 'DEFEND':
                m = random.choice([15, 30, 45])
                PopUp('You arrive to defend the map area. ' + str(m) +
                    ' minutes later, the expected attack occurs.')
                campaign.SpendTime(0, m)
                InitEncounter(counterattack=True)
                if campaign.exiting:
                    return
                PostEncounter(False)
                return

        # check for sunset
        campaign.CheckSunset()

        SaveGame()
        UpdateCActionCon()
        UpdateCOverlay()
        RenderCampaign()


# Await for an enemy attack in the counterattack mission
#  if no_time, then we are triggering an attack right away
def AwaitEnemy(no_time=False):

    if not no_time:

        PopUp('You await an enemy counterattack.')

        # roll for how long it takes until the next enemy attack
        d1, d2, roll = Roll2D6()

        # apply modifier based on expected resistence for the day
        if campaign.scen_res == 'Medium':
            roll += 2
        elif campaign.scen_res == 'Heavy':
            roll += 4

        h = 1
        if roll >= 11:
            m = 15
        elif roll >= 8:
            m = 30
        elif roll >= 6:
            m = 45
        elif roll >= 4:
            h = 2
            m = 0
        else:
            h = 2
            m = 30

        # let time pass
        campaign.SpendTime(h, m)

        # if sunset has hit, don't do an attack
        campaign.CheckSunset()
        if campaign.sunset:
            return

    # show message and start attack
    PopUp('A battle encounter is triggered!')
    WriteJournal('')
    text = 'Battle encounter triggered at ' + str(campaign.hour) + ':' + str(campaign.minute).zfill(2)
    text += ', ' + campaign.GetTerrainDesc(campaign.day_map.player_node) + ' terrain'
    WriteJournal(text)
    campaign.SpendTime(0, 15)

    # determine encounter resistance level: default is day resistance level
    res_level = campaign.scen_res

    nodes = []
    for node in campaign.day_map.player_node.links:
        if not node.friendly_control:
            nodes.append(node)

    if len(nodes) > 0:
        node = random.choice(nodes)
        res_level = node.resistance

    # enter encounter
    InitEncounter(res_level=res_level)

    # if we're exiting, don't bother re-drawing the screen
    if campaign.exiting:
        return

    UpdateCActionCon()
    UpdateCOverlay()
    RenderCampaign()

    # do post-encounter stuff
    PostEncounter()

    campaign.CheckSunset()
    SaveGame()
    UpdateCActionCon()
    UpdateCOverlay()
    RenderCampaign()


# set up call in artillery strike action
def SetupCallStrike():
    if campaign.selected_node is None:
        SelectNextArea()
    campaign.input_mode = 'Call in Strike'
    UpdateCActionCon()
    UpdateCOverlay()
    RenderCampaign()


# attempt to call in an artillery or air strike
def CallStrike(key_char):

    # if target area is friendly, don't allow!
    if campaign.selected_node.friendly_control:
        return

    # if air strike called and not allowed, return
    if key_char in ['r', 'R'] and (campaign.weather.clouds == 'Overcast' or campaign.weather.fog or campaign.weather.precip == 'Snow'):
        return

    # if target area already has been hit by either, return
    if campaign.selected_node.air_strike or campaign.selected_node.arty_strike:
        return

    campaign.input_mode = 'None'

    # calculate time required and odds of success, spend the time and try to call in strike
    d1, d2, roll = Roll2D6()
    success = False

    if key_char in ['a', 'A']:
        campaign.SpendTime(0, 15)
        if roll <= campaign.arty_chance:
            success = True
            text = 'Success: Friendly artillery strikes target area'
            # set flag in area
            campaign.selected_node.arty_strike = True
            if campaign.arty_chance > 2:
                campaign.arty_chance -= 1
        else:
            text = 'Friendly artillery is unable to strike target area'

    else:
        campaign.SpendTime(0, 30)
        if roll <= campaign.air_chance:
            success = True
            text = 'Success: Friendly air forces strike target area'
            # set flag in area
            campaign.selected_node.air_strike = True
            if campaign.air_chance > 2:
                campaign.air_chance -= 1
        else:
            text = 'Friendly air forces are unable to strike target area'

    x,y = campaign.selected_node.x+C_MAP_CON_X, campaign.selected_node.y+4-campaign.c_map_y
    ShowLabel(x, y, text)

    # play sound and show animation if enabled
    if success:
        # clear label
        Wait(400)
        libtcod.console_blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)
        libtcod.console_flush()
        PlaySound('arty_firing')
        ArtyStrikeAnimation(x, y)

        # chance of crew reaction
        if key_char in ['a', 'A']:
            if Roll1D10() <= 3:
                CrewTalk(random.choice(CREW_TALK_ARTY_STRIKE))

    else:
        if key_char in ['a', 'A']:
            # chance of crew reaction
            if Roll1D10() <= 3:
                CrewTalk(random.choice(CREW_TALK_NO_ARTY_STRIKE))

    UpdateCActionCon()
    UpdateCInfoCon(mouse.cx, mouse.cy)
    UpdateCOverlay()
    RenderCampaign()


# do post-encounter, or post-area capture, maintenance stuff
# called by MoveArea as well as DoCampaignDay() when loading right into an
# encounter in progress
def PostEncounter(no_combat=False):

    # check to see if we're ending the campaign because commander is dead or sent home
    if CheckCommander():
        campaign.exiting = True

    # check for repair attempts if we're not exiting out of the campaign and we just
    #  finished a battle encounter
    if not campaign.exiting and not no_combat:
        AttemptRepairs(post_encounter=True)

    # check for exiting campaign or tank destroyed or damaged
    if campaign.exiting or not tank.alive or tank.swiss_cheese:

        campaign.sunset = True

        if not tank.alive:
            WriteJournal('Player tank knocked out, action day is over')
        elif tank.swiss_cheese:
            WriteJournal('Player tank damaged beyond repair, action day is over')
        else:
            return

        # award exp for the day to crew, check for level gain
        campaign.EndOfDay()

        return

    # reset tank after encounter
    tank.ResetAfterEncounter()

    # if player node was not previously under player control, change it now and
    # award VP for capturing area
    if not campaign.day_map.player_node.friendly_control:
        campaign.day_map.player_node.friendly_control = True
        campaign.AwardCaptureVP(campaign.day_map.player_node)

        # record captured area
        campaign.AddStat('Map Areas Captured', 1)

        # check quests
        if campaign.day_map.player_node.quest_type is not None:

            # award VP for capture or rescue quest
            if campaign.day_map.player_node.quest_type in ['CAPTURE', 'RESCUE']:
                campaign.AddStat('Quests Completed', 1)
                text = ('Congratulations, commander. You have captured the ' +
                    'requested map area')
                if campaign.day_map.player_node.quest_type == 'RESCUE':
                    text += ' and rescued your allied units'
                text += ('. You have earned ' +
                    str(campaign.day_map.player_node.quest_vp_bonus) +
                    ' bonus VP.')
                PopUp(text)
                WriteJournal(campaign.day_map.player_node.quest_type +
                    ' quest completed.')

                # award VP
                campaign.day_vp += campaign.day_map.player_node.quest_vp_bonus

            # reset node and campaign flag
            # this will cancel any RECON mission in the area as well
            campaign.day_map.player_node.quest_type = None
            campaign.day_map.player_node.quest_vp_bonus = None
            campaign.day_map.player_node.quest_time_limit = None
            campaign.quest_active = False

    else:
        # possible completion of DEFEND mission
        if campaign.day_map.player_node.quest_type is not None:
            if campaign.day_map.player_node.quest_type == 'DEFEND':
                campaign.AddStat('Quests Completed', 1)
                text = ('Congratulations, commander. You have defended the ' +
                    'requested map area')
                PopUp(text)
                WriteJournal('DEFEND quest completed.')
                campaign.day_vp += campaign.day_map.player_node.quest_vp_bonus
                campaign.day_map.player_node.quest_type = None
                campaign.day_map.player_node.quest_vp_bonus = None
                campaign.quest_active = False

        # possible defense in counterattack mission
        elif not no_combat and campaign.scen_type == 'Counterattack':
            campaign.AwardCaptureVP(campaign.day_map.player_node, counterattack=True)

    # award exp to crew for capturing area
    for crew in tank.crew:
        crew.AwardExp(1)

    # crew recovers, check for crew replacements
    ReplaceCrew()

    # if tank is immobilized, day of combat also ends
    if tank.immobilized:
        WriteJournal('Player tank immobilized, action day is over')
        campaign.sunset = True
        # award exp for the day to crew
        for crew in tank.crew:
            d1, d2, roll = Roll2D6()
            crew.AwardExp(roll)
        CampaignMenu()
        return

    campaign.CheckSunset()

    # trigger view tank to allow player to change hatches, gun load, etc.
    if not campaign.sunset and not no_combat:
        WriteJournal('Battle encounter ended at ' + str(campaign.hour) + ':' + str(campaign.minute).zfill(2))
        PopUp('Set up your tank for the next battle.')
        CampaignViewTank()
        RenderCampaign()

    # we're continuing the day, check if we need to add the "head home" campaign action
    campaign.BuildActionList()
    UpdateCActionCon()

    # if sunset hasn't hit, check for some game events
    if not campaign.sunset:

        # if player just captured the exit area,
        # reset nodes, generate new start and exit areas, move player to new start area
        if campaign.scen_type != 'Counterattack' and campaign.day_map.player_node.exit:
            PopUp('You captured the exit area! Press Enter to move to new map.')
            WriteJournal('Captured exit area and moved to new map')

            libtcod.console_clear(con)
            libtcod.console_print_ex(con, SCREEN_XM, int(SCREEN_HEIGHT/2),
                libtcod.BKGND_NONE, libtcod.CENTER, 'Generating Campaign Map...')
            libtcod.console_blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)
            libtcod.console_flush()

            # generate a new map
            good_map = False
            while not good_map:
                campaign.nodes = []
                good_map = GenerateCampaignMap()
            PaintCampaignMap()

            # move player view to starting node of new map
            campaign.MoveViewTo(campaign.day_map.player_node)

            # set initial input mode to check adjacent area, no time cost
            SetupCheckArea()
            campaign.free_check = True
            RenderCampaign()
            PopUp('Select an adjacent area to check for enemy resistance.')

        # otherwise, check for a counterattack advance or campaign event trigger
        else:

            if campaign.scen_type == 'Counterattack':
                campaign.DoEnemyAdvance()
            else:
                campaign.RandomCampaignEvent()

    SaveGame()

    UpdateDateCon()
    UpdateCActionCon()
    UpdateCOverlay()
    RenderCampaign()


# return the highest crew level to use for replacements
def GetHighestCrewLevel():
    crew_levels = []
    for crewman in tank.crew:
        if crewman.alive and not crewman.v_serious_wound:
            crew_levels.append(crewman.level)
    # no crew left alive!
    if len(crew_levels) == 0:
        return 1
    else:
        return max(crew_levels)


# set the next and previous pointers for all crewmembers
def SetCrewPointers():
    n = 0
    for crewman in tank.crew:
        if n == 0:
            crewman.prev = tank.crew[-1]
        else:
            crewman.prev = tank.crew[n-1]

        if n == len(tank.crew)-1:
            crewman.next = tank.crew[0]
        else:
            crewman.next = tank.crew[n+1]
        n += 1


# replace any dead or very seriously injured crew in the player tank
# replacing 1+ crew takes 30 mins., unless counterattack
def ReplaceCrew():
    replaced = False

    # calculate upper limit for level of replacement crew
    highest_level = GetHighestCrewLevel()

    # check for replacements
    for crewman in tank.crew:

        # generate a replacement crew member for the dead and very seriously wounded
        if not crewman.alive or crewman.v_serious_wound:

            # display a notification window
            text = crewman.name + ' has been '
            if not crewman.alive:
                text += 'killed in action.'
            else:
                text += 'severely wounded and has been sent home.'
            text += ' A final report on their service will be added to the campaign journal.'
            PopUp(text)

            # record final report to campaign journal
            text = crewman.GenerateReport()
            for line in text:
                WriteJournal(line)

            replaced = True
            new_crew = SpawnCrewMember(None, crewman.position, crewman.rank_level, replacement=True, old_member=crewman)

            # determine level of replacement crewman
            new_level = libtcod.random_get_int(0, 1, highest_level)
            new_crew.SetLevel(new_level)

            text = crewman.name + ' is replaced by ' + new_crew.name
            text += ' in the ' + new_crew.position + "'s position"
            PopUp(text)
            WriteJournal(text)
            ShowSkills(new_crew)

        else:
            # reset status flags
            crewman.stunned = False
            crewman.unconscious = False

    # remove the dead and very seriously wounded; record in campaign stats
    for crewman in reversed(tank.crew):
        if not crewman.alive or crewman.v_serious_wound:
            if not crewman.alive:
                campaign.AddStat('Crewmen KIA', 1)
            else:
                campaign.AddStat('Crewmen Sent Home', 1)
            tank.crew.remove(crewman)

    # re-order tank crew list
    CREW_ORDER = ['Commander', 'Gunner', 'Loader', 'Driver', 'Asst. Driver']
    def GetCrewOrder(crew):
        return CREW_ORDER.index(crew.position)
    tank.crew.sort(key = GetCrewOrder)

    # reset next and previous pointers for all crew
    SetCrewPointers()

    # if we replaced 1+ crew and we're in a campaign day, takes time
    # unless in counterattack
    if replaced and campaign.day_in_progress and campaign.scen_type != 'Counterattack':
        PopUp('Crew replacement took 30 mins')
        campaign.SpendTime(0, 30)


# setup resupply attempt
def SetupResupply():

    # do roll
    roll = Roll1D10()

    # spend time required
    if campaign.scen_type == 'Counterattack':
        time_used = 15
        roll = 1
    else:
        time_used = 60
    campaign.SpendTime(0, time_used)

    if roll <= 7:
        PopUp('Supply trucks arrive; you may replenish your ammo stores.')
        # replenish smoke grenade and bomb stores
        tank.smoke_grenades = 6
        tank.smoke_bombs = 15
        campaign.resupply = True
        MainGunAmmoMenu()
        campaign.resupply = False
    else:
        PopUp('You wait for resupply but the supply trucks are delayed and never arrive.')

    # update day clock
    UpdateCActionCon()
    RenderCampaign()

    # check for sunset
    campaign.CheckSunset()


# show the tank stats and allow the player to change ammo load, etc.
def CampaignViewTank(load_ammo_menu=False):
    # darken screen
    libtcod.console_clear(con)
    libtcod.console_blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0,
        0.0, 0.7)

    CON_X = MENU_CON_XM - int(TANK_CON_WIDTH/2)
    CON_Y = int(MENU_CON_HEIGHT/2) - int(TANK_CON_HEIGHT/2)

    # automatically refill smoke grenades and bombs if resupplying
    if campaign.resupply:
        tank.smoke_grenades = 6
        tank.smoke_bombs = 15

    # select first crew member if none selected yet
    if campaign.selected_crew == None:
        campaign.selected_crew = tank.crew[0]

    exit_view = False
    while not exit_view:

        # generate and display menu
        libtcod.console_clear(menu_con)
        libtcod.console_print_frame(menu_con, 0, 0, MENU_CON_WIDTH, MENU_CON_HEIGHT,
            clear=False, flag=libtcod.BKGND_DEFAULT, fmt=0)

        libtcod.console_set_default_foreground(menu_con, MENU_TITLE_COLOR)
        libtcod.console_print_ex(menu_con, MENU_CON_XM, 1,
            libtcod.BKGND_NONE, libtcod.CENTER, 'Player Tank View')
        libtcod.console_set_default_foreground(menu_con, libtcod.white)

        # refresh the tank display
        UpdateTankCon()
        libtcod.console_blit(tank_con, 0, 0, TANK_CON_WIDTH, TANK_CON_HEIGHT, menu_con, CON_X, CON_Y)
        libtcod.console_blit(menu_con, 0, 0, MENU_CON_WIDTH, MENU_CON_HEIGHT, 0, MENU_CON_X, MENU_CON_Y)
        libtcod.console_flush()

        refresh_display = False
        while not refresh_display:

            libtcod.console_flush()

            # exit right away
            if libtcod.console_is_window_closed(): sys.exit()

            # get input from user
            libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS|libtcod.EVENT_MOUSE, key, mouse)

            # exit view
            if key.vk == libtcod.KEY_ENTER:

                # if we're resupplying and haven't loaded any ammo,
                # confirm that player wants to continue
                if campaign.resupply and campaign.day_in_progress:
                    total = 0
                    for ammo_type in AMMO_TYPES:
                        if ammo_type in tank.general_ammo:
                            total += tank.general_ammo[ammo_type]
                    if total == 0:
                        text = 'You have not loaded any ammo, are you sure you want to continue?'
                        if not PopUp(text, confirm=True, skip_update=True):
                            refresh_display = True
                            continue
                exit_view = True
                break

            # get pressed key
            key_char = chr(key.c)

            # select next crew member
            if key_char in ['s', 'S'] or key.vk == libtcod.KEY_DOWN:
                campaign.selected_crew = campaign.selected_crew.next
                refresh_display = True

            # select previous crew member
            elif key_char in ['w', 'W'] or key.vk == libtcod.KEY_UP:
                campaign.selected_crew = campaign.selected_crew.prev
                refresh_display = True

            # toggle hatch status for selected crew member
            elif key_char in ['h', 'H']:
                tank.ToggleHatch(campaign.selected_crew)
                refresh_display = True

            # cycle through ammo reload selections
            elif key_char in ['r', 'R']:
                tank.CycleReload()
                refresh_display = True

            # toggle use of ready rack
            elif key_char in ['t', 'T']:
                tank.use_rr = not tank.use_rr
                refresh_display = True

            # change gun load
            elif key_char in ['g', 'G']:
                tank.ChangeGunLoadMenu()
                refresh_display = True

            # open main gun ammo menu, can be triggered by function var
            elif load_ammo_menu or key_char in ['m', 'M']:
                load_ammo_menu = False
                MainGunAmmoMenu(no_dark=True)
                refresh_display = True


# display the main gun ammunition menu
# allow player to move shells around, load new ammo if possible
def MainGunAmmoMenu(no_dark=False):

    # direction flag; if true we are moving shells into tank / ready rack
    inward = True

    # keys to use for moving shells
    KEY_CODES = [('U', 'J'), ('I', 'K'), ('O', 'L'), ('P', ';')]

    # darken screen
    if not no_dark:
        libtcod.console_clear(con)
        libtcod.console_blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0,
            0.0, 0.7)

    exit_menu = False
    while not exit_menu:

        # refresh menu console
        libtcod.console_clear(menu_con)
        libtcod.console_print_frame(menu_con, 0, 0, MENU_CON_WIDTH, MENU_CON_HEIGHT,
            clear=False, flag=libtcod.BKGND_DEFAULT, fmt=0)
        libtcod.console_set_alignment(menu_con, libtcod.CENTER)
        libtcod.console_set_default_foreground(menu_con, MENU_TITLE_COLOR)
        libtcod.console_print(menu_con, MENU_CON_XM, 1, 'Main Gun Ammunition Menu')

        x = MENU_CON_XM-28

        # display row titles
        libtcod.console_set_default_foreground(menu_con, libtcod.light_grey)
        libtcod.console_set_default_background(menu_con, libtcod.darkest_grey)
        libtcod.console_set_alignment(menu_con, libtcod.LEFT)
        libtcod.console_print(menu_con, x+2, 5, 'Ammo')

        if campaign.resupply:
            libtcod.console_print(menu_con, x+2, 7, 'Supply')
            libtcod.console_rect(menu_con, x+2, 7, 48, 2, False, flag=libtcod.BKGND_SET)

        libtcod.console_print(menu_con, x+2, 12, 'General')
        libtcod.console_print(menu_con, x+3, 13, 'Stores')
        libtcod.console_rect(menu_con, x+2, 12, 48, 2, False, flag=libtcod.BKGND_SET)

        libtcod.console_print(menu_con, x+2, 17, 'Ready')
        libtcod.console_print(menu_con, x+3, 18, 'Rack')
        libtcod.console_rect(menu_con, x+2, 17, 48, 2, False, flag=libtcod.BKGND_SET)

        libtcod.console_set_default_background(menu_con, libtcod.black)

        # display info for each ammo type and totals
        libtcod.console_set_alignment(menu_con, libtcod.RIGHT)
        x += 16
        key_code = 0
        total_g = 0
        total_rr = 0
        for ammo_type in AMMO_TYPES:
            if ammo_type in tank.general_ammo:

                # ammo type header
                libtcod.console_set_default_foreground(menu_con, libtcod.light_grey)
                libtcod.console_print(menu_con, x, 5, ammo_type)
                libtcod.console_set_default_foreground(menu_con, libtcod.white)

                # display amount available
                if campaign.resupply:
                    if ammo_type in ['HE', 'AP', 'WP']:
                        text = chr(236)
                    else:
                        text = '-'
                        if ammo_type == 'HCBI' and campaign.hcbi > 0:
                            text = str(campaign.hcbi)
                        elif ammo_type == 'HVAP' and campaign.hvap > 0:
                            text = str(campaign.hvap)
                        elif ammo_type == 'APDS' and campaign.apds > 0:
                            text = str(campaign.apds)
                    libtcod.console_print(menu_con, x, 7, text)

                # display amount in general stores and ready rack
                text = str(tank.general_ammo[ammo_type])
                libtcod.console_print(menu_con, x, 12, text)
                total_g += tank.general_ammo[ammo_type]

                text = str(tank.rr_ammo[ammo_type])
                libtcod.console_print(menu_con, x, 17, text)
                total_rr += tank.rr_ammo[ammo_type]

                # display key commands
                libtcod.console_set_default_foreground(menu_con, libtcod.light_grey)
                (k1, k2) = KEY_CODES[key_code]
                # only display supply commands if resupply is available
                if campaign.resupply:
                    if not inward:
                        text = chr(24) + k1 + chr(24)
                    else:
                        text = chr(25) + k1 + chr(25)
                    libtcod.console_print(menu_con, x, 10, text)
                    libtcod.console_set_char_foreground(menu_con, x-1, 10, KEY_HIGHLIGHT_COLOR)

                # directional arrows
                if inward:
                    text = chr(25) + k2 + chr(25)
                else:
                    text = chr(24) + k2 + chr(24)
                libtcod.console_print(menu_con, x, 15, text)
                libtcod.console_set_char_foreground(menu_con, x-1, 15, KEY_HIGHLIGHT_COLOR)

                x += 8
                key_code += 1

        # display total and max for general stores and ready rack
        libtcod.console_set_default_foreground(menu_con, libtcod.light_grey)
        libtcod.console_print(menu_con, 90, 5, 'Max')
        libtcod.console_set_default_foreground(menu_con, libtcod.white)

        text = str(total_g) + '/' + str(tank.stats['main_gun_rounds'])
        libtcod.console_print(menu_con, 90, 12, text)

        text = str(total_rr) + '/' + str(tank.stats['rr_size'])
        libtcod.console_print(menu_con, 90, 17, text)

        # display frame
        libtcod.console_set_default_foreground(menu_con, libtcod.light_grey)
        libtcod.console_print_frame(menu_con, MENU_CON_XM-28, 3, 52, 18,
            clear=False, flag=libtcod.BKGND_DEFAULT, fmt=0)

        # display ammo type info
        libtcod.console_set_alignment(menu_con, libtcod.LEFT)
        libtcod.console_print(menu_con, MENU_CON_XM-46, 23, 'HE: High Explosive, ' +
            'used against infantry targets and in advancing fire')
        libtcod.console_print(menu_con, MENU_CON_XM-46, 24, 'AP: Armour-Piercing, ' +
            'used against armoured targets')
        libtcod.console_print(menu_con, MENU_CON_XM-46, 25, 'WP: White Phosporous, ' +
            'generates smoke and can pin infantry')
        libtcod.console_print(menu_con, MENU_CON_XM-46, 26, 'HCBI: Hexachlorothane-Base Initiating, ' +
            'generates a great deal of smoke but no other effect')
        libtcod.console_print(menu_con, MENU_CON_XM-46, 27, 'HVAP: High Velocity Armour-Piercing, ' +
            'used against armoured targets, more effective than AP')
        libtcod.console_print(menu_con, MENU_CON_XM-46, 28, 'APDS: Armour-Piercing Discarding Sabot, ' +
            'used against armoured targets, more effective than AP')

        'APDS'

        # display instructions
        libtcod.console_set_alignment(menu_con, libtcod.CENTER)
        libtcod.console_set_default_foreground(menu_con, libtcod.white)
        libtcod.console_print(menu_con, MENU_CON_XM, MENU_CON_HEIGHT-6, 'Use listed keys to move ammunition')
        libtcod.console_print(menu_con, MENU_CON_XM, MENU_CON_HEIGHT-5,
            '[%cAlt%c] Switch Direction of Move'%HIGHLIGHT)
        libtcod.console_print(menu_con, MENU_CON_XM, MENU_CON_HEIGHT-4,
            '[%c+Shift%c] Move 10 shells'%HIGHLIGHT)
        libtcod.console_print(menu_con, MENU_CON_XM, MENU_CON_HEIGHT-2,
            '[%cEnter%c] Close Menu and Continue'%HIGHLIGHT)

        # blit menu console to screen
        libtcod.console_blit(menu_con, 0, 0, MENU_CON_WIDTH, MENU_CON_HEIGHT, 0,
            MENU_CON_X, MENU_CON_Y)
        libtcod.console_flush()

        refresh_menu = False
        while not refresh_menu and not exit_menu:
            libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS|libtcod.EVENT_MOUSE, key, mouse)

            # update screen
            libtcod.console_flush()

            # exit right away
            if libtcod.console_is_window_closed():
                sys.exit()

            if key.vk == libtcod.KEY_ENTER:
                exit_menu = True

            # refresh menu if alt status has changed
            elif key.vk == libtcod.KEY_ALT:
                inward = not inward
                refresh_menu = True
                continue

            # get pressed key
            key_char = chr(key.c)

            # ready rack commands (ignores SHIFT)
            if key_char in ['j', 'k', 'l', ';', 'J', 'K', 'L', ':']:

                # get the index number of the ammo type to use
                if key_char in ['j', 'J']:
                    n = 0
                elif key_char in ['k', 'K']:
                    n = 1
                elif key_char in ['l', 'L']:
                    n = 2
                else:
                    n = 3

                i = 0
                new_type = None
                for ammo_type in AMMO_TYPES:
                    if ammo_type in tank.rr_ammo:
                        if i == n:
                            new_type = ammo_type
                        i += 1

                # only three ammo types, fourth one selected
                if new_type is None:
                    continue

                # move a shell from ready rack to to general stores if
                #  there is room for it
                if not inward:
                    if tank.rr_ammo[new_type] > 0 and total_g < tank.stats['main_gun_rounds'] + EXTRA_AMMO:
                        tank.rr_ammo[new_type] -= 1
                        tank.general_ammo[new_type] += 1
                        PlaySound('shell_move')

                # move a shell from general stores to rr
                else:
                    if tank.general_ammo[new_type] > 0 and total_rr < tank.stats['rr_size']:
                        tank.general_ammo[new_type] -= 1
                        tank.rr_ammo[new_type] += 1
                        PlaySound('shell_move')

                refresh_menu = True

            # move shells between supply and general stores
            elif campaign.resupply and key_char in ['u', 'i', 'o', 'p', 'U', 'I', 'O', 'P']:

                if key_char in ['u', 'U']:
                    n = 0
                elif key_char in ['i', 'I']:
                    n = 1
                elif key_char in ['o', 'O']:
                    n = 2
                else:
                    n = 3

                if key_char in ['u', 'i', 'o', 'p']:
                    amount = 1
                else:
                    amount = 10

                # get the ammo type
                i = 0
                new_type = None
                for ammo_type in AMMO_TYPES:
                    if ammo_type in tank.general_ammo:
                        if i == n:
                            new_type = ammo_type
                        i += 1

                # only three ammo types, fourth one selected
                if new_type is None:
                    continue

                # remove a shell from general stores
                # if limited amounts, replace into stores (but lost after this morning)
                if not inward:
                    if tank.general_ammo[new_type] >= amount:
                        tank.general_ammo[new_type] -= amount
                        if new_type == 'HCBI':
                            campaign.hcbi += amount
                        elif new_type == 'HVAP':
                            campaign.hvap += amount
                        elif new_type == 'APDS':
                            campaign.apds += amount
                        PlaySound('shell_move')

                # add to general stores if there's room
                # if limited amounts, check that there are enough left
                else:
                    if total_g + amount > tank.stats['main_gun_rounds'] + EXTRA_AMMO:
                        amount = tank.stats['main_gun_rounds'] + EXTRA_AMMO - total_g

                    if new_type == 'HCBI':
                        if campaign.hcbi < amount: continue
                        campaign.hcbi -= amount
                    elif new_type == 'HVAP':
                        if campaign.hvap < amount: continue
                        campaign.hvap -= amount
                    elif new_type == 'APDS':
                        if campaign.apds < amount: continue
                        campaign.apds -= amount

                    tank.general_ammo[new_type] += amount
                    PlaySound('shell_move')

                refresh_menu = True

            # update screen
            libtcod.console_flush()



# display the campaign menu
# if tank is not alive or day has ended, show that
def CampaignMenu():
    # darken screen
    libtcod.console_clear(con)
    libtcod.console_blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0,
        0.0, 0.7)

    # generate and display menu
    libtcod.console_clear(menu_con)
    libtcod.console_print_frame(menu_con, 0, 0, MENU_CON_WIDTH, MENU_CON_HEIGHT,
        clear=False, flag=libtcod.BKGND_DEFAULT, fmt=0)

    libtcod.console_set_alignment(menu_con, libtcod.CENTER)
    libtcod.console_set_default_foreground(menu_con, MENU_TITLE_COLOR)
    libtcod.console_print(menu_con, MENU_CON_XM, 1, 'Campaign Menu')
    libtcod.console_set_default_foreground(menu_con, libtcod.white)

    # day is over
    if campaign.sunset:
        libtcod.console_print(menu_con, MENU_CON_XM, 4, '[%cESC%c] Return to Campaign Calendar'%HIGHLIGHT)
    else:
        libtcod.console_print(menu_con, MENU_CON_XM, 4, '[%cESC%c] Return to Game'%HIGHLIGHT)
        libtcod.console_print(menu_con, MENU_CON_XM, 5, '[%cQ%c] Save Game, Return to Main Menu'%HIGHLIGHT)

    text = 'VP Today: ' + str(campaign.day_vp)
    libtcod.console_print(menu_con, MENU_CON_XM, 8, text)
    text = 'Campaign VP: ' + str(campaign.day_vp + campaign.vp)
    libtcod.console_print(menu_con, MENU_CON_XM, 9, text)

    if not tank.alive:
        libtcod.console_print(menu_con, MENU_CON_XM, 10, 'Your tank has been destroyed')
    elif tank.swiss_cheese:
        libtcod.console_print(menu_con, MENU_CON_XM, 10, 'Your tank has been damaged beyond repair')
    elif tank.immobilized:
        libtcod.console_print(menu_con, MENU_CON_XM, 10, 'Your tank has been immobilized')
    elif campaign.sunset:
        libtcod.console_print(menu_con, MENU_CON_XM, 10, 'The combat day has ended')

    libtcod.console_set_alignment(menu_con, libtcod.LEFT)

    libtcod.console_blit(menu_con, 0, 0, MENU_CON_WIDTH, MENU_CON_HEIGHT, 0, MENU_CON_X, MENU_CON_Y)
    libtcod.console_flush()

    exit_menu = False
    while not exit_menu:
        # get input from user
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS|libtcod.EVENT_MOUSE, key, mouse)

        if key.vk == libtcod.KEY_ESCAPE:
            exit_menu = True

        # get pressed key
        key_char = chr(key.c)

        if not campaign.sunset and tank.alive:
            if key_char in ['q', 'Q']: return True

        # exit right away
        if libtcod.console_is_window_closed():
            sys.exit()

        libtcod.console_flush()

    # re-draw screen if still playing
    if not campaign.sunset and tank.alive:
        RenderCampaign()

    return False


# render campaign consoles to screen
def RenderCampaign(no_flush=False):

    # blit consoles to display console
    libtcod.console_clear(con)

    # display menu bar
    DisplayMenuBar()

    libtcod.console_blit(date_con, 0, 0, DATE_CON_WIDTH, DATE_CON_HEIGHT, con, 1, 2)
    libtcod.console_blit(c_map_con, 0, campaign.c_map_y, C_MAP_CON_WINDOW_W,
        C_MAP_CON_WINDOW_H, con, C_MAP_CON_X, 4)
    libtcod.console_blit(c_overlay_con, 0, campaign.c_map_y, C_MAP_CON_WINDOW_W,
        C_MAP_CON_WINDOW_H, con, C_MAP_CON_X, 4, 1.0, 0.0)

    libtcod.console_blit(c_action_con, 0, 0, C_ACTION_CON_W, C_ACTION_CON_H, con, 1, 4)
    libtcod.console_blit(c_info_con, 0, 0, C_INFO_CON_W, C_INFO_CON_H, con, 1, C_ACTION_CON_H+5)

    # lines between console displays
    libtcod.console_hline(con, 1, 1, SCREEN_WIDTH-2, flag=libtcod.BKGND_DEFAULT)
    libtcod.console_hline(con, 1, 3, SCREEN_WIDTH-2, flag=libtcod.BKGND_DEFAULT)
    libtcod.console_hline(con, 1, C_ACTION_CON_H+4, C_ACTION_CON_W, flag=libtcod.BKGND_DEFAULT)
    libtcod.console_vline(con, C_ACTION_CON_W+1, 4, SCREEN_HEIGHT-4, flag=libtcod.BKGND_DEFAULT)

    # blit display console to screen and update screen
    libtcod.console_blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)
    if not no_flush:
        libtcod.console_flush()



##########################################################################################
#                                  Campaign Day Map                                      #
##########################################################################################

# GetPath - based on http://stackoverflow.com/questions/4159331/python-speed-up-an-a-star-pathfinding-algorithm
# and http://www.policyalmanac.org/games/aStarTutorial.htm
# returns a list of nodes to traverse shortest path from node1 to node2
# if enemy_blocks, enemy-held zones are treated as blocked
def GetPath(node1, node2, enemy_blocks=False):

    # clear pathfinding info
    for node in campaign.day_map.nodes:
        node.ClearPathInfo()

    open_list = set()    # contains the nodes that may be traversed by the path
    closed_list = set()    # contains the nodes that will be traversed by the path

    # calculate the direct distance between two locations
    def GetH(x1, y1, x2, y2):
        return GetDistance(x1, y1, x2, y2)

    # retrace a set of nodes and return the best path
    def RetracePath(end_node):
        path = []
        node = end_node
        done = False
        while not done:
            path.append(node)
            if node.parent is None: break    # we've reached the end
            node = node.parent

        path.reverse()
        path.pop(0)        # remove the first node

        # return the path
        return path

    start = node1
    start.h = GetH(node1.x, node1.y, node2.x, node2.y)
    start.f = start.g + start.h

    end = node2

    # add the start node to the open list
    open_list.add(start)

    last_good_node = None

    while open_list:    # while there are still tiles in the 'potentials' list

        # grab the node with the best H value from the list of open tiles
        current = sorted(open_list, key=lambda inst:inst.f)[0]

        # we've reached our destination
        if current == end:
            return RetracePath(current)

        # move this tile from the open to the closed list
        open_list.remove(current)
        closed_list.add(current)

        # add the nodes connected to this one to the open list
        for node in current.links:
            # ignore nodes on closed list
            if node in closed_list: continue

            # ignore blocked nodes
            if node in campaign.day_map.blocked_nodes: continue

            # can ignore enemy-held areas
            if enemy_blocks and not node.friendly_control: continue

            # calculate g value for travel to linked node based on node
            # type
            if node.node_type == 'D':
                cost = 100
            else:
                cost = 1
            g = current.g + cost

            # if not in open list, add it
            if node not in open_list:
                node.g = g
                node.h = GetH(node.x, node.y, node2.x, node2.y)
                node.f = node.g + node.h
                node.parent = current
                open_list.add(node)
            # if already in open list, check to see if can make a better path
            else:
                if g < node.g:
                    node.parent = current
                    node.g = g
                    node.f = node.g + node.h

    # no path possible
    return []


##########################################################################################


# randomly generate a map for a day of the campaign
def GenerateCampaignMap():

    MIN_DIST = 7        # minimum distance between node centres
    NUM_NODES = 55        # number of nodes to try to create

    # check to make sure that this position is not within the minimum distance to
    # another already-existing map node
    def TooClose(x, y):
        for node in campaign.day_map.nodes:
            if GetDistance(x, y, node.x, node.y) <= MIN_DIST:
                return True
        return False

    # create a new instance of the day map class
    campaign.day_map = CampaignDayMap()

    # clear the currently selected node if any
    campaign.selected_node = None

    # generate the map nodes
    for tries in range(0, 300):

        # find a random location on the map board
        x = libtcod.random_get_int(0, 3, C_MAP_CON_WIDTH-4)
        y = libtcod.random_get_int(0, 3, C_MAP_CON_HEIGHT-4)

        # check that it's not within the minimum distance away from another
        # map node
        if TooClose(x, y):
            continue

        # create the node
        campaign.day_map.nodes.append(MapNode(x, y))

        # break if we have enough nodes
        if len(campaign.day_map.nodes) >= NUM_NODES:
            break

    # create list of character locations and set their node membership
    for y in range(0, C_MAP_CON_HEIGHT):
        for x in range (0, C_MAP_CON_WIDTH):

            # find nearest node to this coordinate
            nearest = None
            nearest_dist = None
            for node in campaign.day_map.nodes:
                dist = GetDistance(x, y, node.x, node.y)
                if nearest is None:
                    nearest = node
                    nearest_dist = dist
                    continue
                if dist < nearest_dist:
                    nearest = node
                    nearest_dist = dist

            # create the new character location
            campaign.day_map.char_locations[(x,y)] = nearest

    # check an adjacent coordinate to see if it belongs to a different map node
    def CheckCoord(x, xmod, y, ymod, node):
        node2 = campaign.day_map.char_locations[(x+xmod,y+ymod)]
        if node2 != node:

            # add to set of edge coordinates
            node.edges.add((x,y))

            # create link if not already present
            if node2 not in node.links:
                node.links.append(node2)
                node2.links.append(node)

    # determine edge coordinates of node, and generate links to adjacent nodes
    for y in range(0, C_MAP_CON_HEIGHT):
        for x in range (0, C_MAP_CON_WIDTH):
            parent_node = campaign.day_map.char_locations[(x,y)]

            # check the four adjacent coordinates; if any are off the map or
            # belong to a different area, this is an edge coordinate
            if x-1<0 or x+1>=C_MAP_CON_WIDTH or y-1<0 or y+1>=C_MAP_CON_HEIGHT:
                parent_node.edges.add((x,y))
                continue

            CheckCoord(x, -1, y, 0, parent_node)
            CheckCoord(x, 1, y, 0, parent_node)
            CheckCoord(x, 0, y, -1, parent_node)
            CheckCoord(x, 0, y, 1, parent_node)

    # set node terrain chances based on day terrain type if any
    today = GetToday()
    if today.has_key('terrain'):
        if today['terrain'] == 'bocage':
            terrain_chances = [(4,'C'), (5,'A'), (8,'F'), (10,'B'), (11,'D'), (12,'E')]
        elif today['terrain'] == 'forest':
            terrain_chances = [(3,'C'), (4,'A'), (8,'D'), (10,'B'), (11,'E')]
    else:
        terrain_chances = [(4,'C'), (5,'A'), (8,'B'), (9,'D'), (12,'E')]

    # sort links for each node and set terrain types
    for node in campaign.day_map.nodes:
        node.links.sort(key=attrgetter('y', 'x'))

        d1, d2, roll = Roll2D6()
        for (target_score, node_type) in terrain_chances:
            if roll <= target_score:
                node.node_type = node_type
                break

        # set special settings for particular nodes types
        if node.node_type == 'C':    # village

            # for village nodes, we need to determine the distance of the
            # closest edge coordinate from the node center, and use this for
            # the radius of the village buildings
            closest = 100
            for (x,y) in node.edges:
                dist = GetDistance(x, y, node.x, node.y)
                if dist < closest:
                    closest = dist
            node.village_radius = closest - 1

            # seems to sometimes be possible to have 0 radius villages, so check
            if node.village_radius == 0:
                node.village_radius = 1

        elif node.node_type == 'E':    # marshland
            campaign.day_map.blocked_nodes.add(node)    # mark as impassible

    ##### Prune any adjacent villages #####
    for node in random.sample(campaign.day_map.nodes, len(campaign.day_map.nodes)):
        if node.node_type == 'C':
            for linked_node in node.links:
                if linked_node.node_type == 'C':
                    node.node_type = 'A'

    ##### Sever links with impassible nodes #####
    for node1 in campaign.day_map.nodes:
        if node1 in campaign.day_map.blocked_nodes:
            # remove all links from other nodes to this one
            for node2 in node1.links:
                node2.links.remove(node1)
            # remove all links from this node to others
            node1.links = []

    # mark map edge nodes
    for x in range (0, C_MAP_CON_WIDTH):
        campaign.day_map.char_locations[(x,0)].top_edge = True
        campaign.day_map.char_locations[(x,C_MAP_CON_HEIGHT-1)].bottom_edge = True
    for y in range (0, C_MAP_CON_HEIGHT):
        campaign.day_map.char_locations[(0,y)].left_edge = True
        campaign.day_map.char_locations[(C_MAP_CON_WIDTH-1,y)].right_edge = True

    start_node = None
    exit_node = None

    # determine start node
    for node in random.sample(campaign.day_map.nodes, len(campaign.day_map.nodes)):

        if node in campaign.day_map.blocked_nodes: continue

        # in counterattack missions, we start on the top edge
        if campaign.scen_type == 'Counterattack':
            if not node.top_edge: continue
        else:
            if not node.bottom_edge: continue

        node.start = True
        # set player node to this node
        campaign.day_map.player_node = node
        node.friendly_control = True
        start_node = node
        break

    # counterattack missions also have an 'exit' node
    for node in random.sample(campaign.day_map.nodes, len(campaign.day_map.nodes)):
        if campaign.scen_type == 'Counterattack':
            if not node.bottom_edge: continue
        else:
            if not node.top_edge: continue
        if node not in campaign.day_map.blocked_nodes:
            node.exit = True
            exit_node = node
            break

    # Make sure a path is possible from start to exit node; if not, return
    #  false since map generation has failed
    if start_node is None or exit_node is None:
        return False
    if GetPath(start_node, exit_node) == []:
        return False

    # for Counterattack missions, make sure we have a start node
    else:
        if start_node is None: return False

    # determine area resistance levels
    for node in campaign.day_map.nodes:

        # skip impassible nodes
        if node in campaign.day_map.blocked_nodes: continue

        # do roll and apply modifiers
        roll = Roll1D10()

        if node.node_type == 'A':
            roll += 1
        elif node.node_type == 'B':
            roll -= 1
        elif node.node_type == 'C':
            roll += 2
        elif node.node_type == 'D':
            roll -= 2

        if len(node.stone_road_links) > 0:
            roll += 2
        if len(node.dirt_road_links) > 0:
            roll += 1

        # check modified roll against odds for different day resistance levels
        if campaign.scen_res == 'Light':
            if roll <= 7:
                area_res = 'Light'
            else:
                area_res = 'Medium'
        elif campaign.scen_res == 'Medium':
            if roll <= 5:
                area_res = 'Light'
            elif roll <= 9:
                area_res = 'Medium'
            else:
                area_res = 'Heavy'
        else:
            if roll <= 4:
                area_res = 'Light'
            elif roll <= 8:
                area_res = 'Medium'
            else:
                area_res = 'Heavy'

        node.resistance = area_res

        # if counterattack scenario, set all map nodes to friendly control
        if campaign.scen_type == 'Counterattack':
            node.friendly_control = True

    # use the default seed to generate a random seed to use to map painting
    # seed is an unsigned 32 bit int
    campaign.day_map.seed = libtcod.random_get_int(0, 0, 4294967295)

    # paint the map console for the first time
    PaintCampaignMap()

    # map complete!
    return True



##########################################################################################

# check for awards, or rank promotions for the tank commander
def CheckAwardsPromotions(new_month=False):

    # check for purple heart awards for USA players
    # (no award for light wound)
    if campaign.player_nation == 'USA':
        for crewman in tank.crew:
            if crewman.serious_wound or crewman.v_serious_wound or not crewman.alive:
                crewman.AwardDecoration('Purple Heart')

    crewman = GetCrewByPosition('Commander')

    # only check for other awards for commander if start of new month
    if new_month:
        # roll 2D6 and add to highest one-day VP score
        d1, d2, roll = Roll2D6()
        award_score = roll + campaign.record_day_vp

        # go through awards and find highest that can be awarded
        for (award_name, text, score_req) in reversed(campaign.decorations):
            if award_score >= score_req:
                crewman.AwardDecoration(award_name)
                break
        # reset highest one-day VP score for new month
        campaign.record_day_vp = 0

    # check for commander promotion; no promotion if dead
    if not crewman.alive:
        return

    # check through ranks in reverse order, finding the highest new rank that can be
    #  awarded
    for n in reversed(range(7)):
        if n == crewman.rank_level: break
        a, b, vp_req = campaign.ranks[n]
        if campaign.vp >= vp_req:
            crewman.rank_level = n
            WriteJournal(crewman.name + ' promoted to rank of ' + crewman.GetRank())
            text = ('Congratulations, commander. Due to your continued service ' +
                'and leadership, you have been promoted to the rank of ' +
                crewman.GetRank())
            PopUp(text)
            break


# check the commander's health
# if we're not in casual mode and he's killed or seriously injured, game is over
def CheckCommander():
    if campaign.casual_commander: return
    crewman = GetCrewByPosition('Commander')
    if crewman.v_serious_wound or not crewman.alive:
        ##### Campaign is over #####
        campaign.over = True
        if not crewman.alive:
            PopUp('You are dead. Your campaign is over')
        else:
            PopUp('You have been seriously injured and are sent home. Your campaign is over.')
        # add high score
        AddHighScore()
        os.remove('savegame')

        # record final journal entries
        text = 'Campaign Over: '
        if crewman.v_serious_wound:
            text += 'Commander was very seriously wounded and was sent home.'
        else:
            text += 'Commander was killed in action.'
        WriteJournal(text)

        # record campaign stats to journal
        WriteJournal('')
        WriteJournal('******')
        WriteJournal('Final Campaign Stats')
        text = ('Days of Combat: ' + str(campaign.stats['Days of Combat']) +
            '/' + str(len(campaign.days)))
        WriteJournal(text)
        text = 'Total Victory Points: ' + str(campaign.vp + campaign.day_vp)
        WriteJournal(text)

        # record remainder of campaign stats
        for stat_name in C_STATS:
            text = stat_name + ': '
            if not campaign.stats.has_key(stat_name):
                text += '0'
            else:
                text += str(campaign.stats[stat_name])
            WriteJournal(text)

        WriteJournal('')
        WriteJournal('******')

        # write journal to file
        RecordJournal()

        # display final campaign stats to player
        ShowCampaignStats()
        return True
    return False


# generate a random model of sherman based on current date and rarity
def RandomPlayerTankModel():

    # build a list of available tank models
    model_list = []
    total_rf = 0
    for vehicle_type in campaign.player_veh_list:
        rf = campaign.GetRF(vehicle_type)
        if rf > 0:
            model_list.append((vehicle_type, rf))
            total_rf += rf
    random.shuffle(model_list)

    result = libtcod.random_get_int(0, 1, total_rf)
    new_type = ''
    for (vehicle_type, rf) in model_list:
        if result <= rf:
            new_type = vehicle_type
            break
        result -= rf

    if new_type == '':
        print 'ERROR: Could not randomly choose a new tank model'
        return 'M4 Turret A'

    return new_type


# prompt the player for a tank name
def GetTankName():
    libtcod.console_set_default_background(con, libtcod.black)
    libtcod.console_clear(con)
    tank_name = GetInput(con, 'Choose a name for your Sherman tank', 25, 17, random_list=TANK_NAMES)
    # choose a random name if none chosen
    if tank_name == '':
        tank_name = random.choice(TANK_NAMES)
    tank.SetName(tank_name)


# prompt the player for a commander name
def GetCommanderName(crewman):
    libtcod.console_set_default_background(con, libtcod.black)
    libtcod.console_clear(con)
    commander_name = GetInput(con, 'Enter your name', 25, NAME_MAX_LEN, get_name=True)
    # select a random name if none chosen
    if commander_name == '':
        crewman.GenerateName()
    else:
        crewman.name = commander_name


# handle either assigning a new crewman or removing a crewmen when switching between a tank
#  without an assistant driver position and one with
def CheckPlayerTankPositions():

    # need a new asst. driver
    if not tank.stats.has_key('no_asst_driver') and GetCrewByPosition('Asst. Driver') is None:
        highest_level = GetHighestCrewLevel()
        new_crew = SpawnCrewMember(None, 'Asst. Driver', 0)
        new_crew.SetLevel(libtcod.random_get_int(0, 1, highest_level))
        SetCrewPointers()
        text = new_crew.name + ' joins the tank crew as the Assistant Driver.'
        PopUp(text)
        WriteJournal(text)
        ShowSkills(new_crew)

    # have an extra asst. driver
    elif tank.stats.has_key('no_asst_driver') and GetCrewByPosition('Asst. Driver') is not None:
        crewman = GetCrewByPosition('Asst. Driver')
        tank.crew.remove(crewman)
        SetCrewPointers()
        text = ('Your new tank has no assistant driver position. ' + crewman.name +
            ' is reassigned elsewhere.')
        PopUp(text)
        WriteJournal(text)


# check the player tank after a campaign day; if it's been disabled then it's repaired,
# if it's destroyed or damaged beyond repair then the player gets a new tank model
def CheckPlayerTank():

    # check for awards and/or rank promotions
    CheckAwardsPromotions()

    if not tank.alive or tank.swiss_cheese:

        # check for crew replacements
        ReplaceCrew()

        # select tank, or assign a new tank
        if campaign.unlimited_tank_selection:
            tank_type = ShowTankInfo(select_tank=True)
        else:
            tank_type = RandomPlayerTankModel()
            text = ('HQ assigns your crew to a ' + tank_type + ' tank.')
            PopUp(text)

        tank.alive = True
        tank.unit_type = tank_type
        tank.Setup()
        SetVehicleStats(tank)

        # get the name for the new tank
        GetTankName()

        WriteJournal('New player tank: ' + tank.unit_type + ' "' + tank.name + '"')

        # check for asst driver changeup
        CheckPlayerTankPositions()

        # reset crew orders, hatch status, and spot ability
        for crewman in tank.crew:
            crewman.order = crewman.default_order
            crewman.CheckHatch()
            crewman.SetSpotAbility()

    else:

        if tank.immobilized:
            tank.immobilized = False
            PopUp('Your tank is repaired for the next day of combat.')

        # clear damage list
        tank.damage_list = []

    # any crewman with light or serious wounds are healed
    for crewman in tank.crew:
        crewman.light_wound = False
        crewman.serious_wound = False


# return a pointer to the current date in the list of campaign days
def GetToday():
    for calendar_day in campaign.days:
        if (int(calendar_day['year']) == campaign.current_date[0] and
            int(calendar_day['month']) == campaign.current_date[1] and
            int(calendar_day['date']) == campaign.current_date[2]):
                return calendar_day
    return None


# set the campaign date record to a given date in the calendar
def SetToday(new_date):
    campaign.current_date[0] = int(new_date['year'])
    campaign.current_date[1] = int(new_date['month'])
    campaign.current_date[2] = int(new_date['date'])


# advance the combat calendar to the next day in the calendar
# show fade-in and fade-out animations and comment for day (location or refit)
# if action day, set up the campaign variables
def AdvanceDay():

    DATE_Y = 24

    # get a pointer to the current date in the list of calendar days
    today = GetToday()

    # clear screen
    libtcod.console_clear(0)
    libtcod.console_flush()
    libtcod.console_set_alignment(0, libtcod.CENTER)

    # if this first day of a new campaign
    if campaign.current_date == [0,0,0]:
        # set to selected start day in the combat calendar
        SetToday(campaign.days[campaign.start_date])

    # advancing to a new day
    else:


        n = campaign.days.index(GetToday())

        # still have at least one more day in the campaign
        if n < len(campaign.days) - 1:
            # advance date one day
            new_date = campaign.days[n+1]

            # start of new calendar month
            if campaign.current_date[1] != int(new_date['month']):
                # check for awards and/or promotions for commander
                CheckAwardsPromotions(new_month=True)

        ##### Reached end of campaign #####
        else:
            PopUp('You have survived and reached the end of the ' +
                'campaign! Congratulations!')
            campaign.over = True
            AddHighScore()
            os.remove('savegame')

            # record final journal entry
            WriteJournal('Campaign Over: End of campaign calendar')
            RecordJournal()

            ShowCampaignStats()
            campaign.exiting = True
            return

        # advance to next date in calendar
        SetToday(campaign.days[n+1])

    # clear screen (in case we did end-of-month stuff)
    libtcod.console_clear(0)
    libtcod.console_flush()

    date_text = campaign.GetDate()

    # do date fade-in
    for c in range(0, 255, 5):
        libtcod.console_set_default_foreground(0, libtcod.Color(c,c,c))
        libtcod.console_print(0, SCREEN_XM, DATE_Y, date_text)
        libtcod.console_flush()
        Wait(2)

    # get a pointer to the new current day
    today = GetToday()

    # record new day in journal
    WriteJournal('')
    WriteJournal('******')
    text = campaign.GetDate()
    if today['comment'] == 'Refitting':
        text += ': Start of refitting period'
    else:
        text += ': ' + today['comment']
    WriteJournal(text)

    # fade-in day comment
    text = today['comment']
    for c in range(0, 255, 5):
        libtcod.console_set_default_foreground(0, libtcod.Color(c,c,c))
        libtcod.console_print(0, SCREEN_XM, DATE_Y+3, text)
        libtcod.console_flush()
        Wait(2)

    # current date is start of a refitting period
    if today['comment'] == 'Refitting':
        campaign.gyro_skill_avail = True    # set gyrostabilier skill flag
        campaign.action_day = False        # set action flag
        # generate new tank model to offer if tank selection is 'strict'
        if not campaign.unlimited_tank_selection:
            campaign.tank_on_offer = RandomPlayerTankModel()

    else:
        # reset offered tank
        campaign.tank_on_offer = ''

        # set action flag
        campaign.action_day = True

        # get string descriptions of day's action
        res = today['resistance_level']
        if res == 'L':
            campaign.scen_res = 'Light'
        elif res == 'M':
            campaign.scen_res = 'Medium'
        else:
            campaign.scen_res = 'Heavy'

        mission = today['mission']
        if mission == 'A':
            campaign.scen_type = 'Advance'
        elif mission == 'B':
            campaign.scen_type = 'Battle'
        else:
            campaign.scen_type = 'Counterattack'

        # write to journal
        WriteJournal('Action Day:')
        WriteJournal(' Mission: ' + campaign.scen_type)
        WriteJournal(' Expected Resistance: ' + campaign.scen_res)
        (h, m) = campaign.GetSunrise()
        WriteJournal(' Sun rose at ' + str(h) + ':' + str(m).zfill(2))

    # pause to show text
    Wait(200)

    # fade out
    for i in range(255, 0, -10):
        libtcod.console_set_fade(i, libtcod.black)
        libtcod.console_flush()
        Wait(1)

    libtcod.console_set_fade(255, libtcod.black)

    libtcod.console_set_alignment(0, libtcod.LEFT)


# run through the campaign calendar and get player input
def RunCalendar(load_day):

    # loading a campaign
    if load_day:
        load_day = False
        LoadGame()

        # set fullscreen mode based on saved settings
        if campaign.fullscreen:
            libtcod.sys_force_fullscreen_resolution(campaign.fs_res_x, campaign.fs_res_y)
            libtcod.console_set_fullscreen(True)

        # loading a campaign day in progress
        if campaign.day_in_progress:
            InitCampaignDay(load=True)
            if campaign.exiting: return
            campaign.day_in_progress = False
            CheckPlayerTank()
            # action day is over so reset the flag
            campaign.action_day = False

    # starting a new campaign
    else:
        SaveGame()

    # load campaign map if any into a console
    campaign_map = None
    if campaign.map_file != '':
        campaign_map = LoadXP(campaign.map_file)

    quit_calendar = False
    while not quit_calendar:

        # get pointer to current day in calendar
        today = GetToday()

        # draw screen
        libtcod.console_set_default_background(con, libtcod.black)
        libtcod.console_clear(con)
        DisplayMenuBar()
        libtcod.console_hline(con, 0, 1, SCREEN_WIDTH, flag=libtcod.BKGND_DEFAULT)
        libtcod.console_set_alignment(con, libtcod.CENTER)

        # display frames and division lines
        libtcod.console_set_default_foreground(con, libtcod.light_grey)
        libtcod.console_print_frame(con, 2, 2, 57, 46, clear=False,
            flag=libtcod.BKGND_DEFAULT, fmt=0)
        libtcod.console_hline(con, 6, 6, 48, flag=libtcod.BKGND_DEFAULT)

        # current calendar date
        libtcod.console_set_default_foreground(con, MENU_TITLE_COLOR)
        libtcod.console_print(con, 30, 4, campaign.GetDate())
        libtcod.console_set_default_foreground(con, libtcod.white)

        # current location or mission
        libtcod.console_print(con, 30, 8, today['comment'])

        # display offered tank model or narrative description of current location / mission
        libtcod.console_set_alignment(con, libtcod.LEFT)
        if campaign.tank_on_offer != '':
            libtcod.console_print(con, 6, 10, 'HQ offers your crew a transfer to a new tank:')
            libtcod.console_print_frame(con, 6, 12, 48, 30,
                clear=False, flag=libtcod.BKGND_DEFAULT, fmt=0)
            ShowVehicleTypeInfo(campaign.tank_on_offer, con, 8, 14, no_image=True)

        # unlimited selection of tank
        elif today['comment'] == 'Refitting' and campaign.unlimited_tank_selection:
            libtcod.console_print(con, 6, 20, 'You have the option of switching')
            libtcod.console_print(con, 6, 21, ' to a new tank model during the refit.')
            libtcod.console_print(con, 6, 22, 'Press [%cS%c] to select a new model.'%HIGHLIGHT)

        # otherwise, description of current location / mission if any
        elif today['description'] is not None:
            lines = wrap(today['description'], 48, subsequent_indent = ' ')
            y = 10
            for line in lines:
                libtcod.console_print(con, 6, y, line)
                y += 1
                # cut off if too long
                if y >= 43:
                    break

        libtcod.console_set_alignment(con, libtcod.CENTER)

        # display mission info if action day
        if campaign.action_day:
            libtcod.console_print(con, 30, 37, 'Mission Type: ' + campaign.scen_type)
            libtcod.console_print(con, 30, 38, 'Expected Resistance for the day: ' + campaign.scen_res)
            DisplayWeather(con, 25, 40)
            libtcod.console_set_default_foreground(con, libtcod.white)
            libtcod.console_set_default_background(con, libtcod.black)

        # finally, display current campaign VP score
        libtcod.console_print(con, 30, 45, 'Current VP Score: ' + str(campaign.vp))

        # display campaign map if any
        if campaign_map is not None:
            libtcod.console_blit(campaign_map, 0, 0, 0, 0, con, 63, 2)

            # display current location on map if any is set
            today = GetToday()
            if today.has_key('map_x') and today.has_key('map_y'):
                x = int(today['map_x'])
                y = int(today['map_y'])
                libtcod.console_put_char(con, x+63, y+2, '@', flag=libtcod.BKGND_NONE)


        # display menu options
        y = 54
        libtcod.console_set_alignment(con, libtcod.LEFT)
        if campaign.action_day:
            text = '[%cB%c]egin combat day'%HIGHLIGHT
        else:
            text = '[%cA%c]dvance to next day'%HIGHLIGHT
        libtcod.console_print(con, 65, y, text)
        libtcod.console_print(con, 65, y+1, '[%cV%c]iew Tank'%HIGHLIGHT)
        if today['comment'] == 'Refitting':
            if campaign.tank_on_offer != '':
                libtcod.console_print(con, 65, y+2, '[%cS%c]witch to Offered Tank'%
                    HIGHLIGHT)
            elif campaign.unlimited_tank_selection:
                libtcod.console_print(con, 65, y+2, '[%cS%c]witch to New Tank'%
                    HIGHLIGHT)
        libtcod.console_print(con, 65, y+3, 'Save and [%cQ%c]uit'%
            HIGHLIGHT)

        libtcod.console_blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)
        libtcod.console_flush()

        refresh = False
        while not refresh:

            # exit right away
            if libtcod.console_is_window_closed():
                sys.exit()

            # exiting the campaign
            if campaign.exiting: return

            # get player input
            libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS|libtcod.EVENT_MOUSE, key, mouse)

            # DEBUG / mapping
            if DEBUG and mouse.rbutton:
                mx, my = mouse.cx, mouse.cy
                if mx >= 63 and my >= 2:
                    print 'Mouse pos: ' + str(mx - 63) + ',' + str(my - 2)

            # get pressed key
            key_char = chr(key.c)

            # help display
            if key.vk == libtcod.KEY_F1 or key.vk == libtcod.KEY_1:
                ShowHelp()
                refresh = True

            # tank info display
            elif key.vk == libtcod.KEY_F2 or key.vk == libtcod.KEY_2:
                ShowTankInfo()
                refresh = True

            # crew info display
            elif key.vk == libtcod.KEY_F3 or key.vk == libtcod.KEY_3:
                ShowCrewInfo()
                refresh = True

            # settings
            elif key.vk == libtcod.KEY_F4 or key.vk == libtcod.KEY_4:
                ShowSettings()
                refresh = True

            # campaign stats
            elif key.vk == libtcod.KEY_F5 or key.vk == libtcod.KEY_5:
                ShowCampaignStats()
                refresh = True

            # screenshot
            elif key.vk == libtcod.KEY_F6 or key.vk == libtcod.KEY_6:
                SaveScreenshot()
                refresh = True

            # save and quit
            if key_char in ['q', 'Q']:
                SaveGame()
                return True

            # view the player tank
            elif key_char in ['v', 'V']:
                campaign.resupply = True
                CampaignViewTank()
                campaign.resupply = False
                refresh = True

            # advance to next day (debug: can always advance day)
            elif key_char in ['a', 'A']:
                if not campaign.action_day or DEBUG:
                    campaign.saw_action = False
                    AdvanceDay()
                    SaveGame()
                    refresh = True

            # start combat day
            elif campaign.action_day and key_char in ['b', 'B']:
                campaign.tank_on_offer = ''
                InitCampaignDay()
                if campaign.exiting: return
                campaign.day_in_progress = False
                CheckPlayerTank()
                # action day is over so reset the flag
                campaign.action_day = False
                campaign.saw_action = True
                refresh = True

            # switch to a new tank
            if today['comment'] == 'Refitting':
                if key_char in ['s', 'S'] and (campaign.tank_on_offer != '' or campaign.unlimited_tank_selection):
                    if PopUp('Switching to a new tank cannot be undone. Are you sure?', confirm=True):
                        if campaign.unlimited_tank_selection:
                            tank_type = ShowTankInfo(select_tank=True)
                            tank.unit_type = tank_type
                        else:
                            tank.unit_type = campaign.tank_on_offer
                            campaign.tank_on_offer = ''
                        CheckPlayerTankPositions()
                        tank.Setup()
                        SetVehicleStats(tank)
                        GetTankName()
                        for crew_member in tank.crew:
                            crew_member.order = crew_member.default_order
                            crew_member.CheckHatch()
                            crew_member.SetSpotAbility()
                    refresh = True

            libtcod.console_flush()


# display campaign settings and allow player to choose
def SetCampaignSettings():

    libtcod.console_clear(0)

    exit_menu = False
    while not exit_menu:

        # generate and display menu
        libtcod.console_clear(menu_con)
        libtcod.console_print_frame(menu_con, 0, 0, MENU_CON_WIDTH, MENU_CON_HEIGHT,
            clear=False, flag=libtcod.BKGND_DEFAULT, fmt=0)

        libtcod.console_set_default_foreground(menu_con, MENU_TITLE_COLOR)
        libtcod.console_print_ex(menu_con, MENU_CON_XM, 1,
            libtcod.BKGND_NONE, libtcod.CENTER, 'Campaign Settings')
        libtcod.console_set_default_foreground(menu_con, libtcod.white)

        libtcod.console_print_ex(menu_con, MENU_CON_XM, 3,
            libtcod.BKGND_NONE, libtcod.CENTER, 'These settings cannot be changed once a campaign has begun')
        libtcod.console_print_ex(menu_con, MENU_CON_XM, 4,
            libtcod.BKGND_NONE, libtcod.CENTER, 'Your selections will be displayed alongside your final score')

        x = 30
        text = '[%cT%c]ank Selection: '%HIGHLIGHT
        if campaign.unlimited_tank_selection:
            text += 'Unlimited'
        else:
            text += 'Strict'
        libtcod.console_set_default_foreground(menu_con, MENU_TITLE_COLOR)
        libtcod.console_print(menu_con, x, 12, text)
        libtcod.console_set_default_foreground(menu_con, libtcod.white)

        if campaign.unlimited_tank_selection:
            libtcod.console_print(menu_con, x, 14, 'You may choose any available model of tank when starting your campaign, when')
            libtcod.console_print(menu_con, x, 15, ' replacing a destroyed tank, or during a refit period.')
        else:
            libtcod.console_print(menu_con, x, 14, 'You must begin the campaign with the assigned tank model, and must accept the')
            libtcod.console_print(menu_con, x, 15, ' model offered to you when replacing a destroyed tank. One randomly selected model')
            libtcod.console_print(menu_con, x, 16, ' will be offered to you during each refit period. Tank model selection is weighted')
            libtcod.console_print(menu_con, x, 17, ' by historical availability and rarity.')

        text = '[%cC%c]ommander Replacement: '%HIGHLIGHT
        if campaign.casual_commander:
            text += 'Casual'
        else:
            text += 'Realistic'
        libtcod.console_set_default_foreground(menu_con, MENU_TITLE_COLOR)
        libtcod.console_print(menu_con, x, 21, text)
        libtcod.console_set_default_foreground(menu_con, libtcod.white)

        if campaign.casual_commander:
            libtcod.console_print(menu_con, x, 23, 'If your tank commander is killed or sent home due to injuries, he will be replaced')
            libtcod.console_print(menu_con, x, 24, ' by a new crewman and you may continue playing.')
        else:
            libtcod.console_print(menu_con, x, 23, 'If your tank commander is killed or sent home due to injuries, your campaign is over.')

        text = 'Campaign Start Date: '
        day = campaign.days[campaign.start_date]
        year = int(day['year'])
        month = int(day['month'])
        date = int(day['date'])
        text += campaign.GetDate(lookup_date = [year, month, date])
        libtcod.console_set_default_foreground(menu_con, MENU_TITLE_COLOR)
        libtcod.console_print(menu_con, x, 26, text)
        libtcod.console_set_default_foreground(menu_con, libtcod.white)
        libtcod.console_print(menu_con, x, 28, '[%cA/D%c] to change starting date of campaign.'%HIGHLIGHT)

        libtcod.console_print_ex(menu_con, MENU_CON_XM, MENU_CON_HEIGHT-3,
            libtcod.BKGND_NONE, libtcod.CENTER, '[%cC/T%c] Toggle Setting'%HIGHLIGHT)
        libtcod.console_print_ex(menu_con, MENU_CON_XM, MENU_CON_HEIGHT-2,
            libtcod.BKGND_NONE, libtcod.CENTER, '[%cEnter%c] Continue'%HIGHLIGHT)

        libtcod.console_blit(menu_con, 0, 0, MENU_CON_WIDTH, MENU_CON_HEIGHT, 0, MENU_CON_X, MENU_CON_Y)

        refresh = False
        while not refresh:

            libtcod.console_flush()

            # get input from user
            libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS|libtcod.EVENT_MOUSE, key, mouse)

            # exit right away
            if libtcod.console_is_window_closed(): sys.exit()

            # continue with these settings
            if key.vk == libtcod.KEY_ENTER:
                exit_menu = True
                break

            # get pressed key
            key_char = chr(key.c)

            if key_char in ['t', 'T']:
                campaign.unlimited_tank_selection = not campaign.unlimited_tank_selection
                refresh = True
            elif key_char in ['c', 'C']:
                campaign.casual_commander = not campaign.casual_commander
                refresh = True

            elif key_char in ['a', 'A']:
                if campaign.start_date == 0:
                    campaign.start_date = len(campaign.days) - 1
                else:
                    campaign.start_date -= 1
                refresh = True

            elif key_char in ['d', 'D']:
                if campaign.start_date < len(campaign.days) - 1:
                    campaign.start_date += 1
                else:
                    campaign.start_date = 0
                refresh = True


# allow player to choose from a list of available campaigns to play
def ChooseCampaign():

    # build list of available campaigns: (filename, name, description)
    campaign_list = []
    filenames = next(os.walk(DATAPATH))[2]
    for f in filenames:
        if f.endswith('.xml'):
            # try to parse this xml file
            test = xml.parse(DATAPATH + f)
            if test is None:
                continue

            # get campaign name and description
            root = test.getroot()
            name = root.find('name').text
            description = root.find('description').text
            campaign_list.append((f, name, description))

    if len(campaign_list) == 0:
        PopUp('Error: No Campaign files found!')
        return None

    # new: sort the list reverse alphabetically
    campaign_list.sort(reverse=True)

    # select first one in list by default
    selected = 0

    libtcod.console_clear(0)

    exit_menu = False
    while not exit_menu:

        # generate and display menu

        libtcod.console_clear(menu_con)
        libtcod.console_print_frame(menu_con, 0, 0, MENU_CON_WIDTH, MENU_CON_HEIGHT,
            clear=False, flag=libtcod.BKGND_DEFAULT, fmt=0)

        libtcod.console_set_default_foreground(menu_con, MENU_TITLE_COLOR)
        libtcod.console_print_ex(menu_con, MENU_CON_XM, 1,
            libtcod.BKGND_NONE, libtcod.CENTER, 'Select a Campaign')
        libtcod.console_set_default_foreground(menu_con, libtcod.light_grey)


        # display info on selected campaign
        (f, name, description) = campaign_list[selected]
        libtcod.console_set_default_foreground(menu_con, SELECTED_COLOR)
        libtcod.console_print_ex(menu_con, MENU_CON_XM, 12,
            libtcod.BKGND_NONE, libtcod.CENTER, name)
        libtcod.console_set_default_foreground(menu_con, libtcod.white)
        lines = wrap(description, 80, subsequent_indent = ' ')
        y = 14
        for line in lines:
            libtcod.console_print(menu_con, 35, y, line)
            y += 1

        libtcod.console_print_ex(menu_con, MENU_CON_XM, MENU_CON_HEIGHT-3,
            libtcod.BKGND_NONE, libtcod.CENTER, '[%cA/D/Left/Right%c] Select Different Campaign'%HIGHLIGHT)
        libtcod.console_print_ex(menu_con, MENU_CON_XM, MENU_CON_HEIGHT-2,
            libtcod.BKGND_NONE, libtcod.CENTER, '[%cEnter%c] Continue with Selected Campaign'%HIGHLIGHT)

        libtcod.console_blit(menu_con, 0, 0, MENU_CON_WIDTH, MENU_CON_HEIGHT, 0, MENU_CON_X, MENU_CON_Y)

        refresh = False
        while not refresh:

            libtcod.console_flush()

            # get input from user
            libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS|libtcod.EVENT_MOUSE, key, mouse)

            # exit right away
            if libtcod.console_is_window_closed(): sys.exit()

            # get pressed key
            key_char = chr(key.c)

            if key.vk == libtcod.KEY_LEFT or key_char in ['a', 'A']:
                if selected > 0:
                    selected -= 1
                else:
                    selected = len(campaign_list) - 1
                refresh = True

            elif key.vk == libtcod.KEY_RIGHT or key_char in ['d', 'D']:
                if selected < len(campaign_list) - 1:
                    selected += 1
                else:
                    selected = 0
                refresh = True

            # return selected campaign filename
            elif key.vk == libtcod.KEY_ENTER:
                n = 0
                for (f, name, description) in campaign_list:
                    if n == selected:
                        return f
                    n += 1


# set up and start a new campaign
def NewCampaign():

    global tank, battle, campaign

    TutorialMessage('welcome')

    # create a new campaign object and an empty battle pointer
    campaign = Campaign()
    battle = None

    # allow player to select from available campaigns
    campaign.campaign_file = ChooseCampaign()

    # write the header entries for the campaign journal
    WriteJournal('*** Armoured Commander Campaign Journal ***')
    WriteJournal('Program Version: ' + VERSION + SUBVERSION)
    WriteJournal('')
    WriteJournal('Campaign Started at ' + datetime.now().strftime("%I:%M%p on %B %d, %Y"))
    WriteJournal('')

    # load basic campaign info into campaign object
    LoadCampaignInfo()

    WriteJournal('Campaign Name: ' + campaign.campaign_name)

    # allow player to select campaign settings
    SetCampaignSettings()

    text = ' Unlimited Tank Selection: '
    if campaign.unlimited_tank_selection:
        text += 'On'
    else:
        text += 'Off'
    WriteJournal(text)

    text = ' Casual Commander Replacement: '
    if campaign.casual_commander:
        text += 'On'
    else:
        text += 'Off'
    WriteJournal(text)
    WriteJournal('')

    # set starting date now
    AdvanceDay()

    # if tank selection is unlimited, allow player to select tank model
    tank_type = None
    if campaign.unlimited_tank_selection:
        tank_type = ShowTankInfo(select_tank=True)

    # create a new player tank object
    tank = PlayerTank(tank_type)
    SetVehicleStats(tank)

    # get or generate tank name
    GetTankName()

    WriteJournal('Starting Tank: ' + tank.unit_type + ' "' + tank.name + '"')

    # set up player tank crew

    # Commander
    crewman = SpawnCrewMember(None, 'Commander', 3)
    crewman.SetLevel(3)
    # get or generate commander name
    GetCommanderName(crewman)
    PopUp(crewman.name + ' is assigned as your tank Commander. You may add/upgrade ' +
        'his skills now or save your skill points for later.')
    # allow player to spend skill points on commander
    ShowSkills(crewman)

    crewman = SpawnCrewMember(None, 'Gunner', 2)
    crewman.SetLevel(2)
    PopUp(crewman.name + ' is assigned as your Gunner.')
    ShowSkills(crewman)

    crewman = SpawnCrewMember(None, 'Loader', 1)
    PopUp(crewman.name + ' is assigned as your Loader.')
    ShowSkills(crewman)

    crewman = SpawnCrewMember(None, 'Driver', 0)
    PopUp(crewman.name + ' is assigned as your Driver.')
    ShowSkills(crewman)

    # some tank models have no assistant driver
    if not tank.stats.has_key('no_asst_driver'):
        crewman = SpawnCrewMember(None, 'Asst. Driver', 0)
        PopUp(crewman.name + ' is assigned as your Assistant Driver.')
        ShowSkills(crewman)

    # start the campaign calendar
    RunCalendar(False)


# start or continue a campaign day of action
def InitCampaignDay(load=False):

    global campaign, tank, battle

    # if we're loading from a saved game
    if load:
        # reset the selected crew pointer
        if campaign.selected_crew is not None:
            campaign.selected_crew = tank.crew[0]
        # reset the exit flag
        campaign.exiting = False
        # paint the campaign map console
        PaintCampaignMap()
        # set up other consoles
        UpdateCActionCon()
        UpdateCInfoCon(mouse.cx, mouse.cy)
        libtcod.console_clear(con)
    else:

        # record the day of combat
        campaign.AddStat('Days of Combat', 1)

        # reset the camapaign object for a new day
        campaign.ResetForNewDay()

        # set flag that day is in progress
        campaign.day_in_progress = True

        # create an empty battle object
        battle = None

        # set time to dawn
        (campaign.hour, campaign.minute) = campaign.GetSunrise()

        # allow player to set up tank
        campaign.resupply = True
        campaign.GenerateAmmo()
        # pop right into the main gun ammo menu
        CampaignViewTank(load_ammo_menu=True)
        campaign.resupply = False
        campaign.ClearAmmo()

        # display mission type briefing if first time for this mission
        if campaign.scen_type == 'Advance':
            TutorialMessage('advance_mission')
        elif campaign.scen_type == 'Battle':
            TutorialMessage('battle_mission')
        elif campaign.scen_type == 'Counterattack':
            TutorialMessage('counterattack_mission')

        # head to start area: apply time and ammo usage
        roll = Roll1D10()

        hours_elapsed = int(floor(roll / 2)) + 1
        ammo_expended = roll * 2

        # don't expend more HE shells than we have
        if tank.general_ammo['HE'] < ammo_expended:
            ammo_expended = tank.general_ammo['HE']
        tank.general_ammo['HE'] -= ammo_expended

        campaign.hour += hours_elapsed
        UpdateDateCon()

        # display message with time and ammo expended
        libtcod.console_clear(con)
        libtcod.console_set_alignment(con, libtcod.CENTER)
        text = 'Heading to your start area took ' + str(hours_elapsed) + ' hour'
        if hours_elapsed > 1:
            text += 's'
        text += ' and your tank expended ' + str(ammo_expended) + ' HE round'
        if ammo_expended > 1 or ammo_expended == 0:
            text += 's'
        text += '.'
        libtcod.console_print(con, SCREEN_XM, 21, text)
        libtcod.console_print(con, SCREEN_XM, SCREEN_HEIGHT-16, 'Press Enter to continue')
        libtcod.console_blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)
        libtcod.console_flush()
        WaitForEnter()

        # reset and clear console
        libtcod.console_clear(con)
        libtcod.console_print(con, SCREEN_XM, int(SCREEN_HEIGHT/2), 'Generating Campaign Map...')
        libtcod.console_blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)
        libtcod.console_flush()
        libtcod.console_set_default_background(con, libtcod.black)
        libtcod.console_set_alignment(con, libtcod.LEFT)

        # generate Campaign Day Map
        # generate a new map
        good_map = False
        while not good_map:
            campaign.nodes = []
            good_map = GenerateCampaignMap()
        # paint the campaign map console
        PaintCampaignMap()

        # set up other consoles
        UpdateCActionCon()
        UpdateCInfoCon(mouse.cx, mouse.cy)
        libtcod.console_clear(con)

        # determine whether tank is lead tank for the day
        tank.SetLeadTank()

        # make sure player node is on screen
        campaign.MoveViewTo(campaign.day_map.player_node)

        # counterattack missions start with one wave of enemy attack
        if campaign.scen_type == 'Counterattack':
            campaign.DoEnemyAdvance()

        # all other missions allow an initial check of an adjacent area, no time cost
        else:
            SetupCheckArea()
            campaign.free_check = True
            PopUp('Select an adjacent area to check for enemy resistance')
            RenderCampaign()

        # save the game before continuing
        SaveGame()

    DoCampaignDay()

    # if we just finished a campaign day
    if campaign.sunset:

        # add VP earned from day to total
        campaign.vp += campaign.day_vp

        # set highest one-day VP score this month if higher
        if campaign.day_vp > campaign.record_day_vp:
            campaign.record_day_vp = campaign.day_vp

        campaign.day_vp = 0
        campaign.day_in_progress = False


# handle campaign actions for a day of action in the campaign
def DoCampaignDay():

    global key, mouse

    # cancel a campaign action in progress
    def CancelAction():
        campaign.input_mode = 'None'
        UpdateCActionCon()
        UpdateCOverlay()
        RenderCampaign()

    # make sure player node is on screen
    campaign.MoveViewTo(campaign.day_map.player_node)

    # if we are loading a saved game and we were in an encounter, init it now
    if battle is not None:
        InitEncounter(load=True)
        if campaign.exiting: return
        PostEncounter()
    else:
        # draw consoles and screen for first time
        UpdateDateCon()
        UpdateCActionCon()
        UpdateCOverlay()
        RenderCampaign()

    exit_campaign = False
    while not exit_campaign:

        # check for exit flag
        if campaign.exiting or campaign.sunset:
            return

        # exit right away
        if libtcod.console_is_window_closed():
            sys.exit()

        # check for keyboard or mouse input
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS|libtcod.EVENT_MOUSE, key, mouse)

        # do mouse stuff first
        mx, my = mouse.cx, mouse.cy

        # check mouse position against last recorded one
        if (mx, my) != campaign.mouseover:
            campaign.mouseover = (mx, my)

            # update campaign info console
            UpdateCInfoCon(mx, my)
            RenderCampaign()

        # campaign menu
        if key.vk == libtcod.KEY_ESCAPE:
            if CampaignMenu():
                campaign.exiting = True
                SaveGame()
                return

        # help display
        elif key.vk == libtcod.KEY_F1 or key.vk == libtcod.KEY_1:
            ShowHelp()

        # tank info display
        elif key.vk == libtcod.KEY_F2 or key.vk == libtcod.KEY_2:
            ShowTankInfo()

        # crew info display
        elif key.vk == libtcod.KEY_F3 or key.vk == libtcod.KEY_3:
            ShowCrewInfo()

        # settings
        elif key.vk == libtcod.KEY_F4 or key.vk == libtcod.KEY_4:
            ShowSettings()

        # campaign stats
        elif key.vk == libtcod.KEY_F5 or key.vk == libtcod.KEY_5:
            ShowCampaignStats()

        # screenshot
        elif key.vk == libtcod.KEY_F6 or key.vk == libtcod.KEY_6:
            SaveScreenshot()

        # get pressed key
        key_char = chr(key.c)

        # debug commands: end campaign day
        if DEBUG:
            if key_char == 'e' and (key.lctrl or key.rctrl):
                (new_hour, new_minute) = campaign.GetSunset()
                campaign.hour = new_hour
                campaign.minute = new_minute
                campaign.CheckSunset()

            # generate a new campaign day map
            elif key_char == 'g' and (key.lctrl or key.rctrl):
                # generate a new map
                good_map = False
                while not good_map:
                    campaign.nodes = []
                    good_map = GenerateCampaignMap()
                PaintCampaignMap()
                UpdateCOverlay()
                RenderCampaign()

        if key_char in ['w', 'W'] or key.vk == libtcod.KEY_UP:
            campaign.c_map_y -= 10
            campaign.CheckYOffset()
            UpdateCInfoCon(mx, my)
            RenderCampaign()

        elif key_char in ['s', 'S'] or key.vk == libtcod.KEY_DOWN:
            campaign.c_map_y += 10
            campaign.CheckYOffset()
            UpdateCInfoCon(mx, my)
            RenderCampaign()

        # if we're in check adjacent area mode
        if campaign.input_mode == 'Check Adjacent Area':

            if key.vk == libtcod.KEY_TAB:
                SelectNextArea()
                campaign.MoveViewTo(campaign.selected_node)

            elif key.vk == libtcod.KEY_ENTER:
                campaign.MoveViewTo(campaign.selected_node)
                CheckArea()
                campaign.CheckSunset()
                campaign.RandomCampaignEvent()

            # cancel action if not free check
            elif key.vk == libtcod.KEY_BACKSPACE and not campaign.free_check:
                CancelAction()

        # we're in move to area mode
        elif campaign.input_mode == 'Move Into Adjacent Area':

            if key.vk == libtcod.KEY_TAB:
                SelectNextArea()
                campaign.MoveViewTo(campaign.selected_node)

            elif key.vk == libtcod.KEY_ENTER:
                campaign.MoveViewTo(campaign.selected_node)
                MoveArea()
                if campaign.exiting: return

                campaign.CheckSunset()
                # in case we've moved to a new map, shift view to selected area
                campaign.MoveViewTo(campaign.selected_node)
                # we don't check for a RandomCampaignEvent() here because it's
                #  handled by PostEncounter

            # cancel action
            elif key.vk == libtcod.KEY_BACKSPACE:
                CancelAction()

        # call strike mode
        elif campaign.input_mode == 'Call in Strike':

            if key.vk == libtcod.KEY_TAB:
                SelectNextArea()
                campaign.MoveViewTo(campaign.selected_node)

            elif key_char in ['a', 'r']:
                campaign.MoveViewTo(campaign.selected_node)
                CallStrike(key_char)
                campaign.CheckSunset()
                campaign.RandomCampaignEvent()

            # cancel action
            elif key.vk == libtcod.KEY_BACKSPACE:
                CancelAction()

        # otherwise, we can choose a new campaign action
        else:

            # only allowed if not counterattack mission
            if campaign.scen_type != 'Counterattack':

                if key_char in ['c', 'C']:
                    SetupCheckArea()
                    campaign.MoveViewTo(campaign.selected_node)
                elif key_char in ['a', 'A']:
                    SetupCallStrike()
                    campaign.MoveViewTo(campaign.selected_node)

            # only allowed in counterattack
            else:
                # await counterattack
                if key_char in ['a', 'A']:
                    AwaitEnemy()

            # allowed in any mission (with some restrictions checked in function)
            if key_char in ['e', 'E']:
                SetupMoveArea()
                campaign.MoveViewTo(campaign.selected_node)

            elif key_char in ['r', 'R']:
                if PopUp('Spend 15 mins. trying to get resupplied?', confirm=True):
                    SetupResupply()
                    # if sunset has hit, don't trigger a battle
                    campaign.CheckSunset()
                    if campaign.sunset:
                        return
                    if campaign.scen_type == 'Counterattack':
                        AwaitEnemy(no_time=True)
                else:
                    RenderCampaign()

            elif key_char in ['v', 'V']:
                CampaignViewTank()
                RenderCampaign()

            elif key_char in ['h', 'H']:
                # check that we can head home
                if [i for i in ENDING_DAMAGES if i in tank.damage_list]:
                    if PopUp('Return to HQ and allow the rest of your ' +
                        'battlegroup to continue on alone?',
                        confirm=True):
                        campaign.HeadHome()

        libtcod.console_flush()


##########################################################################################
#                                 Images, Sound, and Music                               #
##########################################################################################

# load an image, fix its path and filename, and return it
def LoadImage(image_name):
    pathname = DATAPATH + image_name + '.png'
    return libtcod.image_load(pathname)


# return the proper sound file to use for the given main gun type
def GetFiringSound(gun_type):
    if gun_type in ['20L', '50L']:
        return '20_mm_gun'
    if gun_type in ['75', '75L', '75LL']:
        return '75_mm_gun'
    if gun_type in ['76L', '76LL']:
        return '76_mm_gun'
    if gun_type in ['88L', '88LL']:
        return '88_mm_gun'
    return None


# load game sound effects from data archive
def LoadSounds():

    SOUND_LIST = ['20_mm_gun', '75_mm_gun', '76_mm_gun', '88_mm_gun', 'main_gun_misfire',
        'menu_select', 'aa_mg_firing', 'armour_save',
        'arty_firing', 'bow_mg_firing', 'coax_mg_firing', 'dice_roll',
        'engine_noise', 'german_rifle_fire', 'german_mg_fire', 'infantry_moving',
        'panzerfaust_firing', 'radio', 'screenshot', 'shell_move',
        'sherman_movement', 'smoke_hit', 'tank_knocked_out',
        'hatch_open', 'hatch_close', 'he_hit', 'ap_hit', 'main_gun_miss',
        'new_skill'
        ]

    # load the sounds from the zip file into memory
    with zipfile.ZipFile('data/sounds.zip', 'r') as archive:
        for sound_name in SOUND_LIST:
            sound_data = archive.read(sound_name + '.wav')
            bytes_io = io.BytesIO(sound_data)
            sound = pygame.mixer.Sound(bytes_io)
            sound.set_volume(0.50)
            SOUNDS[sound_name] = sound

# play a sound
def PlaySound(sound_name):
    # don't play the sound if campaign sound setting has been set to no sounds
    if campaign is not None:
        if not campaign.sounds:
            return

    # make sure sound is actually part of archive
    if not sound_name in SOUNDS:
        print 'ERROR: Sound file not found: ' + sound_name + '.wav'
        return

    SOUNDS[sound_name].play()


##########################################################################################
#                                        Main Menu                                       #
##########################################################################################

# display game credits
def DisplayCredits():

    current_line = 0
    paused = False

    # animation timing
    animate_time = time.time()

    exit_menu = False
    while not exit_menu:

        refresh = False
        libtcod.console_clear(con)

        libtcod.console_print_frame(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT,
            clear=False, flag=libtcod.BKGND_DEFAULT, fmt=0)

        libtcod.console_set_alignment(con, libtcod.CENTER)

        libtcod.console_set_default_foreground(con, MENU_TITLE_COLOR)
        libtcod.console_print(con, SCREEN_XM, 3, '-- Credits --')
        libtcod.console_set_default_foreground(con, libtcod.white)

        n = 0
        for line in CREDITS_TEXT:
            y = SCREEN_HEIGHT - 10 - (current_line - n)
            n += 1
            if y < 10: continue
            if y > SCREEN_HEIGHT-9: break

            libtcod.console_print(con, SCREEN_XM, y, line)

        libtcod.console_print(con, SCREEN_XM, SCREEN_HEIGHT-4, '[%cP%c] to Pause'%HIGHLIGHT)
        libtcod.console_print(con, SCREEN_XM, SCREEN_HEIGHT-3, '[%cEnter or ESC%c] to Return'%HIGHLIGHT)
        libtcod.console_blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)
        libtcod.console_flush()

        while not refresh:
            # get input from user
            libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS|libtcod.EVENT_MOUSE, key, mouse)

            # exit right away
            if libtcod.console_is_window_closed():
                sys.exit()

            elif key.vk == libtcod.KEY_ENTER or key.vk == libtcod.KEY_ESCAPE:
                return

            elif chr(key.c) in ['p', 'P']:
                paused = not paused

            # update animation
            if not paused:
                if time.time() - animate_time >= 0.75:
                    animate_time = time.time()
                    current_line += 1
                    if current_line >= len(CREDITS_TEXT) + 40:
                        current_line = 0
                    refresh = True


# display a list of high scores
def DisplayHighScores():
    # open bones file
    save = shelve.open('bones')
    bones = save['bones']
    save.close()

    libtcod.console_clear(con)

    libtcod.console_print_frame(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT,
        clear=False, flag=libtcod.BKGND_DEFAULT, fmt=0)

    libtcod.console_set_alignment(con, libtcod.CENTER)

    libtcod.console_set_default_foreground(con, MENU_TITLE_COLOR)
    libtcod.console_print(con, SCREEN_XM, 2, '-- High Scores --')
    libtcod.console_set_default_foreground(con, libtcod.white)

    libtcod.console_set_alignment(con, libtcod.LEFT)

    libtcod.console_print(con, 10, 6, 'Campaign')
    libtcod.console_print(con, 30, 6, 'Tank')
    libtcod.console_print(con, 50, 6, 'Commander')
    libtcod.console_print(con, 70, 6, 'VP Score')
    libtcod.console_print(con, 84, 6, 'Outcome')
    libtcod.console_hline(con, 10, 7, 120, flag=libtcod.BKGND_DEFAULT)

    y = 9
    for (tank, commander, score, outcome, ts, cc, campaign_name) in bones.score_list:
        libtcod.console_print(con, 10, y, campaign_name)
        libtcod.console_print(con, 30, y, tank)
        libtcod.console_print(con, 50, y, commander)

        text = str(score)
        # add notes for campaign options
        if ts or cc:
            text += ' ('
            if ts: text += 'U'
            if cc: text += 'C'
            text += ')'
        libtcod.console_print(con, 70, y, text)

        libtcod.console_print(con, 84, y, outcome)
        y += 1

    libtcod.console_set_alignment(con, libtcod.CENTER)
    libtcod.console_print(con, SCREEN_XM, SCREEN_HEIGHT-6, '[%cEnter%c] Continue'%HIGHLIGHT)
    libtcod.console_blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)
    libtcod.console_flush()
    WaitForEnter()
    PlaySound('menu_select')


# Display the main menu for the game
def MainMenu():

    # grab a random entry from the graveyard to display in the main menu
    def GetRandomGrave():
        save = shelve.open('bones')
        bones = save['bones']
        save.close()
        if len(bones.graveyard) == 0:
            return None
        return random.choice(bones.graveyard)

    # update the cloud layer console
    def UpdateCloudLayer():
        global cloud_altitude, cloud_height, cloud_length, c_cloud_length

        # shift console content over
        libtcod.console_set_key_color(title_cloud_layer, libtcod.black)
        libtcod.console_blit(title_cloud_layer, 1, 0, SCREEN_WIDTH-1,
            30, title_cloud_layer, 0, 0)
        libtcod.console_set_key_color(title_cloud_layer, KEY_COLOR)
        libtcod.console_set_default_background(title_cloud_layer, KEY_COLOR)
        libtcod.console_rect(title_cloud_layer, SCREEN_WIDTH-1,
            0, 1, 30, False, flag=libtcod.BKGND_SET)
        libtcod.console_set_default_background(title_cloud_layer, libtcod.white)

        # see if we need to continue drawing a cloud
        if c_cloud_length > 0:
            h = cloud_height
            if c_cloud_length == cloud_length or c_cloud_length == 1:
                h -= 2
            libtcod.console_rect(title_cloud_layer, SCREEN_WIDTH-1,
                30 - cloud_altitude - int(h/2), 1, h, False,
                flag=libtcod.BKGND_SET)
            c_cloud_length -= 1

        # otherwise, chance of new cloud
        elif libtcod.random_get_int(0, 1, 14) == 1:
            # generate a new altitude, height, length
            cloud_altitude = libtcod.random_get_int(0, 10, 29)
            cloud_height = random.choice([3, 5, 7])
            cloud_length = libtcod.random_get_int(0, 10, 17)
            c_cloud_length = cloud_length

    # randomly change the height of the ground being drawn
    def GetNewGroundHeight(current_height):
        roll = libtcod.random_get_int(0, 1, 10)
        if roll == 1 and current_height > 3:
            return current_height - 1
        elif roll == 10 and current_height < 8:
            return current_height + 1
        return current_height

    # draw the main menu image layers to the main console
    def DrawLayers():
        libtcod.console_blit(title_background, 0, 0, 149, 30, con, 0, 2)
        libtcod.console_blit(title_cloud_layer, 0, 0, 149, 30, con, 0, 2)
        libtcod.console_blit(title_ground_layer, 0, 0, 149, 30, con, 0, 2)
        libtcod.console_blit(title, 0, 0, 80, 25, con, 34, 4)

    # Start of actual Main Menu stuff:
    # generate consoles for main menu

    # generate background console
    title_background = libtcod.console_new(149, 30)
    COLOR1 = libtcod.Color(255,255,114)
    COLOR2 = libtcod.Color(193,8,3)
    for y in range(0, 30):
        color = libtcod.color_lerp(COLOR1, COLOR2, float(y) / 30.0)
        libtcod.console_set_default_background(title_background, color)
        libtcod.console_rect(title_background, 0, y, 149, 1, False, flag=libtcod.BKGND_SET)

    # generate title text console: "ARMOURED COMMANDER"
    title = libtcod.console_new(80, 25)
    libtcod.console_set_key_color(title, KEY_COLOR)
    libtcod.console_set_default_background(title, KEY_COLOR)
    libtcod.console_clear(title)
    libtcod.console_set_default_background(title, libtcod.black)
    y = 0
    for line in TITLE:
        x = 0
        black = False
        for width in line:
            if black:
                libtcod.console_rect(title, x, y, width, 1, False, flag=libtcod.BKGND_SET)
                black = False
            else:
                black = True
            x += width
        y += 1

    # generate cloud layer console
    title_cloud_layer = libtcod.console_new(SCREEN_WIDTH, 30)
    libtcod.console_set_default_background(title_cloud_layer, KEY_COLOR)
    libtcod.console_clear(title_cloud_layer)
    libtcod.console_set_key_color(title_cloud_layer, KEY_COLOR)
    libtcod.console_set_default_background(title_cloud_layer, libtcod.white)

    global cloud_altitude, cloud_height, cloud_length, c_cloud_length
    c_cloud_length = 0
    for x in range(0, SCREEN_WIDTH):
        UpdateCloudLayer()

    # generate ground layer console
    title_ground_layer = libtcod.console_new(SCREEN_WIDTH, 30)
    libtcod.console_set_default_background(title_ground_layer, KEY_COLOR)
    libtcod.console_clear(title_ground_layer)
    libtcod.console_set_default_background(title_ground_layer, TITLE_GROUND_COLOR)
    libtcod.console_set_key_color(title_ground_layer, KEY_COLOR)
    ground_height = libtcod.random_get_int(0, 3, 8)
    for x in range(0, SCREEN_WIDTH):
        libtcod.console_rect(title_ground_layer, x, 30-ground_height, 1,
            ground_height, False, flag=libtcod.BKGND_SET)
        ground_height = GetNewGroundHeight(ground_height)

    # animation timing
    ground_click = time.time()
    cloud_click = time.time()

    # grab a random graveyard entry to display
    tombstone = GetRandomGrave()

    exit_game = False
    while not exit_game:

        # flag to say that there's a good saved game that can (presumably) be loaded
        good_saved_game = False

        # display main menu
        libtcod.console_set_default_background(con, libtcod.black)
        libtcod.console_clear(con)
        libtcod.console_set_alignment(con, libtcod.CENTER)
        libtcod.console_print(con, SCREEN_XM, 33, 'The World War II Tank Commander Roguelike')

        if os.path.exists('savegame'):
            libtcod.console_print(con, SCREEN_XM, 36, '[%cC%c]ontinue Campaign:'%
                HIGHLIGHT)

            # get info from saved game
            save = shelve.open('savegame')
            game_info = save['info']
            save.close()

            # check saved game version against current
            # also checks against a list of compatible previous versions
            if game_info.game_version != VERSION and game_info.game_version not in COMPATIBLE_VERSIONS:
                libtcod.console_set_default_foreground(con, libtcod.light_red)
                text = 'Saved game does not match current game version'
                libtcod.console_print(con, SCREEN_XM, 38, text)
                text = 'You must reload this saved game with version ' + game_info.game_version
                libtcod.console_print(con, SCREEN_XM, 39, text)
            else:
                good_saved_game = True
                libtcod.console_set_default_foreground(con, libtcod.light_grey)
                libtcod.console_print(con, SCREEN_XM, 38, game_info.campaign_name)
                libtcod.console_print(con, SCREEN_XM, 39, game_info.commander_name)
                libtcod.console_print(con, SCREEN_XM, 40, game_info.tank_name)
                libtcod.console_print(con, SCREEN_XM, 41, game_info.current_date)
            libtcod.console_set_default_foreground(con, libtcod.white)

        libtcod.console_print(con, SCREEN_XM, 43, '[%cN%c]ew Campaign'%
            HIGHLIGHT)
        libtcod.console_print(con, SCREEN_XM, 44, '[%cH%c]igh Scores'%
            HIGHLIGHT)
        libtcod.console_print(con, SCREEN_XM, 45, '[%cV%c]iew Credits'%
            HIGHLIGHT)
        libtcod.console_print(con, SCREEN_XM, 46, '[%cQ%c]uit'%
            HIGHLIGHT)

        libtcod.console_set_default_foreground(con, libtcod.light_grey)
        libtcod.console_print_ex(con, SCREEN_XM, SCREEN_HEIGHT-6, libtcod.BKGND_NONE, libtcod.CENTER, VERSION + SUBVERSION)
        text = 'Copyright 2015-2017 Gregory Adam Scott'
        libtcod.console_print_ex(con, SCREEN_XM, SCREEN_HEIGHT-4, libtcod.BKGND_NONE, libtcod.CENTER, text)
        text = 'Free Software under the GNU General Public License'
        libtcod.console_print_ex(con, SCREEN_XM, SCREEN_HEIGHT-3, libtcod.BKGND_NONE, libtcod.CENTER, text)
        text = 'www.armouredcommander.com'
        libtcod.console_print_ex(con, SCREEN_XM, SCREEN_HEIGHT-2, libtcod.BKGND_NONE, libtcod.CENTER, text)

        # display ascii poppy
        libtcod.console_set_default_foreground(con, libtcod.red)
        libtcod.console_set_alignment(con, libtcod.LEFT)
        libtcod.console_print(con, 4, SCREEN_HEIGHT-6, ",--.")
        libtcod.console_print(con, 3, SCREEN_HEIGHT-5, ".\\  /.")
        libtcod.console_print(con, 2, SCREEN_HEIGHT-4, "(  ()  )")
        libtcod.console_print(con, 3, SCREEN_HEIGHT-3, "`/  \\'")
        libtcod.console_print(con, 4, SCREEN_HEIGHT-2, "`--'")

        libtcod.console_set_default_foreground(con, libtcod.white)
        libtcod.console_set_alignment(con, libtcod.CENTER)

        if datetime.now().month == 11 and datetime.now().day == 11:
            text = 'NEVER AGAIN'
        else:
            text = 'In Memoriam'
        libtcod.console_print(con, 16, SCREEN_HEIGHT-3, text)

        # New: display gravestone info if any
        if tombstone is not None:
            libtcod.console_set_default_background(con, libtcod.dark_grey)
            libtcod.console_set_default_foreground(con, libtcod.black)
            y = 8
            libtcod.console_rect(con, SCREEN_WIDTH-28, SCREEN_HEIGHT-y-2, 16, 1, False, flag=libtcod.BKGND_SET)
            libtcod.console_rect(con, SCREEN_WIDTH-29, SCREEN_HEIGHT-y-1, 18, 1, False, flag=libtcod.BKGND_SET)
            libtcod.console_rect(con, SCREEN_WIDTH-30, SCREEN_HEIGHT-y, 20, 8, False, flag=libtcod.BKGND_SET)
            for text in tombstone:
                libtcod.console_print(con, SCREEN_WIDTH-20, SCREEN_HEIGHT-y, text)
                y -= 1
            libtcod.console_set_default_background(con, libtcod.black)
            libtcod.console_set_default_foreground(con, libtcod.white)

        # do an initial draw of the animation layers
        DrawLayers()

        refresh_menu = False
        while not refresh_menu and not exit_game:

            libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS|libtcod.EVENT_MOUSE, key, mouse)

            # exit right away
            if libtcod.console_is_window_closed():
                sys.exit()

            key_char = chr(key.c)
            if key_char in ['c', 'C']:
                if os.path.exists('savegame') and good_saved_game:
                    PlaySound('menu_select')
                    RunCalendar(True)
                    tombstone = GetRandomGrave()
                    refresh_menu = True

            elif key_char in ['n', 'N']:
                PlaySound('menu_select')
                # if there's already a savegame, make sure we want to replace it
                if os.path.exists('savegame'):
                    if PopUp('Starting a new campaign will erase the currently saved one in progress. Are you sure?', confirm=True, skip_update=True):
                        NewCampaign()
                else:
                    NewCampaign()
                tombstone = GetRandomGrave()
                refresh_menu = True

            elif key_char in ['h', 'H']:
                PlaySound('menu_select')
                DisplayHighScores()
                refresh_menu = True

            elif key_char in ['v', 'V']:
                PlaySound('menu_select')
                DisplayCredits()
                refresh_menu = True

            elif key_char in ['q', 'Q']:
                exit_game = True

            # update animated ground layer
            if time.time() - ground_click >= 0.15:
                animation_click = time.time()

                # re-draw the ground layer image
                libtcod.console_set_key_color(title_ground_layer, libtcod.black)
                libtcod.console_blit(title_ground_layer, 1, 0, SCREEN_WIDTH-1,
                    30, title_ground_layer, 0, 0)
                libtcod.console_set_key_color(title_ground_layer, KEY_COLOR)
                libtcod.console_set_default_background(title_ground_layer, KEY_COLOR)
                libtcod.console_rect(title_ground_layer, SCREEN_WIDTH-1,
                    0, 1, 30-ground_height, False,
                    flag=libtcod.BKGND_SET)
                libtcod.console_set_default_background(title_ground_layer, TITLE_GROUND_COLOR)
                libtcod.console_rect(title_ground_layer, SCREEN_WIDTH-1,
                    30-ground_height, 1, ground_height, False,
                    flag=libtcod.BKGND_SET)
                ground_height = GetNewGroundHeight(ground_height)

                DrawLayers()

                # reset timer
                ground_click = time.time()

            # update animated cloud layer
            if time.time() - cloud_click >= 0.30:
                UpdateCloudLayer()
                DrawLayers()
                # reset timer
                cloud_click = time.time()

            # blit main console to screen
            libtcod.console_blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)
            libtcod.console_flush()


##########################################################################################
#                                       Main Script                                      #
##########################################################################################

global mouse, key
global map_con, overlay_con, map_info_con, msg_con, tank_con, date_con, menu_con, text_con
global c_map_con, c_overlay_con, c_action_con, c_info_con
global tk_table
global campaign, battle

# set campaign variable to None, will be reset later on
campaign = None

# create a new console and return it
def CreateConsole(w, h, bc, fc, a):
    new_con = libtcod.console_new(w, h)
    libtcod.console_set_default_background(new_con, bc)
    libtcod.console_set_default_foreground(new_con, fc)
    libtcod.console_set_alignment(new_con, a)
    libtcod.console_clear(new_con)
    return new_con

# set up basic stuff
os.environ['SDL_VIDEO_CENTERED'] = '1'        # center window on screen
libtcod.console_set_custom_font('terminal8x12_armcom.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_ASCII_INROW, 0, 0)
libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, NAME + ' - ' + VERSION + SUBVERSION, False)
libtcod.sys_set_fps(LIMIT_FPS)
libtcod.console_set_keyboard_repeat(0, 0)

# set defaults for screen console
libtcod.console_set_default_background(0, libtcod.black)
libtcod.console_set_default_foreground(0, libtcod.white)

# create the main display console
con = libtcod.console_new(SCREEN_WIDTH, SCREEN_HEIGHT)
libtcod.console_set_default_background(con, libtcod.black)
libtcod.console_set_default_foreground(con, libtcod.white)
libtcod.console_set_alignment(con, libtcod.LEFT)
libtcod.console_clear(con)

# create game consoles
map_con = CreateConsole(MAP_CON_WIDTH, MAP_CON_HEIGHT, libtcod.black, libtcod.black,
    libtcod.LEFT)            # map
overlay_con = CreateConsole(MAP_CON_WIDTH, MAP_CON_HEIGHT, KEY_COLOR, libtcod.black,
    libtcod.LEFT)            # map overlay
libtcod.console_set_key_color(overlay_con, KEY_COLOR)

c_map_con = CreateConsole(C_MAP_CON_WIDTH, C_MAP_CON_HEIGHT, libtcod.black, libtcod.black,
    libtcod.LEFT)            # campaign map
c_overlay_con = CreateConsole(C_MAP_CON_WIDTH, C_MAP_CON_HEIGHT, KEY_COLOR, libtcod.white,
    libtcod.LEFT)            # campaign map overlay
libtcod.console_set_key_color(c_overlay_con, KEY_COLOR)

map_info_con = CreateConsole(MAP_INFO_CON_WIDTH, MAP_INFO_CON_HEIGHT, libtcod.black,
    libtcod.white, libtcod.CENTER)    # map info
msg_con = CreateConsole(MSG_CON_WIDTH, MSG_CON_HEIGHT, libtcod.black, libtcod.white,
    libtcod.LEFT)            # messages
tank_con = CreateConsole(TANK_CON_WIDTH, TANK_CON_HEIGHT, libtcod.black, libtcod.white,
    libtcod.LEFT)            # tank info
date_con = CreateConsole(DATE_CON_WIDTH, DATE_CON_HEIGHT, libtcod.black, libtcod.white,
    libtcod.LEFT)            # date, time, etc. info
menu_con = CreateConsole(MENU_CON_WIDTH, MENU_CON_HEIGHT, libtcod.black, libtcod.white,
    libtcod.LEFT)            # menu console
text_con = CreateConsole(TEXT_CON_WIDTH, TEXT_CON_HEIGHT, libtcod.black, libtcod.white,
    libtcod.LEFT)            # text display console console
c_action_con = CreateConsole(C_ACTION_CON_W, C_ACTION_CON_H, libtcod.black, libtcod.white,
    libtcod.LEFT)            # campaign action console
c_info_con = CreateConsole(C_INFO_CON_W, C_INFO_CON_H, libtcod.black, libtcod.white,
    libtcod.LEFT)            # campaign message console


# init pygame mixer stuff
pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=1024)
pygame.mixer.init()

# create mouse and key event holders
mouse = libtcod.Mouse()
key = libtcod.Key()

# set up colour control for highlighting command keys
libtcod.console_set_color_control(libtcod.COLCTRL_1, KEY_HIGHLIGHT_COLOR, libtcod.black)

# display loading screen
libtcod.console_clear(con)
libtcod.console_set_alignment(con, libtcod.CENTER)
libtcod.console_print(con, SCREEN_XM, 30, 'Loading...')
libtcod.console_blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)
libtcod.console_flush()

# load sound effects
LoadSounds()

# set up empty bones file if doesn't exist yet
if not os.path.exists('bones'):
    print 'No bones file found; creating a new empty bones file.'
    bones = Bones()
    save = shelve.open('bones')
    save['bones'] = bones
    save.close()

# start main menu
MainMenu()
