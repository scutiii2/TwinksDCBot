CREATE TABLE IF NOT EXISTS allowed_guilds(
    guild_id  INTEGER PRIMARY KEY,
    added_by  INTEGER NOT NULL,
    added_at  INTEGER NOT NULL
);
