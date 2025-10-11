import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
from io import BytesIO

def generation():
    # Your date-time strings
    timestamps = ["2023-12-15 19:56:53", "2023-12-16 19:56:53", "2023-12-17 19:56:53", "2023-12-17 19:56:53", "2023-12-07 19:56:53", "2023-12-30 19:56:53", "2023-10-17 19:56:53"]

    # Convert strings to datetime objects
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

fig = generation()

buffer = BytesIO()
fig.savefig(buffer, format="png")
buffer.seek(0)