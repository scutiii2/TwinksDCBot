CREATE TABLE IF NOT EXISTS cases(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    case_number INTEGER NOT NULL,

    target_id INTEGER NOT NULL,

    moderator_id INTEGER NOT NULL,

    action TEXT NOT NULL,

    reason TEXT,

    created_at INTEGER NOT NULL,

    expires_at INTEGER,

    active INTEGER NOT NULL DEFAULT 1
);

CREATE INDEX IF NOT EXISTS idx_cases_number
ON cases(case_number);

CREATE INDEX IF NOT EXISTS idx_cases_target
ON cases(target_id);

CREATE INDEX IF NOT EXISTS idx_cases_action
ON cases(action);