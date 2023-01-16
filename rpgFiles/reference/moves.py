
# {"Michael":{
#     "atk": 14,
#     "defense": 13,
#     "maxHp": 100,
#     "magic": 14,
#     "level": 5,
#     "agil": 1,
#     "luck": 0,
#     "maxMana": 30,
#       "moves": ["Fireball", "MassHeal"]
# }

hero = {}
enemy = {}
class MoveFuncs:

    # same number of inputs
    def fireball(caster, target):
        dmg = caster.magic * (caster.luck + 1)
        caster.currentMana -= 5
        target.hp -= dmg
        print("Fireball just did a shitton of dmg!!" + dmg)

    def massheal(caster, target):
        caster.hp += 50
        print("U just healed a shitton of hp")


movesDict = {
"Fireball": MoveFuncs.fireball
}

#display choices

for index in range(len(hero.moves)):
    print(f"{index}.{hero.moves[index]}")


# player inputs their move
selectedMove = int(input("Pick a move"))


# get string of the move from the hero move list
spellName = hero.moves[selectedMove]


# invoke function with that key from the moveDict
movesDict[spellName](hero,enemy)




