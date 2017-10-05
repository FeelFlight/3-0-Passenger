from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    return "Hello, I am 3-0-passenger, how are you?"


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
