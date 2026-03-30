from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

# Route for the main page
@app.route("/")
def index():
    # Read CSV file
    df = pd.read_csv("bmsdata.csv")

    # Convert dataframe to a dictionary for easy access in HTML
    data = df.to_dict(orient="records")

    # Send data to HTML template
    return render_template("index.html", data=data)

if __name__ == "__main__":
    app.run(debug=True)