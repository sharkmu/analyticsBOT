import asyncio
ids = []

class ChatCount:
    async def updateSum(self, msg: int):
        ids.append(msg)
        await asyncio.sleep(5)
        print("5s is gone")
        if ids[-1] == msg:
            print("TODO: UPDATE DB") #TODO UPDATE DB - DECA'S TASK
        elif len(ids) > 250:
            print("TODO: UPDATE DB") #TODO UPDATE DB - DECA'S TASK