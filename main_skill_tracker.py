from achievements import *
from skills import *
from user import *
from util import *

# Prompts the user to create a simple account if no user data is found
user = get_user()
if user.username is None:
    username = str_input("It appears this is your first time here, please enter a username: ")
    user.username = username
    user.save()

print(f"Hello {user.username}, and welcome to your skill tracker!")

while True:
    print("\nWhat would you like to do?")
    print("1. Add a New Skill " \
        "\n2. Log Progress on a Skill " \
        "\n3. View all Skills " \
        "\n4. Delete a Skill " \
        "\n5. View Profile" \
        "\n6. Exit")
    
    choice = int_input("Enter the number corresponding to your choice: ", False)

    if choice < 1 or choice > 6:
        print("No option corresponds to input, please try again")
        continue
    
    elif choice == 1: # Add a new skill -------------------------------------
        while True:
            new_skill_name = str_input("Name of the new skill: ").lower()
            if skill_existence(new_skill_name):
                print("A skill with that name already exists, please try again")
            else:
                break
        new_skill_hrs = int_input("Number of hours spent so far: ", True)
        while True:
            new_skill_goal = int_input("Goal number of hours: ", False)
            if new_skill_goal <= new_skill_hrs:
                print("Your goal cannot be less than or equal to the number of hours you have so far.")
            else:
                break
        skill = add_skill(new_skill_name, new_skill_goal, new_skill_hrs)
        complete_achievement(1001)

    elif choice == 2: # Make progress on a skill ----------------------------
        if check_empty_list() == 0:
            print("You have no skills to progress")
            continue
        print_all_skills()
        while True:
            update_choice = str_input("Which skill do you want to update? ").lower()
            if not skill_existence(update_choice):
                print("Skill doesn't exist, please try again")
            else:
                break
        skill = get_skill(update_choice)
        update_hrs = int_input("Hours to add: ", True)
        skill.add_progress(update_hrs, user)
        if skill.is_complete():
            complete_achievement(1004)
            print(f"Congratulations! You've reached your goal for {skill.name}!")
            user.addXp(skill.xp_value)
            user.save()
            while True: 
                choice = int_input("Would you like to (1) update your goal or (2) remove the skill from your to-do list? ", False)
                if choice == 1 or choice == 2:
                    break
                else:
                    print("Invalid choice, please try again")
            if choice == 1:
                while True:
                    new_goal = int_input("New goal: ", False)
                    if new_goal > skill.goal:
                        break
                    else:
                        print("Your new goal should be greater than your old goal, please try again")
                skill.update_goal(new_goal)
                print(f"{skill.name} has been updated: ")
                skill.print_info()
            elif choice == 2:
                delete_skill(skill.name)
                user.skills_mastered += 1
                user.save()
                print("Skill mastered!")
                check_mastery_goals(user)
        else:
            if skill.progress_percentage() >= 50.0:
                complete_achievement(1002)
            skill.printInfo()

    elif choice == 3: # View all skills -------------------------------------
        if check_empty_list() == 0:
            print("You have no skills in progress")
        else:
            print(f"{user.username}'s Active Skills: ")
            print_all_skills()

    elif choice == 4: # Delete a skill --------------------------------------
        if check_empty_list() == 0:
            print("You have no skills to delete")
            continue
        print_all_skills()
        while True:
            del_choice = str_input("Which skill do you want to delete? ").lower()
            if not skill_existence(del_choice):
                print("Skill doesn't exist, please try again")
            else:
                break
        delete_skill(del_choice)
        print("\nHere is your new list of skills:")
        print_all_skills()

    elif choice == 5: # View profile ----------------------------------------
        user.print_user()

    elif choice == 6: # Exit
        break