# -*- coding: UTF-8 -*-

##########################################################################################
#                            Definitions for Armoured Commander                          #
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
##########################################################################################

# national definitions: defines ranks and decorations

# ranks for USA
USA_RANKS = [
    ('Pvt.', 'Private', 0),            # no insignia
    ('Pfc.', 'Private First Class', 0),    # one stripe (pointing upwards)
    ('Cpl.', 'Corporal', 0),        # two stripes
    ('Sgt.', 'Sergeant', 0),        # three stripes (commander starts here)
    ('S/Sgt.', 'Staff Sergeant', 500),    # three stripes, joined together in a half circle
    ('2nd Lt.', 'Second Lieutenant', 1000),    # single gold bar, upright
    ('1st Lt.', 'First Lieutenant', 2000),    # single silver bar, upright
    ('Capt.', 'Captain', 3000)        # double golden bars, upright
]

# decorations for USA
USA_DECORATIONS = [
    ('Bronze Star', 'for heroic service', 80),
    ('Silver Star', 'for gallantry in action', 100),
    ('Distinguished Service Cross', 'for extraordinary heroism', 120),
    ('Congressional Medal of Honor', 'for conspicuous gallantry and intrepidity', 140)
]

# ranks for UK and Commonwealth
UKC_RANKS = [
    ('Tpr.', 'Trooper', 0),
    ('LCpl.', 'Lance Corporal', 0),
    ('Cpl.', 'Corporal', 0),
    ('Sgt.', 'Sergeant', 0),
    ('S/Sgt.', 'Staff Sergeant', 500),
    ('2nd Lt.', 'Second Lieutenant', 1000),
    ('Lt.', 'Lieutenant', 2000),
    ('Capt.', 'Captain', 3000)
]

# decorations for UK and Commonwealth
UKC_DECORATIONS = [
    ('Military Medal', 'for bravery in the field', 80),
    ('Military Cross', 'for acts of exemplary gallantry', 100),
    ('Distinguished Service Order', 'for meritorious service', 120),
    ('Victoria Cross', 'for valour in the face of the enemy', 140)
]

# characters and colours for animations
import libtcodpy as libtcod
HE_HIT_ANIMATION = [
    (libtcod.CHAR_RADIO_UNSET, libtcod.dark_yellow, 220),
    (libtcod.CHAR_LIGHT, libtcod.dark_red, 240),
    (libtcod.CHAR_LIGHT, libtcod.red, 200),
    (libtcod.CHAR_BLOCK1, libtcod.darker_grey, 300),
]

AP_HIT_ANIMATION = [
    (libtcod.CHAR_RADIO_UNSET, libtcod.dark_yellow, 220),
    (libtcod.CHAR_RADIO_UNSET, libtcod.dark_red, 240),
    (libtcod.CHAR_RADIO_UNSET, libtcod.red, 200),
    (libtcod.CHAR_RADIO_UNSET, libtcod.darker_grey, 300),
]

# list of stats to track in the campaign object, as well as text to use in campaign stats
# display window

C_STATS = [
    'Map Areas Captured',
    'Tanks Lost',
    'Crewmen Sent Home',
    'Crewmen KIA',
    'Infantry Destroyed by Player',
    'Infantry Destroyed by Allies',
    'AT Guns Destroyed by Player',
    'AT Guns Destroyed by Allies',
    'Tanks & SPGs Destroyed by Player',
    'Tanks & SPGs Destroyed by Allies',
    'Other Vehicles Destroyed by Player',
    'Other Vehicles Destroyed by Allies',
    'Quests Assigned', 'Quests Completed'
]

# list of possible full screen resolutions to try
FS_RES_LIST = [(1366, 768), (1680, 1050), (1920, 1080)]

# Crew Skill defintion
# holds information relating to a type of crew skill
class CrewSkill:
    def __init__(self, name, desc, restrictions, levels):
        self.name = name
        self.desc = desc
        self.restrictions = restrictions
        self.levels = levels            # if always active: [100]
    def __repr__(self):
        return str(self.levels)

SKILLS = []

# Commander
SKILLS.append(CrewSkill('Fire Direction', 'Increases modifier for directing fire by +1.',
    ['Commander'], [3,5,7]))
SKILLS.append(CrewSkill('Driver Direction', 'Increases modifier for movement-related ' +
    'rolls by +1.', ['Commander'], [3,5,7]))
SKILLS.append(CrewSkill('Battle Leadership', 'Increases chance of all other crew skill ' +
    'activations for the encounter turn in which it activates.', ['Commander'], [2,4,6]))
    # current effect is +5% chance of activation
SKILLS.append(CrewSkill('Keen Senses', 'Decreases chances of being ambushed at the start ' +
    'of an Advance or Battle encounter, increases chances of ambushing enemy in a ' +
    'Counterattack encounter.', ['Commander'], [10,20,30]))

# Gunner
SKILLS.append(CrewSkill('Quick Trigger', 'Bonus to Rate of Fire roll.', ['Gunner'], [5,10,15]))
SKILLS.append(CrewSkill('Knows Weak Spots', 'An unmodified roll of 3 counts ' +
    'as a critical hit if activated.', ['Gunner'], [5,10,15]))
SKILLS.append(CrewSkill('Target Tracking', 'No negative to-hit modifier for firing at a moving target.',
    ['Gunner'], [5,10,15]))
SKILLS.append(CrewSkill('Gyrostabilizer', 'Gunner must have at least one level ' +
    'of this skill to fire main gun while moving. If skill activates, to-hit penalty ' +
    'is +2, otherwise it doubles to +4. This skill only becomes available after first ' +
    'refit period of campaign.', ['Gunner'], [15,30,60,100]))

# Loader
SKILLS.append(CrewSkill('Fast Hands', 'Bonus to Rate of Fire roll.', ['Loader'], [5,10,15]))
SKILLS.append(CrewSkill('Shell Juggler', 'If activated, reloaded shell is taken from ' +
    'general stores instead of ready rack.', ['Loader'], [3,5,7]))
SKILLS.append(CrewSkill('Scrounger', 'More rare ammo types for main gun available if activated.',
    ['Loader'], [25,50,75]))

# Driver
SKILLS.append(CrewSkill('Drag Racer', 'If tank is moving from a stopped position, ' +
    'bonus to movement roll.', ['Driver'], [10,20,30]))
SKILLS.append(CrewSkill('Eye for Cover', 'If hatch is open, receives a bonus to achieve ' +
    'Hull Down status.', ['Driver'], [3,5,7]))
SKILLS.append(CrewSkill('Tough Mudder', 'If hatch is open, receives a bonus to unbogging ' +
    'roll.', ['Driver'], [3,5,7]))
SKILLS.append(CrewSkill('Cautious Driver', 'Greater chance for tank to start an encounter ' +
    'Hull Down, otherwise tank starts the encounter Moving.', ['Driver'], [5,10,15]))

# Asst Driver
SKILLS.append(CrewSkill('Apprentice Gunner', 'Bonus to to-kill roll when firing bow MG.',
    ['Asst. Driver'], [10,20,30]))
SKILLS.append(CrewSkill('Shell Tosser', 'Doubles bonus to Rate of Fire roll when passing ' +
    'ammo.', ['Asst. Driver'], [10,20,30]))

# Most
SKILLS.append(CrewSkill('Eagle Eyed', 'This crewman has an uncanny ability to spot and identify enemy units' +
    ' when spotting though an open hatch.', ['Commander', 'Loader', 'Driver',
    'Asst. Driver'], [5,10,15]))

# All
SKILLS.append(CrewSkill('Pocket Bible', 'Chance to ignore a Dead result when wounded.',
    [], [25,50,75]))
SKILLS.append(CrewSkill('Gymnast', 'Bonus to Bail Out roll.', [], [40,60,80]))
SKILLS.append(CrewSkill('Lightning Reflexes', 'Chance to ignore wound from collateral ' +
    'damage when crewman is exposed (open hatch, etc.)', [], [40,60,80]))
SKILLS.append(CrewSkill('True Grit', 'Better odds of recovering from negative status ' +
    'effects, resisting Stun, plus more likely that a wound will be less severe.',
    [], [20,40,60,80,100]))
SKILLS.append(CrewSkill('Mechanic', 'Bonus to repair a tank malfunction.',
    [], [25,60,90]))

# highest level that a crew member can reach
LEVEL_CAP = 40

# possible ammo types for player tanks
AMMO_TYPES = ['HE', 'AP', 'WP', 'HCBI', 'HVAP', 'APDS']

# hex location system
# hx, hy, range, list of sectors
HEXES = [

    # long range hexes
    (0, -3, 2, 4), (1, -3, 2, 4), (2, -3, 2, 5), (3, -3, 2, 5), (3, -2, 2, 5),
    (3, -1, 2, 0), (3, 0, 2, 0), (2, 1, 2, 0), (1, 2, 2, 1), (0, 3, 2, 1),
    (-1, 3, 2, 1), (-2, 3, 2, 2), (-3, 3, 2, 2), (-3, 2, 2, 2),
    (-3, 1, 2, 3), (-3, 0, 2, 3), (-2, -1, 2, 3), (-1, -2, 2, 4),

    # medium range hexes
    (0, -2, 1, 4), (1, -2, 1, 4), (2, -2, 1, 5), (2, -1, 1, 5), (2, 0, 1, 0),
    (1, 1, 1, 0), (0, 2, 1, 1), (-1, 2, 1, 2), (-2, 2, 1, 2),
    (-2, 1, 1, 3), (-2, 0, 1, 3), (-1, -1, 1, 4),

    # close range hexes
    (0, -1, 0, 4), (1, -1, 0, 5), (1, 0, 0, 0), (0, 1, 0, 1),
    (-1, 1, 0, 2), (-1, 0, 0, 3),

    # player hex: special because only player tank can exist there, and range is -1
    (0, 0, -1, -1)

]


# CrewOrder class
# defines the description and restrictions of crew orders
class CrewOrder:
    def __init__(self, name, desc, spot, position_list):
        self.name = name
        self.desc = desc
        self.spot = spot
        self.position_list = position_list

# crew order definitions
# Order Name, Order description, Can Spot (bool)
# List of crew positions that can use this order (if list is empty, any crew
# member can use this order)

CREW_ORDERS = []

# None order available to several crew
CREW_ORDERS.append(CrewOrder('None', 'The crew member does nothing this turn.',
    True, ['Commander', 'Gunner', 'Loader', 'Asst. Driver']))

# Commander
CREW_ORDERS.append(CrewOrder('Direct Movement', 'Help direct the movement of your ' +
    'tank. Reduces the chance of a thrown track or bogging down. Full effect ' +
    'if commander directing from open hatch, half effect if buttoned up and ' +
    'tank has a vision cupola. Otherwise no effect. No effect on firing.',
    True, ['Commander']))
CREW_ORDERS.append(CrewOrder('Direct Main Gun Fire', 'Help direct the fire of the main gun, ' +
    'increasing the chances of a hit.',
    True, ['Commander']))
CREW_ORDERS.append(CrewOrder('Direct Co-ax MG Fire', 'Help direct the fire of the co-ax ' +
    'machine gun, increasing the chances of destroying the target. No effect if this ' +
    'MG is not fired this turn.', True, ['Commander']))
CREW_ORDERS.append(CrewOrder('Direct Bow MG Fire', 'Help direct the fire of the bow ' +
    'machine gun, increasing the chances of destroying the target. No effect if this ' +
    'MG is not fired this turn.', True, ['Commander']))

# Gunner
CREW_ORDERS.append(CrewOrder('Fire Main Gun', 'Fire the main gun at an enemy target. Gun ' +
    'must already have a shell loaded in order to fire. Turret can be rotated before ' +
    'firing, but if so then the first shot will be at a penalty.', False, ['Gunner']))
CREW_ORDERS.append(CrewOrder('Fire Co-Axial MG', 'Fire the Co-axial MG at an enemy target. ' +
    'Turret can be rotated before firing, but if so then the shot will be at a ' +
    'penalty.', True, ['Gunner']))
CREW_ORDERS.append(CrewOrder('Rotate Turret', "Rotate turret to face any sector. Gunner " +
    "may only spot in the sector in front of the turret's new facing", True,
    ['Gunner']))
CREW_ORDERS.append(CrewOrder('Help Repair', 'Assist any crewman attempting to repair a ' +
    'malfunction. Only effective if another crewman is on a repair order.', False,
    ['Gunner']))

# Loader
CREW_ORDERS.append(CrewOrder('Reload', "Reload the main gun if it's fired. No effect if " +
    "main gun is malfunctioning. May only spot if main gun is not fired.", True,
    ['Loader']))
CREW_ORDERS.append(CrewOrder('Repair Main Gun', 'Attempt to repair a malfunctioning ' +
    'main gun.', False, ['Loader']))
CREW_ORDERS.append(CrewOrder('Repair Co-ax MG', 'Attempt to repair a malfunctioning ' +
    'co-axial machine gun.', False, ['Loader']))
CREW_ORDERS.append(CrewOrder('Repair Turret Traverse', 'Attempt to repair a broken turret ' +
    'traverse gear.', False, ['Loader']))
CREW_ORDERS.append(CrewOrder('Repair Radio', 'Attempt to repair a broken turret radio.',
    False, ['Loader']))
CREW_ORDERS.append(CrewOrder('Repair Intercom', 'Attempt to repair a broken tank intercom.',
    False, ['Loader']))
CREW_ORDERS.append(CrewOrder('Fire Smoke Mortar', 'Fire the 2" smoke mortar, creating a smoke ' +
    'marker at Close range to the turret front. Also reloads the mortar if any rounds ' +
    'are still available.', False, ['Loader']))
CREW_ORDERS.append(CrewOrder('Change Gun Load', 'Change the type of round loaded in ' +
    'the main gun to any round available. Will also reload the main gun if fired, but ' +
    'cannot maintain RoF if Loader is on this order.',
    False, ['Loader']))
CREW_ORDERS.append(CrewOrder('Restock Ready Rack', 'Refill the ready rack with any ' +
    'rounds still available. Main gun will not be reloaded if it is fired this turn.',
    False, ['Loader']))

# Driver
CREW_ORDERS.append(CrewOrder('Stop', 'Stop the tank.', True, ['Driver']))
CREW_ORDERS.append(CrewOrder('Forward', 'Move the tank forward.', True, ['Driver']))
CREW_ORDERS.append(CrewOrder('Forward to Hull Down', 'Move the tank forward and ' +
    'attempt to move into a hull down position.', True, ['Driver']))
CREW_ORDERS.append(CrewOrder('Reverse', 'Move the tank backward.', True, ['Driver']))
CREW_ORDERS.append(CrewOrder('Reverse to Hull Down', 'Move the tank backward and ' +
    'attempt to move into a hull down position.', True, ['Driver']))
CREW_ORDERS.append(CrewOrder('Pivot Tank', 'Pivot tank to face any sector. Counts as ' +
    'moving, so may not fire main gun, and any hull down position is lost.',
    True, ['Driver']))
CREW_ORDERS.append(CrewOrder('Attempt Unbog', 'Attempt to free the tank from ' +
    'being bogged down. Bonus if commander is directing movement from an ' +
    'open hatch, penalty if driver is buttoned up.', False, ['Driver']))

# Assistant Driver
CREW_ORDERS.append(CrewOrder('Fire Bow MG', "Fire the bow MG in the sector to the " +
    "tank's front. May not fire if tank is hull down. Subtract crew member's " +
    "skill from the To Kill roll.", True, ['Asst. Driver']))
CREW_ORDERS.append(CrewOrder('Repair Bow MG', 'Attempt to repair a malfunctioning ' +
    'bow MG.', False, ['Asst. Driver']))
CREW_ORDERS.append(CrewOrder('Pass Ammo', 'Pass ammo to the Loader to improve reload ' +
    'time. Increases chance of maintaining Rate of Fire. Has no effect when loading ' +
    'from the ready rack.', False, ['Asst. Driver']))

# Orders available to several crew members
CREW_ORDERS.append(CrewOrder('Throw Smoke Grenade', 'The crew member throws a smoke grenade ' +
    'out of an open hatch, creating one smoke factor in the player hex. No effect if ' +
    'no hatch or hatch is shut.',
    True, ['Commander', 'Loader']))
CREW_ORDERS.append(CrewOrder('Fire AA MG', 'Fire the .50 cal MG mounted on the top of the ' +
    'tank turret. Crew member must have an open hatch, and if Loader it must be a split ' +
    'hatch rather than an oval one. The crew member is much more vulnerable to being ' +
    'wounded while on this order, since they must venture outside of the tank.',
    True, ['Commander', 'Loader']))
CREW_ORDERS.append(CrewOrder('Repair AA MG', 'Attempt to repair a malfunctioning ' +
    'AA machine gun. Crew member must have an open hatch. and if Loader it must be a ' +
    'split hatch rather than an oval one. The crew member is much ' +
    'more vulnerable to being wounded while on this order, since they must venture ' +
    'outside of the tank.', False, ['Commander', 'Loader']))
# Bail out order available to all, only activated if one or more crew is incapacitated or worse
CREW_ORDERS.append(CrewOrder('Abandon Tank', 'Order all crewmen to bail out of the tank, ' +
    'risking injury but heading back to friendly lines. Only one crewman needs to ' +
    'have this order to bail out all crewmen.', False, ['Commander', 'Gunner',
    'Loader', 'Driver', 'Asst. Driver']))


# list of possible random tank names for player's tank
TANK_NAMES = [
    'Fury', 'Vengeance', 'Cobra King', 'Hannibal', 'Thunderbolt', 'Blood & Guts',
    'Colorado', 'Condor', 'Apache', 'Ironside', 'Lucky Legs', 'Cairo',
    'Colbert', 'Hurricane', 'Hellbound', 'Lucky Lady', 'ALF', 'Barnbuster',
    'Caribou', 'Flare Path', 'Steadfast', 'Maiden Castle', 'Little John',
    'Goldcrest', 'Folkestone', 'Predator',
    'Anapola', 'Arsenic', 'Astoria', 'Athena', 'Avenger', 'Bastard Bill',
    'Battling Annie', 'Bed Bug', 'Beelzebub', 'Beowulf', 'Betty',
    'The Black Orchid', 'Block Buster', 'Bomb', 'Boomerang', 'Bright Eyes',
    'Buffalo', 'Buck Private', 'China Gal', 'Clodhopper', 'Comet', 'Corsair',
    'Cougar', 'Davy Jones', 'Draftee', 'Eternity', 'The Flying Scot', 'Hot Box',
    'Hot Lips', 'Hot Pants', 'Hyena', "Jeanne D'Arc", 'King Kong', 'Lady Liberty',
    'Murder Inc.', 'Nightmare', 'Old Faithful', "Pistol Packin' Mama",
    'Rachel', 'Shaman', 'Snafu', 'The Stag', 'Stampede', 'Squirrel', 'War Bride'
]

# list of first names for crewmen
FIRST_NAMES = [
    'Gregory', 'Shane', 'Lee', 'Andre', 'Mario', 'Louis', 'Stephen', 'Kenneth',
    'Angelo', 'Oliver', 'Edward', 'Joshua', 'Ronald', 'Victor', 'Eli', 'Mario',
    'Dallas', 'Arthur', 'Anderson', 'Dylan', 'John', 'Quentin', 'Alexander',
    'Timothy', 'Wesley', 'Spencer', 'Leonardo', 'Edgar', 'Bob', 'Chewy',
    'Frank', 'Dmitry', 'Jens', 'Conrad', 'Eric',
    'Robert', 'James', 'William', 'Charles', 'George', 'Joseph', 'Richard',
    'Donald', 'Thomas', 'Frank', 'Harold', 'Paul', 'Raymond', 'Walter', 'Jack',
    'Henry', 'Kenneth', 'Albert', 'David', 'Harry', 'Eugene', 'Ralph', 'Howard',
    'Carl', 'Willie', 'Louis', 'Clarence', 'Earl', 'Roy', 'Fred', 'Joe', 'Francis',
    'Lawrence', 'Herbert', 'Leonard', 'Ernest', 'Alfred', 'Anthony', 'Stanley',
    'Norman', 'Gerald', 'Daniel', 'Samuel', 'Bernard', 'Billy', 'Melvin', 'Martin',
    'Warren', 'Michael', 'Leroy', 'Russell', 'Leo', 'Andrew', 'Edwin', 'Elmer',
    'Peter', 'Floyd', 'Lloyd', 'Ray', 'Fredrick', 'Theodore', 'Clifford', 'Vernon',
    'Herman', 'Clyde', 'Chester', 'Philip', 'Alvin', 'Lester', 'Wayne', 'Vincent',
    'Gordon', 'Leon', 'Lewis', 'Charlie', 'Glenn', 'Calvin', 'Martin', 'Milton',
    'Jesse', 'Dale', 'Cecil', 'Bill', 'Harvey', 'Roger', 'Victor', 'Benjamin',
    'Wallace', 'Sam', 'Allen', 'Arnold', 'Willard', 'Gilbert', 'Edgar', 'Oscar'
]

# list of last names for crewmen
LAST_NAMES = [
    'Abraham', 'Adler', 'Allen', 'Ankins', 'Applegate', 'Avery',
    'Bacon', 'Baker', 'Barnham', 'Belanger', 'Bentz', 'Bessler', 'Best', 'Blakely',
    'Bleeker', 'Bouche', 'Brant', 'Brawley', 'Bretz', 'Brock', 'Brockman',
    'Bruce', 'Buchman', 'Burnett', 'Burns', 'Butterfield',
    'Caffey', 'Christopher', 'Cleary', 'Codere', 'Collins', 'Coutu', 'Cowell',
    'Cowman', 'Cox', 'Craig', 'Crankovitch', 'Cuthburt', 'Cuttling',
    'Darwin', 'Davis', 'Delarosa', 'Douglass', 'Dorman',
    'Eakley', 'Eddie', 'Edwards', 'Elliott', 'Ellis', 'Elsner', 'English',
    'Fanbrick', 'Farwell', 'Feigel', 'Felten', 'Fenske', 'Feigel',
    'Fields', 'Fillman', 'Finley', 'Firske', 'Fournier', 'France', 'Franklin',
    'Freeman', 'Furlong',
    'Gallaway', 'Garvin', 'Germain', 'Gilchrist', 'Gillespie', 'Gohl', 'Goodwin',
    'Gray', 'Greenwald', 'Greenwalt', 'Griffen', 'Griffith',
    'Hahn', 'Halsted', 'Hammermeister', 'Hancock', 'Harmal', 'Hass', 'Hastings',
    'Hayes', 'Heminger', 'Henchal', 'Hessen', 'Hilt', 'Hollister', 'Hollman',
    'Howell', 'Hyde',
    'Jordon',
    'Kaiser', 'Kasper', 'Kegley', 'Kinney', 'Kleeman',
    'Laird', 'Leach', 'Lehman', 'Lesatz', 'Levard', 'Lindh', 'Lynch',
    'Madison', 'Manse', 'Matchinski', 'Mathews', 'Mauldin', 'McAlpine', 'McBurney',
    'McCain', 'McCarney', 'McCown', 'McCutchen', 'McCutcheon', 'McDonald', 'McGraw',
    'Medeiros', 'Merrick', 'Metic', 'Mondt', 'Morris', 'Moses',
    'Navarro', 'Nickels', 'Normandeau', 'Norval',
    "O'Connell", 'Olson', "O'Neal", 'Ozanich',
    'Patterson', 'Patzer', 'Peppin', 'Petrovich', 'Petty', 'Perkins', 'Porter',
    'Posch', 'Price',
    'Rapin', 'Rapp', 'Raslo', 'Razner', 'Rifenberg', 'Riley', 'Ripley', 'Robertson',
    'Rooney', 'Rosental', 'Rossini', 'Russell', 'Rychech',
    'Sawyer', 'Schafer', 'Schmidt', 'Schroeder', 'Schwartz', 'Scott', 'Shattuck',
    'Shaw', 'Simmons', 'Slack', 'Smith', 'Speltzer', 'Stern', 'Stewart', 'Stone',
    'Strenburg', 'Strong', 'Swanson', 'Syveran',
    'Tenker', 'Thomas', 'Traver', 'Vallier', 'Vann', 'Wagner', 'Walsted', 'Warner',
    'Webber', 'Weir', 'Welch', 'Westin', 'White', 'Winters', 'Woods', 'Wolff'
]

import libtcodpy as libtcod                # The Doryen Library
HIGHLIGHT = (libtcod.COLCTRL_1, libtcod.COLCTRL_STOP)

# menu bar
MENU_BAR1 = '%cESC%c:Menu  |  '%HIGHLIGHT
MENU_BAR2 = (
    '%cF1/1%c:Help  |  '%HIGHLIGHT +
    '%cF2/2%c:Tank Info  |  '%HIGHLIGHT +
    '%cF3/3%c:Crew Info'%HIGHLIGHT +
    '%cF4/4%c:Settings  |  '%HIGHLIGHT +
    '%cF5/5%c:Campaign Stats  |  '%HIGHLIGHT +
    '%cF6/6%c:Screenshot  |  '%HIGHLIGHT +
    '%cF7/7%c:Sound'%HIGHLIGHT
    )

# select spot sector
SPOT_SECTOR_INFO = [
    '[%cW/S/Up/Down%c] Select crew'%HIGHLIGHT,
    '[%cA/D/Left/Right%c] Rotate selected spot sector'%HIGHLIGHT,
    '[%cSpace/End%c] Proceed to Spotting Phase'%HIGHLIGHT
]

# instructions for orders phase
ORDERS_PHASE_INFO = [
    '[%cW/S/Up/Down%c] select crewman'%HIGHLIGHT,
    '[%cA/D/Left/Right%c] change order for selected crew'%HIGHLIGHT,
    'Select [%cO%c]rder for selected crew from a menu'%HIGHLIGHT,
    '[%cR%c] cycle through ammo types to use when Reloading the main gun'%HIGHLIGHT,
    '[%cT%c] toggle use of the Ready Rack for reloading the main gun'%HIGHLIGHT,
    '[%cH%c] toggle Hatch status for selected crew member'%HIGHLIGHT,
    '[%cSpace/End%c] finish Orders and proceed to Crew Actions'%HIGHLIGHT
]

# instructions for selecting an order to issue
ORDER_INFO = [
    '[%cW/S/Up/Down%c] Move order selection'%HIGHLIGHT,
    '[%cO%c] Set the selected order'%HIGHLIGHT,
    '[%cBackspace%c] Cancel and keep current order'%HIGHLIGHT
]

# instructions for pivoting tank
PIVOT_INFO = [
    '[%cA/D/Left/Right%c] Pivot to new facing'%HIGHLIGHT,
    '[%cEnter/End%c] Complete pivot'%HIGHLIGHT
]

# instructions for rotating turret
ROTATE_INFO = [
    '[%cA/D/Left/Right%c] Rotate turret'%HIGHLIGHT,
    '[%cEnter/End%c] Set turret facing and continue'%HIGHLIGHT
]

# instructions for firing main gun
FIRE_GUN_INFO = [
    '[%cA/D/Left/Right%c] Rotate turret'%HIGHLIGHT,
    '[%cTab%c] Next target'%HIGHLIGHT,
    '[%cF%c] Toggle Area and Direct Fire'%HIGHLIGHT,
    '[%cR%c] Change ammo type to use when reloading'%HIGHLIGHT,
    '[%cT%c] Toggle use of Ready Rack for reloading'%HIGHLIGHT,
    '[%cEnter%c] Fire main gun'%HIGHLIGHT,
    '[%cSpace/End%c] Finish firing and proceed to resolve hits or to next phase'%HIGHLIGHT
]

# instructions for firing MGs
FIRE_MGS_INFO = [
    '[%cA/D/Left/Right%c] Rotate turret (if co-ax can fire)'%HIGHLIGHT,
    '[%cM%c] Cycle active MG'%HIGHLIGHT,
    '[%cTab%c] Cycle between available targets'%HIGHLIGHT,
    '[%cEnter%c] Fire an MG'%HIGHLIGHT,
    '[%cSpace/End%c] Finish firing and proceed to next phase'%HIGHLIGHT
]

# Campaign - check adjacent area instructions
CHECK_AREA = [
    'Check an Adjacent Area',
    '',
    '[%cTab%c] Cycle through adjacent areas (Shift to reverse)'%HIGHLIGHT,
    '[%cEnter%c] Check selected area for enemy resistance level'%HIGHLIGHT,
    '[%cBackspace%c] Cancel action'%HIGHLIGHT
]

# Campaign - move into an area
MOVE_AREA = [
    'Move into an Adjacent Area',
    '',
    '[%cTab%c] Cycle through adjacent areas (Shift to reverse)'%HIGHLIGHT,
    '[%cEnter%c] Move into area'%HIGHLIGHT,
    '[%cBackspace%c] Cancel move'%HIGHLIGHT
]

# info on enemy infantry units, displayed when player right-clicks on a unit
UNIT_INFO = {
    'Light Weapons Infantry': """\
A squad of seven to ten riflemen, one of whom likely has a machine gun. Can attack and
destroy friendly infantry. No threat to your tank, unless they attack and a crew member
has an open hatch, or if they are in close range and attack with a Panzerfaust AT weapon.
Only HE or Machine Gun attacks will damage them; AP hits will have no effect.""",
    'MG Team': """\
A team of enemy infantry armed with a medium or heavy machine gun. Can attack and destroy
friendly infantry. No threat to your tank, unless they attack and a crew member has an
open hatch. Only HE or Machine Gun attacks will damage them.""",
    '50L': """\
The PaK 38 Anti-Tank Gun was developed in 1938 and first used in 1941 against Russian tanks.
By 1944 it was relatively underpowered compared to the heaviest tank armour then in use,
but was still widely used in the defense of France and Germany.""",
    '75L': """\
The PaK 40 Anti-Tank Gun was developed between 1939 and 1941 and was the most widely-used
german AT gun of the latter part of the war. Its 75mm gun is also mounted on tank
destroyers.""",
    '88LL': """\
The PaK 43 Anti-Tank Gun is a 88mm gun developed in 1943 as an anti-aircraft gun, but was
also widely used in an anti-tank role. With a maximum range of over 8 miles, it has
enough punch and firepower to knock out virtually any Allied tank."""
}

##########################################################################################
#                           List of possible crew statements                             #
##########################################################################################

CREW_TALK_HEAVY_RES = [
    'Might want to call in some support, Commander.',
    'I guess we could go around.',
    'Maybe we could go around?',
    "Can't we find another route?",
    "We're not going in there, are we?",
    "This doesn't look too good.",
    "I guess it's our job to take care of it.",
    "If we don't deal with them, somebody else will have to.",
    "He who runs away lives to fight another day.",
    "We've seen worst. Then again, we've seen better...",
    "Germans. Always, more Germans."
]

CREW_TALK_ARTY_STRIKE = [
    'Thanks guys!',
    "I love that sound. At least when it's far away.",
    "Better outgoing than incoming!",
    "I never thought I'd come to love the sound of artillery.",
    "I hope these shells find 'em."
]

CREW_TALK_NO_ARTY_STRIKE = [
    'What are they doing over there?',
    'How are we supposed to capture territory without proper artillery support?',
    "Looks like all the fun is going to be ours once again.",
    "We could use some help over here.",
    "All right. We still have a job to do!",
    "Conserving ammunition? What about our lives?",
    "Thanks for nothing guys..."
]

CREW_TALK_NO_RES = [
    "It's quiet. Too quiet.",
    'They must have repositioned.',
    "Somebody must have told them we were coming.",
    "Where are they hiding?",
    "I thought we were going to see some action.",
    "I guess they moved somewhere else."
]

CREW_TALK_THROWN_TRACK = [
    "That's not good!",
    "We're immobilized!",
    "We need to repair that track ASAP!",
    "We're sitting ducks.",
    "Busted another track..."
]

CREW_TALK_ARMOUR_SAVED = [
    'Whoa! That was close!',
    'Incoming AT!',
    "My head is ringing.",
    "Saved by the tin box again.",
    "IS THAT ALL YOU GOT?!?",
    "Come on! You hit like my granny!"
]

CREW_TALK_SHOT_MISSED = [
    'That was close. Too close.',
    'We got lucky on that one.',
    "Good thing they can't aim.",
    "They won't be missing forever!",
    "Our turn now.",
    "Don't let them fire again!"
]

# List of hometowns for USA
# based on http://www.census.gov/population/www/documentation/twps0027/tab17.txt
USA_HOMETOWNS = [
    'New York, NY',
    'Chicago, IL',
    'Philadelphia, PA',
    'Detroit, MI',
    'Los Angeles, CA',
    'Cleveland, OH',
    'Baltimore, MD',
    'St. Louis, MO',
    'Boston, MA',
    'Pittsburgh, PA',
    'Washington, DC',
    'San Francisco, CA',
    'Milwaukee, WI',
    'Buffalo, NY',
    'New Orleans, LA',
    'Minneapolis, MN',
    'Cincinnati, OH',
    'Newark, NJ',
    'Kansas City, MO',
    'Indianapolis, IN',
    'Houston, TX',
    'Seattle, WA',
    'Rochester, NY',
    'Denver, CO',
    'Louisville, KY',
    'Columbus, OH',
    'Portland, OR',
    'Atlanta, GA',
    'Oakland, CA',
    'Jersey City, NJ',
    'Dallas, TX',
    'Memphis, TN',
    'St. Paul, MN',
    'Toledo, OH',
    'Birmingham, AL',
    'San Antonio, TX',
    'Providence, RI',
    'Akron, OH',
    'Omaha, NE',
    'Dayton, OH',
    'Syracuse, NY',
    'Oklahoma City, OK',
    'San Diego, CA',
    'Worcester, MA',
    'Richmond, VA',
    'Fort Worth, TX',
    'Jacksonville, FL',
    'Miami, FL',
    'Youngstown, OH',
    'Nashville, TN',
    'Hartford, CT',
    'Grand Rapids, MI',
    'Long Beach, CA',
    'New Haven, CT',
    'Des Moines, IA',
    'Flint, MI',
    'Salt Lake City, UT',
    'Springfield, MA',
    'Bridgeport, CT',
    'Norfolk, VA',
    'Yonkers, NY',
    'Tulsa, OK',
    'Scranton, PA',
    'Paterson, NJ',
    'Albany, NY',
    'Chattanooga, TN',
    'Trenton, NJ',
    'Spokane, WA',
    'Kansas City, KS',
    'Fort Wayne, IN',
    'Camden, NJ',
    'Erie, PA',
    'Fall River, MA',
    'Wichita, KS',
    'Wilmington, DE',
    'Gary, IN',
    'Knoxville, TN',
    'Cambridge, MA',
    'Reading, PA',
    'New Bedford, MA',
    'Elizabeth, NJ',
    'Tacoma, WA',
    'Canton, OH',
    'Tampa, FL',
    'Sacramento, CA',
    'Peoria, IL',
    'Somerville, MA',
    'Lowell, MA',
    'South Bend, IN',
    'Duluth, MN',
    'Charlotte, NC',
    'Utica, NY',
    'Waterbury, CT',
    'Shreveport, LA',
    'Lynn, MA',
    'Evansville, IN',
    'Allentown, PA',
    'El Paso, TX',
    'Savannah, GA',
    'Little Rock, AR',
    'Honolulu, HT'        # i.e. Hawai`i Territory
]

# List of hometowns for Canada, duplicate entries represent high populations and chances
#   or a crewman being from there
CAN_HOMETOWNS = [
    'Toronto, ON',
    'Toronto, ON',
    'Toronto, ON',
    'Toronto, ON',
    'Toronto, ON',
    'Toronto, ON',
    'Toronto, ON',
    'Toronto, ON',
    'Toronto, ON',
    'Toronto, ON',
    'Toronto, ON',
    'Montreal, QC',
    'Montreal, QC',
    'Montreal, QC',
    'Montreal, QC',
    'Montreal, QC',
    'Montreal, QC',
    'Montreal, QC',
    'Montreal, QC',
    'Montreal, QC',
    'Vancouver, BC',
    'Vancouver, BC',
    'Vancouver, BC',
    'Vancouver, BC',
    'Vancouver, BC',
    'Vancouver, BC',
    'Vancouver, BC',
    'Calgary, AB',
    'Calgary, AB',
    'Calgary, AB',
    'Calgary, AB',
    'Calgary, AB',
    'Edmonton, AB',
    'Edmonton, AB',
    'Edmonton, AB',
    'Edmonton, AB',
    'Edmonton, AB',
    'Ottawa, ON',
    'Ottawa, ON',
    'Ottawa, ON',
    'Ottawa, ON',
    'Gatineau, QC',
    'Gatineau, QC',
    'Gatineau, QC',
    'Quebec City, QC',
    'Quebec City, QC',
    'Quebec City, QC',
    'Quebec City, QC',
    'Quebec City, QC',
    'Winnipeg, MB',
    'Winnipeg, MB',
    'Winnipeg, MB',
    'Winnipeg, MB',
    'Winnipeg, MB',
    'Hamilton, ON',
    'Hamilton, ON',
    'Hamilton, ON',
    'Hamilton, ON',
    'Kitchener, ON',
    'Kitchener, ON',
    'Kitchener, ON',
    'Kitchener, ON',
    'London, ON',
    'London, ON',
    'London, ON',
    'London, ON',
    'Victoria, BC',
    'Victoria, BC',
    'Victoria, BC',
    'Victoria, BC',
    'Halifax, NS',
    'Halifax, NS',
    'Halifax, NS',
    'Halifax, NS',
    'Oshawa, ON',
    'Oshawa, ON',
    'Oshawa, ON',
    'Oshawa, ON',
    'Windsor, ON',
    'Windsor, ON',
    'Windsor, ON',
    'Windsor, ON',
    'Saskatoon, SK',
    'Saskatoon, SK',
    'Saskatoon, SK',
    'Regina, SK',
    'Regina, SK',
    'Regina, SK',
    'Barrie, ON',
    'Barrie, ON',
    'Barrie, ON',
    'Abbotsford, BC',
    'Abbotsford, BC',
    'Kelowna, BC',
    'Kelowna, BC',
    'Sherbrooke, QC',
    'Sherbrooke, QC',
    'Trois-Rivieres, QC',
    'Trois-Rivieres, QC',
    'Guelph, ON',
    'Guelph, ON',
    'Kingston, ON',
    'Kingston, ON',
    'Moncton, NB',
    'Moncton, NB',
    'Sudbury, ON',
    'Sudbury, ON',
    'Chicoutimi-Jonquiere, QC',
    'Chicoutimi-Jonquiere, QC',
    'Thunder Bay, ON',
    'Thunder Bay, ON',
    'Kanata, ON',
    'Kanata, ON',
    'Saint John, NB',
    'Saint John, NB',
    'Brantford, ON',
    'Red Deer, AB',
    'Nanaimo, BC',
    'Lethbridge, AB',
    'White Rock, BC',
    'Peterborough, ON',
    'Sarnia, ON',
    'Milton, ON',
    'Kamloops, BC',
    'Chateauguay, QC',
    'Sault Ste. Marie, ON',
    'Chilliwack, BC',
    'Drummondville, QC',
    'Saint-Jerome, QC',
    'Medicine Hat, AB',
    'Prince George, BC',
    'Belleville, ON',
    'Fredericton, NB',
    'Fort McMurray, AB',
    'Granby, QC',
    'Grande Prairie, AB',
    'North Bay, ON',
    'Beloeil, QC',
    'Cornwall, ON',
    'Saint-Hyacinthe, QC',
    'Shawinigan, QC',
    'Brandon, MB',
    'Vernon, BC',
    'Chatham, ON',
    'Joliette, QC',
    'Charlottetown, PE',
    'Airdrie, AB',
    'Victoriaville, QC',
    'St. Thomas, ON',
    'Courtenay, BC',
    'Georgetown, ON',
    'Rimouski, QC',
    'Woodstock, ON',
    'Sorel-Tracy, QC',
    'Penticton, BC',
    'Prince Albert, SK',
    'Campbell River, BC',
    'Moose Jaw, SK',
    'Cape Breton-Sydney, NS',
    'Midland, ON',
    'Leamington, ON',
    'Stratford, ON',
    'Orangeville, ON',
    'Timmins, ON',
    'Orillia, ON',
    'Walnut Grove, BC',
    'Spruce Grove, AB',
    'Lloydminster, AB',
    'Lloydminster, SK',
    'Alma, QC',
    'Bolton, ON',
    'Saint-Georges, QC',
    'Stouffville, ON',
    'Okotoks, AB',
    'Duncan, BC',
    'Parksville, BC',
    'Leduc, AB',
    "Val-d'Or, QC",
    'Rouyn-Noranda, QC',
    'Buckingham, QC'
]

# Damage type class
# defines types of tank damage that can possibly be repaired by a crewman, or damage that
#  can result from a failed repair attempt
class Damage:
    def __init__(self, name, order, repair_score, break_score, break_result, auto_repair):
        self.name = name            # identifying name of the damage
        self.order = order            # order required to repair ('' if NA)
        self.repair_score = repair_score    # score required to repair (0 if NA)
        self.break_score = break_score        # minimum roll to break (0 if NA)
        self.break_result = break_result    # new damage type to apply if broken ('' if NA)
        self.auto_repair = auto_repair        # automatically repaired after an
                            #  encounter unless break score rolled

DAMAGE_TYPES = []
DAMAGE_TYPES.append(Damage('Main Gun Malfunction', 'Repair Main Gun', 4, 11, 'Main Gun Broken', True))
DAMAGE_TYPES.append(Damage('Main Gun Broken', '', 0, 0, '', False))
DAMAGE_TYPES.append(Damage('Gun Sight Broken', '', 0, 0, '', False))
DAMAGE_TYPES.append(Damage('Engine Knocked Out', '', 0, 0, '', False))
DAMAGE_TYPES.append(Damage('Turret Traverse Malfunction', 'Repair Turret Traverse', 4, 0, 'Turret Traverse Broken', True))
DAMAGE_TYPES.append(Damage('Turret Traverse Broken', '', 0, 0, '', False))
DAMAGE_TYPES.append(Damage('Radio Malfunction', 'Repair Radio', 6, 12, 'Radio Broken', True))
DAMAGE_TYPES.append(Damage('Radio Broken', '', 0, 0, '', False))
DAMAGE_TYPES.append(Damage('Intercom Malfunction', 'Repair Intercom', 8, 12, 'Intercom Broken', True))
DAMAGE_TYPES.append(Damage('Intercom Broken', '', 0, 0, '', False))
DAMAGE_TYPES.append(Damage('AA MG Malfunction', 'Repair AA MG', 8, 12, 'AA MG Broken', True))
DAMAGE_TYPES.append(Damage('AA MG Broken', '', 0, 0, '', False))
DAMAGE_TYPES.append(Damage('Co-ax MG Malfunction', 'Repair Co-ax MG', 8, 12, 'Co-ax MG Broken', True))
DAMAGE_TYPES.append(Damage('Co-ax MG Broken', '', 0, 0, '', False))
DAMAGE_TYPES.append(Damage('Bow MG Malfunction', 'Repair Bow MG', 8, 12, 'Bow MG Broken', True))
DAMAGE_TYPES.append(Damage('Bow MG Broken', '', 0, 0, '', False))


# return a pointer to a given damage type
def GetDamageType(name):
    for d in DAMAGE_TYPES:
        if d.name == name: return d
    return None

# types of damage that allow us to choose to head back to HQ
ENDING_DAMAGES = ['Gun Sight Broken', 'Main Gun Broken', 'Turret Traverse Broken']



HELP_TEXT = [
    ('AP', """\
AP refers to an Armour-piercing gun shell. As the shell is designed to punch through armour,
it has a minimal explosive charge and thus will do no significant damage to infantry units,
including AT guns. Only Direct Fire mode can be used with this type of shell. Enemy tanks,
SPGs, and AT guns will always use AP fire against you and friendly armour.
"""),
    ('HVAP', """\
High velocity Armour-piercing gun shell. Produced for the 76mm guns on American tank
destroyers, they consist of a dense tungsten carbine core surrounded by an aluminium casing.
The shell was able to penetrate armour at much further ranges than the standard 76mm AP
shell. They were normally only issued to Tank Destroyers. Their use by M4 Sherman crews in
this and other simulations is not supported by historical evidence, but rather represents
a few shells 'appropriated' from supplies.
"""),
    ('APDS', """\
Armour-Piercing Discarding Sabot gun shell. A type of shell with a dense core surrounded by
pedal-shaped sabots that separate from the core in flight. Very effective against armour.
APDS rounds in British and Commonwealth forces were rare up to late 1944.
"""),
    ('HE', """\
HE refers to a High-explosive gun shell. These shells are designed for use against lightly
or unarmoured vehicles, gun teams, and other infantry. Fully armoured vehicles will normally
only be damaged by HE in the case of a Critical Hit. HE can be fired in either Direct or Area
fire mode. En route to your starting location, you will use a random number of HE shells
suppressing infantry attacks. You can also use HE as advancing fire when moving into an
enemy-held area.
"""),
    ('WP', """\
WP refers to a White Phosphorus smoke-producing shell. WP burns quickly producing a blanket of
smoke. They are harmful to anyone nearby, and thus are only used against enemy positions. WP
must be fired in Area Fire mode. A successful hit with WP produces 1 Smoke Factor in the target's
hex. Infantry units hit by a WP must pass a Pin test or be pinned.
"""),
    ('HCBI', """\
HCBI refers to a Hexachlorothane-Base Initiating smoke-producing shell. HCBI produces a great deal
of smoke, with the benefit of being safe to use near friendly forces. Only a limited number
of HCBI shells are available each day. HCBI must be fired in Area Fire mode. A successful hit
with HCBI produces 2 Smoke Factors in the target's hex.
"""),
    ('M4 Sherman', """\
A medium tank produced by the United States and in service from 1942 to 1955 in the American
armed forces. There were over a dozen variants of this tank produced, plus other vehicles that
were built on its chassis or hull. The original M4 was intended for infantry support and mobile
attack, and was vastly outclassed by most other medium and heavy German tanks in the later part
of the war.
"""),
    ('Hidden', """\
Hidden units are enemy units that you know are in the area, but to which you do not have a direct
line of sight. Hidden units cannot be targeted by your tank, but nor can they initiate attacks
against you. Units remain hidden until either they or you change their position; no spotting checks
can reveal them unless one of you moves.
"""),
    ('Unspotted', """\
Unspotted units are enemy units that have been reported by friendly observers but which have not yet
been spotted by the crew of your tank. Unspotted units can attack you and friendly units, but you
cannot attack them until they are spotted.
"""),
    ('Unidentified', """\
Unidentified units have been spotted by the crew of your tank, but you do not yet know what specific
type of tank, self-propelled gun, or AT gun they are until they are Identified. Unidentified units
attack and can be targeted as normal, but you do not know how powerful your enemy is until you
can successfully identify it.
"""),
    ('Call Artillery', """\
Call Artillery is an action used on an adjacent enemy-controlled area in the campaign day map. If
successful, an artillery strike is called in on the map area. The action takes 15 mins. of
time. The chance of success depends on your current artillery chance, which decreases by one
each time a strike is successfully called in.
"""),
    ('Hull Down', """\
A vehicle that is Hull Down has its hull hidden behind something that will absorb incoming
fire, such as a hill or stone wall. Targets that are Hull Down are not affected by hits
that would normally affect the hull, and are thus much harder to hit effectively. If your
tank is Hull Down, you cannot fire the Hull MG. Hull Down is lost if your tank moves, and may
be lost if your tank pivots, and if lost must be regained via the appropriate order to the Driver.
"""),
    ('Rate of Fire', """\
Rate of Fire (RoF) means that the Gunner and Loader have worked quickly enough to fire off
multiple shells at the same target in quick succession in the same turn. In order to maintain RoF,
you must
reload a shell into the main gun, and the shell must be compatible with the current target
type. So if you fire an AP shell in Direct Fire and reload a WP shell, you cannot maintain
RoF since WP must be fired in Area Fire mode. The Gunner's and Loader's skills can improve
the chance of maintaining RoF. If you are reloading from the Ready Rack then the chance is
greatly increased; otherwise, if the Assistant Driver is on Pass Ammo orders, then he will
increase the chance of maintaining RoF. You don't have to use the extra shot;
press [End] or [Space] instead to progress to the next phase.
"""),
    ('VP', """\
VP refers to Victory Points. You are awarded VP for capturing areas on the campaign day map,
and for your tank destroying units during an Encounter. Your final VP indicates how
successful your campaign has been.
"""),
    ('Armour', """\
All vehicles in the game are protected by some level of armour. When determining if a hit
on a unit destroys it or not, the armour value of the hit location is used to calculate
the odds of penetrating the armour and destroying the unit. Vehicles can have up to four
different armour values: one each for the turret front and sides, and one each for the hull
front and sides. Armour on the rear of the vehicle is always one level lower than the
side of the same location. Armour levels progress as follows: 0, 1, 2, 3, 4, 6, 8, 11,
14, 18, and 26.
"""),
    ('Advance Mission', """\
In an Advance mission your task is to move through the map, capturing areas and destroying
any enemy resistance you encounter. If you can capture your exit area before nightfall you
will be awarded bonus Victory Points and will have the opportunity to continue advancing
into a new map zone.
"""),
    ('Battle Mission', """\
In a Battle mission your task is to move through the map and capture enemy-controlled
areas, but the resistance you meet will be much stronger, better prepared, and better
fortified than in an Advance mission. Considering making full use of artillery and air
support, as well as advancing fire. Capturing your exit area awards you bonus VP as
normal.
"""),
    ('Counterattack Mission', """\
A Counterattack is quite different from an Advance or Battle mission. Since the enemy is
advancing on you, you begin at the top of the map and the enemy comes to you. If your map
area is surrounded by enemy-controlled areas, your battlegroup must move to rejoin your
battle line. Once an encounter begins you always begin Stopped and Hull Down, and
have a chance to ambush the enemy and attack first. Victory Points are only awarded for
destroying enemy units.
"""),
    ('Direct Fire', """\
In this firing mode you aim the shot directly at the enemy target. The to-hit roll is
affected by range, smoke, terrain, etc. modifiers. Must be used with AP, HVAP, and APDS;
may be used with HE; may not be used with WP and HCBI ammo.
"""),
    ('Area Fire', """\
In this firing mode you aim the shot toward the general location of the enemy target. The
to-hit roll has no modifier for terrain, but any terrain modifier will be applied to any
subsequent to-kill roll. This makes it easier to hit with smoke rounds, and gives a greater
chance of pinning a target infantry unit when a direct hit would be unlikely.
May be used with HE; may not be used with AP, HVAP, and APDS; must be used with WP and HCBI.
"""),
    ('Skill Activations', """\
Crew skills are automatically tested for activation every time they have the possibility of
being activated. For example, a skill that affects firing with the main gun will be checked
every time the main gun is fired.
""")
]

# data to display title screen
TITLE = [
        [1,6,2,6,3,3,3,3,2,6,2,3,2,3,1,6,3,6,1,6],
        [0,8,1,7,2,4,1,4,1,8,1,3,2,3,1,7,2,6,1,7],
        [0,8,1,8,1,9,1,8,1,3,2,3,1,8,1,6,1,8],
        [0,3,2,3,1,3,2,3,1,9,1,3,2,3,1,3,2,3,1,3,2,3,1,3,4,3,2,3],
        [0,3,2,3,1,3,2,3,1,3,1,1,1,3,1,3,2,3,1,3,2,3,1,3,2,3,1,3,4,3,2,3],
        [0,3,2,3,1,3,2,2,2,3,3,3,1,3,2,3,1,3,2,3,1,3,2,2,2,4,3,3,2,3],
        [0,8,1,6,3,3,3,3,1,3,2,3,1,3,2,3,1,6,3,4,3,3,2,3],
        [0,3,2,3,1,3,2,2,2,3,3,3,1,3,2,3,1,3,2,3,1,3,2,2,2,3,4,3,2,3],
        [0,3,2,3,1,3,2,3,1,3,3,3,1,3,2,3,1,3,2,3,1,3,2,3,1,3,4,3,2,3],
        [0,3,2,3,1,3,2,3,1,3,3,3,1,8,1,8,1,3,2,3,1,6,1,8],
        [0,3,2,3,1,3,2,3,1,3,3,3,1,8,1,8,1,3,2,3,1,6,1,7],
        [0,3,2,3,1,3,2,3,1,3,3,3,2,6,3,6,2,3,2,3,1,6,1,6],
        [0],
        [1,7,2,6,2,3,3,3,1,3,3,3,2,6,2,3,2,3,1,6,3,6,1,6],
        [0,8,1,8,1,4,1,4,1,4,1,4,1,8,1,3,2,3,1,7,2,6,1,7],
        [0,8,1,8,1,9,1,9,1,8,1,3,2,3,1,8,1,6,1,8],
        [0,3,6,3,2,3,1,9,1,9,1,3,2,3,1,4,1,3,1,3,2,3,1,3,4,3,2,3],
        [0,3,6,3,2,3,1,3,1,1,1,3,1,3,1,1,1,3,1,3,2,3,1,8,1,3,2,3,1,3,4,3,2,3],
        [0,3,6,3,2,3,1,3,3,3,1,3,3,3,1,3,2,3,1,8,1,3,2,3,1,4,3,3,2,2],
        [0,3,6,3,2,3,1,3,3,3,1,3,3,3,1,8,1,8,1,3,2,3,1,4,3,6],
        [0,3,6,3,2,3,1,3,3,3,1,3,3,3,1,3,2,3,1,3,1,4,1,3,2,3,1,3,4,3,2,2],
        [0,3,6,3,2,3,1,3,3,3,1,3,3,3,1,3,2,3,1,3,2,3,1,3,2,3,1,3,4,3,2,3],
        [0,8,1,8,1,3,3,3,1,3,3,3,1,3,2,3,1,3,2,3,1,8,1,6,1,3,2,3],
        [0,8,1,8,1,3,3,3,1,3,3,3,1,3,2,3,1,3,2,3,1,7,2,6,1,3,2,3],
        [1,7,2,6,2,3,3,3,1,3,3,3,1,3,2,3,1,3,2,3,1,6,3,6,1,3,2,3]
    ]

# Tutorial Text
TUTORIAL_TEXT = {
    'welcome': """\
Welcome to Armoured Commander! Since this is your first time playing (or you deleted your
bones file) messages such as these will pop up from time to time to help get you started.
If you'd rather play without them, simply toggle them off in the Settings menu.""",
    'advance_mission': """\
In an Advance mission your task is to move through the map, capturing areas
and destroying any enemy resistance you encounter. If you can capture your
exit area before nightfall you will be awarded bonus Victory Points and will
have the opportunity to continue advancing into a new map zone.""",
    'battle_mission': """\
In a Battle mission your task is to move through the map and capture enemy-controlled
areas, but the resistance you meet will be much stronger, better prepared, and better
fortified than in an Advance mission. Considering making full use of artillery and
air support, as well as advancing fire. Capturing your exit area awards you bonus VP as
normal.""",
    'counterattack_mission': """\
A Counterattack is quite different from an Advance or Battle mission. Since the
enemy is advancing on you, you do not move your battlegroup around the map. Instead, you
remain in place and await for the enemy to come to you. Between encounters you always
have the chance to resupply. Once an encounter begins you always begin Stopped and Hull
Down, and have a chance to ambush the enemy and attack first. Victory Points are only
awarded for destroying enemy units."""
}

# credits text
CREDITS_TEXT = [
    '*** Armoured Commander ***',
    '',
    '',
    'The World War II Tank Commander Roguelike',
    '',
    '',
    'Designed and Programmed by',
    'Gregory Adam Scott',
    '',
    'Maintained by Eric Normandeau',
    'since version 1.04',
    '',
    '',
    '* Inspired By *',
    'Advanced Squad Leader by Don Greenwood, 1985',
    "Patton's Best by Bruce Shelley, 1987",
    'Flames of War by Phil Yates, 2002',
    '',
    '',
    '* Resources Used *',
    '/r/roguelikedev',
    'Temple of the Roguelike',
    'Roguebasin',
    'The Doryen Library (libtcod)',
    '',
    '',
    '* Special Thanks To *',
    'Josh Ge, Grid Sage Games',
    'Galaga Galaxian',
    'Zomb Lee Youtube channel',
    "Dimosa, Dimosa's Quest Youtube channel",
    "Tim Stone, Rock Paper Shotgun's The Flare Path",
    'Aresbece',
    'Joe Carstensen'

]
