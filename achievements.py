import sqlite3
from datetime import date

from user import *

def get_achievements(user): # Returns all of a user's completed achievements
    with sqlite3.connect("skill_tracker.db") as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * 
            FROM user_achievements 
            WHERE user_id = ?
        """, (user.id,))
        return cursor.fetchall()

def get_achievement(id): # Returns one row from the achievements table (id, name, description, category)
    with sqlite3.connect("skill_tracker.db") as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, name, description, category
            FROM achievements
            WHERE id = ?
            """, (id,))
        return cursor.fetchone()
    
def complete_achievement(user, id): # Marks an achievement as complete and sends a message
    with sqlite3.connect("skill_tracker.db") as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR IGNORE INTO user_achievements
            (user_id, achievement_id, unlocked_at)
            VALUES (?, ?, ?)
        """, (user.id, id, date.today().isoformat()))
        newly_unlocked = cursor.rowcount == 1
    if newly_unlocked:
        print(f"Congratulations, you have unlocked the achievement '{get_achievement(id)[1]}'!")

def check_streak(user): # Checks if the user's streak continues
    with sqlite3.connect("skill_tracker.db") as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        cursor = conn.cursor()
        cursor.execute("""
            SELECT date 
            FROM activity_log 
            WHERE user_id = ?
            ORDER BY date DESC 
            LIMIT 1
        """, (user.id,))
        result = cursor.fetchone()
        if result == None:
            user.active_streak = 1
        else: 
            last_activity = date.fromisoformat(result[0])
            days_since = (date.today() - last_activity).days
            if days_since == 1:
                user.active_streak += 1
            elif days_since == 0:
                pass
            elif days_since > 1:
                user.active_streak = 1
        user.save()
        if user.active_streak >= 3:
            complete_achievement(user, 1003)
        check_achievements(user)

def check_achievements(user):
    check_dedication_goals(user)
    check_mastery_goals(user)
    check_motivation_goals(user)
    check_multitask_goals(user)

def check_multitask_goals(user): #2000s, number of active goals
    with sqlite3.connect("skill_tracker.db") as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        cursor = conn.cursor()
        cursor.execute("""
            SELECT COUNT(*) 
            FROM skills 
            WHERE user_id = ?
        """, (user.id, ))
        num_skills = cursor.fetchone()[0]
        if num_skills >= 20:
            complete_achievement(user, 2004)
        if num_skills >= 10:
            complete_achievement(user, 2003)
        if num_skills >= 5:
            complete_achievement(user, 2002)
        if num_skills >= 3:
            complete_achievement(user, 2001)

def check_dedication_goals(user): #3000s, number of total hours logged
    total_hours = user.hours_logged
    if total_hours >= 10000:
        complete_achievement(user, 3006)
    if total_hours >= 1000:
        complete_achievement(user, 3005)
    if total_hours >= 500:
        complete_achievement(user, 3004)
    if total_hours >= 100:
        complete_achievement(user, 3003)
    if total_hours >= 50:
        complete_achievement(user, 3002)
    if total_hours >= 10:
        complete_achievement(user, 3001)

def check_mastery_goals(user): #4000s, number of mastered skills
    skills_mastered = user.skills_mastered
    if skills_mastered >= 25:
        complete_achievement(user, 4006)
    if skills_mastered >= 15:
        complete_achievement(user, 4005)
    if skills_mastered >= 10:
        complete_achievement(user, 4004)
    if skills_mastered >= 5:
        complete_achievement(user, 4003)
    if skills_mastered >= 3:
        complete_achievement(user, 4002)
    if skills_mastered >= 1:
        complete_achievement(user, 4001)

def check_motivation_goals(user): #5000s, length of streak
    current_streak = user.active_streak
    if current_streak >= 1000:
        complete_achievement(user, 5006)
    if current_streak >= 360:
        complete_achievement(user, 5005)
    if current_streak >= 180:
        complete_achievement(user, 5004)
    if current_streak >= 90:
        complete_achievement(user, 5003)
    if current_streak >= 30:
        complete_achievement(user, 5002)
    if current_streak >= 7:
        complete_achievement(user, 5001)