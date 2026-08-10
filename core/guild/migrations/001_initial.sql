CREATE TABLE IF NOT EXISTS guild_prefixes(
    guild_id INTEGER PRIMARY KEY,
    prefix   TEXT NOT NULL DEFAULT '!'
);