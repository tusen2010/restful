#coding=utf-8
from flask import Flask
from flask.ext.restful import Api, Resource
from kvm.host import HostApi,HostList
from kvm.vm import VmApi,VmList

app = Flask(__name__)
app.config.from_object('config.dev')

api = Api(app)

api.add_resource(HostList, '/host')
api.add_resource(HostApi,'/host/<int:id>')
api.add_resource(VmList, '/vm')
api.add_resource(VmApi, '/vm/<int:id>')

app.run(host='0.0.0.0', port=app.config.get('PORT'))
