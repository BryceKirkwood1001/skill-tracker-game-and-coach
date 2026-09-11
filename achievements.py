import sqlite3
from datetime import date

from user import *

def getAchievements(): # Returns all rows from the achievements table
    with sqlite3.connect("skills.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM achievements""")
        return cursor.fetchall()

def getAchievement(id): # Returns one row from the achievements table (name, description, unlocked)
    with sqlite3.connect("skills.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT name, description, unlocked
            FROM achievements
            WHERE id = ?
            """, (id,))
        return cursor.fetchone()
    
def completeAchievement(id): # Marks an achievement as complete and sends a message
    row = getAchievement(id)
    if row[2] == 1:
        return
    with sqlite3.connect("skills.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE achievements
            SET unlocked = 1
            WHERE id = ?
            """, (id,))
    print(f"Congratulations, you have unlocked the achievement '{row[0]}'!")

def checkStreak(user): # Checks if the user's streak continues
    with sqlite3.connect("skills.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""SELECT date FROM activity_log ORDER BY id DESC LIMIT 1""")
        result = cursor.fetchone()
        if result == None:
            user.active_streak = 1
        else: 
            last_activity = date.fromisoformat(result[0])
            if (date.today() - last_activity).days == 1:
                user.active_streak += 1
            elif (date.today() - last_activity).days == 0:
                pass
            elif date.today() > last_activity:
                user.active_streak = 1
        user.save()
        if user.active_streak >= 3:
            completeAchievement(1003)
        checkMotivationGoals(user)

def checkMultitaskGoals(): #2000s, number of active goals
    with sqlite3.connect("skills.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""SELECT COUNT(*) FROM skills""")
        num_skills = cursor.fetchone()[0]
        if num_skills >= 20:
            completeAchievement(2004)
        if num_skills >= 10:
            completeAchievement(2003)
        if num_skills >= 5:
            completeAchievement(2002)
        if num_skills >= 3:
            completeAchievement(2001)

def checkDedicationGoals(user): #3000s, number of total hours logged
    total_hours = user.hours_logged
    if total_hours >= 10000:
        completeAchievement(3006)
    if total_hours >= 1000:
        completeAchievement(3005)
    if total_hours >= 500:
        completeAchievement(3004)
    if total_hours >= 100:
        completeAchievement(3003)
    if total_hours >= 50:
        completeAchievement(3002)
    if total_hours >= 10:
        completeAchievement(3001)

def checkMasteryGoals(user): #4000s, number of mastered skills
    skills_mastered = user.skills_mastered
    if skills_mastered >= 25:
        completeAchievement(4006)
    if skills_mastered >= 15:
        completeAchievement(4005)
    if skills_mastered >= 10:
        completeAchievement(4004)
    if skills_mastered >= 5:
        completeAchievement(4003)
    if skills_mastered >= 3:
        completeAchievement(4002)
    if skills_mastered >= 1:
        completeAchievement(4001)

def checkMotivationGoals(user): #5000s, length of streak
    current_streak = user.active_streak
    if current_streak >= 1000:
        completeAchievement(5006)
    if current_streak >= 360:
        completeAchievement(5005)
    if current_streak >= 180:
        completeAchievement(5004)
    if current_streak >= 90:
        completeAchievement(5003)
    if current_streak >= 30:
        completeAchievement(5002)
    if current_streak >= 7:
        completeAchievement(5001)