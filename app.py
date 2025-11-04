# app.py
from flask import Flask, render_template, request, jsonify
import os
import requests

app = Flask(__name__, template_folder="templates")

OPENWEATHER_API_KEY = os.environ.get("OPENWEATHER_API_KEY")

if not OPENWEATHER_API_KEY:
    # Warn but allow app to start — feature-limited without key.
    app.logger.warning("OPENWEATHER_API_KEY is not set. API calls will fail without it.")

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/weather", methods=["GET"])
def weather():
    """
    Query: /weather?city=London
    Response: JSON with weather data or error message
    """
    city = request.args.get("city", "").strip()
    if not city:
        return jsonify({"error": "Please provide a city query parameter, e.g. ?city=London"}), 400

    if not OPENWEATHER_API_KEY:
        return (
            jsonify({"error": "Server missing OPENWEATHER_API_KEY environment variable."}),
            500,
        )

    try:
        url = "https://api.openweathermap.org/data/2.5/weather"
        params = {"q": city, "appid": OPENWEATHER_API_KEY, "units": "metric"}
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()

        # Build a small, clean response
        result = {
            "city": data.get("name"),
            "weather": data.get("weather", [{}])[0].get("description"),
            "temp_c": data.get("main", {}).get("temp"),
            "humidity": data.get("main", {}).get("humidity"),
            "wind_m_s": data.get("wind", {}).get("speed"),
        }
        return jsonify(result)
    except requests.exceptions.HTTPError as e:
        try:
            return jsonify({"error": resp.json()}), resp.status_code
        except Exception:
            return jsonify({"error": "Upstream API HTTP error", "detail": str(e)}), 502
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Upstream API request failed", "detail": str(e)}), 502
    except Exception as e:
        app.logger.exception("Unhandled error in /weather")
        return jsonify({"error": "Internal server error", "detail": str(e)}), 500

if __name__ == "__main__":
    # Respect PORT env var for platforms like Heroku, or Docker run -e PORT=...
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
