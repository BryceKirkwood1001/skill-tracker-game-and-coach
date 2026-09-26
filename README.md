# Skill Progress Tracker

A Python-based skill and goal tracking application that turns personal development into a progression system.

Skill Progress Tracker allows users to create skills they want to improve, set hour-based goals, log their progress, earn XP, level up, maintain activity streaks, and unlock achievements. The project is inspired by progression and achievement systems found in games, applied to real-world learning and self-improvement.

The project is currently a command-line application backed by SQLite, with plans to expand it into a full web application with a graphical interface, authentication, additional gamification, and AI-powered progress analysis.

## Features

### Skill Tracking

Users can:

- Create skills and set hour-based goals
- Log additional hours toward a skill
- View all active skills and their progress
- Update a goal after completing it
- Mark completed skills as mastered
- Delete skills they no longer want to track
- View progress percentages and XP rewards

Skills are represented using an object-oriented `Skill` model that manages skill state and behavior.

### User Profiles

Each user profile tracks:

- Username
- Total XP
- Current level
- XP required for the next level
- Total hours logged
- Number of skills mastered
- Current activity streak

User information is represented using a `User` model and persisted between sessions using SQLite.

### XP & Leveling

Completing skill goals rewards XP.

As users accumulate XP, they level up and work toward progressively larger XP milestones. Skill XP rewards are based on the size of the goal, allowing larger goals to provide larger rewards.

### Achievements

The application includes an achievement system that rewards milestones across several categories.

Current achievements include milestones for:

- Creating a first goal
- Reaching 50% progress on a goal
- Completing a first goal
- Maintaining multiple active goals
- Logging total hours
- Mastering skills
- Maintaining activity streaks

Achievement progress is stored in the database so unlocked achievements persist between sessions.

### Activity Streaks

The application records days on which the user logs progress.

This allows it to:

- Track consecutive active days
- Reset a streak after missed days
- Prevent multiple sessions on the same day from increasing the streak multiple times
- Unlock achievements for longer streaks

## Technologies

- **Python** — application logic
- **SQLite** — persistent storage
- **Object-Oriented Programming** — `User` and `Skill` models
- **SQL** — user, skill, achievement, and activity data management
- **Git / GitHub** — version control and project development

The project uses Python's built-in `sqlite3` library and currently does not require external dependencies.

## Database

Application data is stored in `skills.db`.

The database contains four primary tables:

- `skills` — active skills, goals, hours, and XP rewards
- `user_info` — profile information, XP, levels, total hours, mastery count, and streak
- `achievements` — achievement information and unlock status
- `activity_log` — dates on which progress was logged

The database itself is not included in the repository so that each installation can maintain its own user data.

`database_setup.py` initializes the required tables and default application data.

## Running the Project

### Requirements

- Python 3
- No third-party packages are currently required

### Setup

Clone the repository:

```bash
git clone <repository-url>
cd <repository-folder>
```

Initialize the database:

```bash
python database_setup.py
```

This creates the local SQLite database and populates the default application data.

Then start the application:

```bash
python main_skill_tracker.py
```

On the first run, the application will prompt you to create a username.

After setup, the database will persist your skills, profile statistics, achievements, and activity history between sessions.

## Project Structure

```text
.
├── main_skill_tracker.py   # Main CLI and application flow
├── skills.py               # Skill model and skill management
├── user.py                 # User model and profile management
├── achievements.py         # Achievement and streak logic
├── util.py                 # Input validation and utility functions
├── database_setup.py       # SQLite database initialization
├── .gitignore
└── README.md
```

## Planned Features

The current command-line application serves as the foundation for a larger skill-development platform.

Planned additions include:

- **Web interface** — Replace the command-line interface with a browser-based dashboard
- **Flask backend** — Connect the existing Python application logic to a web application
- **Authentication** — Support secure accounts and multiple users
- **Improved database architecture** — Adapt the database for multiple users and additional application data
- **Achievement dashboard** — Visually display unlocked and locked achievements
- **Expanded gamification** — Additional rewards, collectibles, progression systems, and statistics
- **Progress visualization** — Charts and dashboards showing skill development over time
- **AI goal analysis** — Analyze goals and progress patterns to provide personalized feedback, milestone suggestions, and recommendations
- **Improved UI/UX** — Create a polished interface for managing skills and viewing progression

## What I Built & Learned

This project was built from scratch as a personal learning project.

It originally began as a small Python command-line program that stored skills in JSON files. As the application grew, I progressively redesigned it to introduce technologies and software development concepts I wanted to learn.

So far, I have:

- Designed the application's skill tracking and gamification systems
- Built CRUD functionality for creating, reading, updating, and deleting skills
- Migrated application storage from JSON files to a relational SQLite database
- Designed database tables for skills, users, achievements, and activity history
- Written parameterized SQL queries for database operations
- Built an XP and leveling system
- Designed and implemented a persistent achievement system
- Built activity logging and consecutive-day streak tracking
- Added input validation and edge-case handling
- Refactored the application into multiple Python modules
- Refactored dictionary- and function-based code into object-oriented `User` and `Skill` models
- Worked through database transaction, locking, state synchronization, and persistence issues
- Used Git and GitHub to version and document the project

Rather than beginning with a finished architecture, I have intentionally expanded and refactored the application as I learn new concepts. This has allowed the project to evolve from a basic Python script into a more structured application while giving me hands-on experience with database design, object-oriented programming, application architecture, debugging, and persistent state management.

## Current Status

**In Development**

The core command-line application is functional, including skill tracking, user progression, achievements, streaks, and SQLite persistence.

The next major development phase is transitioning the project from a command-line program into a web application.