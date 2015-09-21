from flask.ext.restful import Api, Resource, fields, marshal_with, reqparse, marshal
from kvm.db import db,Vm
from flask import jsonify


vm_fields = {
    'id': fields.Integer,
    'domain': fields.String,
    'ip': fields.String,
    'host': fields.String,
    'uri': fields.String(attribute=lambda x: 'http://127.0.0.1:5000/host/' + str(x.id))
    }

vmapi_fields = {
    'id': fields.Integer,
    'domain': fields.String,
    'ip': fields.String
}

class VmList(Resource):

    @marshal_with(vm_fields)
    def get(self):
        query = Vm.query.all()
        return query

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('domain', type=str,required=True)
        parser.add_argument('ip', type=str,required=True)
        parser.add_argument('host', type=str,required=True)
        args = parser.parse_args()
        query = Vm(args.get('domain'),args.get('ip'),args.get('host'))
        db.session.add(query)
        db.session.commit()
        return jsonify(args)

class VmApi(Resource):

    def get(self,id):
        query = Vm.query.get(id)
        if query:
            return marshal(query,vmapi_fields)
        else:
            status = "%d not found" % id
            return ({"error":status}),404

    def put(self,id):
        parser = reqparse.RequestParser()
        parser.add_argument('domain', type=str,required=True)
        parser.add_argument('ip', type=str,required=True)
        parser.add_argument('host', type=str,required=True)
        args = parser.parse_args()
        query = Vm.query.get(id)
        query.name = args.get('name')
        query.ip = args.get('ip')
        query.host = args.get('host')
        db.session.commit()
        return jsonify(args)

    def delete(self,id):
        query = Vm.query.get(id)
        if query:
            db.session.delete(query)
            db.session.commit()
            return jsonify({'status': 'ok'})
        else:
            status = "%d not found" % id
            return ({"error":status}),404

