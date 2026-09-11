import sqlite3

class User:
    def __init__(self, id, username, xp, level, xp_milestone, skills_mastered, hours_logged, active_streak):
        self.id = id
        self.username = username
        self.xp = xp
        self.level = level
        self.xp_milestone = xp_milestone
        self.skills_mastered = skills_mastered
        self.hours_logged = hours_logged
        self.active_streak = active_streak

    def addXp(self, amt):
        self.xp += amt
        if self.xp >= self.xp_milestone:
            while self.xp >= self.xp_milestone:
                self.level += 1
                self.xp_milestone = (self.level + 1) * (100 + (self.level // 10 * 25))
            print(f"Congratulations, you have leveled up to level {self.level}!")
            print(f"You need {self.xp_milestone - self.xp} more XP to get to level {self.level + 1}.")

    def save(self):
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
                active_streak = ?
            WHERE id = ?
            """, (
                self.username,
                self.xp, 
                self.level, 
                self.xp_milestone,
                self.skills_mastered, 
                self.hours_logged, 
                self.active_streak, 
                self.id
            ))

    def printUser(self):
        print(f"{self.username}'s Profile: \nXP: {self.xp} \nLevel: {self.level} \nXP Milestone: {self.xp_milestone} \nSkills Mastered: {self.skills_mastered} \nHours Logged: {self.hours_logged} \nStreak: {self.active_streak}")


def getUser():
    with sqlite3.connect("skills.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
        SELECT id, username, xp, level, xp_milestone, skills_mastered, hours_logged, active_streak
        FROM user_info
        """)
        row = cursor.fetchone()
        if row is None:
            raise Exception("No user found")
    return User(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7])