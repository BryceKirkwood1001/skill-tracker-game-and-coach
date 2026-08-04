import sqlite3

def getUser():
    with sqlite3.connect("skills.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
        SELECT id, username, xp, level, xp_milestone, skills_mastered, hours_logged, streak
        FROM user_info
        """)
        row = cursor.fetchone()
        if row is None:
            raise Exception("No user found")
    return {
        "id": row[0],
        "username": row[1],
        "xp": row[2],
        "level": row[3],
        "xp milestone": row[4],
        "skills mastered": row[5],
        "hours logged": row[6],
        "streak": row[7]
    }

def updateUser(user):
    with sqlite3.connect("skills.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
        UPDATE user_info
        SET
            username = ?,
            xp = ?, 
            level = ?,
            xp_milestone = ?,
            skills_mastered = ?,
            hours_logged = ?,
            streak = ?
        WHERE id = ?
        """, (
            user["username"],
            user["xp"], 
            user["level"], 
            user["xp milestone"],
            user["skills mastered"], 
            user["hours logged"], 
            user["streak"], 
            user["id"]
        ))

def addXp(val): # Adds xp to userData and checks for level-ups
    user = getUser()
    user["xp"] += val
    if user["xp"] >= user["xp milestone"]:
        while user["xp"] >= user["xp milestone"]:
            user["level"] += 1
            user["xp milestone"] = (user["level"] + 1) * 100
        print(f"Congratulations, you have leveled up to level {user['level']}!")
        print(f"You need {user["xp milestone"] - user['xp']} more XP to get to level {user['level'] + 1}.")
    updateUser(user)

def printUser():
    user = getUser()
    print(f"{user["username"]}'s Profile: \nXP: {user["xp"]} \nLevel: {user["level"]} \nXP Milestone: {user["xp milestone"]} \nSkills Mastered: {user["skills mastered"]} \nHours Logged: {user["hours logged"]} \nStreak: {user["streak"]}")