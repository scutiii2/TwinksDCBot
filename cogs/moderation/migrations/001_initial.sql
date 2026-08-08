-- -----------------------------------------------------------------------------
-- Other Moderation 
-- -----------------------------------------------------------------------------
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

-- -----------------------------------------------------------------------------
-- Role option messages
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS role_options(
    message_id INTEGER PRIMARY KEY,
    channel_id INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS role_option_roles(
    message_id INTEGER NOT NULL,
    role_id INTEGER NOT NULL,
    emoji TEXT NOT NULL,

    PRIMARY KEY(
        message_id,
        role_id
    ),

    UNIQUE(
        message_id,
        emoji
    ),

    FOREIGN KEY(
        message_id
    )
    REFERENCES role_options(message_id)
    ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_role_option_roles_emoji
ON role_option_roles(message_id, emoji);