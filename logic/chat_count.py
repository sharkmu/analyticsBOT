import asyncio

class ChatCount:
    def __init__(self):
        self.guilds = {}
        self.messages = {}
        self.i = 0
        self.count = {}

    async def updateSum(self, gId: int, aId: int, mId: int, tDate: str):
        if gId not in self.guilds:
            self.guilds[gId] = {"messageId": None, "update_task": None}
        if gId not in self.count:
            self.count[gId] = {"index": 0}
        
        guild = self.guilds[gId]
        if guild["update_task"] is not None:
            guild["update_task"].cancel()

        self.count[gId]["index"] += 1
        self.i += 1
        self.messages[self.i] = {"guildId": gId, "authorId": aId, "timeDate": tDate}

        guild["messageId"] = mId
        guild["update_task"] = asyncio.create_task(self.delayed_db_update(gId))

    async def delayed_db_update(self, gId):
        if self.count[gId]["index"] >= 5:
            print(f"TODO: UPDATE DB for {gId}")
            self.count[gId]["index"] = 0
            print(self.count)
            self.guilds[gId]["update_task"].cancel()
        await asyncio.sleep(5)
        print(f"TODO: UPDATE DB for {gId}")
        self.count[gId]["index"] = 0