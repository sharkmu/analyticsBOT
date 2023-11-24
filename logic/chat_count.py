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
        self.i += 1
        self.messages[self.i] = {"guildId": gId, "authorId": aId, "timeDate": tDate}

        guild = self.guilds[gId]

        self.count[gId] = {"index": self.i}

        if guild["update_task"] is not None:
            guild["update_task"].cancel()

        guild["messageId"] = mId

        guild["update_task"] = asyncio.create_task(self.delayed_db_update(gId))

    async def delayed_db_update(self, gId):
        if self.count[gId]["index"] > 5:
            print(f"i is greater than 5 {gId}") 
            self.i = 0
        await asyncio.sleep(5)
        print(f"TODO: UPDATE DB for {gId}") #TODO UPDATE DB - DECA'S TASK
        print(self.messages)