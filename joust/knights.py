from Fortuna import *
from joust.gear import Weapon, Armor, Shield


def pop_random(arr: list):
    if arr:
        return arr.pop(random_index(len(arr)))


class Knight:
    modifiers = {
        'Muggle': (1, 1, 1),
        'Dwarf': (0, 1, 2),
        'Troll': (0, 2, 1),
        'Elf': (1, 0, 2),
        'Orc': (1, 2, 0),
        'Halfling': (2, 0, 1),
        'Goblin': (2, 1, 0),
        'Nephilim': (3, 0, 0),
        'Teraphim': (0, 3, 0),
        'Seraphim': (0, 0, 3),
    }
    random_bloodline = TruffleShuffle(set(modifiers.keys()))
    farm_implements = (
        'Pitchfork', 'Rolling Pin', 'Shovel', 'Rake', 'Broom Handle',
        'Walking Stick', 'Gnarled Cane', 'Dirty Mop', 'Wooden Sword',
    )

    def __init__(self, name):
        self.name = name
        self.rank = 0
        self.bloodline = self.random_bloodline()
        self.mind, self.body, self.soul = self.modifiers[self.bloodline]
        self.background = f'Little is known about this {self.title}.'
        self.weapon = Weapon(random_value(self.farm_implements))
        self.apply_bonuses(self.weapon)
        self.armor = Armor()
        self.shield = Shield()
        self.gold = dice(10, 10)
        self.inventory = [Weapon(), Weapon(), Weapon(), Weapon(), Weapon()]

    def apply_bonuses(self, item):
        mind, body, soul = item.bonuses
        self.mind += mind
        self.body += body
        self.soul += soul

    def remove_bonuses(self, item):
        mind, body, soul = item.bonuses
        self.mind -= mind
        self.body -= body
        self.soul -= soul

    @property
    def title(self):
        if self.rank < 10:
            return 'Squire'
        elif self.rank < 20:
            return 'Knight'
        elif self.rank < 50:
            return 'Captain'
        elif self.rank < 100:
            return 'Commander'
        else:
            return 'Monarch'

    @property
    def offense(self):
        return max(self.mind, self.body, self.soul) + self.weapon.bonus

    @property
    def defence(self):
        return min(self.mind, self.body, self.soul) + self.armor.bonus

    @property
    def balance(self):
        return smart_clamp(self.mind, self.body, self.soul) + self.shield.bonus

    @property
    def score(self):
        return self.offense + self.defence + self.balance

    def details(self):
        output = (
            f'Name: {self.name}',
            f'Title: {self.title}',
            f'Rank: {self.rank}',
            f'Bloodline: {self.bloodline}',
            f'Heroic Aspects:',
            f' • Mind: {self.mind}',
            f' • Body: {self.body}',
            f' • Soul: {self.soul}',
            f'Joust Modifiers:',
            f' • Offense: {self.offense}',
            f' • Defence: {self.defence}',
            f' • Balance: {self.balance}',
            f'Equipped Gear:',
            f' • Weapon: {self.weapon}',
            f' • Armor: {self.armor}',
            f' • Shield: {self.shield}',
            f'Background: {self.background}',
            f'Gold Coin: {self.gold}',
            f'War Chest: {", ".join(set(map(str, self.inventory)))}',
        )
        return '\n'.join(output)

    def summary(self):
        output = (
            f'Name: {self.name}',
            f'Title: {self.title}',
            f'Rank: {self.rank}',
            f'Bloodline: {self.bloodline}',
            f'Equipped Gear:',
            f' • Weapon: {self.weapon}',
            f' • Armor: {self.armor}',
            f' • Shield: {self.shield}',
            f'Background: {self.background}',
        )
        return '\n'.join(output)

    def __str__(self):
        return self.summary()

    def rank_up(self):
        self.rank += 1
        if percent_true(100/3):
            self.mind += 1
        elif percent_true(50):
            self.body += 1
        else:
            self.soul += 1

    def victory(self, other_knight):
        self.rank_up()
        self.gold += d(10) + 10
        if other_knight.inventory:
            self.inventory.append(pop_random(other_knight.inventory))
        else:
            self.gold += other_knight.gold
            other_knight.gold = 0

    def equip(self, item):
        for idx, itm in enumerate(self.inventory):
            if item == itm.name:
                tmp = self.weapon
                self.remove_bonuses(self.weapon)
                self.weapon = self.inventory.pop(idx)
                self.apply_bonuses(self.weapon)
                self.inventory.append(tmp)
                break

    def equip_best(self):
        if self.inventory:
            self.inventory.sort(key=lambda x: x.value)
            weapon, best = self.weapon, self.inventory[-1]
            if weapon.value <= best.value:
                self.equip(best.name)


def turn(knight: Knight):
    a, b, c = d(20), d(20), d(20)
    attack = a + knight.offense
    block = b + knight.defence
    balance = c + knight.balance
    crit = a + b + c == 60
    return attack, block, balance, crit


def joust(attacker: Knight, defender: Knight):
    a_down, d_down = False, False
    a_points, d_points = 0, 0
    rounds = 0
    while not a_down and not d_down:
        rounds += 1
        a_attack, a_block, a_bal, a_crit = turn(attacker)
        d_attack, d_block, d_bal, d_crit = turn(defender)

        if a_attack > d_block or a_crit:
            a_points += 1
            if a_bal > d_bal or a_crit:
                a_points += 4
                d_down = True
                if a_crit:
                    break

        if d_attack > a_block or d_crit:
            d_points += 1
            if d_bal > a_bal or d_crit:
                d_points += 4
                a_down = True
                if d_crit:
                    break

        if a_points != d_points:
            if a_points > 2 or d_points > 2:
                break

    if d_down and not a_down:
        attacker.victory(defender)
        return f"After {rounds} rounds, {attacker.name} defeated {defender.name} by knockdown!"
    elif a_down and not d_down:
        defender.victory(attacker)
        return f"After {rounds} rounds, {defender.name} defeated {attacker.name} by knockdown!"
    elif a_points > d_points:
        attacker.victory(defender)
        return f"After {rounds} rounds, {attacker.name} defeated {defender.name} by points, {a_points} to {d_points}."
    elif d_points > a_points:
        defender.victory(attacker)
        return f"After {rounds} rounds, {defender.name} defeated {attacker.name} by points, {d_points} to {a_points}."
    else:
        return f"After {rounds} rounds, the joust is a tie."


if __name__ == '__main__':
    fred = Knight("Fred")
    fred.equip_best()
    george = Knight('George')
    george.equip_best()
    knights = [fred, george, Knight('Blue Knight'), Knight('Red Knight')]
    print()
