from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Passenger(db.Model):
    __tablename__ = 'passenger'
    id            = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email         = db.Column(db.Unicode(128))
    username      = db.Column(db.Unicode(128))
    firstname     = db.Column(db.Unicode(128))
    lastname      = db.Column(db.Unicode(128))
    password      = db.Column(db.Unicode(128))
    telegramid    = db.Column(db.Integer, nullable=False, unique=True)
    age           = db.Column(db.Integer)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __iter__(self):
        return self.to_dict().iteritems()
