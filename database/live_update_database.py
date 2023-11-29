from dataclasses import dataclass
from database.base import Database


@dataclass
class GuildData:
    guild_id: str | None = None
    member_count: int = 0
    user_ban_count: int = 0
    chat_count: int = 0


class LiveUpdateDatabase(Database):
    def __init__(self, db_name: str | None = None):
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

        language = cur.execute(
            """
                CREATE TABLE IF NOT EXISTS
                    languages (
                        guild_id TEXT PRIMARY KEY, 
                        language TEXT
                    );
            """
        )

        chat_count_guild = cur.execute(
            """
                CREATE TABLE IF NOT EXISTS
                    chat_count_guild (
                        guild_id TEXT PRIMARY KEY
                    );
            """
        )

        chat_count_user = cur.execute(
            """
                CREATE TABLE IF NOT EXISTS
                    chat_count_user (
                        user_id TEXT PRIMARY KEY
                    );
            """
        )

        chat_count_data = cur.execute(
            """
                CREATE TABLE IF NOT EXISTS 
                    chat_count_data (
                        guild_id TEXT,
                        user_id TEXT,
                        data_value TEXT,
                        FOREIGN KEY(guild_id) REFERENCES chat_count_guild(guild_id),
                        FOREIGN KEY(user_id) REFERENCES chat_count_user(user_id)
                    );
            """
        )

        con.commit()
        con.close()

        tables = [guild, language, chat_count_guild, chat_count_user, chat_count_data]
        if any(table is None for table in tables):
            raise Exception("Could not complete database setup.")

    def get_language(self, guild_id: str, update: bool):
        con = self.get_connection()
        cur = con.cursor()

        language = cur.execute(
            """
                SELECT
                    language
                FROM
                    languages
                WHERE
                    guild_id = ?;
            """,
            (guild_id,)
        ).fetchone()

        con.commit()
        con.close()
        
        if update:
            return language
        else:
            if language is not None:
                for i in range(len(language)):
                    if language[i] is None:
                        language[i] = "english"
                return language
            if language is None:
                language = ["english"]
                return language
            return language
            


    def get_guild(self, guild_id: str) -> GuildData | None:
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

        if guild is not None:
            guild_data = GuildData(
                guild_id=guild[0],
                member_count=guild[1],
                user_ban_count=guild[2],
                chat_count=guild[3]
            )

            return guild_data
        else:
            return None

    def add_or_update_guild(self, guild_id: str, guild_data_arg: GuildData | None = None):
        con = self.get_connection()
        cur = con.cursor()

        existing_guild = self.get_guild(guild_id)

        # Use default value when neither the argument
        # nor the existing guild data has a value.
        default = GuildData(
            guild_id=guild_id,
            member_count=0,
            user_ban_count=0,
            chat_count=0
        )

        if existing_guild and existing_guild:
            using_guild_data = existing_guild
        else:
            using_guild_data = default

        using_guild_data = GuildData(
            guild_id=guild_id,
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
        if existing_guild is not None:
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
        elif existing_guild is not None:
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
    

    def update_language(self, guild_id: str, language_data: str):
        con = self.get_connection()
        cur = con.cursor()

        guild = self.get_language(guild_id, True)
        
        if guild is None:
            cur.execute(
                """
                    INSERT INTO
                        languages
                    VALUES 
                        (?, ?);
                """,
                (
                    guild_id,
                    language_data,
                )
            )
        elif guild is not None:
            cur.execute(
                """
                    UPDATE
                        languages
                    SET
                        language = ?
                    WHERE
                        guild_id = ?;
                """,
                (
                    language_data,
                    guild_id,
                )
            )

        con.commit()
        con.close()