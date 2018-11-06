########### Seyhan Van Khan
########### Vietnam War Game
########### November 2018
""" CLASSES LIST
    Array:
        Place(name, coordinates)
        SpaceEmpty(coordinates)
        RandCoord()
        FindPos(element)
        CheckMaxCoor(coordinates)
        DistanceBetween(object1, object2)
        OutputWarZone()

    Race(Array):
        ShowStats()
        Pos(xy)
        Energy_Points()
        ChangeWeapon(new_weapon1)
        ChangeEP(amount)
        Change_Health(amount)
        ChangeAccuracy(amount)
        SetName(boardname, displayname)
        InputAttack(opponents, mine=None)
        Attack(attacked, weapon, coordinates)
        InputMove()
        Move(horizontal, vertical)

    American(Race)

    Vietnamese(Race)

    Weapon(Array):
        EPCost()
        Attack()
        CalculateDamage()

    Mine(Weapon):
        PlaceMine()
        OverMine(coordinates)

    M16(Weapon)

    AK47(Weapon)

    Tank(Weapon)

    Sniper(Weapon)
"""


from random import randint, choice


################################# WARZONE CLASS ################################


class Array:
    """ Contains the shared 2d warzone array, in which the soldiers fight in
    + a map of location of mines"""
    empty = "---"
    warzonelength = 10
    warzone = [["---"] * 10 for i in range(10)]
    Map = [[""] * 10 for i in range(10)]

    def Place(name, coordinates):
        # Places a string name in a specfic position (coordinate) in warzone array
        xcor, ycor = Array.CheckMaxCoor(coordinates)
        Array.warzone[ycor][xcor] = name

    def SpaceEmpty(coordinates):
        # Checks if the given coordinate is free & empty
        xcor, ycor = Array.CheckMaxCoor(coordinates)
        return True if Array.warzone[ycor][xcor] == "---" else False

    def RandCoord():
        # Creates a random free & empty coordinate
        while True:
            xrand, yrand = randint(0, len(Array.warzone[0]) - 1), randint(0, len(Array.warzone) - 1)
            if Array.SpaceEmpty((xrand, yrand)):
                return xrand, yrand

    def FindPos(element):
        # Finds the position of an element given its board name
        for row in Array.warzone:
            if element in row:
                break
        return row.index(element), Array.warzone.index(row)

    def CheckMaxCoor(coordinates):
        # Adjusts coordinates to fit within the boundaries of the warzone array
        xcor, ycor = coordinates
        x = 0 if xcor < 0 else (9 if xcor > 9 else xcor)
        y = 0 if ycor < 0 else (9 if ycor > 9 else ycor)
        return x, y

    def DistanceBetween(object1, object2):
        # Calculates the distance between 2 objects using pythagoras' theorem
        # (change in x)^2 + (change in y)^2 = c^2
        if type(object1) == tuple or type(object1) == list:
            x1, y1, = Array.CheckMaxCoor(object1)
            x2, y2, = Array.CheckMaxCoor(object2)
        else:
            x1, y1 = Array.CheckMaxCoor(object1.Pos())
            x2, y2 = Array.CheckMaxCoor(object2.Pos())

        return ((y2 - y1) ** 2 + (x2 - x1) ** 2) ** 0.5

    def OutputWarZone():
        # Outputs the current warzone array
        for n in range(10):
            print("   " + str(n), end='')
        print()
        i = 0
        for row in Array.warzone:
            print(i, end=' ')
            i += 1
            for elem in row:
                print(elem, end=' ')
            print()
        print()


################################## RACES CLASS #################################


class Race(Array):
    """ Contains the attributes & methods for all races / soldiers """
    def __init__(self, playerID, displayname, boardname, weapon1, start_energy_points, accuracy, start_pos):
        # The name showed in terminal
        self.displayname = displayname + str(playerID)
        # The name showed in the warzone array
        self.boardname = boardname + str(playerID)
        # Character's main weapon (other than mines)
        self.weapon1 = weapon1
        # Composes a Mine object for each race to use
        self.mine = Mine()
        self._maxhealth = self.health = 100
        # Each soldiers must manage their energy points
        # Used to move, attack, place mines
        # +5 for every kill
        # +1 for not moving in 1 turn
        self._energy_points = start_energy_points
        # Affects the damage done when attacking
        self._accuracy = accuracy
        # Its position / coordinate
        self.xcor, self.ycor = start_pos
        Array.warzone[self.ycor][self.xcor] = self.boardname

    def ShowStats(self):
        # Prints in terminal the top important stats for the soldier
        # Health, EP remaining, current main weapon
        print(self.displayname)
        print("Health:", self.health, "\t\tEP:", self._energy_points, "\t\tWeapon:", self.weapon1.name)
        input()

    def Pos(self, xy='xy'):
        # Returns the objects current position in the warzone array
        # Function can be specified for just x or y coordinate
        x, y = 'x' in xy, 'y' in xy
        if x and y:
            return self.xcor, self.ycor
        if x:
            return self.xcor
        if y:
            return self.ycor

    def Energy_Points(self):
        return self._energy_points

    def ChangeWeapon(self, new_weapon1=None):
        # Changes the main weapon and aggregates the new weapon onto the object
        if new_weapon1 is not None:
            self.weapon1 = new_weapon1

    def ChangeEP(self, amount):
        self._energy_points += amount

    def Change_Health(self, amount):
        self.health += amount
        if self.health > self._maxhealth:
            self.health = self._maxhealth

    def ChangeAccuracy(self, amount):
        # To make the game equal or to change the difficulty
        self._accuracy += amount

    def SetName(self, boardname="", displayname=""):
        # Reset the display and board name
        if displayname:
            self.displayname = displayname
        if boardname:
            self.boardname = boardname

    def InputAttack(self, opponents, mine=None):
        # Player inputs attack
        # Inputs coordinate and checks attack is valid
        if mine is not None:
            if self.mine._left == 0:
                print("You have no more mines.")
                return 0
            if self._energy_points < self.mine.EPCost():
                print("You don't have enough energy points")
                return 0
            print("Choose a coordinate to place mine")
            while True:
                try:
                    xy = tuple(int(x.strip()) for x in input().split(','))
                    if Array.DistanceBetween(self.Pos(), xy) <= 1.5:
                        break
                    print("Must be within 1 square of position")
                except ValueError:
                    continue
            self.Attack(None, "mine", xy)
        else:
            print("Choose a coordinate to attack (x,y): ")
            while True:
                try:
                    xy = tuple(int(x.strip()) for x in input().split(','))
                    break
                except ValueError:
                    continue
            for opp in opponents:
                if opp.Pos() == xy:
                    self.Attack(opp)
                    break

    def Attack(self, attacked=None, weapon=None, coordinates=None):
        # Calls the attack function in the aggregated main weapon class
        # OR calls the Mine placing function in composed Mine class at certain coordinates
        if weapon is None:
            weapon = self.weapon1.Attack(self, attacked)
        elif self._energy_points > self.mine.EPCost():
            self.ChangeEP(-self.mine.EPCost())
            self.mine.PlaceMine(self, coordinates)


    def InputMove(self):
        # Player chooses direction and magnitude of movement
        # Checks the move is valid and possible
        # If no movement, player recieves 1 EP
        while True:
            while True:
                direction = input("Move vertical or horizontal: ").lower()
                if "v" in direction:
                    x, y = 0, 1
                    break
                if "h" in direction:
                    x, y = 1, 0
                    break

            orig_x, orig_y = self.Pos()
            try:
                movement = int(input("Number of squares: "))
            except ValueError:
                print("Please enter an integer")
                continue
            if movement == 0:
                self.ChangeEP(1)
                return 0
            if movement <= self._energy_points and Array.SpaceEmpty((orig_x + x * movement, orig_y + y * movement)):
                break

            if movement > self._energy_points:
                print("You don't have enough energy points to move that far")
            else:
                print("Try a different location!")

        self.Move(x * movement, y * movement)


    def Move(self, horizontal, vertical):
        # Moves the object's name and coordinates to a new point in the warzone array
        # Checks if they stepped over mine and calculates damage from function in Weapon class
        if abs(horizontal + vertical) <= self._energy_points:
            Array.warzone[self.ycor][self.xcor] = Array.empty
            self.ChangeEP(-abs(horizontal + vertical))

            self.xcor, self.ycor = Array.CheckMaxCoor((self.xcor + horizontal, self.ycor + vertical))

            Array.warzone[self.ycor][self.xcor] = self.boardname
            overmine, name = self.mine.OverMine(self.Pos())
            if overmine:
                damage = self.mine.CalculateDamage(name, self)
                self.Change_Health(-damage)
                print("%s has stepped over a mine placed by %s and lost %s damage." % (self.displayname, name.displayname, damage))



class American(Race):
    """ Class inheriting Race attributes and methods
        and changing values based to fit a American Soldier in the Vietnam War """
    def __init__(self, id, weapon1, start_pos):
        super().__init__(playerID=id, displayname="US Soldier #", boardname="US",
                        weapon1=weapon1, start_energy_points=20, accuracy=70,
                        start_pos=start_pos)


class Vietnamese(Race):
    """ Class inheriting Race attributes and methods
        and changing values based to fit a Vietnamese Soldier in the Vietnam War """
    def __init__(self, id, weapon1, start_pos):
        super().__init__(playerID=id, displayname="Vietcong #", boardname="VC",
                        weapon1=weapon1, start_energy_points=20, accuracy=62,
                        start_pos=start_pos)


################################# WEAPONS CLASS ################################


class Weapon(Array):
    """ Used to attack and cause damage
        Inherits Array class in order to access Warzone array and functions """
    def __init__(self, name, damage_per_hit, reloadtime, accuracy, range, rangemodifier, EP_cost):
        self.name = name
        self._damage_per_hit = damage_per_hit
        self._reload_time = reloadtime
        self._accuracy = accuracy
        self._range = range
        # How the damage changes as the distance of shot increases
        self._rangemodifier = rangemodifier
        # The cost in EP of firing once
        self._EP_cost = EP_cost

    def EPCost(self):
        return self._EP_cost

    def Attack(self, attacker, attacked):
        # Calculates damage done & reduces the health of the attacked
        # Checks attack if valid & possible
        damage_done = self.CalculateDamage(attacker, attacked)

        if damage_done == 0:
            print(attacker.displayname, "missed his shot at", attacked.displayname)

        elif attacker.Energy_Points() >= self.EPCost():
            attacker.ChangeEP(-self.EPCost())
            print(attacker.displayname, "has fired at", attacked.displayname)
            attacked.Change_Health(-damage_done)
            print("Damage done:", damage_done)

        else:
            print("%s doesn't have enough EP (attack costs %s EP)" % (attacker.displayname, self.EPCost()))
        input()

    def CalculateDamage(self, attacker, attacked):
        # Calculates the actual damage depending on:
            # Its base damage
            # The weapon's & shooter's accuracy combined
            # The weapon's maximum range
            # Its range modifier - how damage changes over distance
        # See graph for a visual representation of determining the damage algorithm
        # https://www.desmos.com/calculator/yjr3ixiwhc
        distance = Array.DistanceBetween(attacker, attacked)
        if distance < self._range:
            rand1 = randint(0,100)
            aim_chance = round((attacker._accuracy + self._accuracy) / 2)
            if rand1 < aim_chance:
                damage = self._damage_per_hit * randint(aim_chance, 100) / 100
            else:
                damage = self._damage_per_hit * randint(50, 50 + (aim_chance % 50)) / 100

            return round(damage * (self._rangemodifier ** (distance / 2)))
        else:
            print(attacker.displayname, "is too far away!")
            return 0


class Mine(Weapon):
    """ Mine weapon """
    def __init__(self):
        super().__init__("MINE", 50, 0, 90, 1.5, 0.85, 5)
        self._left = 1

    def PlaceMine(self, opponent, coordinates):
        # Places a mine by placing on the mine map array
        if self._left > 0:
            xcor, ycor = Array.CheckMaxCoor(coordinates)
            Array.Map[ycor][xcor] = opponent
            print("Someone has planted an M14 mine.")
            self._left -= 1
            input()

    def OverMine(self, coordinates):
        # Checks if the coordinates of warzone array match the coordinates of a mine in map array
        xcor, ycor = Array.CheckMaxCoor(coordinates)
        element = Array.Map[ycor][xcor]
        return element != "", element


class M16(Weapon):
    """ M16 SubMachine Gun weapon - American """
    def __init__(self):
        super().__init__("M16", 44, 1, 67, 6, 0.64, 2)

class AK47(Weapon):
    """ AK47 SubMachine Gun weapon - Vietnamese """
    def __init__(self):
        super().__init__("AK47", 50, 0.5, 70, 5, 0.62, 1)

class Tank(Weapon):
    """ Tank Heavy weapon - American """
    def __init__(self):
        super().__init__("TANK", 60, 10, 75, 20, 0.80, 3)

class Sniper(Weapon):
    """ Sniper Heavy weapon - Vietnamese """
    def __init__(self):
        super().__init__("SNIPER", 54, 5, 81, 20, 0.84, 4)
