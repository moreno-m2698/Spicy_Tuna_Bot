import random
import json
import math





class Unit:
    def __init__(self, name: str, atk: int, defense: int, maxHp: int, magic: int, level: int, agil: int, luck: int):
        self.name = name
        self.atk = atk
        self.defense = defense
        self.maxHp = maxHp
        self.currentHp = self.maxHp
        self.magic = magic
        self.agil = agil
        self.luck = luck
        self.level = level

    def __str__(self):
        return f' {self.name}: Health:{self.currentHp}/{self.maxHp}' 

    def dodge(self):
        success = 1 == random.randint(1, 100 -  (4 * self.agil) - self.luck)
        if success:
            print(f'{self.name} dodged the attack!')
        return success

    
    def attack(self, target):

        print(f'{self.name} attacked the {target.name}!')

        if not(Unit.dodge(target)):
            

            critChance = random.randint(1, 50 - (2 * self.luck) - self.agil)
            damage = 0
            if critChance == 1:
                print('It was a critical hit!')
                damage = int(self.atk * 100 / (100 + target.defense) * 2)
            else:
                damage = int(self.atk * 100 / (100 + target.defense))

            print(f'{self.name} did {damage} damage.')
            target.currentHp -= damage

            return target.currentHp
        

    
    
    
    
    
    
    
    
    
    
    
    
    
    #def attack(self, target): ***This was an experiment with ternary operators
        # damage = 0
        # #ternary operator example
        # modifier = (critChance == 9) if 2 else 1
        # damage = self.atk * 100 / (100 + slime.defense) * modifier
        # # damage = self.atk * 100 / (100 + slime.defense) * ((critChance == 9) if 2 else 1)
        # hitString = (critChance == 9) if f"Slime got critically hit for {damage}." else f"Slime got hit for {damage}."
        # print(hitString)
    
    
    # def generateMonsterJSON():
    #     monsterFile = open('JSON/monsterList.json')
    #     monsterSelect = json.load(monsterFile)

    #     slime = monsterSelect[0]


    #     return Monster(slime['atk'], slime['defense'], slime['maxHp'], slime['currentHp'], slime['type'])
       

    # come back and work on how to spawn in units later


