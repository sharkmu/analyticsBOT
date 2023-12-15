import asyncio
from database.live_update_database import LiveUpdateDatabase
from config import config

class ChatCount:
    def __init__(self):
        self.task = None
        self.messages = {}
        self.i = 0
        self.db = LiveUpdateDatabase()
        self.data = {}

    async def updateSum(self, gId: int, aId: int, mId: int, tDate: str):
        if self.task is not None:
            self.task.cancel()

        if gId not in self.data:
            self.data[gId] = {}

        if aId not in self.data[gId]:
            self.data[gId][aId] = []

        self.data[gId][aId].append(tDate)

        self.task = asyncio.create_task(self.delayed_task(self.data))

    async def delayed_task(self, datas):
        if self.i >= config.MAX_INDEX:
            self.update_db(datas)
            self.i = 0
            self.task.cancel() #type: ignore

        await asyncio.sleep(config.DELAY)

        self.update_db(datas)
        self.i = 0
    
    def update_db(self, datas):
        for gId, aId in datas.items():
            for aId, messages in aId.items():
                for message in messages:
                    self.db.update_chat_count(str(gId), str(aId), str(message))
                    self.data = {}