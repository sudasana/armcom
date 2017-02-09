# -*- coding: UTF-8 -*-

# Vehicle Type Definitions for Armoured Commander

##########################################################################################
#
#    Copyright 2015 Gregory Adam Scott (sudasana@gmail.com)
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

# New Rarity Factor system, intended to work with any list of vehicle types:
# (2.0 - ASL Model RF) * 100 * (portion)

# 6 vs 14

# first item in the list is always a string unique to the vehicle type and sub-type
# used for identifying the correct entry

VEHICLE_TYPES = [
	
	# American Tanks
	
	# M4 Sherman, Turret A
	['M4 Turret A',
	('vehicle_type', 'M4 Sherman'),
	('sub_type', 'Turret A'),
	('overhead_view', 'm4_a.xp'),
	('vehicle_class', 'Medium Tank'),
	('target_size', 'Large'),
	('main_gun', '75'),
	('co_ax_mg', 4),
	('bow_mg', 2),
	('aa_mg', 4),
	('hull_front_armour', 8),
	('hull_side_armour', 4),
	('turret_front_armour', 8),
	('turret_side_armour', 6),
	('main_gun_rounds', 89),
	('rr_size', 8),
	('rof_num', 5),
	('loader_hatch', 'None'),
	('rarity', [6,5,3,1,1,1,1,1,1]),
	('info_text', 'The M4 was one of the first Sherman variants to be approved, ' +
		'distinguished from the M4A1 by its welded hull. This early turret design lacks ' +
		'a loader hatch, smoke mortar, and vision cupola, features that ' +
		'were later added or refitted to most models.')],
	
	# M4 Sherman, Turret B
	['M4 Turret B',
	('vehicle_type', 'M4 Sherman'),
	('sub_type', 'Turret B'),
	('overhead_view', 'm4_b.xp'),
	('vehicle_class', 'Medium Tank'),
	('target_size', 'Large'),
	('main_gun', '75'),
	('co_ax_mg', 4),
	('bow_mg', 2),
	('aa_mg', 4),
	('hull_front_armour', 8),
	('hull_side_armour', 4),
	('turret_front_armour', 8),
	('turret_side_armour', 6),
	('main_gun_rounds', 89),
	('rr_size', 8),
	('rof_num', 5),
	('loader_hatch', 'Oval'),
	('smoke_mortar', ''),
	('rarity', [14,10,7,3,3,2,1,1,1]),
	('info_text', 'Based on combat experience, the M4 was enhanced with a smoke ' +
		"mortar starting from June 1943, and a hatch over the loader's " +
		'position starting from December 1943.')],
	
	# M4 Sherman, Turret C
	['M4 Turret C',
	('vehicle_type', 'M4 Sherman'),
	('sub_type', 'Turret C'),
	('overhead_view', 'm4_c.xp'),
	('vehicle_class', 'Medium Tank'),
	('target_size', 'Large'),
	('main_gun', '75'),
	('co_ax_mg', 4),
	('bow_mg', 2),
	('aa_mg', 4),
	('hull_front_armour', 8),
	('hull_side_armour', 4),
	('turret_front_armour', 8),
	('turret_side_armour', 6),
	('main_gun_rounds', 89),
	('rr_size', 8),
	('rof_num', 5),
	('loader_hatch', 'Oval'),
	('vision_cupola', ''),
	('smoke_mortar', ''),
	('rarity', [0,0,0,1,1,1,1,1,1]),
	('info_text', "This represents an M4 produced with a smoke mortar and loader's " +
		"hatch, with the commander's hatch enhanced by a vision cupola, perhaps " +
		'retrofitted in the field.')],
	
	# M4A1 Sherman, Turret A
	['M4A1 Turret A',
	('vehicle_type', 'M4A1 Sherman'),
	('sub_type', 'Turret A'),
	('overhead_view', 'm4_a1_a.xp'),
	('vehicle_class', 'Medium Tank'),
	('target_size', 'Large'),
	('main_gun', '75'),
	('co_ax_mg', 4),
	('bow_mg', 2),
	('aa_mg', 4),
	('hull_front_armour', 11),
	('hull_side_armour', 4),
	('turret_front_armour', 8),
	('turret_side_armour', 6),
	('main_gun_rounds', 83),
	('rr_size', 8),
	('rof_num', 5),
	('loader_hatch', 'None'),
	('rarity', [7,6,5,2,1,1,1,1,1]),
	('info_text', 'The M4A1 was the first variant of Sherman tank to be produced, ' +
		'and is distinguished by its cast hull. This early turret design lacks ' +
		'a loader hatch, smoke mortar, and vision cupola, features that ' +
		'were later added or refitted to most models.')],
	
	# M4A1 Sherman, Turret B
	['M4A1 Turret B',
	('vehicle_type', 'M4A1 Sherman'),
	('sub_type', 'Turret B'),
	('overhead_view', 'm4_a1_b.xp'),
	('vehicle_class', 'Medium Tank'),
	('target_size', 'Large'),
	('main_gun', '75'),
	('co_ax_mg', 4),
	('bow_mg', 2),
	('aa_mg', 4),
	('hull_front_armour', 11),
	('hull_side_armour', 4),
	('turret_front_armour', 8),
	('turret_side_armour', 6),
	('main_gun_rounds', 83),
	('rr_size', 8),
	('rof_num', 5),
	('loader_hatch', 'Oval'),
	('smoke_mortar', ''),
	('rarity', [18,14,10,7,3,3,2,1,1]),
	('info_text', 'This represents either a later M4A1 built with an oval loader ' +
		'hatch, or an earlier model that had a loader hatch field-fitted.')],
	
	# M4A1 Sherman, Turret C
	['M4A1 Turret C',
	('vehicle_type', 'M4A1 Sherman'),
	('sub_type', 'Turret C'),
	('overhead_view', 'm4_a1_c.xp'),
	('vehicle_class', 'Medium Tank'),
	('target_size', 'Large'),
	('main_gun', '75'),
	('co_ax_mg', 4),
	('bow_mg', 2),
	('aa_mg', 4),
	('hull_front_armour', 11),
	('hull_side_armour', 4),
	('turret_front_armour', 8),
	('turret_side_armour', 6),
	('main_gun_rounds', 83),
	('rr_size', 8),
	('rof_num', 5),
	('loader_hatch', 'Oval'),
	('vision_cupola', ''),
	('smoke_mortar', ''),
	('rarity', [0,0,0,1,1,1,1,1,1]),
	('info_text', 'This is an M4A1 fitted with an oval loader hatch, a vision cupola ' +
		"for the commander's hatch, and a smoke mortar for the loader.")],
	
	# M4A3 Sherman, Turret A
	['M4A3 Turret A',
	('vehicle_type', 'M4A3 Sherman'),
	('sub_type', 'Turret A'),
	('overhead_view', 'm4_a3_a.xp'),
	('vehicle_class', 'Medium Tank'),
	('target_size', 'Large'),
	('main_gun', '75'),
	('co_ax_mg', 4),
	('bow_mg', 2),
	('aa_mg', 4),
	('hull_front_armour', 8),
	('hull_side_armour', 4),
	('turret_front_armour', 8),
	('turret_side_armour', 6),
	('main_gun_rounds', 89),
	('rr_size', 8),
	('rof_num', 5),
	('loader_hatch', 'None'),
	('rarity', [2,2,2,1,1,1,1,1,1]),
	('info_text', 'The M4A3 was the third variant of Sherman tank, similar to the ' +
		'M4 but powered by a Ford V-8 engine. This early turret design lacks ' +
		'a loader hatch, smoke mortar, and vision cupola, features that ' +
		'were later added or refitted to most models.')],
	
	# M4A3 Sherman, Turret B
	['M4A3 Turret B',
	('vehicle_type', 'M4A3 Sherman'),
	('sub_type', 'Turret B'),
	('overhead_view', 'm4_a3_b.xp'),
	('vehicle_class', 'Medium Tank'),
	('target_size', 'Large'),
	('main_gun', '75'),
	('co_ax_mg', 4),
	('bow_mg', 2),
	('aa_mg', 4),
	('hull_front_armour', 8),
	('hull_side_armour', 4),
	('turret_front_armour', 8),
	('turret_side_armour', 6),
	('main_gun_rounds', 89),
	('rr_size', 8),
	('rof_num', 5),
	('loader_hatch', 'Oval'),
	('smoke_mortar', ''),
	('rarity', [2,2,3,2,2,2,3,2,1]),
	('info_text', 'This represents an M4A3 with an oval loader hatch and a smoke ' +
		'mortar.')],
	
	# M4A3 Sherman, Turret C
	['M4A3 Turret C',
	('vehicle_type', 'M4A3 Sherman'),
	('sub_type', 'Turret C'),
	('overhead_view', 'm4_a3_c.xp'),
	('vehicle_class', 'Medium Tank'),
	('target_size', 'Large'),
	('main_gun', '75'),
	('co_ax_mg', 4),
	('bow_mg', 2),
	('aa_mg', 4),
	('hull_front_armour', 8),
	('hull_side_armour', 4),
	('turret_front_armour', 8),
	('turret_side_armour', 6),
	('main_gun_rounds', 89),
	('rr_size', 8),
	('rof_num', 5),
	('loader_hatch', 'Oval'),
	('vision_cupola', ''),
	('smoke_mortar', ''),
	('rarity', [0,0,0,1,1,1,1,1,1]),
	('info_text', 'This represents an M4A3 fitted with an oval loader hatch, a ' +
		"commander's vision cupola, and a smoke mortar.")],
	
	# M4A3(75)W Sherman, Turret D
	['M4A3(75)W Turret D',
	('vehicle_type', 'M4A3(75)W Sherman'),
	('sub_type', 'Turret D'),
	('overhead_view', 'm4_a3_75_d.xp'),
	('vehicle_class', 'Medium Tank'),
	('target_size', 'Large'),
	('main_gun', '75'),
	('co_ax_mg', 4),
	('bow_mg', 2),
	('aa_mg', 4),
	('hull_front_armour', 11),
	('hull_side_armour', 4),
	('turret_front_armour', 8),
	('turret_side_armour', 6),
	('main_gun_rounds', 100),
	('rr_size', 4),
	('rof_num', 5),
	('loader_hatch', 'Oval'),
	('smoke_mortar', ''),
	('wet_stowage', ''),
	('rarity', [20,18,19,21,19,16,12,10,6]),
	('info_text', 'The M4A3(75) W was a later modification of the M4A3 design, ' +
		'with a thicker, single-piece front hull armour sheet. W indicates ' +
		'wet stowage, meaning that ammunition is stored surrounded by liquid ' +
		'to prevent fires. This turret design has an oval loader hatch and ' +
		'a smoke mortar.')],
	
	# M4A3(75)W Sherman, Turret E
	['M4A3(75)W Turret E',
	('vehicle_type', 'M4A3(75)W Sherman'),
	('sub_type', 'Turret E'),
	('overhead_view', 'm4_a3_75_e.xp'),
	('vehicle_class', 'Medium Tank'),
	('target_size', 'Large'),
	('main_gun', '75'),
	('co_ax_mg', 4),
	('bow_mg', 2),
	('aa_mg', 4),
	('hull_front_armour', 11),
	('hull_side_armour', 4),
	('turret_front_armour', 8),
	('turret_side_armour', 6),
	('main_gun_rounds', 100),
	('rr_size', 4),
	('rof_num', 5),
	('loader_hatch', 'Oval'),
	('vision_cupola', ''),
	('smoke_mortar', ''),
	('wet_stowage', ''),
	('HVSS', 3),
	('rarity', [0,1,5,9,13,16,19,24,28]),
	('info_text', "This is an M4A3(75) W with a commander's vision cupola and " +
		'possible Horizontal Volute Spring Suspension.')],
	
	# M4A3E2(75)W Sherman, Turret F
	['M4A3E2(75)W Turret F',
	('vehicle_type', 'M4A3E2(75)W Sherman'),
	('sub_type', 'Turret F'),
	('overhead_view', 'm4_a3_e2_75_f.xp'),
	('vehicle_class', 'Medium Tank'),
	('nickname', 'Jumbo'),
	('target_size', 'Large'),
	('main_gun', '75'),
	('co_ax_mg', 4),
	('bow_mg', 2),
	('aa_mg', 4),
	('hull_front_armour', 18),
	('hull_side_armour', 8),
	('turret_front_armour', 18),
	('turret_side_armour', 11),
	('main_gun_rounds', 100),
	('rr_size', 4),
	('rof_num', 5),
	('loader_hatch', 'Oval'),
	('smoke_mortar', ''),
	('vision_cupola', ''),
	('wet_stowage', ''),
	('duckbills', ''),
	('rarity', [0,5,5,5,5,5,5,5,5]),
	('info_text', 'The "Jumbo" was an attempt to build an assault tank that could ' +
		'stand up to heavy German anti-tank weapons. Extra armour plating was ' +
		'welded on to an M4A3, at the expense of speed. The "Jumbo" was also ' +
		'fitted with extended "Duckbill" tracks, which sacrificed speed for ' +
		'traction and reliability.')],
	
	# M4A3E2(76)W Sherman, Turret F
	['M4A3E2(76)W Turret F',
	('vehicle_type', 'M4A3E2(76)W Sherman'),
	('sub_type', 'Turret F'),
	('overhead_view', 'm4_a3_e2_76_f.xp'),
	('vehicle_class', 'Medium Tank'),
	('nickname', 'Jumbo'),
	('target_size', 'Large'),
	('main_gun', '76L'),
	('co_ax_mg', 4),
	('bow_mg', 2),
	('aa_mg', 4),
	('hull_front_armour', 18),
	('hull_side_armour', 8),
	('turret_front_armour', 18),
	('turret_side_armour', 11),
	('main_gun_rounds', 65),
	('rr_size', 6),
	('rof_num', 4),
	('loader_hatch', 'Oval'),
	('vision_cupola', ''),
	('smoke_mortar', ''),
	('wet_stowage', ''),
	('duckbills', ''),
	('rarity', [0,0,1,1,1,1,1,1,1]),
	('info_text', 'A few "Jumbo" Shermans were fitted with a 76mm gun, but these were ' +
		'exceedingly rare.')],
	
	# M4A1(76)W Sherman, Turret G
	['M4A1(76)W Turret G',
	('vehicle_type', 'M4A1(76)W Sherman'),
	('sub_type', 'Turret G'),
	('overhead_view', 'm4_a1_76_g.xp'),
	('vehicle_class', 'Medium Tank'),
	('target_size', 'Large'),
	('main_gun', '76L'),
	('co_ax_mg', 4),
	('bow_mg', 2),
	('aa_mg', 4),
	('hull_front_armour', 11),
	('hull_side_armour', 4),
	('turret_front_armour', 8),
	('turret_side_armour', 6),
	('main_gun_rounds', 65),
	('rr_size', 6),
	('rof_num', 4),
	('loader_hatch', 'Split'),
	('loader_aa_mg', ''),
	('vision_cupola', ''),
	('smoke_mortar', ''),
	('wet_stowage', ''),
	('HVSS', 5),
	('rarity', [10,10,15,14,12,10,9,7,5]),
	('info_text', 'This represents an M4A1 upgraded with a 76mm gun. Because the ' +
		'loader hatch is a split type, the loader cannot fire the AA MG.')],
	
	# M4A1(76)W Sherman, Turret H
	['M4A1(76)W Turret H',
	('vehicle_type', 'M4A1(76)W Sherman'),
	('sub_type', 'Turret H'),
	('overhead_view', 'm4_a1_76_h.xp'),
	('vehicle_class', 'Medium Tank'),
	('target_size', 'Large'),
	('main_gun', '76L'),
	('co_ax_mg', 4),
	('bow_mg', 2),
	('aa_mg', 4),
	('hull_front_armour', 11),
	('hull_side_armour', 4),
	('turret_front_armour', 8),
	('turret_side_armour', 6),
	('main_gun_rounds', 65),
	('rr_size', 6),
	('rof_num', 4),
	('loader_hatch', 'Oval'),
	('vision_cupola', ''),
	('smoke_mortar', ''),
	('wet_stowage', ''),
	('HVSS', 5),
	('rarity', [0,0,0,1,3,5,6,7,9]),
	('info_text', 'This represents an M4A1 upgraded with a 76mm gun, and fitted with ' +
		'an oval loader hatch.')],
	
	# M4A3(76)W Sherman, Turret G
	['M4A3(76)W Turret G',
	('vehicle_type', 'M4A3(76)W Sherman'),
	('sub_type', 'Turret G'),
	('overhead_view', 'm4_a3_76_g.xp'),
	('vehicle_class', 'Medium Tank'),
	('nickname', 'Easy Eight'),
	('target_size', 'Large'),
	('main_gun', '76L'),
	('co_ax_mg', 4),
	('bow_mg', 2),
	('aa_mg', 4),
	('hull_front_armour', 11),
	('hull_side_armour', 4),
	('turret_front_armour', 8),
	('turret_side_armour', 6),
	('main_gun_rounds', 65),
	('rr_size', 6),
	('rof_num', 4),
	('loader_hatch', 'Split'),
	('loader_aa_mg', ''),
	('vision_cupola', ''),
	('smoke_mortar', ''),
	('wet_stowage', ''),
	('HVSS', 5),
	('rarity', [20,25,25,25,26,23,21,18,15]),
	('info_text', 'The "Easy Eight" is an M4A3 upgraded with a 76mm gun and often ' +
		'has Horizontal Volute Spring Suspension has well. The combination of ' +
		'speed, firepower, and reliability made this one of the most effective ' +
		'models of Sherman tank in the war.')],
	
	# M4A3(76)W Sherman, Turret H
	['M4A3(76)W Turret H',
	('vehicle_type', 'M4A3(76)W Sherman'),
	('sub_type', 'Turret H'),
	('overhead_view', 'm4_a3_76_h.xp'),
	('vehicle_class', 'Medium Tank'),
	('nickname', 'Easy Eight'),
	('target_size', 'Large'),
	('main_gun', '76L'),
	('co_ax_mg', 4),
	('bow_mg', 2),
	('aa_mg', 4),
	('hull_front_armour', 11),
	('hull_side_armour', 4),
	('turret_front_armour', 8),
	('turret_side_armour', 6),
	('main_gun_rounds', 65),
	('rr_size', 6),
	('rof_num', 4),
	('loader_hatch', 'Oval'),
	('vision_cupola', ''),
	('smoke_mortar', ''),
	('wet_stowage', ''),
	('HVSS', 5),
	('rarity', [0,0,0,3,6,10,14,18,21]),
	('info_text', 'An "Easy Eight" with an oval loader hatch.')],
	
	# British and Commonwealth Tanks
	
	# Sherman II (M4A1)
	['Sherman II',
	('vehicle_type', 'Sherman II'),
	('overhead_view', 'm4_a1_a.xp'),
	('vehicle_class', 'Medium Tank'),
	('target_size', 'Large'),
	('main_gun', '75'),
	('co_ax_mg', 4),
	('bow_mg', 2),
	('hull_front_armour', 11),
	('hull_side_armour', 4),
	('turret_front_armour', 8),
	('turret_side_armour', 6),
	('main_gun_rounds', 83),
	('rr_size', 8),
	('rof_num', 5),
	('smoke_mortar', ''),
	('loader_hatch', 'None'),
	('rarity', [2,2,2,2,2,2,2,2,2]),
	('info_text', 'The Sherman II was the British and Commonwealth designation for ' +
		'the M4A1. This version has a smoke mortar but no loader hatch.')],
	
	# Sherman V (M4A4)
	['Sherman V',
	('vehicle_type', 'Sherman V'),
	('overhead_view', 'm4_a3_a.xp'),
	('vehicle_class', 'Medium Tank'),
	('target_size', 'Large'),
	('main_gun', '75'),
	('co_ax_mg', 4),
	('bow_mg', 2),
	('hull_front_armour', 8),
	('hull_side_armour', 4),
	('turret_front_armour', 8),
	('turret_side_armour', 6),
	('main_gun_rounds', 89),
	('rr_size', 8),
	('rof_num', 5),
	('smoke_mortar', ''),
	('loader_hatch', 'None'),
	('rarity', [2,2,2,2,2,2,2,2,2]),
	('info_text', 'The Sherman V was the British and Commonwealth designation for ' +
		'the M4A4.')],
	
	# Firefly (M4A4)
	['Sherman VC Firefly',
	('vehicle_type', 'Sherman VC'),
	('overhead_view', 'm4_vc.xp'),
	('sub_type', 'Firefly'),
	('vehicle_class', 'Medium Tank'),
	('target_size', 'Large'),
	('main_gun', '76LL'),
	('co_ax_mg', 4),
	('hull_front_armour', 8),
	('hull_side_armour', 4),
	('turret_front_armour', 8),
	('turret_side_armour', 6),
	('main_gun_rounds', 73),
	('rr_size', 5),
	('rof_num', 3),
	('smoke_mortar', ''),
	('no_asst_driver', ''),
	('loader_hatch', 'Oval'),
	('rarity', [1,1,1,1,1,2,2,2,2]),
	('info_text', 'The Sherman VC (Firefly) was a Sherman V fitted with a 17-pounder ' +
		'main gun, intended to defeat German heavy armour. To leave room to store ' +
		'the larger main gun ammunition, the assistant driver position and the ' +
		'bow MG were both removed. Unlike the standard Sherman V it does have a ' +
		'loader hatch in the turret.')],
	
	
	# German Tanks
	
	# PzKw IV H (or J)
	['PzKw IV H',
	('vehicle_type', 'PzKw IV'),
	('sub_type', 'H'),
	('vehicle_class', 'Medium Tank'),
	('target_size', 'Medium'),
	('main_gun', '75L'),
	('hull_front_armour', 8),
	('hull_side_armour', 3),
	('turret_front_armour', 6),
	('turret_side_armour', 4),
	('turret_traverse', 'Fast'),
	('info_text', 'Panzer IV Tank. A medium tank armed with a 75L main gun. Roughly ' +
		'equivalent to an M4 Sherman but with a better long range attack and ' +
		'lighter side and turret armour.')],
	
	# PzKw V G, Panther
	['PzKw V G',
	('vehicle_type', 'PzKw V'),
	('sub_type', 'G'),
	('vehicle_class', 'Heavy Tank'),
	('nickname', 'Panther'),
	('target_size', 'Large'),
	('main_gun', '75LL'),
	('hull_front_armour', 18),
	('hull_side_armour', 6),
	('turret_front_armour', 14),
	('turret_side_armour', 6),
	('turret_traverse', 'Restricted Slow'),
	('info_text', 'Panzer V "Panther". A medium tank armoured with a 75LL gun, ' +
		'excellent at longer ranges. Very heavy front hull armour.')],
	
	# PzKw VI E, Tiger
	['PzKw VI E',
	('vehicle_type', 'PzKw VI'),
	('sub_type', 'E'),
	('vehicle_class', 'Heavy Tank'),
	('nickname', 'Tiger'),
	('target_size', 'Large'),
	('main_gun', '88L'),
	('hull_front_armour', 11),
	('hull_side_armour', 8),
	('turret_front_armour', 14),
	('turret_side_armour', 8),
	('turret_traverse', 'Restricted Slow'),
	('info_text', 'Panzer VIe "Tiger I". A heavy tank mounting an 88L gun. Very ' +
		'heavily armoured.')],
	
	# PzKw VI B, King Tiger
	['PzKw VI B',
	('vehicle_type', 'PzKw VI'),
	('sub_type', 'B'),
	('vehicle_class', 'Heavy Tank'),
	('nickname', 'King Tiger'),
	('target_size', 'Very Large'),
	('main_gun', '88LL'),
	('hull_front_armour', 26),
	('hull_side_armour', 8),
	('turret_front_armour', 18),
	('turret_side_armour', 11),
	('turret_traverse', 'Restricted Slow'),
	('unreliable', ''),	# no effect yet
	('info_text', 'Panzer VIb "Tiger II". A heavy tank known as the "King Tiger" to ' +
		'allied forces. Armed with an 88LL gun with excellent long-range power ' +
		'and accuracy.')],
	
	# SPGs
	
	# STuG III G
	['STuG III G',
	('vehicle_type', 'STuG III'),
	('sub_type', 'G'),
	('vehicle_class', 'Self-Propelled Gun'),
	('target_size', 'Small'),
	('main_gun', '75L'),
	('hull_front_armour', 8),
	('hull_side_armour', 3),
	('turret_front_armour', 8),
	('turret_side_armour', 3),
	('turret_traverse', 'None'),
	('info_text', 'Sturmgeschutz III Assault Gun. Built on a Panzer III chassis, ' +
		'initially intended as an infantry support gun but later used as a tank ' +
		'destroyer. Mounts the same 75L gun as a Panzer IV. The main gun is ' +
		'hull-mounted, so it must rotate to change its facing.')],
	
	# Marder II
	['Marder II',
	('vehicle_type', 'Marder II'),
	('vehicle_class', 'Self-Propelled Gun'),
	('target_size', 'Normal'),
	('main_gun', '75L'),
	('hull_front_armour', 3),
	('hull_side_armour', 1),
	('turret_front_armour', 2),
	('turret_side_armour', 0),
	('turret_traverse', 'None'),
	('info_text', 'Marder II Tank Destroyer. Built on a Panzer II chassis, designed ' +
		'to overcome heavy tanks on the Eastern Front. Mounts the same 75L gun ' +
		'as a Panzer IV. Very light armour, largely obsolete by late 1944.')],
	
	# Marder III H
	['Marder III H',
	('vehicle_type', 'Marder III'),
	('sub_type', 'H'),
	('vehicle_class', 'Self-Propelled Gun'),
	('target_size', 'Normal'),
	('main_gun', '75L'),
	('hull_front_armour', 4),
	('hull_side_armour', 1),
	('turret_front_armour', 3),
	('turret_side_armour', 1),
	('turret_traverse', 'None'),
	('info_text', 'Marder III Tank Destroyer. Built on a Panzer 38(t) chassis. ' +
		'Mounts the same 75L gun as a Panzer IV. Very light armour all around.')],
	
	# JgdPz IV
	['JgdPzKw IV',
	('vehicle_type', 'JgdPzKw IV'),
	('vehicle_class', 'Self-Propelled Gun'),
	('target_size', 'Small'),
	('main_gun', '75L'),
	('hull_front_armour', 14),
	('hull_side_armour', 3),
	('turret_front_armour', 14),
	('turret_side_armour', 4),
	('turret_traverse', 'None'),
	('info_text', 'Jagdpanzer IV Tank Destroyer. Built on a Panzer IV chassis. ' +
		'Mounts the same 75L gun as a Panzer IV. Very heavy front armour.')],
	
	# JgdPz 38(t)
	['JgdPz 38(t)',
	('vehicle_type', 'JgdPz 38(t)'),
	('vehicle_class', 'Self-Propelled Gun'),
	('target_size', 'Small'),
	('main_gun', '75L'),
	('hull_front_armour', 14),
	('hull_side_armour', 3),
	('turret_front_armour', 14),
	('turret_side_armour', 3),
	('turret_traverse', 'None'),
	('info_text', 'Jagdpanzer 38 "Hetzer" Light Tank Destroyer. Built on a modified ' +
		'Panzer 38(t) chassis, with a hull-mounted 75L gun. Very heavy front ' +
		'armour, but side and rear armour are both very light.')],
	
	# Other German Vehicles
	
	# SPW 251
	['SPW 251',
	('vehicle_type', 'SPW'),
	('vehicle_class', 'Transport'),
	('sub_type', '251'),
	('target_size', 'Small'),
	('main_gun', 'MG'),
	('hull_front_armour', 1),
	('hull_side_armour', 1),
	('turret_front_armour', 1),
	('turret_side_armour', 1),
	('turret_traverse', 'None'),
	('info_text', 'Schutzenpanzerwagen Armoured Personnel Carrier. Armed with ' +
		'machine guns, it can attack and destroy friendly infantry. No threat ' +
		'to your tank, unless it attacks you and a crew member has an open hatch.')],
	
	# PSW 232
	['PSW 232',
	('vehicle_type', 'PSW'),
	('sub_type', '232'),
	('vehicle_class', 'Armoured Car'),
	('target_size', 'Normal'),
	('main_gun', '20L'),
	('hull_front_armour', 3),
	('hull_side_armour', 1),
	('turret_front_armour', 3),
	('turret_side_armour', 1),
	('turret_traverse', 'Restricted Slow'),
	('info_text', 'Schwerer Panzerspahwagen Armoured Reconnaissance Vehicle. Armed ' +
		'with a light gun, can destroy friendly infantry teams and can wound any ' +
		'crewmember with an open hatch. They are able to spot your tank and report ' +
		'your position to other enemy units, improving their chance of hitting you.')],
	
	# Opel Truck
	['Opel',
	('vehicle_type', 'Truck'),
	('vehicle_class', 'Transport'),
	('target_size', 'Normal'),
	('turret_traverse', 'None'),
	('info_text', 'An Opel Blitz 3-ton Truck, used to transport infantry and war ' +
		'materials. Cannot attack, but worth some VP if destroyed. HE is more ' +
		'effective than AP, which may just punch through the vehicle without ' +
		'doing any real damage.')]
]
