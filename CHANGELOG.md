# History of changes

## 1.04 Changelog (now maintained by Eric Normandeau)
- InTheWork: Feature: Use "Space" to clear pop up messages instead of "Enter"
- Cleanup: Removed all instances of "is not None" in code
- Feature: Added pop up "Screenshot saved as: ..." for screenshots
- Feature: Menu items (help...) are now accessible through F keys AND number keys
- Feature: Added "On the way!" as possible gunner call upon firing
- Feature: Added more crew talk diversity and increased odds for artillery
- Feature: If 10 round cannot be added to tank, add maximum possible
- BugFix: Wrong caliber of gun reported by crew ("That sounded like a 8mm gun")
- Cleanup: Use spaces instead of tabulations in Python scripts
- Cleanup: Save Python scripts with Linux line endings
- Cleanup: Split readme.md into README.md and CHANGELOG.md
- Add dependent libraries (libSDL and libtcod)
- Cleanup repository
- NOTE: First version maintained by Eric Normandeau

## 1.03 Changelog
- BugFix: Removed Main Gun Broken at game start (EN)
- added additional hometowns for Canadian crew (GS and EN)
- hometown text transcoded properly to handle accented characters (UTF-8 -> IBM850) (GS)
- added additional strings for in-battle crew observations (GS and EN)
- added text description of gun sounds when hidden unidentified enemy fires with a gun (GS)
- advancing fire now no longer possible if main gun is malfunctioning or broken (GS)
- fixed a rare crash when moving in a counterattack mission (GS)
- NOTE: First version with contributions from Eric Normandeau

## 1.02 Changelog
- Made the terrain symbols that are displayed next to enemy units on the encounter map
   slightly more visible against the background
- Updated the in-game help text, as some entries were long out of date and described earlier
   versions of the game!
- Fixed a bug where in counterattack missions, nodes could be 'captured' by the enemy
   twice in the same campaign turn
- Fixed a bug relating to the player having to re-position when surrounded in a
   counterattack mission
é
## 1.01 Changelog
- Fixed a bug where the assistant driver did not have his Fire Bow MG order properly
   disabled when an encounter starts with the player tank Hull Down
- Hopefully fixed a bug where a marshland area could be assigned as the target for
   a 'capture' mission

## 1.0 preview1 Changelog
- Changed fullscreen settings so that it should reflect whatever the window is set to
   at the moment, and try to set the campaign preferences accordingly
- Changed experience level calculations, and movement times required and weather modifier
   to constants, so can be easily adjusted in future versions

## Beta 3.08 Changelog
 General Game Stuff
- Lowered the volume of bow MG sound effect by 10 db
- Added animated credits menu
- LW and MG enemy units now less likely to be hit with smoke from friendly action
- Changed the lowest rank for British & Commonwealth tank crews to Trooper (Tpr.)
- Campaign day map events (quests, etc.) no longer trigger right at the start of the day
- Added a confirmation prompt when trying to resupply in the campaign day map
 Campaigns
- Completed day descriptions and map locations for Patton's Best campaign
- Created a new map image for the Patton's Best campaign when I realized that the final
   few locations would not fit on the existing map!
- Completed day descriptions and map locations for Canada's Best campaign
- Fixed a crash in the Canada's Best campaign when the calendar reached 8/31

## Beta 3.07 Changelog
- Removed a previous check to make sure that campaign map node centres can be connected
   by a straight line without passing through another node. Turned out to be too restrictive
- Fixed a bug where if an enemy attack caused a penetrating hit, it could immediately
   do another action
- Fixed a bug with the spacing in day descriptions of the PB campaign
- Fixed bug where Rescue mission time limit would expire even if completed exactly on the
   time deadline
- Changed text description for enemy units moving closer to the player
- Improved appearance of bocage map nodes
- If the player captures the exit area and moves to a new map, the view of the new map
   will be shifted to the bottom of the map, with the player's location visible
- Impassible nodes no longer marked as under friendly control on campaign day map
- Counterattack Mission:
  - Enemy forces will no longer advance into impassible map nodes
- Fixed a bug where the display of tank movement and hull down status would not be updated
   soon enough to be displayed during starting steps of a new encounter

## Beta 3.06 Changelog
- Fixed a bug to do with handling an extra assistant driver or assigning a new one when
   assigned a new tank in the Canada's Best campaign

## Beta 3.05 Changelog
- Added a campaign map image for Canada's Best campaign
- Started adding descriptions for days in the Canada's Best campaign calendar
- Bonus modifier for 'Eye for Cover' skill has been doubled to -2
- Message console will now be cleared at the start of a battle encounter
- Added new sound files for main gun fire: 20/50mm, 75mm, 76mm, and 88mm. Sound played
   will be different depending on the gun type used.
- Added animation for LW attacks on friendly infantry and on player tank
- Fixed a bug where APDS ammo would sometimes not be treated as AP ammo
- Updated some of the help entries

## Beta 3.04 Changelog
- Fixed typo in message about tank stopping
- Action handler for enemy units has been re-written to hopefully be more reliable and
   less wonky. Program will do 300 attempts to find a random action that the unit can
   actually perform.
- 1/3 chance each round of there being no random event
- Panzerfaust attack no longer a random event, instead it's a possible unit action
- Started building a list of hometowns for Canadian crewmen

## Beta 3.03 Changelog
- incorporates hotfixes to Beta 3.02, fixing crashes
- campaign list now sorted reverse alphabetically, so that Patton's Best appears first
- shortened the maximum name length for crewmen slightly
- fixed a crash when a crew report was generated
- fixed the generation of crewman reports
- reports for all crewmen will be generated at the end of a campaign as well
- fixed a bug whereby the savegame file would be re-saved after it was erased

## Beta 3.02 Changelog
 fixed a bug whereby the 'abandon tank' order would not appear

## Beta 3.01 Changelog
 fixed a crash that occured when replacing crewmen

## Beta 3.0 Changelog
 "Out of commission, become a pillbox. Out of ammo, become a bunker. Out of time,
   become heroes." - Daskal, The Beast of War (1988)
 General
- New function for displaying tutorial messages in a pop-up window: each message is only
   displayed once for each player, intended to help new players get accustomed to the game
- Now possible to start campaign at any point during the campaign calendar
- Highscores file is now a bones file
  - also records information about dead crewmen
- Key commands now accepted in lower case or upper case format; eg. having caps lock engaged
   will no longer cause key commands to stop working
- Operation of alt key in main gun ammunition menu has changed to a toggle rather than a
   hold to modify
- New tank model: Sherman VC 'Firefly'
  - has a very powerful 76LL main gun, but no assistant driver position
  - has access to ADPS ammo; similar to HVAP, but more plentiful in 1945
  - never assigned as lead tank for the day, more likely to start encounters hull down
     and stopped, and tend to be at greater range from enemy units when they spawn
  - however: 33% chance of a Tank, SPG, and AT Gun attacks against the lead tank will
     attack player tank instead, reflects the fact that Fireflies were targeted more often
- If player switches to a new tank without an assistant driver position, that crewman will
   be removed. If they switch to a new tank that does have such a position, a new crewman
   will be assigned.
- New Terrain type: Bocage
  - worth 3 VP to capture
  - much more likely for enemy vehicles to be hull down, spawn at closer ranges
  - ambush at start of encounter much more likely
  - same modifier to trigger a battle when moving into it as a village node
  - more likely for player to start hull down too, gain hull down status when moving
- More detail for recording number of enemy units destroyed in campaign stats
- Crewmen that are KIA will be recorded in the bones file and displayed in the main menu
   screen
- Crewmen dialogue now displayed using the standard on-screen label function
- Purple Heart now only awarded for serious wound, very serious wound, or KIA
- Fixed a bug with displaying the campaign journal in-game, would crash if journal was shorter
   than window and player pressed PgUp
- Campaign map now stored in an .XP file and set in the campaign file
- Re-implemented the player location marker on the campaign map
- Main gun types now have standard display format in combat (ie 75LL gun displayed as 75mm)
- Campaigns can now add activation chance modifiers based on date, eg. to have tanks spawn
   less often later in the campaign
- Activation chance tables in campaign files don't have to add up to 100 any more;
   whatever the total is will be used to determine spawn chance
- New sound effects for: adding/upgrading a crew skill, HE and AP hits, main gun miss
 Campaign Day Map
- Any map nodes that are adjacent but cannot have a line drawn between node centres without
   passing through a 3rd node will no longer be linked up; produces more realistic
   connections on the campaign day map
- Boundary between friendly and hostile map areas now indicated with a red border line
- Selecting an adjacent area now cycles either clockwise or counterclockwise around the
   player
- Exit area moved random event will no longer trigger if player is within 2 nodes of
   current exit
- All mission locations will now be within 2 map nodes of player's current position
- Selected map node will be cleared if a new map is generated (eg. moving to a new map
   after capturing the exit area)
- When a mission is assigned, the player's view will be moved to the event node and it will
   be highlighted for a moment, then the message reporting on the mission will be displayed
 Battle Encounters
- Fixed a bug where a successful Pocket Bible skill check would still result in crewman's death
- Enemy units moving on the encounter map are no longer drawn with their terrain
   moving along with them
- Commonwealth (Canada only for now, but UK and others in future) get a bonus to all
   artillery attacks
- Enemy APCs will dismount any passengers if immobilized or destroyed; dismounted unit is
   automatically pinned
- Some changes to how battle information is reported:
  - 'Unknown' enemy status is now called 'Unspotted', effect is the same as before
  - Initial enemy spotted message now more simple; doesn't bother reporting that the newly
     spawned unit is Unspotted because they all are at first
- When a crewmember is KIA or sent home, a notification window appears after the battle is
   over, and a report on their final stats is added to the campaign journal
- Added a line to campaign journal on whether crewman bails out successfully or not
- Gunner will sometimes call out 'Firing' just before firing the main gun
- If main gun is fired and loader reloads a different shell type, he will call this out
- Final to-hit score required must be 2 or more to get a critical hit (was previously an
   automatic hit regardless of required score)
- The Sector Control mechanic has been completely removed. This means that enemy units
   can spawn behind the player (although much more rarely than in front) and the result table
   for random events has been changed to remove the two events that impacted sector control.
- New animations for HE and AP hits on enemy units
- All results from tank movement, plus tank stopping in the case of drive incapacitation, are
   now displayed as pop-up messages. Tank movement is pretty important so this result deserves
   its own pop-up as opposed to being buried in the combat message window.
 Known Bugs / Incomplete Features
- Player location marker on campaign map not yet fully implemented
- Canadian crewmen don't have hometowns yet
- Still missing several sound effects

## Beta 2.06 Changelog
- Actual time cost of movement on the campaign map now properly reflects new values
- All vehicles now apply effects of being Stunned properly. If an armoured car is spotting
   the player tank and is Stunned, they stop spotting
- Added an in-game error message if a hidden unit manages to somehow attack the player.
   I've had one report of this happening but can't figure out how given the action selection
   process in DoAction()
- Added new tank names to pool for random selection, thanks to N. Pratchett
- Added the M4A1(76)W Turret G tank model to the default campaign; should have been
   there from the start but I forgot to add it to the list!

## Beta 2.05 Changelog
- Added overhead views of player tanks in the tank info window
- Added a zoom-in effect for battle encounters

## Beta 2.04 Changelog
- Height of campaign day map decreased, minimum distance between map nodes also decreased,
   so nodes will be smaller on average
- Time required to travel between map areas has been increased
- More in-game events are now recorded to the Campaign Journal
  - all enemy units destroyed by player tank should now be recorded properly
- VP now awarded for defending map areas in Counterattack missions
- Increased minimum time elapsed until battle begins when awaiting an enemy counterattack
- Volume of some sound effects has been normalized
- "Eagle Eyed" skill no longer allowed for Gunner; could not make use of it anyway
- Can no longer spend skill points on dead crewmen
- Campaign action console now updated after resupply; time of day was not being re-drawn
- Replacement crewmen are now generated at any level between 1 and the highest experience
   level of existing crewmen.
- Firing at a new target now correctly clears any acquired target levels on any other
   enemy units
- Random campaign events will no longer trigger after sunset
- Notification of MG malfunction will now only appear after the roll result is displayed

## Beta 2.03 Changelog
- Fixed a bug in the way that new skills / skill increases were recorded to the Campaign
   Journal; some small additions and fixes to events that are recorded in the journal
- Added an option to view the current campaign journal from the Campaign Stats menu
- Adjusted exp threshholds for levels slightly
- Fixed a bug where resupplying would always trigger a counterattack encounter

## Beta 2.02 Changelog
- Tank movement animation on campaign day map now only shown if animations are set to
   on in campaign settings
- Added a pop-up notification when crewmen gain a level
- Crewmen will now gain levels properly when action day ends because tank is destroyed
   or damaged beyond repair

## Beta 2.01 Changelog
- Exit Area Changed and Friendly Advance random events will no longer select Exit nodes,
   so the player can still capture this node and trigger generation of a new map
- In Counterattack missions, front-line map areas to which the player can move are now
   highlighted in red
- If the player tank has suffered a penetrating hit, and thus must be abandoned at the
   end of the encounter, this is now displayed in the tank console

## Beta 2.0 Changelog

## Campaign Calendar
- Calendar now made up of a fixed number of action days, no more roll to see if player
   sees action.
- The animation for advancing to a new campaign calendar day has been simplified
- Information that used to be displayed in a 'morning briefing' is now displayed in the
   campaign calendar screen

## Campaign Day Map: Random Events
- Random chance of events occurring in the campaign day map:
  - Exit Area Changed
  - Reconnaissance Report: Reveals expected resistance level in an adjacent area
  - Enemy Reinforcements: Previously known resistance level is increased
  - Enemy Advance: Previously captured area is lost
  - Friendly Advance: Nearby enemy-held area is captured
- Also a small chance of new orders (quests) coming in via radio message. These are
   optional but include an extra VP bonus if completed:
  - RECON: check an enemy-held area for resistance level
  - CAPTURE: enter an enemy-held area, automatically triggers a battle encounter
  - DEFEND: enter a friendly-held area, wait for attack
  - RESCUE: like CAPTURE but with a time limit
- Note that these events are not triggered during Counterattack missions, since these
   missions have their own procedure for enemy advance

## Counterattack Missions
- Player now begins at top of map, with all map nodes initially under friendly control
- At the start of the day, and after every battle, the enemy map advance and capture
   friendly-controlled zones
  - Any map area on the top edge of the map, or adjacent to a zone that is already
     under enemy control, may be captured. Higher resistance levels adjacent to the zone
     will increase the chances that the area is captured.
- at start of day or after a battle, player has option to move into any adjacent
   friendly area that is also adjacent to an enemy-held area or the top map edge
  - but an encounter will be triggered in the new area afterwards
- Battle encounter resistance level is based on random choice from adjacent enemy-held
   areas; if none, then based on day resistance level
- Resupplying in a Counterattack mission day now takes 15 mins, is still always
   successful, and always triggers a battle encounter afterwards
- Random Events are not triggered during a Counterattack campaign day

## General
- Changed the procedure for spawning new crewmen, giving the player a chance to
   add/upgrade skills right away
- All consoles in main menu screen are now internally generated rather than loaded from
   external image files
- Added a display of current campaign calendar day vs. total days in campaign stats menu
- If no shell loaded in main gun at start of orders phase, Reload order for Loader is
   now disabled
- If tank is immobilized during ambush attack, driver's movement orders will now be
   disabled
- If driver is Stunned, tank will now stop in movement phase
- Hull Down status is now highlighted in the tank console to make it more prominent
- Added animation for player tank movement on the campaign day map
- If a to-kill roll is not possible (roll required is < 2) then armour save sound will
   be played after hit resolution
- Scrounger skill now has a different effect and activation levels: if activated, number
   of shells of rare ammo types (HCBI, HVAP, ADPS) available for the day is increased
- Toggling a crewman's hatch should no longer reset his current order
- Each crewman is awarded 1 exp per enemy-held area captured, even if there is no
   encounter triggered
- Final campaign stats are now written to the campaign journal as well as displayed on
   the screen at the end of a campaign
- Capturing the exit area not gives a 20 VP bonus, rather than multiplying the capture
   bonus based on the area terrain type
- Destroying a vehicle will now play the correct sound effect
- VP thresholds for promotions and decorations have been changed slightly

## Beta 1.6 Changelog
- Fixed a bug where no crewmen would be selected if advance fire destroyed all enemies
   on the encounter map

## Beta 1.5 Changelog
- If on-screen labels are set to pause and wait for enter before clearing, this message
   won't be included when the label text is recorded in the message console
   i.e. " [Enter to Continue]" doesn't appear in the message console any more
- Crew can now have their names set and reset freely
- Fixed a bug with the to-kill roll not being displayed properly sometimes
- More messages reporting no results from arty attacks, etc., appear as pop-ups rather
   than as just messages
- VP bonus for capturing exit area now does not stack with bonus for advance mission
- Nickname added to decoration award screen
- Fixed display of dates: 3rd, 23rd
- Added sound for opening / closing crew hatch
- Fixed crew order not being set to None when Stunned

## Beta 1.4 Changelog
- Added brief outline of ammo types to the main gun ammo menu
- Broken periscopes now replaced after combat encounter
- Added option to return to HQ, ending the campaign day, if your tank has one or more
   of the following damage: Gun Sight Broken, Main Gun Broken, Turret Traverse Broken
- Greatly expanded pool of first and last names for crewmen
- Tiger I now armed with correct 88L gun rather than 88LL
- Crew that are killed will no longer have any wounds listed
- Armoured Cars:
  - Now spawned in battle and counterattack missions
  - Have their own set of AI actions (used to be similar to Trucks)
  - May spot the player tank and relay its position to other enemy units, giving them
     one point of acquired target if they attack the player
- Adjusted score requirements for rank promotions and medals 

## Beta 1.3 Changelog
- Added more colour highlighting of command keys in menus
- Changed some sound effects slightly based on user feedback
- Added menu select sound effect
- Redesigned the layout of the campaign calendar view and added in a static version
   of the campaign map
- Sound effect files are now stored in a zipped archive and loaded at boot rather than
   being loaded and cleared each time they are played
- If a to-kill roll is an automatic success or no chance to succeed, display of the dice
   roll will be skipped, unless MG was used for attack and result was a malfunction

## Beta 1.2 Changelog
- Fixed a rare bug where MG fire could target armoured vehicles, and would affect them
   as if they were unarmoured trucks
- Even if a hit is an automatic kill or no chance to damage, the to-kill roll will still
   occur in case there's an MG malfunction rolled

## Beta 1.1 Changelog
- Fixed minor typo in decoration line in campaign journal
- Fixed a bug with text alignment when viewing the help interface from the campaign
   day map

## Beta 1.0 Changelog
- If advancing fire, artillery, and/or air strike attacks manage to destroy all enemies
   initially spawned on the encounter map, the ambush and spotting phases are skipped and
   play proceeds directly to the orders phase
- Reduced maximum crew name length from 20 to 19 characters, full length would bump up
   against the position column in the tank console
- New main gun ammunition menu, used for resupplying and for restocking the ready rack.
   This separate menu should make ammunition management much clearer, especially for new
   players.
- Removed update check; was not really that useful, especially with the slower pace of
   updates.
- Commander Awards: at end of every calendar month, program will check for medal awards
   for the commander, based on highest one-day VP score that month. Possible awards are:
   Bronze Star, Silver Star, Distinguished Service Cross, Congressional Medal of Honor
- Commander rank promotions: at end of every day, program will check to see if commander
   has earned enough VP over the campaign so far to earn a promotion. Commanders start at
   the rank of Sergeant, can be promoted to Staff Sergeant, Second Lieutenant, First
   Lieutenant, and finally Captain
- When starting a new day, the tank console view automatically opens the main gun ammo
   menu to start so that player can load ammo
- By default, on-screen labels will require player to press Enter to clear them. This
   setting can be changed in the settings menu to pausing before automatically clearing.
- Slightly decreased the effectiveness of artillery, air strikes, and advancing fire
- Fixed a bug where Stunned crew could be issued orders
- Fixed a bug where crew would repair tank even after it had been completely destroyed
   or damaged beyond repair
- Campaign Journal: Records various events during the course of the campaign and outputs
   them to a text file after the campaign is over. Data recorded includes:
  - Real-world local time and date that campaign was started
  - Model and name of tank
  - Rank and name of starting crew members
  - Crew gaining levels, adding new skills or upgrading existing skills
  - Each date in the campaign calendar, whether the crew saw action and if so, what
     the mission type and expected resistance was
  - Time of battle encounters and terrain of map area
  - Enemy units destroyed by player action
  - Crew members wounded and/or killed
  - When time passes during a battle encounter
  - When a battle encounter ends
  - When an action day ends and why (due to sunset, player tank destroyed, etc.)
  - Promotions and medals awarded
  - Replacement crew assigned, replacement tank chosen or assigned
  - Why the campaign finished

## Alpha 9.2 Changelog
- The game now keeps track of how many enemy reinforcement units have arrived into a
   battle encounter. If there have already been one or more reinforcements, the game
   rolls a D6. On a 1 the unit arrives, otherwise if the total of the roll plus the
   number of reinforcements is equal to or greater than 7, no random event occurs this
   round.
   So if one enemy reinforcement has already arrived and the random event generated is
   another one, it will arrive on a roll of 1-5. If two, 1-4, etc. to a minimum of 1.
- The number of rounds in battle encounters is now recorded and displayed at the top
   of the encounter map console.
- Fixed a bug where the "very serious" wound level was not actually being used at all
- Tank console is now updated after every crew wound
- Added a simple display of enemy unit terrain to their depiction on the encounter map
- Reorganized the tank console display slightly to make room for a damage report
- Changed the effect of the Fire penetration result: one minor damage result, one
   possible collateral damage wound for one randomly chosen crewman
- Added minor damage: can result from light weapons attacks or a penetrating hit that
   does not knock out the player tank. Crew can attempt to repair most types of damage,
   but some is permanent and will only be repaired after an encounter ends or at the end
   of the combat day
- An original roll of 12 on an MG to-kill roll does no damage to target and causes a
   malfunction in the fired MG
- New Skill: Mechanic. If activated, adds a bonus to repair attempt roll. Most useful for
   the Loader but all crew positions can take this skill.
- Added some checks to make sure HVAP is treated as an AP round (eg. no damage to infantry
   units)
- Fixed a bug with damage repair

## Alpha 9.17 Changelog
- Changed the way that sounds are loaded and played so that they are loaded just before
   they are played, rather than being all loaded into memory at boot. Still unable to get
   ogg files playing as sound effects, however.
- Added sound effects: enemy infantry moving, dice roll, friendly tank destroyed
- Combined both acquired target and acquired player as target info into a single line in
   the enemy unit info console
- Changed the advance day display a little
- Removed the large campaign map: there just wasn't a way to get this to look right. Will
   revisit the idea in a future version.
- Removed the 'Resupplying' label from the tank console while in a Counterattack
   encounter

## Alpha 9.16 Changelog
- Dead crewmen no longer have the possibility of suffering an initial wound when player
   tank knocked out
- Confirmation from player now required before crewmen will carry out an abandon tank
   order
- Removed the action day roll modifier
- A WP hit on an infantry unit will, in addition to creating smoke, force it to pass
   a pin test or else be pinned. HCBI has no such effect.
- Clearer display of crew wounds and status in the tank console
- Fixed some display and layout bugs on refit days, added a message to let the player
   know when a refit period is beginning.
- Improved the display of calendar day advancement
- Changed experience points thresholds for gaining levels slightly

## Alpha 9.15 Changelog
- Friendly Action system now a 2D6 rather than a D100 system.
- Fixed a bug where the Loader would be reset to Reload orders if main gun malfunctioned,
   resulting in a crash to desktop if the left/right arrows were used in a later orders
   phase
- Fixed a bug where the campaign day map would shift momentarily when calling in an air
   strike, since the 'S' command is also used to scroll the map display. The command to
   attempt an air strike has been changed to 'R'.
- If the to-kill roll for a hit that penetrates the player tank's armour was an original
   2, or the roll was less than half of the score required, two rolls are made to
   determine the result of the penetration and the worse of the two is applied.
- Panzerfaust attacks now do a to-kill roll, although the base score required is 31!
- Fixed a potential crash when replacing crewmen
- Dead, stunned, or unconscious crewmen can no longer add or upgrade skills until such
   time as they recover

## Alpha 9.14 Changelog
- Level of replacement crewman based on average level of surviving crewmen, with some
   minor random variation
- New Skill: True Grit: Gives better odds of recovering from negative status effects,
   resisting Stun, plus more likely that a wound will be less severe. Very useful, so
   there are five possible levels to invest your skill points into.
- Modified the experience level inflation slightly.
- Adjusted advancing fire to be slightly less effective at all ranges
- Fixed a bug where the advance to next day display would be centre rather than left
   justified

## Alpha 9.13 Changelog
- Fixed a bug where all orders would be reset after tank movement phase, meaning that
   no actions could be performed!

## Alpha 9.12 Changelog
- This time, really fixed the bug where the asst. driver could remain on Fire Hull MG
   order after tank goes Hull Down, resulting in a crash when the player later tries to
   change the order

## Alpha 9.11 Changelog
- Fixed a bug in player tank armour penetration
- Fixed a bug where the asst. driver could remain on Fire Hull MG order after tank goes
   Hull Down, resulting in a crash when the player later tries to change the order
- Changed message for a fire starting in the player tank, since this feature hasn't been
   fully added yet.

## Alpha 9.0 Changelog
- New format for the highscores file: NOTE if you had an older highscores file that you
   continued to use with this version, it is incompatible and must be replaced
- Program will now check with the webserver to see if a newer version of the
   game is available, and display a notice on the main menu if so. This check will only
   occur if the previous check has never occurred or it was five or more days ago.
- Added a mission briefing for each of Advance, Battle, and Counterattack missions. These
   are displayed before heading to the day's start area, and each one is only displayed
   once per campaign, the first time that the mission type occurs. I've also added the
   text of the briefing to the Help dictionary.
- Added sound effect for enemy vehicle movement
- Added new skills:
   Pocket Bible: Gives a chance to ignore a Dead result when a crewman is wounded
   Gymnast: Gives a bonus to bail out if activated
   Lightning Reflexes: Gives a chance to avoid a wound from collateral damage when
     crewman is exposed (hatch open)
- Availability of ADPS ammunition increases at start of 1945, from 1-3 to 2-5 per day
- Added animation for successful air or artillery strike on the campaign day map, also
   used when enemy artillery attacks player during Random Event phase of encounters
- Enemy units that are forced off the encounter map as a result of player movement now
   apply a penalty of 1/2 their VP value to the encounter.

## Alpha 8.32 Changelog
- New standard for in-game unit portraits
  - Still lots of units missing portraits but they will be added in the future
  - Unit portraits displayed full-scale in tank info screen
  - Unit portraits displayed 1/2 scale in roll results screen
  - If attacker or target is unknown or needs to be identified, a question mark
     portrait image is displayed instead
- New animation for MG attacks, used for player MG attacks on enemy units, enemy MG
   attacks on friendly infantry, and MG attacks on player tank
- Added new sound effects: screenshot; radio report of enemy unit spawn
- Advancing fire now only possible when tank has 6 or more HE shells; prompt will tell
   player how many HE shells they have when asking whether to use advancing fire
- Fixed incorrect plural when player used 1 shell for advancing fire
- Fixed a bug where the correct description wasn't being used for a unit that was hidden
- Fixed a typo in the description for the Firefly
- Fixed a bug where crew orders would reset to default after reloading into an
   encounter in progress

## Alpha 8.31 Changelog
- Fixed a bug where I had left in a function that didn't exist, meaing the main gun
   would not work!

## Alpha 8.3 Changelog
- New screen for advancing to next calendar day; no longer possible to save and quit
   or issue commands on days when the player doesn't not see action, but there's very
   little that has to be done on those days anyway. This system provides more of a
   smoothly flowing narrative and moves gameplay quickly to the next active campaign day
   or refit period
- Changed key to issue a crew order to 'o', now you open the orders menu with 'o'
   and issue the order with the same key, should be more intuitive
- Changed the text description used for enemy units so that instead of TANK or SPG a
   more descriptive text string is used instead, eg. 'Tank' and 'Self-propelled Gun'
- Slightly increased the pause time before on-screen labels are cleared
- Added confirmation window if player has no main gun ammunition loaded and tries
   to leave resupply tank view (eg. at the start of a campaign day)
- PSW/SPW unit class no longer exists, has been replaced with two separate classes:
  - APC: Armoured Personnel Carrier
  - AC: Armoured Car
  - the specific units in the Patton's Best campaign remain the same as before, but each
     unit class will have new unique abilities in the future
- The Gyrostabilizer skill is now restricted to USA player forces. Doesn't have any
   effect yet but will matter when new campaigns are added
- System for selecting a random tank model as a replacement for a knocked out one has
   been updated; more streamlined and will be easier to shift to a new, more generic
   tank rarity system in the future
- Campaign info is now held within an XML file, when starting a new campaign the player
   has a choice of which campaign file to load. For now this screen is disabled since
   there's only one playable campaign!
- The "Canada's Best" campaign has been disabled for now, as has the screen to select
   a campaign, since there's still a few more features that need to be added to make the
   Canadian campaign work.
- Sherman VC 'Firefly' added to player tank list for Canadian campaign
  - 76LL main gun and APDS ammo added for the Firefly
  - Added flag for player tanks to not have an assistant driver position, a crewman for
     this position won't be generated for these tanks
- AA, co-ax, and bow MG FP ratings are now stored in the vehicle info; if a tank does
   not have a particular MG, the order to fire it will not be included in list of crew
   orders
- Several changes to the calendar for the Patton's Best campaign, changed based on
   ongoing research
- Fixed a bug where the enemy gun type was not being passed to the player tank knockout
   function properly. It had been using a variable I created and never ended up using.
- Fixed a bug where PaK 43 AT Guns were being given an 88L rather than an 88LL gun.
   This small correction is going to be very bad for players!

## Alpha 8.22 Changelog
- Fixed a bug where activation of the 'scrounger' skill would crash the game

## Alpha 8.21 Changelog
- Fixed: menu bar not being displayed properly on the campaign calendar window after being
   assigned a new tank
- Reduced the volume of the Sherman moving sound slightly
- If Loader is on 'Change Gun Load' order, the main gun can still be fired with the newly
   loaded ammo type, and the gun will be reloaded, but Rate of Fire cannot be maintained

## Alpha 8.2 Changelog
- Added a preview of the currently saved campaign to the main menu
- Game will check version of saved game against current game version and, if there is
   a mismatch, will not allow loading the saved game
- Replaced several variables with constants, should sped up display rendering slightly

## Alpha 8.1 Changelog
 New Campaign Calendar System
- Player must now manually advance through each day in the campaign calendar
  - Added an animated display for advancing to next day
- Each day has an action rating, if 2D6 roll is equal to or under rating, tank sees
   action
- Action chance modifier begins at 0, set at +2 after you see action, reduced by one for
   each day you don't see action to a minimum of 0
- If no action, day proceeds without anything dramatic happening
- Changed action chances for each day to match new 2D6 system
- Added sound effects:
  - Successful armour save by vehicle hit by AP or by player tank
  - Player tank movement, both on the campaign day map and on the encounter map
  - Co-ax and AA MG on player tank firing
- Changed the timing of the sound effect for a smoke hit
- Changed screenshot function to use bmp; png colours didn't look right

## Alpha 8 Changelog
- Fixed a minor rendering error in the animated main menu image
- Fixed text input console display so that entering a new nickname for a crew member
   does not further darken the screen background
- Changed the procedure for firing MGs: now you select one MG from a list of possible
   ones to fire, and target selection will proceed according to that MG's restrictions
   (eg. coax can only fire in front of turret, etc.)
- Added abandon tank order, only activated if one or more crewmen are incapacitated or
   worse, or if tank is immobilized
- Added different colour schemes for the campaign map based on season and ground cover
- Added a message if no shells remaining and can't change gun load
- Added vehicle notes on remaing Sherman types
- Campaign day map view now begins with player node in view
- Added sound effects:
  - Player tank knocked out

## Alpha 7.6 Changelog
- Added gyrostabilizer skill for Gunner
  - skill first becomes available after first refit period: RunCalendar should set a flag
     in the campaign object when this happens
  - always applies a +2 penalty to hit in FireMainGun
  - works a little differently: if gunner has at least one level of the skill, then firing
     on the move is possible, skill check every time firing on the move, but if the skill is
     failed then the penalty to hit is doubled
  - skill can go up to 100%
- If a skill activation level is at 100%, no message will be displayed when it activates

## Alpha 7.5 Changelog
- Changed command to issue an order to a crewman to [O]; this brings up a list of
   possible orders, while you can also use A/D/Left/Right to cycle through orders
- Fixed a bug where the current day's VP wasn't being added to your highscore when
   KIA or being sent home ended the campaign
- Added option to use advancing fire upon entering enemy-controlled areas. Uses 1-6
   HE rounds, and if a battle encounter is triggered, you get an attack on enemy units
   right after any artillery or air strikes. Advancing fire affects all enemy units on
   the map, but is less effective against vehicles, against units at medium or long
   range, and pins units rather than laying smoke.
- Fixed a bug where the currently selected crewmember would be reset after saving and
   reloading a game. System relies on no two crew members having the same name, but I
   also updated the GenerateName function so that it will throw out any name that is
   already being used by a crew member (unlikely, but not impossible)
- Improved display of crew fate after tank is knocked out, uses the menu console now

## Alpha 7.4 Changelog
- Reduced screen height to 732 pixels so the window will fit better on 1366x768
- If full screen mode has been selected in display settings, resuming a saved game
   will automatically switch to full screen mode
- Added a Campaign Stats window with various stats about the current campaign, this
   screen is displayed at the end of a campaign to summarize your game

## Alpha 7.3 Changelog
- Changed the way in which enemy spawn sectors are calculated: now they have an equal
   chance of appearing in any enemy-controlled sector
- Changed the way that tank pivoting works: now you select your new facing rather than
   rotating the entire map as you pivot. Should still be easy to see where enemy units
   will end up after you pivot.
- When pivoting your tank, there is a small chance of throwing a track: natural 12 on a
   2D6, followed by a 5+ (so, less than 1%)
- If you are Hull Down and pivot your tank, there is a 41.66% chance of maintaining Hull
   Down after the pivot (<=6 on 2D6, no modifiers)
- MG attacks on infantry units will Pin them automatically if the modified roll is equal
   to the required roll to destroy
- Now possible to carry up to 30 extra main gun rounds, but the more extra rounds you
   carry will increase the chance that your tank explodes if it is knocked out!
- Added option to add 10 shells at once when loading main gun ammo into your tank
- Enemy AT guns can now rotate in place to face you and friendly forces before attacking,
   but will suffer a to-hit penalty for doing so.
- On-map labels will now be displayed so that they don't fall outside the map area; labels
   were overlapping the tank console and were difficult to read
- If no enemy units can be spotted and/or identifed, the Set Spot Sector phase for crew
   who can only spot in one sector is now skipped
- Enemy-controlled sectors now explicity marked with a GER, also fixed the location of
   sector control display slightly
- If a hit on the player tank has no chance to knock it out, the to-kill roll is skipped
   and a label to this effect is displayed instead
- Changed the way that the list of possible targets is compiled, should not have any
   notcieable effect on gameplay but makes it easier to add the AA MG attack
- Added Fire AA MG order for Commander, and if the loader has a split hatch, for Loader
   as well. Same range as the Bow MG but same Firepower as the Co-ax, it can be fired in
   any direction. If a Crewman on this order takes a wound, however, collateral damage
   is much more severe since they must stand outside the turret, while a normal knock-out
   hit is less severe as they are not subject to spalling or other internal dangers.
   Finally, crew on Fire AA MG orders bails out automatically, since they are already
   outside the tank!
- Enemy tanks and SPGs are now less likely to move in mud or deep snow ground conditions;
   if a move action is rolled, it's re-rolled and the new result is applied
- Now possible to cycle through list of possible crew orders for selected crew during the
   orders phase simply using A/D or Left/Right arrow
- Changed the way that sectors are selected for crew who can only spot in one sector
- Improved the appearance of the selection dialogue used in fire MGs, changing the gun
   load, etc.

## Alpha 7.2 Changelog
- Increased the height of campaign day map slightly
- Added rifle fire sound effect for enemy LW attacks
- Added campaign area info console, with basic information about the map area on mouseover
- Changed how campaign day map actions are stored, now adjusts for effects of weather on
   time needed to move into an adjacent area
- Air strikes added, more effective than arty against vehicles but does not place smoke;
   will pin infantry units instead
- Artillery and Air strikes now part of same action, can be called on any adjacent area,
   but does not trigger until your forces move into the area and a battle is triggered
- Map areas can have an arty or air strike called on them, but only one
- To call in artillery or an air atrike the game rolls 2D6, score must be equal to or
   under your current chance rating; each successful strike reduces the rating by 1, to
   a minimum of 2
- Fixed a bug relating to display of enemy locations on the encounter map info console
- Added a short instruction line to mouseover units on encounter map

## Alpha 7.1 Changelog
- Added screenshot function accessed via F12
- Lots of changes to campaign day map generation:
  - Appearance of maps will now remain the same across saving and loading games
  - New terrain type: Marshland, which is impassible to your forces
  - Layout of roads should now appear more natural
  - Different colour and character rules for painting the map
  - Enemy resistance is calculated at time of map generation, and is now more likely
     in areas with an improved road or dirt road, and less likely in Fields and Woods
     terrain areas

## Alpha 7 Changelog
- Replacement crew members now start at the highest level of any remaining crew, minus 3, plus
   2 for replacement Commanders and plus 1 for replacement Gunners, minimum level 1.
- Fix a bug with Commander directing main gun fire: bonus is now -2 if hatch open, -1 if hatch
   shut but tank has vision cupola
- Counterattack scenarios no longer award double VP for encounters
- Rain, fog, or falling snow now increase the chance of an Ambush
- Changed way that encounter map hex sectors are stored, should not have any impact on
   gameplay but should be more efficient
- Changed the effect of Fire Direction and Driver Direction skills slightly

## Alpha 7rc2 Changelog
- Updated key commands in the campaign tank view to match those in the encounter tank
   view: R for Ammo Reload Type, T to Toggle ready rack usage
- All crew will now have their orders reset to default after an encounter has finished
- Fixed a bug where the asst. driver's skill activation and either the gunner or the loader's
   could both have an effect on the RoF roll; now only the best modifier applies for any
   single roll
- Fixed an ancient bug where PSW/SPW units would not actually do anything!
- Decreased chance of checking for weather conditions change to 10% per 15 mins
- Using Tab to select a target map area on the campaign map, you can now hold Shift to move
   selection in opposite direction
- After triggering a minefield attack that disables your tank, the driver's available orders
   should now be immediately updated
- Hidden units that roll an attack action will now re-roll first; if another attack action
   is rolled, unit does nothing. Should mean that Hidden units move more often and do nothing
   less often.
- If unit positions change due to player tank movement, this will now reset spotted and
   hidden status, as well as any target acquired level on all enemy units
  - Also, the map should be updated more quickly to show them in their new positions
- If there are no live enemy units on the map, the Friendly Action Phase will be skipped,
   as will the random events Friendly Artillery and Flanking Fire
- Fixed some rendering issues with opening the Help, and Tank and Crew Info windows in
   the campaign calendar view
 Updates To Pinning and Stunning Enemy Units:
- Enemy infantry units (LW, MW, AT GUN) can be Pinned, and enemy vehicles can be Stunned:
  - If an infantry unit is hit by HE but not destroyed, they must take a morale test; the
     difference between the TK roll and score required is added as a positive modifier.
     If the morale test is failed, they are Pinned.
  - If a TK roll on an infantry unit is exactly equal to the number required, the unit
     is automatically Pinned.
  - If an already Pinned unit is pinned again, they must pass a morale test or be
     destroyed. Any terrain DRM for the unit is added as a positive modifier for this roll.
  - Pinned units can only do nothing or move away as their action.
  - Stunning works like pinning on vehicles, except that if you fail to destroy a vehicle
     with AP, they aren't subject to Stunning. The only way a vehicle can be Stunned is
     by rolling exactly the number required on a To Kill roll.
  - Pinned and Stunned units automatically test to recover during the enemy action
     phase, but if they recover they do no other action that turn. If they don't
     recover, infantry units can still move away from the player as their action, but
     remain Pinned. AT Guns can't move, so they can only do nothing if Pinned.
  - Each time a unit recovers from pinning, its morale level is reduced by one to
     represent fatigue, to a minimum of 2.
  - An original roll of 12 on a morale test is always a fail, regardless of modifiers.

## Alpha 7rc1 Changelog
- Fixed a bug where stunned enemy vehicles would still act as normal!
- Fixed a bug where every day would start cloudy
- Fixed a bug where immobile enemy units at medium or long range in fog or falling
   snow could move closer to the player
- Orders now reset each turn only for Driver and Loader, other crewmen will keep their
   order until the end of the encounter or circumstances make their order impossible
- Changed the odds of enemy morale values slightly
- Made spotting and identifying enemy units slightly more difficult
- All enemy AT Guns are assumed to be emplaced; this means they always get a +2 terrain
   DRM to hit, or to kill with an area fire hit. If they are in a fortification, they
   get the +3 DRM instead.
- AT Guns are never set up moving, and will not move during a battle encounter
- Their only actions are: Do nothing; fire at friendly tank (player if fired upon
   in previous turn); fire at player tank; fire at lead tank
- AT Guns have a facing set at spawn, and which can be changed if player tank moves
- If an AT Gun rolls an attack action and is not facing the player, it rotates to face
   the player
- Any critical hit on an AT Gun, whether direct or area fire, will automatically destroy
   it
- Enemy infantry units (LW, MW, AT GUN) can now be Pinned:
  - if an infantry unit is hit by HE but not destroyed, they must take a morale test;
     if they fail, they are pinned
  - if a TK roll on an infantry unit is exactly equal to the number required, the target
     is automatically pinned
  - pinned units can only do nothing or move away as their action
  - pinned units can test to unpin at the end of the encoutner turn by rolling against
     their morale level

## Alpha 6.8 Changelog
- Added a "Generating Campaign Map" message when heading to a new campaign area
- Added Panzerfaust attacks:
  - LW units have a random chance of being armed with a PF when spawned. This chance is
     slightly higher in 1945.
  - Whether or not an LW unit has a PF is not known to the player until it attacks
  - If a Panzerfaust event is rolled on the Random Events table, any LW unit that is
     in close range, has a PF, is neither in a building nor a fortification, and is neither
     hidden, pinned, nor broken, has a chance of firing a PF at the player
  - PF attacks have a greater chance of happening during or after December 1944, if the
     player tank is moving, if it is the lead tank, and if the attack comes from the rear
     three sectors of the tank. They are more likely in Advance missions, and much more
     likely during Battle missions
  - If an attack is triggered, the LW must pass a to-hit roll. DRM are +2 if player tank
     is moving, and smoke DRM apply as normal
  - If the attack hits the hull or turret of the player tank, it is destroyed. Hull Down
     and Thrown Track results apply as normal.
  - There will only be one PF attack per Random Event if the attack misses

## Alpha 6.7 Changelog
- Added display of crew wounds to the Tank Info console and Crew Info window
- Fixed a serious bug where Tanks and SPGs that were immobile could still turn to face
   the player when attacking
  - For now, enemy tank turret facings are not tracked, so immobile tanks will also not
     be able to turn to face the player.

## Alpha 6.6 Changelog
- Unlimited tank model selection now restricted to tank models that have a rarity factor
   of at least one; means that player cannot select a tank model that was historically
   unavailable during that month
- Uncovered and fixed a bad re-use of a global variable name
- If animations are disabled, on-map labels appear all at once rather than being drawn
   gradually
- Rotate Turret phase has been fixed
- Changed command for toggling Ready Rack usage to T - was in conflict with the new
   commands for rotating the turret while in Fire Main Gun mode
- Edited the command explanations for Main Gun Fire slightly
- Crew orders will now reset to their default order at end of turn - eg. Loader will
   go on Reload order, Driver on Stop, etc.

## Alpha 6.5 Changelog
- Updated the in-game description of some crew orders; was still referring to old crew
   skill bonuses
- Fire Main Gun and Fire Co-ax MG orders have been changed: now you no longer have to use
   a separate order if you plan on rotating the turret. During the firing phase, you have
   the option to rotate the turret to face any direction before firing. To-hit penalties
   for turret rotation are applied automatically. If you don't rotate the turret, no penalty
   is applied
- A Line of Sight is drawn when selecting a target in the Fire Main Gun or Fire MGs phases
- Changed the way that the Set Spot Sector display is drawn
- Added 'Keen Senses' skill for Commander
- Added 'Cautious Driver' skill for Driver

## Alpha 6.4 Changelog
- Fixed a couple display errors in the To Kill roll display: was reporting gun type and
   die results incorrectly
- Improved the look of the Encounter Menu
- Changed "Load" order to "Reload". This just make more sense, and should be clearer to
   the player what it actually does. Functionality remains exactly the same.
- Being Hull Down will now disable the Fire Bow MG order automatically; previously you
   could issue this order but the MG could not be fired.
- Fixed a bug where destroyed units would be moved and/or rotated when player tank moved
- If movement results in an enemy unit having a different facing toward the player, this
   is shown in an on-map label rather than the mysterious message "You may have moved far
   enough to change enemy facings"
- Fixed a bug where the day_in_progress flag wasn't being reset after player tank destroyed
   and returned to campaign calendar
- Added a display of current campaign settings in the Game Settings window
- if tank is knocked out or immobilized during an encounter, VP and experience points from
   that campaign day are still awarded, and the campaign menu is displayed to show the player
   experience point and level gains by crew

## Alpha 6.3 Changelog
- the campaign calendar map is still being worked on and not yet complete, so I've disabled
   display of player's location on the map for now
- appearance of dice roll results window improved slightly; display animation for this
   window is shown only if animations are enabled in game settings
- fixed a bug where the resistance level and mission would not display on first combat
   day
- Added in crew nicknames for Galaga Galaxian. Nicknames can be set and reset at any time
   via the Crew Info window (F3)
- Crew wounds system substantially changed from original, should make more sense now:
   Wounds:
     Light Wound: Recovers at end of encounter, but +1 chance to be wounded later in encounter
     Serious Wound:
       For now: Recovers at end of encounter, but +2 chance to be wounded later in encounter
       For future: Must go to hospital after encounter, random recovery time
     Very Serious Wound: Sent home after encounter, +3 chance to be wounded later in encounter
   Status Effects:
     Stunned: Crewman cannot perform any actions, but automatically recovers at end of action phase
     Incapacitated: Crewman cannot perform any orders, but can attempt to bail out if needed
       Crewman rolls to recover at end of action phase
     Unconscious: Crewman cannot perform any orders, and cannot attempt to bail out
       Crewman rolls to recover at end of action phase
     Dead: Crewman is dead

## Alpha 6.2 Changelog
- added fortification terrain for enemy infantry units encountered in Battle missions
- added morale ratings for enemy units; these are not displayed to the player 
  - Panthers, Tigers, and King Tigers have a better chance of having a higher morale level
  - infantry units will also make use of these ratings in the future
- added Stunned status for armoured vehicles; if TK roll is exactly number required, target
   is Stunned, and must pass a morale test to recover in their next action phase. Stunned
   enemies will neither attack nor move. If a Stunned enemy is Stunned again, the crew
   abandons the vehicle and it counts as destroyed
- added Campaign settings, player can select whether they want permadeath for their commander
   and how tank model selection is handled
- campaign calendar data is now set via a CSV file, and campaign information is now
   stored in an object rather than hard-coded 
- reorganized high scores screen, top 40 may now be recorded, and if you choose Unlimited
   Tank selection and/or casual commander replacement, this is displayed as codes alongside
   your final score
- loading images should now correctly format the full path name based on OS preferences.
   This is also done for the new CSV file that defines the campaign calendar
- in the combat calendar, advancing now moves directly to next action day or refit
   period, skipping all days where the battlegroup does not see action
- some minor changes to the script for Py2Exe, should not produce any noticable changes
   in the Win32 binary

## Alpha 6.1 Changelog
- added fancy animation for main menu
- added animation for main gun firing
- added sounds: 75mm main gun firing, MG attack
- 'throw smoke grenade' order is now disabled if crewman has no hatch, or if tank
   has no smoke grenades remaining
- unmodified roll of 12 (boxcars) now results in an automatic miss; this means that
   to-hit rolls with target scores of 12 or more still have a chance to miss
- combined EncounterMessage and CampaignMessage into a single function that
   sends the messsage to the right place; no effect on the game, just easier to code
   for in the future
- removed logging messages to logfile.txt, was not really useful any more
- default background colour for all consoles should now be plain black
- in-game help reorganized somewhat, now uses menu console
- firing smoke at an enemy does not increase its chances of firing back at you,
   nor will it increase its chances of moving away if firing on its side
- campaign player tank view now uses the menu console, looks better
- added counterattack mission type; for now, player can move off board and win encounter
   with no penalty, but in future if encounter is won this way no VP will be awarded; any
   enemy units moved off baord through player movement will count as negative VP
  - time between battles based on campaign day's resistance level
  - resupply is always available between battles
  - crew replacement does not use up any time
  - encounter VP is doubled, positive or negative  
- added wet stowage to M4A3(75)W Turret D, which it ought to have
- added settings window: animations and sounds can be turned on or off
- after an encounter, the view tank window automatically pops up: player will likely want
   to change ready rack load, hatch status, etc. in preparation for next battle
- rain was making smoke disappear in the same turn that it was placed; changed modifier
   for smoke depletion slightly
- if fog or falling snow, hexes at medium and long ranges will be greyed out to show that
   spotting and combat only possible at close range while either of these weather conditions
   are in effect
- replaced gunners start at level 2 (replaced commanders start at level 3, but right now
   no way to continue if commander is dead or seriously injured)
- fixed identified units not being labeled properly if they move and are later not spotted
- fixed a bug where PSWs and SPWs would be spawned without a facing set
- changed layout of date / time console slightly

## Alpha 6rc2 Changelog
- fixed MG main guns showing up as 'MGmm' in vehicle info view
- moved crew info display in tank information console slightly to fit longer names
- removed an extra message about not being able to fire bow MG while hull down
- fixed driver orders list not being correctly rebuilt after tank bogs down
- fixed campaign message console not being drawn properly on reload and on moving
   to a new map area
- added a line to display the current phase at top of encounter map console

## Alpha 6rc1 Changelog
- added skills, experience points, levels, and skill points
- changed TEM for Woods to +1 for all attack types
- fixed a small bug where enemy reinforcements would not use the correct table for battle
   scenarios
- fixed a bug where enemy units would move closer from close range and end up in the same
   hex as they started from

## Alpha 5.5 Changelog
- if raining, smoke depletes twice as fast as normal
- if there's fog or falling snow, spotting and combat is only allowed at close range,
   and all direct fire attacks count as going through smoke
- weather has a small chance of changing every 15 mins.
- rain, snow, or dry weather for two hours in a given day will change the ground
   cover: mud can dry, dry ground can be turned to mud, and falling snow can accumilate,
   but ground snow will only after a new day begins
- HE hits on infantry are less effective when ground conditions are Mud or Deep Snow
- mud, snow, or deep snow on ground increases chance of throwing track or bogging down
   when moving tank in an encounter, also increases difficulty of successfuly moving
   and/or attaining a hull down position
- tank can now get bogged down, and driver must try to unbog it instead of moving
- if an enemy tank or SPG is not facing the player and rolls an attack action, it
   pivots to face the player instead
- main gun hits on enemy units are handled differently now, so that non-critical,
   area fire HE hits apply terrain DRM to the to-kill roll properly; they are
   also applied in the order that they hit

- crew orders no longer reset at the end of an encounter round
- changed the way that the list of possible crew orders is built; now possible for
   programme to disable orders that are not allowed in the current round (eg. 
   movement orders when tank is immbolized, etc.) and add orders for special 
   situations (eg. unbogging attempts)
- changed slightly the target score for moving and successfully changing enemy unit
   positions, but this roll is also now affected by ground mud/snow/deep snow

- fixed a bug where the identity of an enemy unit wouldn't immediately display when
   identified during spotting phase
- fixed a bug in enemy tank actions where one result was never being selected; enemy
   tanks will now propery attack friendly tanks, and will choose to target the player
   if the player fired at their front in their previous action
- fixed a bug where a crewman's bail out modifier wouldn't reset properly after an
   encounter

## Alpha 5.4 Changelog
- fixed incorrect message when enemy positions were changed
- fixed moving to new area after sunset had already triggered, hopefully also fixed
   process for replacing crew after an encounter as well
- fixed commander directing MG fire not giving a bonus to the attack
- fixed HVSS being available to tank before November, 1944
- added note when mouse cursor is over an AT gun
- fixed bailed out flag not being reset for crew after player tank was destroyed; this
   means that crew who had bailed out would not be handled properly when they had to
   bail out in the future
- changed "fire mortar" order to "fire smoke mortar" to be more clear
- added option to change reload shell type while in Fire Main Gun phase

## Alpha 5.3 Changelog
- several minor bugfixes
- smoke grenades now only last a single turn
- extended combat journal through to April 18
- added ranks for crew; promotion not possible yet
- added display for weather conditions to encounter map; weather doesn't change yet
- dice roll display now shows series of random numbers followed by each die result
   and total dice roll
- can input or randomly generate commander's name

- Note: counterattack scenario not added yet, treats instead as Battle

## Alpha 5.2 Changelog
- Smoke mortar added to tanks that have it
- Battle scenario added

## Alpha 5.1 Changelog
- Added player tank info screen to encounter and campaign day interface
- "Brew up" roll after player tank knocked out now takes into account wet stowage and
   better ammo protection of later M4A1 and M4A3 Sherman models
- Roll for player movement has been updated to a 2D6 system; previously motion forward
   or backward should have had a chance to change enemy facings but didn't, that has been
   corrected
- HVSS has a chance of being on tank models that historically had it, gives a positive
   modifier to movement
- Hits on the turret of the player tank are applied based on turret facing; previously only
   the hull facing was taken into account.
- Lead tank mechanic added. If player is not a Jumbo, then they will never be Lead Tank two
   combat days in a row. Jumbo tanks have much greater chance of being put in the front. 
- Player will now be offered a new tank model during refitting periods
- Extended combat journal through the first month of 1945; note that weather effects are
   still not implemented so no snow over the winter!
- On the encounter map, changed sector shapes and sizes, no more hexes that straddle two
   sectors, and more likely that units in medium range will be in hull front sector
- Fixed a bug where rotating the turret and firing the co-ax would not properly identify
   targets for the attack
- If an enemy AT Gun is moving, it must spend a turn emplacing itself before firing
- Updated Spotting roll to use 2D6 system
- Vehicle info, including armour levels, now displayed after right-clicking on enemy unit
- During ambush, enemy units are more likely to fire rather than reposition themselves
- Smoke factors now apply a +2 modifier to hit and to spot

## Alpha 5 Changelog
- Combat journal: campaign can be played through to Sept 1st, further dates to be added
  in the future
- Game window height reduced to 744px to fit on smaller screens
- Player tank display reorganized, thanks to input from brushfe
- If your tank is destroyed, you will be assigned a new one
- Vehicle units are now stored in a more generic format; this will also easier addition
  of new player tanks and enemy units
- To-hit and to-kill rolls for most actions are now calculated based on the core ASL
  rules, rather than using pre-calculated tables
- Additional models of sherman tank added, including better armour, loader hatch,
  as well as 76mm guns and HVAP ammo
  - some extra equipment on these tanks, such as smoke mortars, have not yet been added
- Closing the game window when the program is waiting for input should now exit the game
  immediately; good in case there's a game-crashing bug
- If loader is on Load order and main gun is fired, he cannot spot in next spotting phase
- Vehicle MGs can't fire at long range; bow MG has penalty at medium range, co-ax has no
   penalty for medium range. This is an abstraction due to the fact that AC only has three
   range bands
- Dead or incapacitated crew are properly replaced after tank is destroyed
- Expected resistence for the day will now vary based on combat journal
- New high scores screen
