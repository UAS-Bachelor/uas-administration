from flask import Flask, render_template
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    try:
        login = requests.get('http://127.0.0.1:5002/login').text        
    except requests.exceptions.ConnectionError:
        return 'Login service unavailable'
    return render_template('layout.html', html=login)

if __name__ == '__main__':
    app.run(debug=True)