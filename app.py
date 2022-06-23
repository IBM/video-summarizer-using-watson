from flask import Flask, render_template
import os

transcript = ''
filename_converted = ''

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

port = os.getenv('VCAP_APP_PORT', '8080')
if __name__ == '__main__':
    from apis import *
    app.secret_key = os.urandom(12)
    app.run(host='0.0.0.0', port=port, debug=True)