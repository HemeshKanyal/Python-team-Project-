import random

inventory = []
player_stats = {
    "health": 100,
    "attack": 10,
    "disarm_skill": 1,
    "gold": 100 
}

enemy_stats = {
    "health": 50,
    "attack": 5
}

def practice_disarming():
    print("You approach a training trap. The instructor sets the difficulty...")

    difficulty = random.randint(1, 5)
    print(f"The practice trap's difficulty level is {difficulty}.")

    base_success_rate = 0.4
    skill_modifier = player_stats["disarm_skill"] * 0.1
    success_chance = base_success_rate + skill_modifier - (0.05 * difficulty)
    success_chance = max(0.1, min(success_chance, 0.9))

    print(f"Your success chance is {int(success_chance * 100)}%.")

    if random.random() < success_chance:
        print("You successfully disarm the training trap! Your skill improves.")
        increase_disarm_skill()
    else:
        print("You fail to disarm the training trap. Keep practicing!")

def disarm_npc_interaction():
    print("You meet a wise Trapmaster NPC.")
    print("The Trapmaster offers to train you in the art of disarming traps.")

    choice = input("Do you wish to accept the Trapmaster's training? (yes/no): ").lower()
    if choice == "yes":
        print("The Trapmaster sets up a series of increasingly difficult traps for you...")
        for _ in range(3):
            practice_disarming()
        print("The Trapmaster nods in approval of your progress.")
    else:
        print("You politely decline the training and move on.")

def practice_room():
    print("You have entered a special Practice Room.")
    print("An instructor offers you a chance to practice your disarm skills on training traps.")

    choice = input("Would you like to practice disarming traps here? (yes/no): ").lower()
    if choice == "yes":
        practice_disarming()
    else:
        print("You decide not to practice and leave the room.")

def combat():
    global player_stats, enemy_stats
    print("A battle begins!")

    while player_stats["health"] > 0 and enemy_stats["health"] > 0:
        print("\nYou attack the enemy!")
        damage = player_stats["attack"]
        enemy_stats["health"] -= damage
        print(f"You dealt {damage} damage. Enemy health is now {enemy_stats['health']}.")

        if enemy_stats["health"] <= 0:
            print("You defeated the enemy!")
            break

        print("\nThe enemy attacks you!")
        enemy_damage = random.randint(1, enemy_stats["attack"])
        player_stats["health"] -= enemy_damage
        print(f"The enemy dealt {enemy_damage} damage. Your health is now {player_stats['health']}.")

        if player_stats["health"] <= 0:
            print("You were defeated by the enemy...")
            break

def trap_room():
    print("You have entered a suspicious-looking room...")
    traps = {
        "Spikes": {"description": "spikes shoot out of the ground", "damage": random.randint(5, 15)},
        "Poison Gas": {"description": "poisonous gas fills the room", "damage": random.randint(3, 10), "effect": "poison"},
        "Confusion Rune": {"description": "a rune lights up, confusing you", "effect": "confusion"}
    }

    trap_type = random.choice(list(traps.keys()))
    trap = traps[trap_type]
    print(f"Trap triggered! {trap['description']}.")

    choice = input("Would you like to try to disarm the trap? (yes/no): ").lower()
    if choice == "yes":
        success = attempt_disarm()
        if success:
            print("You successfully disarm the trap and avoid any damage!")
            return
        else:
            print("You failed to disarm the trap! It activates...")

    if "damage" in trap:
        player_stats["health"] -= trap["damage"]
        print(f"You take {trap['damage']} damage. Your health is now {player_stats['health']}.")

    if player_stats["health"] <= 0:
        print("The trap has claimed your life... Game over!")
        global running
        running = False

def add_to_inventory(item):
    inventory.append(item)
    print(f"You collected a {item}!")

def view_inventory():
    if inventory:
        print("Your inventory contains:")
        for item in inventory:
            print(f"- {item}")
    else:
        print("Your inventory is empty.")

def enemy_encounter():
    print("You encounter an enemy! Prepare for battle!")
    combat()
    enemy_stats["health"] = 50

def puzzle_room():
    print("You enter a room with a mysterious puzzle on the wall.")
    print("Solve the riddle to proceed:")
    print("I speak without a mouth and hear without ears. I have no body, but I come alive with wind. What am I?")

    answer = input("Your answer: ").lower().strip()
    if answer == "echo":
        print("Correct! The puzzle is solved, and you are rewarded with a health boost.")
        player_stats["health"] += 10
        print(f"Your health is now {player_stats['health']}.")
    else:
        print("Incorrect! The room's magic zaps you for failing.")
        player_stats["health"] -= 10
        print(f"Your health is now {player_stats['health']}.")

def treasure_room():
    print("You find a treasure chest! You collect some valuable items.")
    items = ["gold coin", "magic potion", "sword"]
    for item in items:
        add_to_inventory(item)

def increase_disarm_skill():
    if player_stats["disarm_skill"] < 10:
        player_stats["disarm_skill"] += 1
        print(f"Your disarm skill has increased! New skill level: {player_stats['disarm_skill']}.")

def attempt_disarm():
    base_success_rate = 0.4
    skill_modifier = player_stats["disarm_skill"] * 0.1
    success_chance = base_success_rate + skill_modifier
    success_chance = min(success_chance, 0.9)
    print(f"Your disarm skill level is {player_stats['disarm_skill']}. Success chance: {int(success_chance * 100)}%")

    if random.random() < success_chance:
        print("You successfully disarm the trap!")
        increase_disarm_skill()
        return True
    else:
        print("You failed to disarm the trap!")
        return False

def npc_trapmaster():
    print("You meet a wise Trapmaster NPC.")
    print("The Trapmaster offers to train you in the art of disarming traps.")

    choice = input("Do you wish to accept the Trapmaster's training? (yes/no): ").lower()
    if choice == "yes":
        print("The Trapmaster sets up a series of increasingly difficult traps for you...")
        for _ in range(3):
            practice_disarming()
        print("The Trapmaster nods in approval of your progress.")
    else:
        print("You politely decline the training and move on.")

def npc_merchant():
    print("\nYou encounter a merchant NPC.")
    print("The merchant offers you some items for sale.")

    print(f"Items for sale: \n1. Healing Potion (50 gold) \n2. Trap Disarm Kit (100 gold) \n3. Exit")
    choice = input("What would you like to buy? Enter item number (1-3): ")

    if choice == "1" and player_stats["gold"] >= 50:
        player_stats["gold"] -= 50
        inventory.append("Healing Potion")
        print("You purchased a Healing Potion.")
    elif choice == "2" and player_stats["gold"] >= 100:
        player_stats["gold"] -= 100
        inventory.append("Trap Disarm Kit")
        print("You purchased a Trap Disarm Kit.")
    elif choice == "3":
        print("You decide not to buy anything.")
    else:
        print("You don't have enough gold for that item.")

def npc_quest_giver():
    print("\nYou meet a Quest Giver NPC.")
    print("The Quest Giver asks you to find a rare gem and return it to them.")

    choice = input("Do you want to accept the quest? (yes/no): ").lower()
    if choice == "yes":
        print("The Quest Giver gives you the details and you head off to find the gem.")
        print("Quest: Find the Rare Gem and return to the Quest Giver.")
        quest_success = random.choice([True, False])
        if quest_success:
            print("You successfully find the Rare Gem and return it.")
            player_stats["gold"] += 200
            print("You receive 200 gold as a reward!")
        else:
            print("You couldn't find the Rare Gem this time. Better luck next time.")
    else:
        print("You decline the quest and move on.")

def npc_enemy():
    print("\nYou encounter a hostile enemy NPC!")
    print("The enemy prepares for battle...")

    player_attack = player_stats["attack"]
    enemy_health = 30
    enemy_attack = 8

    while enemy_health > 0 and player_stats["health"] > 0:
        print(f"\nYour Health: {player_stats['health']}, Enemy Health: {enemy_health}")
        action = input("What will you do? (attack/defend): ").lower()

        if action == "attack":
            enemy_health -= player_attack
            print(f"You attack the enemy for {player_attack} damage.")
        elif action == "defend":
            player_stats["health"] -= max(0, enemy_attack - 5)
            print("You defend yourself, taking reduced damage.")

        if enemy_health > 0:
            player_stats["health"] -= enemy_attack
            print(f"The enemy attacks you for {enemy_attack} damage.")

    if player_stats["health"] <= 0:
        print("You have been defeated by the enemy...")
    else:
        print("You defeated the enemy! Well done!")
        player_stats["gold"] += 50
        print("You receive 50 gold as a reward!")

def npc_healer():
    print("You encounter a kind healer NPC.")
    print("The healer offers to heal your wounds for a small fee.")

    choice = input("Do you wish to accept the healer's offer? (yes/no): ").lower()
    if choice == "yes":
        healing_amount = random.randint(10, 30)
        player_stats["health"] += healing_amount
        print(f"The healer heals you for {healing_amount} health. Your health is now {player_stats['health']}.")
    else:
        print("You decline the healer's offer and move on.")

def exit_room():
    print("Congratulations! You found the exit and escaped the dungeon.")
    global running
    running = False

dungeon_map = [
    ["Start", "Empty", "Enemy"],
    ["Puzzle", "Practice Room", "Trap"],
    ["Treasure", "NPC - Trapmaster", "NPC - Healer"],
    ["NPC - Merchant", "NPC - Quest Giver", "Exit"]
]

def display_map():
    print("Dungeon Map:")
    for r, row in enumerate(dungeon_map):
        for c, room in enumerate(row):
            if [r, c] == player_position:
                print("P", end=" ")  
            else:
                print("?", end=" ") 
        print()

player_position = [0, 0]

def search_room():
    print("You search the room...")
    discoveries = [
        "You found a gold coin!",
        "You discovered a healing potion!",
        "You found nothing of interest.",
        "You uncovered a hidden clue about the dungeon's exit!",
    ]
    discovery = random.choice(discoveries)
    print(discovery)

    if "gold coin" in discovery:
        player_stats["gold"] += 10
        print("You gained 10 gold! Current gold: {}".format(player_stats["gold"]))
    elif "healing potion" in discovery:
        inventory.append("Healing Potion")
        print("You added a Healing Potion to your inventory.")
    elif "hidden clue" in discovery:
        print("The clue says: 'The exit is in the southeast corner of the map.'")

def move_player(direction):
    global player_position
    row, col = player_position

    if direction == "north" and row > 0:
        player_position[0] -= 1
    elif direction == "south" and row < len(dungeon_map) - 1:
        player_position[0] += 1
    elif direction == "east" and col < len(dungeon_map[0]) - 1:
        player_position[1] += 1
    elif direction == "west" and col > 0:
        player_position[1] -= 1
    else:
        print("You can't move in that direction.")
        return

    row, col = player_position
    room_type = dungeon_map[row][col]
    print(f"You moved to a new room: {room_type}")

    if room_type == "Enemy":
        enemy_encounter()
    elif room_type == "Puzzle":
        puzzle_room()
    elif room_type == "Practice Room":
        practice_room()
    elif room_type == "Treasure":
        treasure_room()
    elif room_type == "Trap":
        trap_room()
    elif room_type == "NPC - Trapmaster":
        npc_trapmaster()
    elif room_type == "NPC - Healer":
        npc_healer()
    elif room_type == "NPC - Merchant":
        npc_merchant()
    elif room_type == "NPC - Quest Giver":
        npc_quest_giver()
    elif room_type == "Exit":
        exit_room()

def main():
    print("Welcome to the Escape the Dungeon Game!")
    global running
    running = True

    while running:
        print("\nPlayer Stats: ")
        print(f"Health: {player_stats['health']}, Gold: {player_stats['gold']}, Inventory: {inventory}")
        print("\nYou are in a dark room. What would you like to do?")
        print("1. Move")
        print("2. Search the room")
        print("3. Check inventory")
        print("4. View map")
        print("5. Exit game")

        choice = input("Enter your choice (1-5): ")

        if choice == "1":
            direction = input("Enter a direction to move (north/south/east/west): ").lower()
            move_player(direction)
        elif choice == "2":
            search_room()
        elif choice == "3":
            view_inventory()
        elif choice == "4":
            display_map()
        elif choice == "5":
            print("Exiting game. Goodbye!")
            running = False
        else:
            print("Invalid choice. Please select an option from 1 to 5.")

if __name__ == "__main__":
    main()