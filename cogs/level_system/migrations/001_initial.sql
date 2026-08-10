CREATE TABLE IF NOT EXISTS user_levels(
    user_id   INTEGER NOT NULL,
    guild_id  INTEGER NOT NULL,
    xp        INTEGER NOT NULL DEFAULT 0,
    level     INTEGER NOT NULL DEFAULT 1,
    PRIMARY KEY (user_id, guild_id)
);

-- 🔎 Fast lookup indexes
-- Quickly fetch a user’s level in a guild
CREATE INDEX IF NOT EXISTS idx_user_levels_user_guild
ON user_levels(user_id, guild_id);

-- Efficiently rank users by XP in a guild
CREATE INDEX IF NOT EXISTS idx_user_levels_guild_xp
ON user_levels(guild_id, xp DESC);

-- Optional: if you often query by user_id globally
CREATE INDEX IF NOT EXISTS idx_user_levels_user
ON user_levels(user_id);
