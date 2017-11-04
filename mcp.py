import time
import string
import random
import couchdb
from   flask          import Flask, jsonify, make_response, request
from   flask_httpauth import HTTPBasicAuth

app   = Flask(__name__)
auth  = HTTPBasicAuth()
couch = couchdb.Server('http://couchdb:5984/')


@auth.get_password
def get_password(username):
    if username == 'ansi':
        return 'test'
    return None


@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)


@app.route('/api/v1.0/passengers/', methods=['GET'])
@auth.login_required
def all_passengers():
    return ""


@app.route('/api/v1.0/passengers/<id>', methods=['GET'])
@auth.login_required
def get_passenger_by_telegramid(id):
    try:
        db = couch['passenger']

        if id in db:
            d = db[id]
        else:
            d = {'_id': id}

        d['lastseen'] = time.time()
        db.save(d)
        return jsonify(d)

    except Exception as e:
        print("Error in get_passenger_by_telegramid")
        print(e)
        return make_response(jsonify({'error': 'missing data'}), 400)


@app.route('/api/v1.0/passengers/<id>', methods=['POST'])
@auth.login_required
def set_passenger_by_telegramid(id):
    try:
        db = couch['passenger']

        if id in db:
            d = db[id]
        else:
            d = {'_id': id}

        d['lastseen'] = time.time()
        db.save(d)
        return jsonify(d)

    except Exception as e:
        print("Error in get_passenger_by_telegramid")
        print(e)
        return make_response(jsonify({'error': 'missing data'}), 400)


@app.route('/api/v1.0/passengers/', methods=['POST'])
@auth.login_required
def add_new_passenger():
    r = request.get_json(silent=True)
    #return jsonify(nu.as_dict())
    #return make_response(jsonify({'error': 'missing data'}), 400)
    return ""


def _configureDB():
    for dbname in ['passenger']:
        try:
            db = couch[dbname]
        except Exception as e:
            db = couch.create(dbname)


if __name__ == '__main__':
    _configureDB()
    app.run(host="::", port=8030)
