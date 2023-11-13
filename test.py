import unittest
from database.classes import GuildData, Guild, DiscordBotDatabase

# Enter following command to run tests:
# python3 -m unittest


class DatabaseTest(unittest.TestCase):
    def test_add_guild(self):
        db = DiscordBotDatabase()
        db.add_or_update_guild(guild_id="1234567890", guild_data=GuildData(
            member_count=32, user_ban_count=4, chat_count=0))

        self.assertEqual(db.get_guild(guild_id="1234567890"), Guild(guild_id='1234567890', guild_data=GuildData(
            member_count=0, user_ban_count=0, chat_count=0), user_data=[]))

    def test_delete_guild(self):
        db = DiscordBotDatabase()
        is_successful = db.delete_guild(guild_id="1234567890")

        self.assertEqual(is_successful, True)


if __name__ == '__main__':
    unittest.main()
