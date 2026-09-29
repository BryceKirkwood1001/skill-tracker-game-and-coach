# Skill Tracker

A command-line application for tracking progress toward real-world skills and goals through a game-inspired progression system.

Skill Tracker allows users to create hour-based skill goals, log their progress, earn XP, level up, maintain activity streaks, master skills, and unlock achievements. The project combines a traditional goal tracker with progression mechanics inspired by video games.

**Status: v1.0 — Complete**

This repository represents the completed first version of Skill Tracker. The application was developed as a personal learning project and evolved substantially over its development, from a simple Python script using JSON files into a modular, object-oriented application backed by a relational database.

## Features

### Skill Tracking

Users can create skills they want to improve and assign each one an hour-based goal. The application supports:

- Creating and deleting skills
- Logging hours toward active skills
- Viewing current hours, goals, and progress percentages
- Completing and mastering skills
- Extending completed goals
- Earning XP for reaching goals

### User Progression

Skill Tracker maintains a persistent user profile containing:

- Username
- Total XP
- Current level
- XP milestone for the next level
- Total hours logged
- Number of skills mastered
- Current activity streak

XP earned from completing goals contributes toward an increasing level progression system.

### Achievements

Achievements reward milestones across several categories, including:

- Creating and progressing through goals
- Maintaining multiple active skills
- Logging total hours
- Mastering skills
- Maintaining consecutive-day activity streaks

Unlocked achievements are saved between sessions.

### Activity Streaks

Skill Tracker records days on which progress is logged and uses this history to maintain an activity streak.

The system recognizes consecutive active days, prevents multiple logs on the same day from artificially increasing a streak, resets broken streaks, and awards achievements for longer streaks.

### Persistent Storage

All application data is stored locally using SQLite.

The database maintains:

- Active skills and their progress
- User profile and progression data
- Achievement status
- Activity history

This allows progress to persist between application sessions without requiring an external service or account.

## Technologies & Concepts

- **Python**
- **SQLite**
- **SQL**
- **Object-Oriented Programming**
- **Relational database design**
- **Git & GitHub**

The project uses Python's built-in `sqlite3` module and does not currently require third-party packages.

## Project Structure

```text
.
├── main_skill_tracker.py   # Main CLI and application flow
├── skills.py               # Skill model and skill management
├── user.py                 # User model and profile management
├── achievements.py         # Achievement and streak logic
├── util.py                 # Input validation and utilities
├── database_setup.py       # Creates and initializes the database
├── .gitignore
└── README.md
```

`User` and `Skill` are represented as Python objects while SQLite provides persistent storage for their data.

## Running Skill Tracker

### Requirements

- Python 3

No third-party Python packages are required.

### 1. Clone the repository

```bash
git clone <repository-url>
cd <repository-folder>
```

### 2. Initialize the database

Run:

```bash
python database_setup.py
```

This creates `skills.db`, initializes the necessary database tables, and adds the application's default achievements.

### 3. Start the application

Run:

```bash
python main_skill_tracker.py
```

On the first run, Skill Tracker will prompt you to choose a username. Your subsequent progress will be saved locally in `skills.db`.

## Development

Skill Tracker began as a much smaller Python program that stored skill and user information in JSON files. Rather than starting with the application's current architecture, I expanded and refactored it as I encountered new problems and learned new concepts.

Over the course of the project, I:

- Designed the skill tracking and gamification systems
- Implemented CRUD operations for skill management
- Built an XP and leveling system
- Designed an achievement system with multiple categories of milestones
- Implemented activity logging and consecutive-day streak tracking
- Added input validation and handling for application edge cases
- Migrated persistent storage from JSON files to SQLite
- Designed relational database tables for users, skills, achievements, and activity history
- Wrote parameterized SQL queries for database operations
- Debugged database transaction and locking issues
- Refactored the original program into multiple Python modules
- Refactored dictionary- and function-based code into object-oriented `User` and `Skill` models
- Managed synchronization between in-memory objects and persistent database state
- Used Git and GitHub throughout development for version control

One of the main goals of the project was to learn new concepts by introducing them when the growing application created a practical reason to use them. As a result, the architecture evolved alongside my understanding of Python application development.

## Scope of v1.0

The original concept for Skill Tracker included ideas for a much larger application, including a graphical web interface, user authentication, deeper statistics and visualization, additional gamification systems, and AI-assisted goal analysis.

Those features are not required for the completed v1.0 release.

Instead, v1.0 focuses on providing a complete local command-line experience: users can create goals, track their progress over time, build streaks, earn achievements and XP, level up, master skills, and retain their progress between sessions.

The project may be expanded in the future, but this release represents the completed scope of the original learning project.

## Potential Future Development

If development resumes in the future, possible extensions include:

- Browser-based user interface
- Flask backend
- Multi-user support and authentication
- Progress charts and historical statistics
- Achievement and profile dashboards
- Additional progression and collectible systems
- AI-assisted goal analysis and progress recommendations

These ideas are possible extensions rather than requirements for the current release.

## Version

**Skill Tracker v1.0**

A complete local CLI skill-tracking and gamification application built with Python and SQLite.