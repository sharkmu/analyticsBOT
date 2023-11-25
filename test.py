from database.live_update_database import GuildData, LiveUpdateDatabase
import unittest
import os

# Enter following command to run tests:
# python3 -m unittest


class TestLiveUpdateDatabase(unittest.TestCase):
    def setUp(self):
        self.db = LiveUpdateDatabase()

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
        expected_output = GuildData(
            guild_id="123",
            member_count=32,
            user_ban_count=4,
            chat_count=0,
        )
        self.assertEqual(
            input,
            expected_output
        )

    def test_6_delete_guild(self):
        is_successful = self.db.delete_guild(guild_id="123")
        self.assertEqual(is_successful, True)


if __name__ == '__main__':
    unittest.main()