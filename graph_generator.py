import psycopg2
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import matplotlib.dates as mdates
import matplotlib.patches as mpatches
import os
from dotenv import load_dotenv
import numpy as np
import pandas as pd

LITTERBOX_BIN_SIZE = 5

load_dotenv()


def generate_graph():
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS")
    )
    cur = conn.cursor()
    

    #region Pet weight over time
    query = """
        SELECT timestamp, content_pet_weight_lb
        FROM litterbox_events
        WHERE content_pet_weight_lb IS NOT NULL AND enum_event_type = 'pet_out'
        ORDER BY timestamp ASC;
    """
    cur.execute(query)
    rows = cur.fetchall()
    
    

    if not rows:
        print("No data found.")
        return

    times, weights = zip(*rows)

    plt.figure(figsize=(10, 4))
    plt.plot(times, weights, marker='o')
    plt.title("Mi-chan Weight Over Time")
    plt.xlabel("Time")
    
    date_format = DateFormatter("%a %m/%d")
    hour_format = DateFormatter("%I:%M %p")
    plt.gca().xaxis.set_major_formatter(date_format)
    plt.gca().xaxis.set_minor_formatter(hour_format)
    plt.xticks(rotation=90)
    

    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=1))
    plt.gca().xaxis.set_minor_locator(mdates.HourLocator(interval=4))

    for label in plt.gca().get_xticklabels(minor=False) + plt.gca().get_xticklabels(minor=True):
        label.set_rotation(90)
        label.set_ha('center')  # optional: aligns text for readability
    
    # Set major tick labels to blue
    for label in plt.gca().get_xticklabels(minor=False):
        label.set_color("blue")

    plt.ylabel("Weight (lb)")
    plt.grid(True)
    plt.tight_layout()
    os.makedirs("static", exist_ok=True)
    plt.savefig("static/weight_chart.png")
    plt.close()
    #endregion

    cur.close()
    conn.close()

def generate_duration_histogram():
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS")
    )
    cur = conn.cursor()

    query = """
        SELECT content_toilet_duration, content_toilet_usage_type
        FROM litterbox_events
        WHERE content_toilet_duration IS NOT NULL
          AND content_toilet_usage_type IN ('pee', 'poo')
          AND timestamp >= NOW() - INTERVAL '30 days';
    """

    cur.execute(query)
    rows = cur.fetchall()
    cur.close()
    conn.close()

    if not rows:
        print("No data for histogram.")
        return

    # Separate durations by usage type
    durations_pee = [row[0] for row in rows if row[1] == 'pee']
    durations_poo = [row[0] for row in rows if row[1] == 'poo']

    bin_edges = list(range(30,200,LITTERBOX_BIN_SIZE))

    # Calculate averages
    avg_pee = np.mean(durations_pee) if durations_pee else 0
    avg_poo = np.mean(durations_poo) if durations_poo else 0

    plt.figure(figsize=(8, 4))
    plt.hist(
        [durations_pee, durations_poo],
        bins=bin_edges,
        color=['gold', 'saddlebrown'],
        label=['Pee', 'Poo'],
        edgecolor='black',
        stacked=True
    )
    plt.title("Distribution of Litterbox Duration - Last 30 Days")
    plt.xlabel("Duration (seconds)")
    plt.ylabel("Frequency")
    plt.grid(True)
    plt.tight_layout()

    # Overlay average lines
    
    pee_patch = mpatches.Patch(color='yellow', label='Pee')
    poo_patch = mpatches.Patch(color='saddlebrown', label='Poo')
    avg_pee_line = mpatches.Patch(facecolor='none', edgecolor='gold', linestyle='--', linewidth=2, label=f'Avg Pee: {avg_pee:.1f} s')
    avg_poo_line = mpatches.Patch(facecolor='none', edgecolor='saddlebrown', linestyle='--', linewidth=2, label=f'Avg Poo: {avg_poo:.1f} s')

    plt.legend(handles=[pee_patch, poo_patch, avg_pee_line, avg_poo_line])

    plt.axvline(avg_pee, color='gold', linestyle='--', linewidth=2)
    plt.axvline(avg_poo, color='saddlebrown', linestyle='--', linewidth=2)
    #plt.legend()

    os.makedirs("static", exist_ok=True)
    plt.savefig("static/toilet_duration_histogram.png")
    plt.close()

def generate_usage_bar_chart():
    # Connect to DB
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS")
    )
    query = """
        SELECT
            DATE(timestamp) AS day,
            content_toilet_usage_type,
            COUNT(*) AS count
        FROM litterbox_events
        WHERE content_toilet_usage_type IN ('pee', 'poo')
          AND timestamp >= NOW() - INTERVAL '14 days'
        GROUP BY day, content_toilet_usage_type
        ORDER BY day ASC;
    """
    df = pd.read_sql(query, conn)
    conn.close()

    # convert df['day'] to datetime
    df['day'] = pd.to_datetime(df['day'])

    # Pivot to get stacked bar format: rows = day, columns = usage_type
    pivot_df = df.pivot(index='day', columns='content_toilet_usage_type', values='count').fillna(0)

    # Sort columns to ensure 'pee' then 'poo' order
    pivot_df = pivot_df[['pee', 'poo']] if 'pee' in pivot_df and 'poo' in pivot_df else pivot_df

    # Plot
    ax = pivot_df.plot(
        kind='bar',
        stacked=True,
        figsize=(12, 6),
        color={'pee': 'gold', 'poo': 'saddlebrown'},
        width=0.8,
        edgecolor='black'
    )
    plt.title("Daily Toilet Usage (Last 14 Days)")
    plt.xlabel("Date")
    plt.ylabel("Number of Events")
    plt.xticks(rotation=45, ha='center')
    plt.tight_layout()

    # Format x-axis tick labels as date strings:
    formatted_dates = pivot_df.index.strftime('%a %m/%d')  # format each date string
    ax.set_xticklabels(formatted_dates, rotation=45, ha='center')

    #annotate the bars with counts
    # Annotate each bar segment
    for i, (index, row) in enumerate(pivot_df.iterrows()):
        cumulative_height = 0
        for usage_type in pivot_df.columns:
            value = row[usage_type]
            if value > 0:
                ax.text(
                    i,                              # x-position (bar index)
                    cumulative_height + value / 2,  # y-position (middle of segment)
                    str(int(value)),                # label text
                    ha='center', va='center', fontsize=14, color='black'
                )
                cumulative_height += value

    os.makedirs("static", exist_ok=True)
    plt.savefig("static/toilet_usage_bar_chart.png")
    plt.close()

if __name__ == "__main__":
    #generate_graph()
    #generate_duration_histogram()
    generate_usage_bar_chart()