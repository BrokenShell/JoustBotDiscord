import pickle
from joust.gear import Weapon, Armor, Shield
from joust.knights import Knight, joust


def get_name(author):
    name, _ = str(author).split("#")
    return name


def save_knight(knight: Knight, player=None):
    file_name = player if player else knight.name
    pickle.dump(knight, open(f'./characters/{file_name}.joust', 'wb'))


def open_knight(name: str) -> Knight:
    try:
        return pickle.load(open(f'./characters/{name}.joust', 'rb'))
    except FileNotFoundError:
        return Knight(name)


def make_knight(name, rank):
    knight = Knight(name)
    knight.equip_best()
    while knight.rank < rank:
        joust(knight, Knight('Gray Knight'))
    save_knight(knight)
    return knight


def edit_knight(name,
                new_name=None, background=None, gold=None,
                weapon=False, armor=False, shield=False,
                war_chest=None):
    knight = open_knight(name)
    if new_name:
        knight.name = new_name
    if background:
        knight.background = background
    if gold:
        knight.gold = gold
    if weapon:
        knight.weapon = Weapon()
    if armor:
        knight.armor = Armor()
    if shield:
        knight.shield = Shield()
    if war_chest:
        n = max(len(knight.inventory), war_chest)
        knight.inventory = [Weapon() for _ in range(n)]
    save_knight(knight)
    return knight


# if __name__ == '__main__':
#     broken = make_knight("Broken", 25)
#     print(broken.details())
#     broken.remove_bonuses(broken.weapon)
#     weapon = Weapon('Dragonlance of the Zodiac')
#     weapon.bonuses = (5, 5, 5)
#     armor = Armor('Field Plate of the Zodiac')
#     armor.name = 'Field Plate of the Zodiac'
#     armor.bonus = 5
#     shield = Shield('Dragonscale Jousting Shield')
#     shield.bonus = 10
#     broken.weapon = weapon
#     broken.armor = armor
#     broken.shield = shield
#     broken.apply_bonuses(weapon)
#     print()
#     save_knight(broken, "Broken")
#     print(broken.details())
