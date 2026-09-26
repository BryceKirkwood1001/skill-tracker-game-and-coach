import sqlite3
from datetime import date

from achievements import *
from user import *
from util import *

class Skill:
    def __init__(self, name, hours, goal, xp_value=None):
        self.name = name
        self.hours = hours
        self.goal = goal
        if xp_value is None:
            self.xp_value = goal * 10
        else:
            self.xp_value = xp_value

    def is_complete(self): # Checks if the skill's goal is reached
        return self.hours >= self.goal

    def progress_percentage(self): # Retruns the the user's progress as a percentage
        if self.goal <= 0:
            print("Error calculating progress, skill goal is 0 or less")
            return -1
        return round((self.hours / self.goal) * 100, 1)

    def print_info(self): # Prints the skill's info
        print(f"{self.name}: ")
        print(f"   Hours Logged: {self.hours} hrs")
        print(f"   Goal: {self.goal} hrs")
        print(f"   Progress: {self.progress_percentage()}%")
        print(f"   XP Value: {self.xp_value} XP")

    def update_goal(self, new_goal): # Updates the goal of the skill and adjusts XP accordingly
        self.xp_value = (new_goal - self.goal) * 10
        self.goal = new_goal
        self.save()

    def add_progress(self, add_hours, user): # Adds hours towards competing a skill
            self.hours += add_hours
            self.save()
            check_streak(user)
            with sqlite3.connect("skills.db") as conn:
                cursor = conn.cursor()
                cursor.execute("""
                INSERT OR IGNORE INTO activity_log (date)
                VALUES (?)
                """, (date.today().isoformat(),))
            user.hours_logged += add_hours
            user.save()
            check_dedication_goals(user)

    def save(self): # Sends any changes made to the skill to the database
        with sqlite3.connect("skills.db") as conn:
            cursor = conn.cursor()
            cursor.execute("""
            UPDATE skills
            SET
                hours = ?,
                goal = ?, 
                xp_value = ?
            WHERE name = ?
            """, (
                self.hours,
                self.goal, 
                self.xp_value, 
                self.name
            ))

def get_skill(name): # Returns a Skill object from the skills table (hours, goal, xp)
    if not skill_existence(name):
        print(f"Error retrieving skill info; cannot find skill with name {name}.")
        return None
    with sqlite3.connect("skills.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT hours, goal, xp_value
            FROM skills
            WHERE name = ?
            """, (name,))
        row = cursor.fetchone()
        return Skill(name, row[0], row[1], row[2])
    
def add_skill(name, goal, past_hrs): # Adds a new skill to the skills table, returns a Skill object of the new skill
    with sqlite3.connect("skills.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO skills
            (name, goal, hours, xp_value)
            VALUES (?, ?, ?, ?)
            """, (name, goal, past_hrs, goal * 10))
    check_multitask_goals()
    return get_skill(name)
        
def delete_skill(del_choice): # Deletes a skill from the skills table
    with sqlite3.connect("skills.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
        DELETE FROM skills
        WHERE name = ?
        """, (del_choice,))

def skill_existence(skill_name): # Returns True if skillName exists and False otherwise
    with sqlite3.connect("skills.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""SELECT EXISTS(SELECT 1 FROM skills WHERE name = ?)""", (skill_name,))
        existence = cursor.fetchone()[0]
    return existence == 1

def check_empty_list(): # Returns 0 if there are no skills and >0 otherwise
    with sqlite3.connect("skills.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""SELECT COUNT(*) FROM skills""")
        empty = cursor.fetchone()[0]
    return empty

def get_skills_array(): # Returns an array of Skill objects representing all of the user's skills
    with sqlite3.connect("skills.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
        SELECT name, hours, goal, xp_value
        FROM skills
        """)
        rows = cursor.fetchall()
    return [Skill(name, hours, goal, xp_value) for name, hours, goal, xp_value in rows]

def print_all_skills(): # Prints data from the skills table using getSkillsArray
    for skill in get_skills_array():
        skill.print_info()