import sqlite3

connection = sqlite3.connect("skill_tracker.db")
cursor = connection.cursor()

# user_info, skills, activity_log, achievements, user_achievements
# TABLE CREATION ---------------------------------
cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_info
    (  
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL, 
        password_hash TEXT NOT NULL, 
        xp INTEGER NOT NULL DEFAULT 0, 
        level INTEGER NOT NULL DEFAULT 0, 
        xp_milestone INTEGER NOT NULL DEFAULT 100,
        skills_mastered INTEGER NOT NULL DEFAULT 0, 
        hours_logged INTEGER NOT NULL DEFAULT 0, 
        active_streak INTEGER NOT NULL DEFAULT 0
    )
    """)

cursor.execute("""
    CREATE TABLE IF NOT EXISTS skills
    (
        name TEXT NOT NULL,
        hours INTEGER NOT NULL,
        goal INTEGER NOT NULL,
        xp_value INTEGER NOT NULL, 
        user_id INTEGER NOT NULL, 

        PRIMARY KEY (user_id, name),

        FOREIGN KEY (user_id)
            REFERENCES user_info(id)
            ON DELETE CASCADE
    )
    """)

cursor.execute("""
    CREATE TABLE IF NOT EXISTS activity_log
    (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        date TEXT NOT NULL, 
        user_id INTEGER NOT NULL, 

        FOREIGN KEY (user_id)
            REFERENCES user_info(id)
            ON DELETE CASCADE,

        UNIQUE (user_id, date)
    )
    """)

cursor.execute("""
    CREATE TABLE IF NOT EXISTS achievements
    (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        description TEXT NOT NULL, 
        category TEXT NOT NULL
    )
    """)

cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_achievements
    (
        user_id INTEGER NOT NULL,
        achievement_id INTEGER NOT NULL,
        unlocked_at TEXT NOT NULL,

        PRIMARY KEY (user_id, achievement_id), 

        FOREIGN KEY (user_id)
            REFERENCES user_info(id)
            ON DELETE CASCADE,

        FOREIGN KEY (achievement_id)
            REFERENCES achievements(id)
            ON DELETE CASCADE
    )
""")

# TABLE INITILIZATION ------------------------------

# Numbering: 
# 1 = intro
# 2 = active skills based
# 3 = hours based
# 4 = skill mastery based 
# 5 = daily activity based
default_achievements = [
    (1001,"The First Step","Create your first goal","intro"),
    (1002,"Well on Your Way","Reach 50% progress on a goal for the first time","intro"),
    (1003,"The Opening Stretch","Log hours 3 days in a row","intro"),
    (1004,"Already a Pro","Complete your first goal","intro"),
    (2001,"Multitasker I","Have 3 active goals","multitask"),
    (2002,"Multitasker II","Have 5 active goals","multitask"),
    (2003,"Multitasker III","Have 10 active goals","multitask"),
    (2004,"Unstoppable Force","Have 20 active goals","multitask"),
    (3001,"Dedication I","Log 10 hours total","dedication"),
    (3002,"Dedication II","Log 50 hours total","dedication"),
    (3003,"Dedication III","Log 100 hours total","dedication"),
    (3004,"Dedication IV","Log 500 hours total","dedication"),
    (3005,"Dedication V","Log 1,000 hours total","dedication"),
    (3006,"Lifelong Commitment","Log 10,000 hours total","dedication"),
    (4001,"Masterful I","Master 1 skill","mastery"),
    (4002,"Masterful II","Master 3 skills","mastery"),
    (4003,"Masterful III","Master 5 skills","mastery"),
    (4004,"Masterful IV","Master 10 skills","mastery"),
    (4005,"Masterful V","Master 15 skills","mastery"),
    (4006,"Grandmaster of All","Master 25 skills","mastery"),
    (5001,"Motivation I","Log hours 7 days in a row","motivation"),
    (5002,"Motivation II","Log hours 30 days in a row","motivation"),
    (5003,"Motivation III","Log hours 90 days in a row","motivation"),
    (5004,"Motivation IV","Log hours 180 days in a row","motivation"),
    (5005,"Motivation V","Log hours 360 days in a row","motivation"),
    (5006,"Moving Mountains","Log hours 1000 days in a row","motivation")
    ]

for id, name, desc, category in default_achievements:
    cursor.execute("""
        INSERT OR IGNORE INTO achievements
        (id, name, description, category)
        VALUES (?, ?, ?, ?)
        """, (id, name, desc, category))

connection.commit()
connection.close()

print("database created")