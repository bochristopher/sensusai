from flask import Flask, render_template_string

app = Flask(__name__)

@app.route("/")
def home():
    return render_template_string("<h1>SensusAI Dashboard</h1><p>Status: OK</p>")

if __name__ == "__main__":
    app.run(debug=True)
