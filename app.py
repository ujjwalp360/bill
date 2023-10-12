from flask import Flask, render_template, request

app = Flask(__name)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/say_hello', methods=['POST'])
def say_hello():
    return "Hello, World!"

if __name__ == '__main__':
    app.run()
