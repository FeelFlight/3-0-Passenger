import string
import random
from   flask          import Flask, jsonify, make_response, request
from   passenger      import db, Passenger
from   flask_httpauth import HTTPBasicAuth

app  = Flask(__name__)
auth = HTTPBasicAuth()

db.init_app(app)
db.create_all(app=app)


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
    res = db.session.execute(select([Passenger]))
    return len(res)#jsonify([dict(r) for r in res])


@app.route('/api/v1.0/passengers/<id>', methods=['GET'])
@auth.login_required
def get_passenger_by_telegramid(id):
    q = db.session.query(Passenger).filter(Passenger.telegramid == id)
    passenger = q.first()
    if passenger is not None:
        return jsonify(passenger.as_dict())
    else:
        return make_response(jsonify({'error': 'user not found'}), 400)


@app.route('/api/v1.0/passengers/', methods=['POST'])
@auth.login_required
def add_new_passenger():
    r = request.get_json(silent=True)
    if r is not None:
        nu = Passenger()
        nu.username   = r['from']['username']
        nu.firstname  = r['from']['first_name']
        nu.lastname   = r['from']['last_name']
        nu.telegramid = r['from']['id']
        nu.password   = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(6))
        try:
            db.session.add(nu)
            db.session.commit()
        except Exception as e:
            return make_response(jsonify({'error': 'dupe entry'}), 200)
        return jsonify(nu.as_dict())
    return make_response(jsonify({'error': 'missing data'}), 400)


def createAdmin():
    with app.app_context():
        q = db.session.query(Passenger).filter(Passenger.email == 'ansi@23-5.eu')
        user = q.first()
        if user is None:
            admin            = Passenger()
            admin.email      = 'ansi@23-5.eu'
            admin.firstname  = "Ansi"
            admin.lastname   = "Schmidt"
            admin.telegramid = 21212
            admin.password   = "wed23d2"
            db.session.add(admin)
            db.session.commit()
    return app


if __name__ == '__main__':
    createAdmin()
    app.run(host="::", port=8030)
