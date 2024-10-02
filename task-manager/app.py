from flask import Flask

app = Flask(__name__)

@app.route('/')
def health():
    return 'App is up and running!'



if __name__ == '__main__':
    app.run(debug=True, port=8080)
