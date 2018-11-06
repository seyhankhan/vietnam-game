########### Seyhan Van Khan
########### Vietnam War Game
########### November 2018

from random import randint, choice
from shutil import get_terminal_size

from intro import IntroduceGame
from classes import *


################################### CONSTANTS ##################################


# Number of columns in terminal
columns = get_terminal_size().columns
# Whether to skip the text introduction to the game
skip_menu = False
# The number of opponents
num_opponents = 3


##################################### INTRO ####################################


IntroduceGame(skip_menu)


################################### CREATION ###################################


races = ["us", "american", "viet", "vietnamese"]
m16, ak47, tank, sniper = M16(), AK47(), Tank(), Sniper()
# List of all possible main weapon choices
weapons = [m16, tank, ak47, sniper]
weapon_names = [gun.name for gun in weapons]

while True:
    # Establish race
    raceinput = input("US or Vietnamese: ").lower()
    if raceinput in races:
       break

while True:
    # Establish main weapon
    print('\t'.join(gun.name for gun in weapons))
    weaponinput = input("Weapon: ").upper()
    correct_gun = False
    # Checks whether weapon is valid & avaiable
    for gun in weapons:
       if weaponinput == gun.name.upper():
           weapon = gun
           correct_gun = True
           break

    if correct_gun:
        # Checks the weapon matches the race
        if (races.index(raceinput) < 2 and weapon_names.index(weaponinput) < 2 or
        races.index(raceinput) > 1 and weapon_names.index(weaponinput) > 1
        ):
            break
        else:
            print("\nWeapon must match race.")
    else:
        print("\nPlease choose from the above weapon choices")

# Initiliases the opponents list
# Will contain all opponent objects to iterate through during turns
opponents = []

# If race is AMERICAN
if races.index(raceinput) < 2:
    # Initiliases object player with an ID of 1 and random starting coordinate
    player = American(1, weapon, Array.RandCoord())
    player.displayname = "US Soldier (You)"
    # Creates a number of opponents of opposite race
    # with a matching random weapon (SMG more likely) based on num_opponents
    for i in range(num_opponents):
        opponents.append(Vietnamese(i + 1, choice((weapons[2], choice(weapons[2:]))), Array.RandCoord()))

# If race is VIETNAMESE
else:
    player = Vietnamese(1, weapon, Array.RandCoord())
    player.displayname = "Vietnamese (You)"
    for i in range(num_opponents):
        opponents.append(American(i + 1, choice((weapons[0], choice(weapons[:2]))), Array.RandCoord()))

# Renames the player displayname
player.SetName("YOU")
player.Move(0,0)

# Accuracy is increased for player and decreased for all opponents
# As there is 1 player to multiple opponents
player.ChangeAccuracy(20)
for opp in opponents:
    opp.ChangeAccuracy(-20)


################################### MAIN LOOP ##################################


roundnum = 0
# Game doesn't end until player dies or wins (by killing all opponents)
while True:
    roundnum += 1
    # Prints round number at center of terminal
    print(("ROUND " + str(roundnum) + ":").center(columns))


    """ Show stats of all soldiers """
    player.ShowStats()
    for opp in opponents:
        opp.ShowStats()

        """ Displays the shared warzone of all soldiers """
    Race.OutputWarZone()


    """ Players turn """
    # Step 1: Move
    player.InputMove()

    # Step 2: Choose attack
    while True:
        attacktype = input("Attack type? (main / mine / none) ").lower()
        if "none" in attacktype or "main" in attacktype or "mine" in attacktype and player.Energy_Points() > player.mine.EPCost():
            break

    # Step 2: Attack
    if "main" in attacktype:
        player.InputAttack(opponents)
    else:
        player.InputAttack(opponents, True)

        """ Checks for opponent deaths """
    havedied = []
    for opp in opponents:
        # If opp is dead
        if opp.health <= 0:
            havedied.append(opp)
            # Set board name to XX
            opp.SetName(boardname="XXX")
            opp.Move(0,0)
            # Player receives 5 EP reward for each kill
            player.ChangeEP(5)
            print(opp.displayname, "has died. +5 Energy Points\n")

    for deadopp in havedied:
        opponents.remove(deadopp)

        """ Opponents turn """
    for opp in opponents:
        while True:
            # Create a movement that moves each opponent randomly but closer to player
            move_x = choice([True, False])
            movement = randint(-2,2)
            x, y = int(move_x) * movement, int(not(move_x)) * movement
            opp_x, opp_y = opp.Pos()
            # If the new position is free & is closer to player
            if (Array.SpaceEmpty((opp_x + x, opp_y + y)) and
                Array.DistanceBetween(player.Pos(), (opp_x + x, opp_y + y)) < Array.DistanceBetween(player, opp) + 0.5
                ):
                break
        # Step 1: Move
        opp.Move(x, y)
        print(opp.displayname, "has moved to", opp.Pos())

        # Step 2: Attack
        opp.Attack(player)

        """ Natural Healing Per Turn """
        opp.Change_Health(8)

    # Step 2: Attack - MINES
    # Outside of opponents turn loop so the mine placer is unknown
    for opp in opponents:
        if randint(0,10) > 7 and opp.Energy_Points() > 7:
            mine_pos = Array.CheckMaxCoor((opp.Pos("x") + choice([-1,1]), opp.Pos("y") + choice([-1,1])))
            opp.Attack(player, True, mine_pos)

    """ Natural Healing Per Turn """
    player.Change_Health(10)

    """ Checks if player dead """
    if player.health <= 0:
        print("YOU DIED")
        break
        """ Checks if player won """
    # If all opponents dead
    if len(opponents) == 0:
        print("YOU WIN")
        break
