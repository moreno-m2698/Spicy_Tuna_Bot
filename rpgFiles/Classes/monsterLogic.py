import random
import math
from rpgFiles.Classes.unitLogic import Unit
import json
from rpgFiles.Classes.playerLogic import Hero

class Monster(Unit):
    def __init__(self, name: str, atk: int, defense: int, maxHp: int, magic: int, level: int, agil: int, luck: int, drops: dict):
        super().__init__(name, atk, defense, maxHp, magic, level,agil, luck)
        self.drops = drops
        self.isEpic = False
        # self.drops = drops
        # self.baseChanceDrops = baseChanceDrops
        #come back and add these

    def __str__(self):
        
        return f'{super().__str__()} |'

    def generateMonsterJSON(file):
            monsterFile = open(file)
            monsterDict = json.load(monsterFile)
    
            monsterKey = random.choice(list(monsterDict))

            monsterSubKey = random.choice(list(monsterDict[monsterKey]))
            name = f'{monsterSubKey} {monsterKey}'

            m = monsterDict[monsterKey][monsterSubKey]

            return Monster(name, m['atk'], m['defense'], m['maxHp'], m['magic'], m['level'], m['agil'], m['luck'], m['drops'])
    

