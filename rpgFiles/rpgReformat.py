import random
import json
import math
from Classes.actions import Item, ItemFuncs, Specials, MoveFuncs
from Classes.playerLogic import Hero
from Classes.monsterLogic import Monster
import gameLogic
import time

def topBar():
    print('------------------/\------------------')

def bottomBar():
    print('------------------\/------------------')
def bar():
    print('--------------------------------------')
    time.sleep(1)


# Create game dto object
# Contain a player dto object and a monster dto object (basically classes we have but work on seeing how to hold information
# DB will hold player level, monsters slain, current player/monster stats
# Create a login
# Create a player save option
# See about implementing a visual loading bar using embeds and emojis
# Items and moves will be stored in there own embeds
# Create a back arrow
# Create embed card for the monster
# Maybe implement choice cards for the encounter system
# Look at isekaid bot and use individual embeds for the encounters and actions




def main():
                
    allItems = Item.itemSpawn(ItemFuncs.getFuncDictionary())
    allMoves = Specials.moveSpawn(MoveFuncs.getMoveDict())
    turn = 0
    

    print("Welcome to Michael and Bichael's slime massacre RPG.\nDo you want to play as Michael or Bichael?")
    heroName = input()
        

    if heroName == 'Michael' or heroName == 'Bichael':

        hero = Hero.heroSelection(heroName)
        print(hero)

        print('Your epic begins now!')

        while True:
            # This loop makes the game infinite
            time.sleep(.45)
            enemy = gameLogic.encounter()
            koProtection = True

            while not(hero.currentHp <= 0 or enemy.currentHp <= 0):

                if turn == 0:

                    # Player turn
                    print(hero)
                    print(enemy)

                
                    time.sleep(1)
                    topBar()
                    action = print(f'What will {heroName} do?\n1. Attack\n2. Special Move\n3. Look at Inventory \n4. Pass\n5. Run Away\n6. End Game') # This will be tied to the discord ui
                    bottomBar()
                    action = int(input())
                    if action == 1:
                        time.sleep(1)
                        Hero.attack(hero,enemy)
                        bar()

                        turn = 1

                        

                    elif action == 2:
                        
                        
                        index = Hero.movesAccess(hero,allMoves)
                        movels = list(hero.moves)

                        while True:
                                print(f'Type the name of the item that you want to use or type "close" to close the inventory\n')
                                bar()
                                choice = input()


                                if choice.isdigit() and not(int(choice) <= 0) and not(int(choice) >= index):
                                    choice = int(choice)
                                    
                                    #Write code for item use
                                    currentMove = allMoves[movels[choice-1]]
                                    ManaCost = Specials.costCalc(currentMove.cost,hero)
                                    if ManaCost > hero.manaCurrent:
                                        print(f"{hero.name} doesn't have enough mana")
                                    else:
                                        # Now we get into the item use code
                                        print(f'{heroName} used {currentMove.name}.')
                                        print(currentMove.active(hero, enemy))
                                        turn = 1
                                        break
                                    

                                
                                elif choice == 'close':
                                    break
                                else:
                                    print('Please give a valid input.')
                            
                    elif action == 4:

                        Hero.passTurn(hero)
                        bar()
                        turn = 1

                    elif action == 3:

                        if hero.inventory == {}:
                            print(f"{heroName}'s inventory is empty.")
                        else:
                            index = Hero.inventoryAccess(hero, allItems)
                            inventoryls = list(hero.inventory)
                            
                            
                            while True:
                                choice = input(f'Type the name of the item that you want to use or type "close" to close the inventory\n')
                                if choice.isdigit() and not(int(choice) <= 0) and not(int(choice) >= index):
                                    choice = int(choice)
                                    #Write code for item use
                                    currentItem = allItems[inventoryls[choice-1]]
                                    
                                    # Now we get into the item use code
                                    print(f'{heroName} used a {currentItem.name}.')
                                    print(currentItem.use(hero, enemy))
                                    turn = 1
                                    
                                    break
                                
                                elif choice == 'close':
                                    break
                                else:
                                    print('Please give a valid input.')

                    elif action == 5:
                        #respite
                        print(f'{heroName} ran away...')
                        enemy = None
                        i = 0
                        while i < 3:
                            time.sleep(.45)
                            print("...")
                            i += 1
                        print("You come across a large clearing.")
                        while True:
                            
                            enemy = None
                            print(f"What do you want to do?\n 1. Use Item\n2. Relax\n3. Continue")
                            choice = input()
                            input("just ctrl c")
                            if choice == 1:
                                
                                print(f"{hero.name} looks inside his bag.")
                                if hero.inventory == {}:
                                    print("It is empty")
                                else: 
                                    index = Hero.inventoryAccess(hero, allItems)
                                    inventoryls = list(hero.inventory)

                                    while True: 
                            
                        

                    elif action == 6:
                        print("Exiting game!!")
                        exit()

                    else:

                        print('Please give a valid input')

                    if enemy.currentHp <= 0:

                            print(f'You defeated the {enemy.name}!')
                            gameLogic.rewards(hero,enemy)
                            turn = 0
                            bar()
                            
                            break



                elif turn == 1:

                        
                    Monster.attack(enemy,hero)
                    if koProtection and hero.currentHp <= 0:
                        print(f"{heroName} did not succumb...")
                        hero.currentHp = 1
                    koProtection = False
                    bar()
                    turn = 0

                if hero.currentHp <= 0:
                    print(f'{heroName} blacks out....\n Game Over')
                    exit()
                    

            
if __name__ == '__main__':
    main()       