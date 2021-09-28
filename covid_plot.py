from flask import Flask
from flask import render_template

import io
import random
from flask import Response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import pandas as pd

import threading


data_url = "https://covid19-lake.s3.us-east-2.amazonaws.com/rearc-covid-19-world-cases-deaths-testing/csv/covid-19-world-cases-deaths-testing.csv"

# data_url = "covid-19-world-cases-deaths-testing.csv"

def plot_data():

    data = pd.read_csv(data_url)

    newzealand = data[data["location"] == "New Zealand"]

    last30 = newzealand[-30:]

    date = pd.to_datetime(last30["date"]).dt.strftime("%m/%d")

    fig = Figure(figsize=(18, 12))

    axis1 = fig.add_subplot(2, 1, 1)

    axis1.plot(date, last30["total_cases"], label='Total Cases')

    axis1.set_title("Total Cases in recent 30 days")

    axis2 = fig.add_subplot(2, 1, 2)

    axis2.plot(date, last30["total_deaths"], label = "Total Deaths")

    axis2.set_title("Total Deaths in recent 30 days")
    
    output = io.BytesIO()

    FigureCanvas(fig).print_png(output)

    return data, output


data, output = plot_data()



one_day = 60 * 60 * 24

# one_day = 60


def upddate_plot():

    global data
    global output

    print("update")

    try:
        data, output = plot_data()
    except Exception as e:
        print(e)
    finally:

        timer = threading.Timer(one_day, upddate_plot)

        timer.start()



timer = threading.Timer(one_day, upddate_plot)

timer.start()

app = Flask(__name__)

@app.route('/plot.png')
def image_plot():
    # fig = create_figure()
    # output = io.BytesIO()
    # FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

@app.route('/')
def getIndex(name=None):
    return render_template('index.html', name=name)


