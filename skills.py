import sqlite3
from datetime import date

from achievements import *
from user import *
from util import *

def getSkills(): # Returns all rows from the skills table
    with sqlite3.connect("skills.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM skills""")
        skills = cursor.fetchall()
    return skills

def getSkill(name): # Returns a single row from the skills table (hours, goal, xp)
    with sqlite3.connect("skills.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT hours, goal, xp_value
            FROM skills
            WHERE name = ?
            """, (name,))
        return cursor.fetchone()
    
def addSkill(name, goal): # Adds a new skill to the skills table
    with sqlite3.connect("skills.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO skills
            (name, goal, hours, xp_value)
            VALUES (?, ?, ?, ?)
            """, (name, goal, 0, goal * 10))
        checkMultitaskGoals()
        
def deleteSkill(del_choice): # Deletes a skill from the skills table
    with sqlite3.connect("skills.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
        DELETE FROM skills
        WHERE name = ?
        """, (del_choice,))

def progressSkill(name, addHours): # Adds hours towards competing a skill
    with sqlite3.connect("skills.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
        UPDATE skills
        SET hours = hours + ?
        WHERE name = ?
        """, (addHours, name))
    checkStreak()
    with sqlite3.connect("skills.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
        INSERT OR IGNORE INTO activity_log (date)
        VALUES (?)
        """, (date.today().isoformat(),))
    user = getUser()
    user["hours logged"] += addHours
    updateUser(user)
    checkDedicationGoals()

def skillExistence(skillName): # Returns True if skillName exists and False otherwise
    with sqlite3.connect("skills.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""SELECT EXISTS(SELECT 1 FROM skills WHERE name = ?)""", (skillName,))
        existence = cursor.fetchone()[0]
    return existence == 1

def checkEmptyList(): # Returns 0 if there are no skills and >0 otherwise
    with sqlite3.connect("skills.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""SELECT COUNT(*) FROM skills""")
        empty = cursor.fetchone()[0]
    return empty

def skillPrint(): # Prints data from the skills table in a readable format
    skills = getSkills()
    for name, goal, hours, xp_value in skills:
        print(f"\n{name.title()}: ")
        print(f"   Hours Logged: {hours} hrs")
        print(f"   Goal: {goal} hrs")
        if goal != 0:
            print(f"   Progress: {(hours / goal) * 100 :.1f}%")
        else:
            print("   Error calculating progress percentage, goal is 0")
        print(f"   XP Value: {xp_value}")

def progressCheck(skillName): # Checks if a user has completed a skill and handles next steps
    user = getUser()
    row = getSkill(skillName)
    if row is None:
        print("Error: Skill not found")
        return
    if row[0] >= row[1]:
        completeAchievement(1004)
        print(f"Congratulations! You've reached your goal for {skillName}!")
        addXp(row[2])
        while True:
            prog_choice = intInput("Would you like to (1) update your goal or (2) remove the skill from your to-do list? ", False)

            if prog_choice == 1: 
                old_goal = row[1]
                while True:
                    updated_hours = intInput("New goal: ", False)
                    if updated_hours > old_goal:
                        break
                    else:
                        print("Your new goal should be greater than your old goal, please try again")
                with sqlite3.connect("skills.db") as conn:
                    cursor = conn.cursor()
                    cursor.execute("""
                        UPDATE skills
                        SET goal = ? 
                        WHERE name = ?
                        """, (updated_hours, skillName))
                    cursor.execute("""
                        UPDATE skills 
                        SET xp_value = ? 
                        WHERE name = ?""", ((updated_hours - old_goal) * 10, skillName))
                row = getSkill(skillName)
                break

            elif prog_choice == 2:
                deleteSkill(skillName)
                user["skills mastered"] += 1
                updateUser(user)
                checkMasteryGoals()
                print("Skill mastered!")
                break

            else:
                print("Invalid choice, please try again")
    else:
        if row[1] == 0:
            print("Error calculating progress, skill goal is 0")
        else:
            if row[0] / row[1] >= 0.5:
                completeAchievement(1002)
            print("Your current progress in " + skillName + ": ")
            print(f"   Hours Logged: {row[0]} hrs")
            print(f"   Goal: {row[1]} hrs")
            print(f"   Progress: {(row[0] / row[1]) * 100 :.1f}%")