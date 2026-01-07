PRAGMA foreign_keys = ON;

-- =========================
-- ORGANIZATIONS / WORKSPACES
-- =========================
CREATE TABLE organizations (
    org_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    domain TEXT UNIQUE,
    created_at TIMESTAMP NOT NULL
);

-- =====
-- USERS
-- =====
CREATE TABLE users (
    user_id TEXT PRIMARY KEY,
    org_id TEXT NOT NULL,
    full_name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    role TEXT CHECK (role IN ('admin', 'member')) NOT NULL,
    joined_at TIMESTAMP NOT NULL,
    FOREIGN KEY (org_id) REFERENCES organizations(org_id)
);

-- =====
-- TEAMS
-- =====
CREATE TABLE teams (
    team_id TEXT PRIMARY KEY,
    org_id TEXT NOT NULL,
    name TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL,
    FOREIGN KEY (org_id) REFERENCES organizations(org_id)
);

-- ==================
-- TEAM MEMBERSHIPS
-- ==================
CREATE TABLE team_memberships (
    team_id TEXT NOT NULL,
    user_id TEXT NOT NULL,
    PRIMARY KEY (team_id, user_id),
    FOREIGN KEY (team_id) REFERENCES teams(team_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- =========
-- PROJECTS
-- =========
CREATE TABLE projects (
    project_id TEXT PRIMARY KEY,
    team_id TEXT NOT NULL,
    name TEXT NOT NULL,
    project_type TEXT CHECK (
        project_type IN ('engineering', 'marketing', 'operations')
    ) NOT NULL,
    created_at TIMESTAMP NOT NULL,
    due_date DATE,
    FOREIGN KEY (team_id) REFERENCES teams(team_id)
);

-- =========
-- SECTIONS
-- =========
CREATE TABLE sections (
    section_id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    name TEXT NOT NULL,
    position INTEGER NOT NULL,
    FOREIGN KEY (project_id) REFERENCES projects(project_id)
);

-- =====
-- TASKS
-- =====
CREATE TABLE tasks (
    task_id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    section_id TEXT,
    assignee_id TEXT,
    name TEXT NOT NULL,
    description TEXT,
    due_date DATE,
    completed BOOLEAN NOT NULL DEFAULT 0,
    created_at TIMESTAMP NOT NULL,
    completed_at TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES projects(project_id),
    FOREIGN KEY (section_id) REFERENCES sections(section_id),
    FOREIGN KEY (assignee_id) REFERENCES users(user_id)
);

-- =========
-- SUBTASKS
-- =========
CREATE TABLE subtasks (
    subtask_id TEXT PRIMARY KEY,
    parent_task_id TEXT NOT NULL,
    assignee_id TEXT,
    name TEXT NOT NULL,
    completed BOOLEAN NOT NULL DEFAULT 0,
    created_at TIMESTAMP NOT NULL,
    completed_at TIMESTAMP,
    FOREIGN KEY (parent_task_id) REFERENCES tasks(task_id),
    FOREIGN KEY (assignee_id) REFERENCES users(user_id)
);

-- ==========
-- COMMENTS
-- ==========
CREATE TABLE comments (
    comment_id TEXT PRIMARY KEY,
    task_id TEXT NOT NULL,
    user_id TEXT NOT NULL,
    body TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL,
    FOREIGN KEY (task_id) REFERENCES tasks(task_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- =====
-- TAGS
-- =====
CREATE TABLE tags (
    tag_id TEXT PRIMARY KEY,
    name TEXT UNIQUE NOT NULL
);

-- ====================
-- TASK ↔ TAG MAPPING
-- ====================
CREATE TABLE task_tags (
    task_id TEXT NOT NULL,
    tag_id TEXT NOT NULL,
    PRIMARY KEY (task_id, tag_id),
    FOREIGN KEY (task_id) REFERENCES tasks(task_id),
    FOREIGN KEY (tag_id) REFERENCES tags(tag_id)
);

-- =====================
-- CUSTOM FIELD DEFINITIONS
-- =====================
CREATE TABLE custom_fields (
    field_id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    name TEXT NOT NULL,
    field_type TEXT CHECK (
        field_type IN ('text', 'number', 'enum')
    ) NOT NULL,
    FOREIGN KEY (project_id) REFERENCES projects(project_id)
);

-- =====================
-- CUSTOM FIELD VALUES
-- =====================
CREATE TABLE custom_field_values (
    field_id TEXT NOT NULL,
    task_id TEXT NOT NULL,
    value TEXT,
    PRIMARY KEY (field_id, task_id),
    FOREIGN KEY (field_id) REFERENCES custom_fields(field_id),
    FOREIGN KEY (task_id) REFERENCES tasks(task_id)
);
