# -*- coding: utf-8 -*-

from flask import Flask, render_template, make_response, request
import ConfigParser
from fbUnipdbot import fbUnipdbot
import os

# initialize pyUnipd get configs from settings.ini
fbUni = fbUnipdbot()

config = ConfigParser.ConfigParser()
config.read(os.path.dirname(os.path.abspath(__file__)) + '/settings.ini')
Environment = config.get('main', 'environment')
if Environment == 'debug':
    IsDebug = True
else:
    IsDebug = False

verifytoken = str(config.get('main', 'token'))


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/webhook/', methods=["POST", "GET"])
def webhook():
    if request.method == "GET":
        if request.args.get("hub.verify_token") == verifytoken:
            return make_response(request.args.get("hub.challenge"))
        else:
            return make_response('Error, invalid token')
    else:
        fbUni.replier(request.get_json(force=True))
        return "", 200


if __name__ == '__main__':
    app.run(debug=IsDebug, port=8000)
