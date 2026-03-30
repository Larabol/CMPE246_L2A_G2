from flask import Flask, render_template, jsonify
import pandas as pd
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import DatetimeTickFormatter
import json
import os

app = Flask(__name__)

# Route for the main page
@app.route("/")
def index():
    # Read CSV file
    df = pd.read_csv("bmsdata.csv")

    # Rename columns for easier access in Jinja
    df.rename(columns={
    'timestamp': 'time',
    'voltage': 'voltage',
    'current': 'current',
    'temperature': 'temperature',
    'soc': 'soc'
    }, inplace=True)

    # Convert dataframe to list of dictionaries
    data = df.to_dict(orient='records')

    df['time'] = pd.to_datetime(df['time'])

    # Create Bokeh figure
    p = figure(
        title="Voltage vs Time", 
        y_axis_label="Voltage (mV)",
        x_axis_label="Time(???)",
        x_axis_type= 'datetime',
        height=300, 
        sizing_mode="stretch_width"
    )

    x_values = df['time'][:50]
    y_values = df['voltage'][:50]

    p.xaxis.formatter = DatetimeTickFormatter(
        seconds="%H:%M:%S",
        minutes="%H:%M",
        hours="%H:%M"
    )
    
    p.line(x_values, y_values, line_width=2, color="navy", alpha=0.7)

    # Extract script and div components
    script, div = components(p)

    # Debugging: Print script and div to check if they are generated
    print("Generated Script:", script[:50])
    print("Generated Div:", div[:50])
    print(df.columns)

    # Render an HTML template with the components
    return render_template('index.html', data=data, script=script, div=div)

## Route for json data
@app.route("/latest_status")
def latest_status():
    if not os.path.exists("tatest_status.json"):
        return jsonify({"Error": "latest_status.json not found"}), 404
        
    with open("latest_status.json", "r") as f:
        status_data = json.load(f)
        
    return jsonify(status_data)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=False)
