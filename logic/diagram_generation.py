from database.live_update_database import LiveUpdateDatabase
import matplotlib.dates as mdates
from datetime import datetime
import matplotlib.pyplot as plt
import json

class DiagramLogic:
    def __init__(self):
        self.db = LiveUpdateDatabase()
    
    def generate(self, guild_id, author_id):
        data = self.db.get_chat_count(guild_id, author_id)

        s = data[0]

        lst = json.loads(s)
        
        timestamps = [i for i in lst]
        
        timestamps = [datetime.strptime(ts, "%Y-%m-%d %H:%M:%S") for ts in timestamps]

        # Some example data
        data = [1, 3, 2, 5, 7281, 189, 1]

        # Create the plot
        fig, ax = plt.subplots()
        ax.plot(timestamps, data, marker="o")

        # Format the x-axis to display the dates correctly
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))
        fig.autofmt_xdate()

        return fig