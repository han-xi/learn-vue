from flask import Flask
from flask_cors import CORS

from flask import jsonify

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
CORS(app)

from loaddata import loaddata
from updata import updata
from mail import mail
# from search import search
app.register_blueprint(loaddata, url_prefix='/')
app.register_blueprint(updata, url_prefix='/')
app.register_blueprint(mail, url_prefix='/')

# app.register_blueprint(search, url_prefix='/search')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9004, threaded=True, debug=True)
