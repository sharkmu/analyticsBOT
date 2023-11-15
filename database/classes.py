import sqlite3
import os
from dataclasses import dataclass


@dataclass
class UserData:
    guild_id: str
    user_id: str
    chat_count: int = 0


@dataclass
class GuildData:
    member_count: int
    user_ban_count: int = 0
    chat_count: int = 0


@dataclass
class Guild:
    guild_id: str
    guild_data: GuildData
    user_list: list[UserData]


class Database:
    def __init__(self, db_name: str | None, temp_db_name: str = "bot_test"):
        cwd = os.getcwd()

        os.makedirs(f"{cwd}/database/db", exist_ok=True)

        if db_name == None or db_name == "":
            self.db_path = f"{cwd}/database/db/{temp_db_name}.db"
        else:
            self.db_path = f"{cwd}/database/db/{db_name}.db"

        self.get_connection = lambda: sqlite3.connect(self.db_path)


class DiscordBotDatabase(Database):
    def __init__(self, db_name: str = None):
        super().__init__(db_name)

        con = self.get_connection()
        cur = con.cursor()

        guild = cur.execute("""
            CREATE TABLE IF NOT EXISTS
                guilds (
                    guild_id TEXT PRIMARY KEY, 
                    member_count INTEGER, 
                    user_ban_count INTEGER, 
                    chat_count INTEGER
                );
""")
        users = cur.execute("""
            CREATE TABLE IF NOT EXISTS
                users(
                    guild_id TEXT, 
                    user_id TEXT, 
                    chat_count INTEGER, 
                    PRIMARY KEY (guild_id, user_id)
                );
        """)

        con.commit()
        con.close()

        if guild == None or users == None:
            raise Exception("Could not complete database setup.")

    def get_guild(self, guild_id: str) -> Guild | None:
        con = self.get_connection()
        cur = con.cursor()

        guild = cur.execute("""
            SELECT
                *
            FROM
                guilds
            WHERE
                guild_id = ?;
        """, (guild_id,)
        ).fetchone()
        users = cur.execute("""
            SELECT
                *
            FROM
                users
            WHERE
                guild_id = ?;
        """, (guild_id,)
        ).fetchall()

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
                user_list=[
                    UserData(
                        guild_id=user[0],
                        user_id=user[1],
                        chat_count=user[2]
                    ) for user in users
                ]
            )

            return guild_data
        else:
            return None

    def get_user(self, guild_id: str, user_id: str) -> UserData | None:
        con = self.get_connection()
        cur = con.cursor()

        user = cur.execute(
            """
            SELECT
                *
            FROM
                users
            WHERE
                guild_id = ?
                AND user_id = ?;
            """,
            (
                guild_id,
                user_id,
            )
        ).fetchone()

        con.commit()
        con.close()

        if user != None:
            user_data = UserData(
                guild_id=user[0],
                user_id=user[1],
                chat_count=user[2]
            )

            return user_data
        else:
            return None

    def add_or_update_guild(self, guild_id: str, guild_data: GuildData = None):
        con = self.get_connection()
        cur = con.cursor()

        # If guild data is not provided, use default values.
        using_guild_data = GuildData(
            member_count=0,
            user_ban_count=0,
            chat_count=0
        )
        if guild_data != None:
            using_guild_data = GuildData(
                member_count=0 if guild_data.member_count == None else guild_data.member_count,
                user_ban_count=0 if guild_data.user_ban_count == None else guild_data.user_ban_count,
                chat_count=0 if guild_data.chat_count == None else guild_data.chat_count
            )

        # Update guild data if the guild already exists. Otherwise, add one.
        existing_guild = self.get_guild(guild_id)

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
                ))

        con.commit()
        con.close()

    def add_or_update_user(self, guild_id: str, user_id: str, user_data: UserData = None):
        con = self.get_connection()
        cur = con.cursor()

        # If user data is not provided, use default values.
        using_user_data = UserData(
            user_id=user_id,
            guild_id=guild_id,
            chat_count=0
        )
        if user_data != None:
            using_user_data = UserData(
                user_id=user_id,
                guild_id=guild_id,
                chat_count=0 if user_data.chat_count == None else user_data.chat_count
            )

        # Update user data if the user already exists. Otherwise, add one.
        existing_user_data = self.get_user(guild_id, user_id)

        if existing_user_data != None:
            cur.execute(
                """
                UPDATE
                    users
                SET
                    chat_count = ?
                WHERE
                    guild_id = ? AND user_id = ?;
                """,
                (using_user_data.chat_count, guild_id, user_id,)
            )

        elif existing_user_data == None:
            cur.execute(
                """
                INSERT INTO
                    users
                VALUES
                    (?, ?, ?);
                """,
                (guild_id, user_id, 0,)
            )

        con.commit()
        con.close()

    def delete_guild(self, guild_id: str) -> bool:
        con = self.get_connection()
        cur = con.cursor()

        cur.execute(
            "DELETE FROM users WHERE guild_id = ?",
            (guild_id,)
        )
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

    def delete_user(self, guild_id: str, user_id: str) -> bool:
        con = self.get_connection()
        cur = con.cursor()

        cur.execute(
            """
            DELETE FROM
                users
            WHERE
                guild_id = ?
                AND user_id = ?
            """,
            (guild_id, user_id,)
        )
        deleted_rows = cur.rowcount

        con.commit()
        con.close()

        if deleted_rows < 1:
            return False

        return True
