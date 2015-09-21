from flask.ext.restful import Api, Resource, reqparse, fields, marshal_with, marshal
from flask import jsonify
from kvm.db import db, Host

host_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'ip': fields.String,
    'uri': fields.String(attribute=lambda x: 'http://127.0.0.1:5000/host/' + str(x.id))
}

hostapi_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'ip': fields.String
}


class HostList(Resource):
    @marshal_with(host_fields)
    def get(self):
        query = Host.query.all()
        return query

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True)
        parser.add_argument('ip', type=str, required=True)
        args = parser.parse_args()
        query = Host(args.get('name'), args.get('ip'))
        db.session.add(query)
        db.session.commit()
        return jsonify(args)


class HostApi(Resource):
    def get(self, id):
        query = Host.query.get(id)
        if query:
            return marshal(query, hostapi_fields)
        else:
            status = "%d not found" % id
            return ({"error": status}), 404

    def put(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True)
        parser.add_argument('ip', type=str, required=True)
        args = parser.parse_args()
        query = Host.query.get(id)
        query.name = args.get('name')
        query.ip = args.get('ip')
        db.session.commit()
        return jsonify(args)

    def delete(self, id):
        query = Host.query.get(id)
        if query:
            db.session.delete(query)
            db.session.commit()
            return jsonify({'status': 'ok'})
        else:
            status = "%d not found" % id
            return ({"error": status}), 404
