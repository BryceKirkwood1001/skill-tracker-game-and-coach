# Skill Tracker

**A Python-based skill tracking application that gamifies personal growth through XP, levels, achievements, and activity streaks.**

Skill Tracker is a command-line application that allows users to create personal development goals, log hours toward those goals, and earn rewards as they make progress.

Inspired by progression systems in video games, Skill Tracker aims to make learning and self-improvement more engaging by turning real-world accomplishments into measurable progress.

The application supports multiple user accounts, secure password hashing, and persistent storage through SQLite. Each user maintains their own skills, progression statistics, achievements, and activity history.

**Project Status:** Active Development — Functional CLI Application

## Features

### Skill Tracking

Users can create and manage skills they want to improve, with each skill having an hour-based goal.

Current functionality includes:

- Create skills with customizable goals and existing hours
- Log additional hours toward a skill
- View active skills, progress percentages, and XP rewards
- Complete goals and earn XP
- Extend completed goals
- Master and remove completed skills
- Delete skills that are no longer being pursued

Skills are managed using an object-oriented `Skill` class, which handles skill data, progress calculations, goal updates, and database persistence.

### User Accounts & Authentication

Skill Tracker supports multiple accounts, allowing different users to maintain independent progression histories.

Users can:

- Register an account with a unique username and password
- Log into an existing account
- Log out and switch accounts
- Access their saved profile and skill data across sessions

Passwords are hashed using Werkzeug's password hashing utilities rather than being stored in plaintext.

Each account is assigned a unique user ID. Skills, activity records, and unlocked achievements are associated with that ID to keep user data separate.

### XP & Leveling

Completing skill goals rewards XP, which contributes to the user's overall level.

The application includes:

- XP rewards based on goal size
- Level progression
- Increasing XP milestones as levels rise
- Persistent XP and level information

Users can view their progression through their profile.

### Achievements

Skill Tracker features an achievement system that rewards users for reaching milestones in several categories.

| Category | Examples |
|---|---|
| Introductory | Create a first goal, reach 50% progress, complete a goal |
| Multitasking | Maintain 3, 5, 10, or 20 active goals |
| Dedication | Accumulate 10, 50, 100, or more logged hours |
| Mastery | Master 1, 3, 5, or more skills |
| Motivation | Maintain consecutive-day activity streaks |

Achievement definitions are shared across the application, while unlock records are maintained separately for each user.

Previously unlocked achievements persist between sessions and cannot be awarded multiple times to the same user.

### Activity Streaks

Skill Tracker records the dates on which users log progress and tracks consecutive days of activity.

The system:

- Tracks each user's activity history independently
- Increases streaks for consecutive active days
- Avoids counting multiple activity logs on the same day as multiple streak days
- Resets streaks following missed days
- Awards achievements for streak milestones

### User Profiles

Each account maintains the following statistics:

- Username
- Current XP
- Current level
- Next XP milestone
- Total hours logged
- Skills mastered
- Current activity streak

All statistics persist between sessions.

## Technologies

| Technology | Purpose |
|---|---|
| Python | Core application logic and CLI |
| SQLite | Persistent relational database |
| SQL | Data retrieval, updates, and relationships |
| Werkzeug | Secure password hashing and verification |
| Object-Oriented Programming | User and Skill models |
| Git & GitHub | Version control and project management |

## Database Architecture

Skill Tracker uses a local SQLite database, `skill_tracker.db`, containing five tables.

| Table | Purpose |
|---|---|
| `user_info` | User accounts, password hashes, and progression statistics |
| `skills` | User-owned skills, goals, hours, and XP rewards |
| `achievements` | Shared achievement definitions |
| `user_achievements` | Achievements unlocked by individual users |
| `activity_log` | User-specific activity dates for streak tracking |

### Multi-User Data Management

The application uses unique user IDs and relational database foreign keys to associate records with the accounts that own them.

For example:

```text
user_info
   |
   +---- skills
   |
   +---- activity_log
   |
   +---- user_achievements
              |
              +---- achievements
```

The `user_achievements` table establishes a many-to-many relationship between users and achievements. This allows multiple users to unlock the same achievement independently without duplicating the achievement definitions.

Skill queries are filtered by user ID to ensure that users only retrieve or modify their own skill records.

Database constraints also prevent duplicate activity entries for the same user on the same date.

## Installation & Usage

### Requirements

- Python 3
- Werkzeug

### 1. Clone the Repository

```bash
git clone <repository-url>
cd <repository-folder>
```

Replace the placeholders with the URL and directory name of this repository.

### 2. Install Dependencies

Install Werkzeug:

```bash
python -m pip install werkzeug
```

### 3. Initialize the Database

```bash
python database_setup.py
```

This creates the local SQLite database, initializes the required tables, and populates the default achievement definitions.

### 4. Start the Application

```bash
python main_skill_tracker.py
```

On startup, the application presents an account menu:

```text
1. Log In
2. Create Account
3. Exit App
```

Create an account or log into an existing one to access the main application.

Once authenticated, users can create and manage skills, log progress, view their profiles, and earn achievements.

Logging out returns the user to the account menu without closing the application.

## Project Structure

```text
Skill-Tracker/
│
├── main_skill_tracker.py  # Account menu and main CLI
├── user.py                # User model and authentication
├── skills.py              # Skill model and management
├── achievements.py        # Achievement and streak systems
├── database_setup.py      # Database schema and initialization
├── util.py                # Input validation helpers
├── .gitignore             # Ignored local files
└── README.md              # Project documentation
```

The `skill_tracker.db` database is created locally during setup and should not be committed to the repository.

## Development & What I Built

Skill Tracker began as a small Python command-line program storing user and skill information in JSON files.

As I continued developing it, I expanded the application's functionality and redesigned its architecture to incorporate new programming concepts and technologies.

Throughout the project, I have:

- Designed and implemented a skill and goal tracking system
- Developed XP, leveling, skill mastery, and achievement mechanics
- Built activity logging and streak tracking functionality
- Migrated persistent storage from JSON files to SQLite
- Designed relational database tables and relationships
- Implemented CRUD operations using parameterized SQL queries
- Refactored the application into multiple Python modules
- Introduced object-oriented `User` and `Skill` models
- Implemented registration, login, and logout functionality
- Added password hashing and verification using Werkzeug
- Expanded the database architecture to support multiple users
- Implemented foreign keys, uniqueness constraints, and user-specific database queries
- Redesigned achievement storage using a many-to-many relationship
- Debugged issues involving database transactions, object state, and persistent storage
- Used Git and GitHub to track changes and document development

One of the main goals of this project has been to learn new technologies and software engineering concepts through practical implementation.

Rather than beginning with a predetermined architecture, I have continually expanded and refactored the program as its requirements evolved.

The transition from a single-user, JSON-based CLI into a multi-user, SQLite-backed application has provided experience with database design, authentication, object-oriented programming, modular architecture, and managing persistent application state.

## Future Development

The current version focuses on providing a functional command-line experience with persistent, account-specific progress tracking.

Potential upcoming additions include:

### Web Interface

- Transition from the terminal to a browser-based application
- Build a Python web backend using Flask
- Create a dashboard for skills, progression, and achievements
- Implement interactive forms for goal creation and progress logging
- Improve the visual presentation of gamification mechanics

### AI Skill Coach

- Integrate a large language model API
- Analyze users' existing goals and progress
- Generate personalized recommendations
- Suggest realistic milestones and improvements
- Provide feedback based on skill development patterns

### Additional Improvements

- Historical progress visualizations
- More detailed achievement displays
- Additional profile customization
- Expanded gamification systems
- Improvements to account security and user experience

These are planned directions rather than features of the current release.

## Project Status

**Core CLI: Functional**

**Multi-User Support: Implemented**

**Web Interface: Planned**

**AI Coach: Planned**

Skill Tracker remains an ongoing learning project. Its current version provides a functional foundation for tracking skill development across multiple user accounts, with the possibility of additional features as development continues.