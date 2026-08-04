import sqlite3
from datetime import date

from achievements import *
from skills import *
from user import *
from util import *

# Prompts the user to create a simple account when a new user data file is created
user = getUser()
if user["username"] == None:
    username = strInput("It appears this is your first time here, please enter a username: ")
    user["username"] = username
    updateUser(user)

print(f"Hello {user["username"]}, and welcome to your skill tracker!")

while True:
    print("\nWhat would you like to do?")
    print("1. Add a New Skill " \
        "\n2. Log Progress on a Skill " \
        "\n3. View all Skills " \
        "\n4. Delete a Skill " \
        "\n5. View Profile" \
        "\n6. Exit")
    
    choice = intInput("Enter the number corresponding to your choice: ", False)

    if choice < 1 or choice > 6:
        print("No option corresponds to input, please try again")
        continue
    
    elif choice == 1: # Add a new skill -------------------------------------
        while True:
            new_skill_name = strInput("Name of the new skill: ").lower()
            if skillExistence(new_skill_name):
                print("A skill with that name already exists, please try again")
            else:
                break
        new_skill_goal = intInput("Goal number of hours: ", False)
        new_skill_hrs = intInput("Number of hours spent so far: ", True)

        addSkill(new_skill_name, new_skill_goal)
        progressSkill(new_skill_name, new_skill_hrs)

        completeAchievement(1001)

    elif choice == 2: # Make progress on a skill ----------------------------
        if checkEmptyList() == 0:
            print("You have no skills to progress")
            continue
        skillPrint()
        while True:
            update_choice = strInput("Which skill do you want to update? ").lower()
            if not skillExistence(update_choice):
                print("Skill doesn't exist, please try again")
            else:
                break

        update_hrs = intInput("Hours to add: ", True)
        progressSkill(update_choice, update_hrs)

        progressCheck(update_choice)

    elif choice == 3: # View all skills -------------------------------------
        if checkEmptyList() == 0:
            print("You have no skills in progress")
        else:
            print(f"{user["username"]}'s Active Skills: ")
            skillPrint()

    elif choice == 4: # Delete a skill --------------------------------------
        if checkEmptyList() == 0:
            print("You have no skills to delete")
            continue
        skillPrint()
        while True:
            del_choice = strInput("Which skill do you want to delete? ").lower()
            if not skillExistence(del_choice):
                print("Skill doesn't exist, please try again")
            else:
                break
        deleteSkill(del_choice)
        print("\nHere is your new list of skills:")
        skillPrint()

    elif choice == 5: # View profile ----------------------------------------
        printUser()

    elif choice == 6: # Exit
        break