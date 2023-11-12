import sqlite3
from dataclasses import dataclass


@dataclass
class UserData:
    user_id: str
    chat_count: int


@dataclass
class GuildData:
    member_count: int
    user_ban_count: int
    chat_count: int


@dataclass
class Guild:
    guild_id: str
    guild_data: GuildData
    user_data: list[UserData]


class Database:
    def __init__(self, path: str):
        path_with_extension = path if ".db" in path else f"{path}.db"

        self.connection = sqlite3.connect(path_with_extension)
        self.cursor = self.connection.cursor()


class DiscordBotDatabase(Database):
    def __init__(self, path: str = "discord_bot_database.db"):
        super().__init__(path)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS guilds (
                guild_id TEXT PRIMARY KEY, 
                member_count INTEGER, 
                user_ban_count INTEGER, 
                chat_count INTEGER
            )
""")
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users(
                guild_id TEXT, 
                user_id TEXT, 
                chat_count INTEGER, 
                PRIMARY KEY (guild_id, user_id)
            )
        """)

    def get_guild(self, guild_id: str):
        pass

    def add_or_update_guild(guild_id: str, guild_data: GuildData):
        pass

    def remove_guild(guild_id: str):
        pass

    def add_or_update_user(guild_id: str, user_id: str):
        pass
