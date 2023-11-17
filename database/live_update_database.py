import sqlite3
import os
from dataclasses import dataclass


@dataclass
class GuildData:
    member_count: int
    user_ban_count: int = 0
    chat_count: int = 0


@dataclass
class Guild:
    guild_id: str
    guild_data: GuildData


class Database:
    def __init__(self, db_name: str | None, temp_db_name: str = "bot_test"):
        cwd = os.getcwd()

        os.makedirs(f"{cwd}/database/db", exist_ok=True)

        if db_name == None or db_name == "":
            self.db_path = f"{cwd}/database/db/{temp_db_name}.db"
        else:
            self.db_path = f"{cwd}/database/db/{db_name}.db"

        self.get_connection = lambda: sqlite3.connect(self.db_path)


class LiveUpdateDatabase(Database):
    def __init__(self, db_name: str = None):
        super().__init__(db_name)

        con = self.get_connection()
        cur = con.cursor()

        guild = cur.execute(
            """
                CREATE TABLE IF NOT EXISTS
                    guilds (
                        guild_id TEXT PRIMARY KEY, 
                        member_count INTEGER, 
                        user_ban_count INTEGER, 
                        chat_count INTEGER
                    );
            """
        )

        con.commit()
        con.close()

        if guild == None:
            raise Exception("Could not complete database setup.")

    def get_guild(self, guild_id: str) -> Guild | None:
        con = self.get_connection()
        cur = con.cursor()

        guild = cur.execute(
            """
                SELECT
                    *
                FROM
                    guilds
                WHERE
                    guild_id = ?;
            """,
            (guild_id,)
        ).fetchone()

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
            )

            return guild_data
        else:
            return None

    def add_or_update_guild(self, guild_id: str, guild_data_arg: GuildData = None):
        con = self.get_connection()
        cur = con.cursor()

        existing_guild = self.get_guild(guild_id)

        # Use default value when neither the argument
        # nor the existing guild data has a value.
        default = GuildData(
            member_count=0,
            user_ban_count=0,
            chat_count=0
        )

        if existing_guild and existing_guild.guild_data:
            using_guild_data = existing_guild.guild_data
        else:
            using_guild_data = default

        using_guild_data = GuildData(
            member_count=getattr(
                guild_data_arg,
                'member_count',
                using_guild_data.member_count
            ),
            user_ban_count=getattr(
                guild_data_arg,
                'user_ban_count',
                using_guild_data.user_ban_count
            ),
            chat_count=getattr(
                guild_data_arg,
                'chat_count',
                using_guild_data.chat_count
            )
        )

        # Update guild data if the guild already exists.
        # Otherwise, add one.
        if existing_guild != None:
            cur.execute(
                """
                    UPDATE
                        guilds
                    SET
                        member_count = ?,
                        user_ban_count = ?,
                        chat_count = ?
                    WHERE
                        guild_id = ?;
                """,
                (
                    using_guild_data.member_count,
                    using_guild_data.user_ban_count,
                    using_guild_data.chat_count,
                    guild_id
                )
            )
        elif existing_guild == None:
            cur.execute(
                """
                    INSERT INTO
                        guilds
                    VALUES
                        (?, ?, ?, ?);
                """,
                (
                    guild_id,
                    using_guild_data.member_count,
                    using_guild_data.user_ban_count,
                    using_guild_data.chat_count,
                )
            )

        con.commit()
        con.close()

    def delete_guild(self, guild_id: str) -> bool:
        con = self.get_connection()
        cur = con.cursor()

        cur.execute(
            """
                DELETE FROM
                    guilds
                WHERE
                    guild_id = ?
            """,
            (guild_id,)
        )
        deleted_rows = cur.rowcount

        con.commit()
        con.close()

        if deleted_rows < 1:
            return False

        return True
