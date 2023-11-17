import unittest
from database.base import GuildData, UserData, Guild, DiscordBotDatabase
import os

# Enter following command to run tests:
# python3 -m unittest


class DatabaseMethodTest(unittest.TestCase):
    def setUp(self):
        self.db = DiscordBotDatabase()

    def test_1_delete_db(self):
        os.remove(self.db.db_path)

    def test_2_add_guild(self):
        self.db.add_or_update_guild(
            guild_id="123",
            guild_data_arg=GuildData(
                member_count=32,
                user_ban_count=4,
                chat_count=0,
            )
        )

        # ----
        input = self.db.get_guild(guild_id="123")
        expected_output = Guild(
            guild_id="123",
            guild_data=GuildData(
                member_count=32,
                user_ban_count=4,
                chat_count=0,
            ),
            user_list=[]
        )
        self.assertEqual(
            input,
            expected_output
        )

    def test_3_add_user(self):
        self.db.add_or_update_user(
            guild_id="123",
            user_id="1"
        )

        # ----
        input = self.db.get_user(
            guild_id="123",
            user_id="1"
        )
        expected_output = UserData(
            guild_id="123",
            user_id="1",
            chat_count=0
        )
        self.assertEqual(
            input,
            expected_output
        )

    def test_4_update_user_chat_count(self):
        updating_user_data = self.db.get_user(
            guild_id="123",
            user_id="1",
        )

        self.db.add_or_update_user(
            guild_id="123",
            user_id="1",
            user_data_arg=UserData(
                guild_id="123",
                user_id="1",
                chat_count=updating_user_data.chat_count + 1
            )
        )

        # ----
        input = self.db.get_user(
            guild_id="123",
            user_id="1"
        )
        expected_output = UserData(
            guild_id="123",
            user_id="1",
            chat_count=1
        )
        self.assertEqual(input, expected_output)

    def test_5_delete_user(self):
        is_successful = self.db.delete_user(
            guild_id="123",
            user_id="1"
        )
        self.assertEqual(is_successful, True)

    def test_6_delete_guild(self):
        is_successful = self.db.delete_guild(guild_id="123")
        self.assertEqual(is_successful, True)


if __name__ == '__main__':
    unittest.main()
