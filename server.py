"""Flask server for image differencing application"""

from flask import Flask, request, jsonify, render_template
from model import User, InputImage, DiffImage


app = Flask(__name__)

@app.route("/")
def show_index():
        """Index/homepage"""

        return render_template("index.html")

@app.route("")
def register_user():



if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")