import sqlite3
import os
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
    def __init__(self, db_name: str | None, temp_db_name: str = "bot_test_db"):
        cwd = os.getcwd()

        os.makedirs(f"{cwd}/database/db", exist_ok=True)

        if db_name == None or db_name == "":
            self.db_path = f"{cwd}/database/db/{temp_db_name}"
        else:
            self.db_path = f"{cwd}/database/db/{db_name}"

        self.get_connection = lambda: sqlite3.connect(self.db_path)


class DiscordBotDatabase(Database):
    def __init__(self, db_name: str = None):
        super().__init__(db_name)

        con = self.get_connection()
        cur = con.cursor()

        guild = cur.execute("""
            CREATE TABLE IF NOT EXISTS guilds (
                guild_id TEXT PRIMARY KEY, 
                member_count INTEGER, 
                user_ban_count INTEGER, 
                chat_count INTEGER
            )
""")
        users = cur.execute("""
            CREATE TABLE IF NOT EXISTS users(
                guild_id TEXT, 
                user_id TEXT, 
                chat_count INTEGER, 
                PRIMARY KEY (guild_id, user_id)
            )
        """)

        con.commit()
        con.close()

        if guild == None or users == None:
            raise Exception("Could not complete database setup.")

    def get_guild(self, guild_id: str) -> Guild:
        con = self.get_connection()
        cur = con.cursor()

        guild = cur.execute(
            "SELECT * FROM guilds WHERE guild_id = ?", (guild_id,)).fetchone()
        users = cur.execute(
            "SELECT * FROM users WHERE guild_id = ?", (guild_id,)).fetchmany()

        con.commit()
        con.close()

        if guild != None:
            guild_data = Guild(
                guild_id=guild[0],
                guild_data=GuildData(
                    member_count=guild[1],
                    user_ban_count=guild[2],
                    chat_count=guild[3]
                ),
                user_data=users
            )

            return guild_data
        else:
            return None

    def add_or_update_guild(self, guild_id: str, guild_data: GuildData):
        con = self.get_connection()
        cur = con.cursor()

        existing_guild = self.get_guild(guild_id)

        # Update guild data if it already exists
        # Otherwise, add one.
        if existing_guild != None and existing_guild.guild_data != guild_data:
            existing_guild.guild_data = guild_data
        elif existing_guild == None:
            existing_guild = cur.execute(
                "INSERT INTO guilds VALUES (?, ?, ?, ?)", (guild_id, 0, 0, 0,)).fetchone()

        con.commit()
        con.close()

        # Return added or updated guild
        if existing_guild != None:
            returning_guild = Guild(
                guild_id=existing_guild.guild_id,
                guild_data=GuildData(
                    member_count=existing_guild.guild_data.member_count,
                    user_ban_count=existing_guild.guild_data.user_ban_count,
                    chat_count=existing_guild.guild_data.chat_count
                ),
                user_data=[existing_guild.user_data]
            )

            return returning_guild
        else:
            return None

    def delete_guild(self, guild_id: str):
        con = self.get_connection()
        cur = con.cursor()

        cur.execute("DELETE FROM guilds WHERE guild_id = ?", (guild_id,))
        deleted_rows = cur.rowcount

        con.commit()
        con.close()

        # Return `False` when no rows were deleted.
        if deleted_rows > 0:
            return True
        else:
            return False

    def add_or_update_user(guild_id: str, user_id: str):

        pass
