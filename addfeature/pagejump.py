import tkinter as tk
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database.database import Database
from addfeature.notificationbox import opennotification
from sessions import Session
from datetime import datetime

db=Database()
allexer=db.getRelation('ExerRecord').getRowsWhereEqual('user_id',6)
exerrecords=dict()
for i in allexer:
    if i[3].strftime("%Y-%m-%d") in exerrecords:
        exerrecords[i[3].strftime("%Y-%m-%d")]+=1
    else:
        exerrecords[i[3].strftime("%Y-%m-%d")]=1
print(exerrecords)
# userdata=room1.getRowsWhereEqual("user_id",3)
sorted_list = sorted(exerrecords.items(), key=lambda x: datetime.strptime(x[0], "%Y-%m-%d"))
print(sorted_list)
displaynum=8
if len(sorted_list)>displaynum:
    sorted_list=sorted_list[-displaynum:]

dates = []
values = []
num_bars = len(sorted_list)
for i in sorted_list:
    dates.append(i[0])
    values.append(i[1])

root = tk.Tk()
root.title("Bar Chart Example")

        # Create a Canvas to draw the chart
canvas = tk.Canvas(root, width=600, height=400, bg="white")
canvas.pack(fill="both", expand=True)

# Draw the bar chart


def draw_bar_chart():
    # Dimensions
    chart_width = 500
    chart_height = 300
    padding = 50
    bar_width = 40
    max_value = max(values)

    # Calculate scaling factor
    scale = chart_height / max_value if max_value > 0 else 1

    # X-axis and Y-axis
    canvas.create_line(
        padding, chart_height + padding, chart_width + padding, chart_height + padding, width=2
    )
    canvas.create_line(
        padding, padding, padding, chart_height + padding, width=2
    )

    # Draw bars and labels

    for i in range(num_bars):
        x0 = padding + i * (bar_width + 20)
        y0 = chart_height + padding - (values[i] * scale)
        x1 = x0 + bar_width
        y1 = chart_height + padding

        # Draw the bar
        canvas.create_rectangle(x0, y0, x1, y1, fill="blue", outline="black")

        # Add text labels (value)
        canvas.create_text(
            (x0 + x1) / 2, y0 - 10, text=str(values[i]), anchor="s", font=("Arial", 10)
        )

        # Add text labels (date)
        canvas.create_text(
            (x0 + x1) / 2, chart_height + padding + 15, text=dates[i], anchor="n", font=("Arial", 10)
        )

draw_bar_chart()

root.mainloop()