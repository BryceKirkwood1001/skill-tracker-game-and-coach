import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

from util import *

class User:
    def __init__(self, id, username, password_hash, xp, level, xp_milestone, skills_mastered, hours_logged, active_streak):
        self.id = id
        self.username = username
        self.password_hash = password_hash
        self.xp = xp
        self.level = level
        self.xp_milestone = xp_milestone
        self.skills_mastered = skills_mastered
        self.hours_logged = hours_logged
        self.active_streak = active_streak

    def add_xp(self, amt): # Adds xp to the user and levels them up
        self.xp += amt
        if self.xp >= self.xp_milestone:
            while self.xp >= self.xp_milestone:
                self.level += 1
                self.xp_milestone = (self.level + 1) * (100 + (self.level // 10 * 25))
            print(f"Congratulations, you have leveled up to level {self.level}!")
            print(f"You need {self.xp_milestone - self.xp} more XP to get to level {self.level + 1}.")

    def save(self): # Sends any changes made to the user to the database
        with sqlite3.connect("skill_tracker.db") as conn:
            conn.execute("PRAGMA foreign_keys = ON")
            cursor = conn.cursor()
            cursor.execute("""
            UPDATE user_info
            SET
                username = ?,
                password_hash = ?,
                xp = ?, 
                level = ?,
                xp_milestone = ?,
                skills_mastered = ?,
                hours_logged = ?,
                active_streak = ?
            WHERE id = ?
            """, (
                self.username,
                self.password_hash,
                self.xp, 
                self.level, 
                self.xp_milestone,
                self.skills_mastered, 
                self.hours_logged, 
                self.active_streak, 
                self.id
            ))

    def print_user(self): # Prints the user's info
        print(f"{self.username}'s Profile: \nXP: {self.xp} \nLevel: {self.level} \nXP Milestone: {self.xp_milestone} \nSkills Mastered: {self.skills_mastered} \nHours Logged: {self.hours_logged} \nStreak: {self.active_streak}")

def user_exists(username):
    with sqlite3.connect("skill_tracker.db") as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id
            FROM user_info
            WHERE username = ?
        """, (username,))
        if cursor.fetchone() is None:
            return False
        return True

def user_creation(): # Returns a User object upon successful creation, None otherwise
    while True:
        new_username = str_input("Username: ")
        if user_exists(new_username):
            print("A user with that name already exists, please try again.")
        else:
            break
    new_password = str_input("Password: ")
    conf_password = str_input("Confirm Password: ")
    if new_password != conf_password:
        print("Passwords don't match, no account created.")
        return None
    password_hash = generate_password_hash(new_password)
    with sqlite3.connect("skill_tracker.db") as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO user_info
            (username, password_hash)
            VALUES (?, ?)
        """, (new_username, password_hash))
    return get_user(new_username)

def user_login(): # Returns a User object upon successful login, None otherwise
    username = str_input("Username: ")
    password = str_input("Password: ")
    if not user_exists(username):
        print("Invalid login credentials, please try again.")
        return None
    user = get_user(username)
    if not check_password_hash(user.password_hash, password):
        print("Invalid login credentials, please try again.")
        return None
    return user

def get_user(username): # Returns a User object with all of the user's info
    with sqlite3.connect("skill_tracker.db") as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, username, password_hash, xp, level, xp_milestone, skills_mastered, hours_logged, active_streak
            FROM user_info
            WHERE username = ?
        """, (username,))
        row = cursor.fetchone()
        if row is None:
            raise Exception("No user found")
    return User(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8])