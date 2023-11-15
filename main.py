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
        html += "    <tr>\n"
        for col in row[:2]:
            html += f"        <td>{col}</td>\n"
        html += "    </tr>\n"

    html += "    </table>"

    return rows[1][0], html

def make_html(path, last_month, html_table):
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
    <p><em>Last updated: {date.today()}</em></p>    
    <p>
        This site contains graphs and a table of Caltrain's average weekday ridership from Jul 2017 to {last_month} sourced from <a href="https://www.caltrain.com/past-board-meetings">Caltrain Board of Directors meeting agendas</a> and JPB Citizens Advisory Committee documents.
        Average weekday ridership is reported with a 1-month lag, so the most recent data is from {last_month}.
    </p>
    <p>
        You can find a <a href="https://github.com/iechevarria/caltrain-ridership/blob/main/ridership.csv">CSV</a> of Caltrain's average weekday ridership and the script to generate this site on <a href="https://github.com/iechevarria/caltrain-ridership">GitHub</a>.
        You can find more of my work on my website, <a href="https://echevarria.io">echevarria.io</a>.
    </p>
    <h2>Why I made this</h2>
    <p>
        It's surprisingly difficult to get a simple graph or table of Caltrain ridership numbers.
        Caltrain's official <a href="https://web.archive.org/web/20220629064038/https://www.caltrain.com/about-caltrain/statistics-reports/ridership">ridership page</a> has links to three different sources, only one of which, the Caltrain Board of Directors monthly meeting agendas, is up-to-date.
        The agenda PDFs are not standardized, so I've manually extracted the ridership numbers from each one and made them available here.
    </p>
    <h2>Graphs</h2>
    <img src="ridership-since-2020.png" alt="Caltrain Ridership">
    <img src="ridership-since-2017.png" alt="Caltrain Ridership">
    <h2>Table (<a href="https://github.com/iechevarria/caltrain-ridership/blob/main/ridership.csv">CSV</a>)</h2>
    {html_table}
    <br>
    <p><em>Site by <a href="https://echevarria.io">Ivan Echevarria</a></em>.</p>
    <script data-goatcounter="https://caltrain-ridership.goatcounter.com/count" async src="//gc.zgo.at/count.js"></script>
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
    last_month, table = generate_html_table("ridership.csv")
    make_html("site/index.html", last_month, table)

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
