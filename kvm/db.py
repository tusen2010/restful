from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config.dev')
db = SQLAlchemy(app)


class Host(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    ip = db.Column(db.String(50))
    # vm = db.relationship('Vm', backref='host')

    def __init__(self, name, ip):
        self.name = name
        self.ip = ip

    def __repr__(self):
        return '%r' % self.name


class Vm(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    domain = db.Column(db.String(50))
    ip = db.Column(db.String(50))
    # host = db.Column(db.Integer, db.ForeignKey('host.id'))
    host = db.Column(db.String(50))

    def __init__(self, domain, ip, host):
        self.domain = domain
        self.ip = ip
        self.host = host

    def __repr__(self):
        return 'Domain %r' % self.domain
