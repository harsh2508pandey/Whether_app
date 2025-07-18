from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    # Sample dummy data for testing
    weather = {
        "city": "New York",
        "temperature": 25,
        "condition": "Sunny"
    }
    return render_template('index.html', weather=weather)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
