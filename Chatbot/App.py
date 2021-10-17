from flask import Flask, render_template, request
from chat import ChatBot
app = Flask(__name__)

bot = ChatBot()
@app.route("/", methods=["POST", "GET"])
def home():


    data = request.form.get('nm')
    if data==None:
        data='Hello'
    output = bot.get_response(str(data))
    return render_template('chat.html', output=output)


if __name__ == "__main__":
    app.run(debug=True)
