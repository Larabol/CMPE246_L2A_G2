from flask import Flask, render_template, jsonify
import pandas as pd
import json
import threading
import time
from Runtime import RunBMSScripts
from smbusutils import BMS

app = Flask(__name__)

CSV_FILE = "bmsdata.csv"
MAX_ROWS = 20      # Limit rows shown in table
CHART_POINTS = 100  # Points to plot

addr=0x0b
bus = BMS(addr)
def bms_loop():
    bms = RunBMSScripts(
        raw_data_file="battery_data.csv",
        processed_data_file="battery_data_processed.csv",
        fault_model_file="fault_model.pkl",
        temp_model_file="temp_model.pkl"
    )
    count = 0

    while True:
        try:
            bms.run_predictions(bus)
            time.sleep(2)
            print("hello")

        except Exception as e:
            print(f"BMS loop error: {e}")
            time.sleep(2)

@app.route("/")
def index():
    return render_template("index2.html")

@app.route("/data")
def data():
    try:
        # Tab-separated file, columns: timestamp, voltage, temperature, current (soc optional)
        df = pd.read_csv(CSV_FILE)

        df['time'] = pd.to_datetime(df['timestamp'])

        has_soc = 'soc' in df.columns

        # Latest values for stat cards
        latest = df.iloc[-1]

        # Chart data (last N points)
        chart_df = df.tail(CHART_POINTS)
        chart_data = {
            "time":        chart_df['time'].dt.strftime('%H:%M:%S').tolist(),
            "voltage":     chart_df['voltage'].tolist(),
            "current":     chart_df['current'].tolist(),
            "temperature": chart_df['temperature'].tolist(),
            "soc":         chart_df['soc'].tolist() if has_soc else [],
        }

        # Table data (last N rows, newest first)
        table_df = df.tail(MAX_ROWS).iloc[::-1]
        table_data = []
        for _, row in table_df.iterrows():
            table_data.append({
                "time":        row['time'].strftime('%Y/%m/%d %H:%M:%S'),
                "voltage":     round(float(row['voltage']), 2),
                "current":     round(float(row['current']), 2),
                "temperature": round(float(row['temperature']), 2),
                "soc":         round(float(row['soc']), 2) if has_soc else None,
            })

        return jsonify({
            "ok": True,
            "has_soc": has_soc,
            "latest": {
                "voltage":     round(float(latest['voltage']), 3),
                "current":     round(float(latest['current']), 3),
                "temperature": round(float(latest['temperature']), 3),
                "soc":         round(float(latest['soc']), 3) if has_soc else None,
                "time":        latest['time'].strftime('%H:%M:%S'),
            },
            "chart": chart_data,
            "table": table_data,
            "total_rows": len(df),
        })

    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route("/latest_status")
def latest_status():
    try:
        with open("latest_status.json", "r") as f:
            status_data = json.load(f)
        return jsonify(status_data)
    except FileNotFoundError:
        return jsonify({"Ok": False, "Error": "latest_status.json not found"}), 404
    except Exception as e:
        return jsonify({"Ok": False, "Error": str(e)}), 500
        

if __name__ == "__main__":
    thread = threading.Thread(target=bms_loop, daemon=True)
    thread.start()
    app.run(host='0.0.0.0', port=5000, debug=False)
