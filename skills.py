import sqlite3
from datetime import date

from achievements import *
from user import *
from util import *

class Skill:
    def __init__(self, name, hours, goal, user_id, xp_value=None):
        self.name = name
        self.hours = hours
        self.goal = goal
        if xp_value is None:
            self.xp_value = goal * 10
        else:
            self.xp_value = xp_value
        self.user_id = user_id

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
            with sqlite3.connect("skill_tracker.db") as conn:
                conn.execute("PRAGMA foreign_keys = ON")
                cursor = conn.cursor()
                cursor.execute("""
                INSERT OR IGNORE INTO activity_log (date, user_id)
                VALUES (?, ?)
                """, (date.today().isoformat(), user.id))
            user.hours_logged += add_hours
            user.save()
            check_achievements(user)

    def save(self): # Sends any changes made to the skill to the database
        with sqlite3.connect("skill_tracker.db") as conn:
            conn.execute("PRAGMA foreign_keys = ON")
            cursor = conn.cursor()
            cursor.execute("""
            UPDATE skills
            SET hours = ?, goal = ?, xp_value = ?
            WHERE name = ?
            AND user_id = ?
            """, (
                self.hours,
                self.goal, 
                self.xp_value, 
                self.name, 
                self.user_id
            ))

def get_skill(name, user): # Returns a Skill object from the skills table (hours, goal, xp)
    if not skill_existence(name, user):
        print(f"Error retrieving skill info; cannot find skill with name {name}.")
        return None
    with sqlite3.connect("skill_tracker.db") as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        cursor = conn.cursor()
        cursor.execute("""
            SELECT hours, goal, xp_value, user_id
            FROM skills
            WHERE name = ?
            AND user_id = ?
            """, (name, user.id))
        row = cursor.fetchone()
        return Skill(name, row[0], row[1], row[3], row[2])
    
def add_skill(name, goal, past_hrs, user): # Adds a new skill to the skills table, returns a Skill object of the new skill
    with sqlite3.connect("skill_tracker.db") as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO skills
            (name, goal, hours, xp_value, user_id)
            VALUES (?, ?, ?, ?, ?)
            """, (name, goal, past_hrs, goal * 10, user.id))
    check_achievements(user)
    return get_skill(name, user)
        
def delete_skill(del_choice, user): # Deletes a skill from the skills table
    with sqlite3.connect("skill_tracker.db") as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        cursor = conn.cursor()
        cursor.execute("""
            DELETE FROM skills
            WHERE name = ?
            AND user_id = ?
        """, (del_choice, user.id))

def skill_existence(skill_name, user): # Returns True if skillName exists and False otherwise
    with sqlite3.connect("skill_tracker.db") as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        cursor = conn.cursor()
        cursor.execute("""SELECT EXISTS(SELECT 1 FROM skills WHERE name = ? AND user_id = ?)""", (skill_name, user.id))
        existence = cursor.fetchone()[0]
    return existence == 1

def check_empty_list(user): # Returns 0 if there are no skills and >0 otherwise
    with sqlite3.connect("skill_tracker.db") as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        cursor = conn.cursor()
        cursor.execute("""
            SELECT COUNT(*)
            FROM skills 
            WHERE user_id = ?
        """, (user.id,))
        empty = cursor.fetchone()[0]
    return empty

def get_skills_array(user): # Returns an array of Skill objects representing all of the user's skills
    with sqlite3.connect("skill_tracker.db") as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        cursor = conn.cursor()
        cursor.execute("""
            SELECT name, hours, goal, xp_value, user_id
            FROM skills
            WHERE user_id = ?
        """, (user.id,))
        rows = cursor.fetchall()
    return [Skill(name, hours, goal, user_id, xp_value) for name, hours, goal, xp_value, user_id in rows]

def print_all_skills(user): # Prints data from the skills table using getSkillsArray
    for skill in get_skills_array(user):
        skill.print_info()