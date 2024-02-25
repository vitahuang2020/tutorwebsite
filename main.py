from flask import Flask
from website import create_app


app = create_app()
app = Flask(__name__)

# entry point to app
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)