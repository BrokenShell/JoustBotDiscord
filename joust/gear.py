from Fortuna import TruffleShuffle, RandomValue, front_linear, percent_true


class Weapon:
    weapons = {
        'Sword': 1,
        'Flail': 1,
        'Battleaxe': 1,
        'Morningstar': 1,
        'Greatsword': 2,
        'Spear': 2,
        'Pike': 2,
        'Glaive': 3,
        'Halberd': 3,
        'Lance': 3,
    }
    random_weapon = RandomValue(weapons.keys(), zero_cool=front_linear)
    modifiers = {
        ' of the Owl': (1, 0, 0),
        ' of the Wolf': (0, 1, 0),
        ' of the Pixie': (0, 0, 1),
        ' of the Raven': (2, 0, 0),
        ' of the Lion': (0, 2, 0),
        ' of the Dryad': (0, 0, 2),
        ' of the Fool': (0, 0, 0),
        ' of the Dragon': (3, 0, 0),
        ' of the Sphinx': (0, 3, 0),
        ' of the Unicorn': (0, 0, 3),
        ' of the Gorgon': (3, 0, 3),
        ' of the Righteous': (0, 3, 3),
        ' of the Titan': (3, 3, 0),
        ' of the Zodiac': (3, 3, 3),
    }
    random_suffix = RandomValue(modifiers.keys(), zero_cool=front_linear)

    def __init__(self, name=None):
        if name:
            self.weapon = None
            self.bonus = 0
            self.name = name
            self.bonuses = (0, 0, 0)
        else:
            self.weapon = self.random_weapon()
            self.bonus = self.weapons[self.weapon]
            self.suffix = ''
            if percent_true(25):
                self.suffix = self.random_suffix()
                self.bonuses = self.modifiers[self.suffix]
            else:
                self.bonuses = (0, 0, 0)
            self.name = f'{self.weapon}{self.suffix}'
        self.value = self.bonus + sum(self.bonuses)

    def __str__(self):
        return self.name


class Armor:
    random_color = TruffleShuffle((
        'Red', 'Blue', 'Green',
        'Yellow', 'Purple', 'Orange',
        'Black', 'White', 'Gray',
        'Magenta', 'Indigo', 'Pink',
    ))
    modifiers = {
        'Tunic': 0,
        'Leather': 1,
        'Studded Leather': 1,
        'Chain Mail': 2,
        'Scale Mail': 2,
        'Field Plate': 3,
    }
    random_armor = RandomValue(modifiers.keys(), zero_cool=front_linear)

    def __init__(self, name=None):
        self.color = self.random_color()
        if name:
            self.armor = None
            self.bonus = 0
            self.name = f'{self.color} {name}'
        else:
            self.armor = self.random_armor()
            self.bonus = self.modifiers[self.armor]
            self.name = f'{self.random_color()} {self.armor}'

    def __str__(self):
        return self.name


class Shield:
    materials = {
        'Wooden': 0,
        'Bronze': 1,
        'Iron': 2,
        'Dragonscale': 3,
    }
    random_material = RandomValue(materials.keys(), zero_cool=front_linear)
    shields = {
        'Shield': 1,
        'Heater Shield': 2,
        'Kite Shield': 3,
        'Jousting Shield': 4,
    }
    random_shield = RandomValue(shields.keys(), zero_cool=front_linear)

    def __init__(self, name=None):
        if name:
            self.material = None
            self.shield = None
            self.bonus = 0
            self.name = name
        else:
            self.material = self.random_material()
            self.shield = self.random_shield()
            self.bonus = self.materials[self.material] + self.shields[self.shield]
            self.name = f'{self.material} {self.shield}'

    def __str__(self):
        return self.name


if __name__ == '__main__':
    # print(Weapon('Rolling Pin'))
    # print(Armor('Wine Barrel'))
    # print(Shield('Saucepan Lid'))

    arr = [Weapon('Bowling Pin'), Weapon(), Weapon(), Weapon()]
    print(*arr, sep=', ')
    arr.sort(key=lambda x: x.value)
    print(*arr, sep=', ')
