from flask import Flask, request, render_template
import requests
import os

app = Flask(__name__)
conversation_history = []  

# Function to get cryptocurrency price
def get_crypto_price(crypto_name):
    try:
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={crypto_name}&vs_currencies=usd"
        response = requests.get(url)
        data = response.json()
        if crypto_name in data:
            price = data[crypto_name]['usd']
            return f"The current price of {crypto_name.capitalize()} is ${price} USD."
        else:
            return "Sorry, I couldn't fetch the price. Please ensure the cryptocurrency name is valid."
    except Exception as e:
        return f"Error fetching cryptocurrency data: {str(e)}"

# Function to get weather using OpenWeatherMap API
def get_weather(city_name):
    try:
        api_key = os.getenv("WEATHER_API_KEY")
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric"
        response = requests.get(url)
        data = response.json()
        if data.get("main"):
            temp = data["main"]["temp"]
            weather_description = data["weather"][0]["description"]
            return f"The current weather in {city_name.capitalize()} is {temp}°C with {weather_description}."
        else:
            return "Sorry, I couldn't fetch the weather. Please ensure the city name is valid."
    except Exception as e:
        return f"Error fetching weather data: {str(e)}"

# Function to call Google Generative AI (Gemini)
def call_google_gemini(user_input):
    try:
        api_key = os.getenv("GOOGLE_API_KEY")
        url = "https://generativelanguage.googleapis.com/v1beta2/models/text-bison-001:generateText"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        json_data = {
            "model": "gemini-1.5-flash",
            "prompt": user_input,
            "temperature": 0.7,
            "candidate_count": 1,
        }
        response = requests.post(url, headers=headers, json=json_data)
        data = response.json()
        if "candidates" in data:
            return data["candidates"][0]["output"]
        else:
            return "Sorry, I couldn't generate a response using Google Gemini."
    except Exception as e:
        return f"Error generating response with Google Gemini: {str(e)}"

@app.route("/", methods=["GET", "POST"])
def index():
    global conversation_history
    user_input = ""
    ai_response = ""

    if request.method == "POST":
        user_input = request.form["user_input"].lower()

        if "price" in user_input:
            crypto_keywords = ["bitcoin", "ethereum", "dogecoin", "litecoin", "cardano", "solana"]
            crypto_name = next((keyword for keyword in crypto_keywords if keyword in user_input), "")
            ai_response = get_crypto_price(crypto_name) if crypto_name else "Please specify a valid cryptocurrency."

        elif "weather" in user_input:
            city_name = user_input.split()[-1]
            ai_response = get_weather(city_name)

        else:
            ai_response = call_google_gemini(user_input)

        conversation_history.append(f"You: {user_input}\nAI: {ai_response}")

    return render_template("index_bitcoin.html", response=ai_response, history=conversation_history)

if __name__ == "__main__":
    app.run(debug=True)
