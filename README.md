# Asana Workspace Seed Data Simulator

This project generates a realistic, relational seed dataset simulating an enterprise-scale
Asana workspace. The dataset is designed to support reinforcement learning (RL) environments
for evaluating computer-use agents on project management workflows.

The simulated organization represents a mid-sized B2B SaaS company using Asana for
engineering, marketing, and operations workstreams.

---

## Features

- Relational SQLite schema modeling core Asana entities
- Realistic users, teams, projects, sections, tasks, and subtasks
- Configurable dataset scale and temporal window
- Deterministic generation via seeded randomness
- Referential and temporal consistency across all entities

---

## Project Structure

```text
├── README.md                # Project overview, setup, and usage
├── requirements.txt         # Python dependencies
├── schema.sql               # SQLite database schema (DDL)
├── .env.example             # Environment variable template
├── src/
│   ├── main.py              # Entry point and orchestration logic
│   ├── generators/          # Data generation modules
│   │   ├── organizations.py
│   │   ├── users.py
│   │   ├── teams.py
│   │   ├── projects.py
│   │   ├── sections.py
│   │   ├── tasks.py
│   │   ├── subtasks.py
│   │   ├── comments.py
│   │   ├── tags.py
│   │   └── custom_fields.py
│   └── utils/               # Shared utilities and helpers
│       ├── db.py
│       ├── dates.py
│       └── random.py
├── output/
│   └── asana_simulation.sqlite  # Generated Asana workspace database
```


## Setup Instructions

### 1. Create a virtual environment (recommended)

```

bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate or venv\Scripts\Activate.ps1

```

### 2. Install dependencies

```
pip install -r requirements.txt

```

### 3. Configure environment variables

```
cp .env.example .env

```
## Running the Generator

First, activate the virtual environment:

```
source venv/bin/activate   # Windows: venv\Scripts\activate or venv\Scripts\Activate.ps1
```

Then run the following command from the project root:

```
python src/main.py
```

## What This Script Does

Running the generator performs the following steps:

- Initializes the SQLite database
- Creates all tables using the schema defined in `schema.sql`
- Generates synthetic yet realistic seed data
- Saves the final database to `output/asana_simulation.sqlite`

---

## Output

The generated SQLite database contains the following entities:

- Organizations and users
- Teams and team memberships
- Projects and sections
- Tasks, subtasks, and comments
- Tags and custom fields

---

## Use Cases

The generated dataset is suitable for:

- Reinforcement learning (RL) environment initialization
- Model evaluation and fine-tuning
- Synthetic simulation of enterprise project management workflows

---

## Notes

- All text content is generated using deterministic templates and heuristics
- No external APIs or large language models (LLMs) are required
- The dataset scale can be increased or decreased by modifying values in the `.env` file
