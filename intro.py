########### Seyhan Van Khan
########### Vietnam War Game
########### November 2018

def Bold(string):
    return '\033[1m' + string + '\033[0m'

opening = ("""Welcome to the Vietnam War.

I see you already have 20 energy points..
(Energy points are used for moving or attacking)

2 sides: the """ + Bold('AMERICANS') + " and " + Bold('VIETNAMESE') + """

Each side - 2 """ + Bold('WEAPON') + """ choices:
1. Light and quick SMG
2. A heavy, slow but POWERFUL weapon
( Each also get 1 mine to place around map )

Americans: """ + Bold('M16') + " and " + Bold('TANK') + """
Vietnamese: """ + Bold('AK47') + " and " + Bold('SNIPER') + """

Each round consist of a turn per player:
1. """ + Bold('Moving') + """ (-1 EP per square) (+1 if no moving)
2. """ + Bold('Attacking') + """ (-1 or -3 EP per attack)
If """ + Bold('EP == NONE') + ", you " + Bold('SKIP') + """ your turn until you have EP again!

At the end of each round, you also slightly """ + Bold('HEAL') + """

NB:
The same shot from the the same gun and player with never be exactly the same.
There is a """ + Bold('small random element to damage') + """ but are largely affected by:

-    The gun's """ + Bold('range') + """
-    The gun's """ + Bold('base damage') + """
-    The gun's """ + Bold('accuracy') + """
-    The soldier's """ + Bold('accuracy') + """

Remember to keep an eye on your remaining ENERGY POINTS (EP)!

""").splitlines()



def IntroduceGame(skip_menu):
    if not skip_menu:
        see_menu = input("Would you like to see the introduction? (yes / no) ").lower()
        if "y" in see_menu:
            for line in opening:
                if bool(line):
                    print(line)
                else:
                    input()
