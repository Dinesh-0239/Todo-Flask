from datetime import datetime
from flask import Flask,render_template,redirect
app = Flask(__name__)

@app.route('/')
def home():
    year = datetime.now().year
    return render_template('home.html',year=year)

if __name__ == '__main__':
    app.run(debug=True)