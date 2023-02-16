"""
opens ridership.csv and generates a web page with a plot and table of the data

columns: month (string e.g. Jan 2017), average weekday ridership (int), notes (string)
"""

import csv
import matplotlib.pyplot as plt
from datetime import date

def generate_html_table(path):
    """generates an html table from a csv file"""
    with open(path, "r") as f:
        reader = csv.reader(f)
        rows = [("Month", "Average weekday ridership")] + list(reader)[:1:-1]

    html = "<table>\n"

    for row in rows:
        html += "  <tr>\n"
        for col in row[:2]:
            html += f"    <td>{col}</td>\n"
        html += "  </tr>\n"

    html += "</table>\n"

    return html

def make_html(path):
    """creates an html file from a template"""
    site_template=f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Caltrain Ridership</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <h1>Caltrain Ridership</h1>
    <p>Last updated: {date.today()}</p>
    <p>Caltrain ridership data from July 2017 to Dec 2022</p>
    <p>Source: <a href="https://www.caltrain.com/about/ridership.html">https://www.caltrain.com/about/ridership.html</a></p>
    <h2>Graphs</h2>
    <img src="ridership-since-2020.png" alt="Caltrain Ridership">
    <img src="ridership-since-2017.png" alt="Caltrain Ridership">
    <h2>Table</h2>
    <div>
    {generate_html_table("ridership.csv")}
    </div>
</body>
"""
    with open(path, "w") as f:
        f.write(site_template)


def make_plot(months, ridership, name):
    """creates a plot of ridership data"""
    plt.rcParams["font.family"] = "Courier New"
    plt.plot(months, ridership)
    plt.xticks(months[::int(len(months)/5)])
    plt.ylabel("Average Weekday Ridership")
    plt.title(f"Average Weekday Ridership by Month ({months[0]} - {months[-1]})")
    plt.gca().spines["top"].set_visible(False)
    plt.gca().spines["right"].set_visible(False)
    plt.plot(months, ridership, color="#0000ff")
    plt.savefig(f"site/{name}.png", dpi=200, bbox_inches="tight")
    plt.clf()


def main():
    make_html("site/index.html")

    # plot ridership data
    with open("ridership.csv", "r") as f:
        reader = csv.reader(f)
        rows = list(reader)

    months = []
    ridership = []

    for row in rows[1:]:
        months.append(row[0])
        ridership.append(int(row[1]))

    make_plot(months, ridership, "ridership-since-2017")
    make_plot(months[33:], ridership[33:], "ridership-since-2020")

    
if __name__ == '__main__':
    main()
