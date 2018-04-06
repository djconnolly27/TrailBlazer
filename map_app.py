"""
Put your Flask app code here.
"""

from flask import Flask
from flask import render_template
from flask import request
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('my_map.html')

if __name__ == '__main__':
    app.run()
