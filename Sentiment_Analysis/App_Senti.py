from flask import Flask, render_template, request
from textblob import TextBlob

app = Flask(__name__)

# Route to handle homepage and sentiment analysis
@app.route("/", methods=["GET", "POST"])
def index():
    result = ""
    polarity = 0.0
    subjectivity = 0.0

    if request.method == "POST":
        user_text = request.form.get("user_text")
        if user_text:
            analysis = TextBlob(user_text)
            polarity = round(analysis.polarity, 2)
            subjectivity = round(analysis.subjectivity, 2)

            # Simpler classification: Positive, Negative, or Neutral
            if polarity > 0:
                result = "Positive 😊"
            elif polarity < 0:
                result = "Negative 😞"
            else:
                result = "Neutral 😐"

    return render_template("index.html", result=result, polarity=polarity, subjectivity=subjectivity)


if __name__ == "__main__":
    app.run(debug=True)
