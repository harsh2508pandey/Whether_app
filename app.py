from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)
API_KEY = os.getenv("WEATHER_API_KEY")

@app.route('/', methods=['GET', 'POST'])
def index():
    weather = {}
    if request.method == 'POST':
        city = request.form['city']
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(url).json()
        if response.get('main'):
            weather = {
                'city': city,
                'temperature': response['main']['temp'],
                'description': response['weather'][0]['description'],
            }
    return render_template('index.html', weather=weather)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
