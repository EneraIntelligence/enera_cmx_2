#!/usr/bin/python
# coding=utf-8

# from flask.ext.pymongo import PyMongo

# mongo = PyMongo()

from flask.ext.mongoengine import MongoEngine
from mongoengine import *
import datetime
import pytz

mongo = MongoEngine()

# connect('enera', username='enera', password='enera', host='ds056998.mongolab.com', port=56998)

connect('enera', username='', password='', host='query0.enera-intelligence.mx')

class Clients(DynamicDocument):
    meta = {'collection': 'clients'}


class CmxRaw(DynamicDocument):
    created_at = DateTimeField(default=datetime.datetime.now(pytz.utc))
    updated_at = DateTimeField(default=datetime.datetime.now(pytz.utc))

    meta = {'collection': 'cmx_raw'}

    def save(self, *args, **kwargs):
        # if not self.created_at:
        #     self.created_at = datetime.datetime.now()
        self.updated_at = datetime.datetime.now(pytz.utc)
        return super(CmxRaw, self).save(*args, **kwargs)


class CmxUrl(DynamicDocument):
    meta = {'collection': 'cmx_url'}


class Network(DynamicDocument):
    meta = {'collection': 'networks'}


class SummaryNetwork(DynamicDocument):
    created_at = DateTimeField(default=datetime.datetime.now(pytz.utc))
    updated_at = DateTimeField(default=datetime.datetime.now(pytz.utc))
    meta = {'collection': 'summary_networks'}

    def save(self, *args, **kwargs):
        # if not self.created_at:
        #     self.created_at = datetime.datetime.now()
        self.updated_at = datetime.datetime.now(pytz.utc)
        return super(SummaryNetwork, self).save(*args, **kwargs)


class Branch(DynamicDocument):
    meta = {'collection': 'branches'}


class Administrator(DynamicDocument):
    meta = {'collection': 'administrators'}


class User(DynamicDocument):
    meta = {'collection': 'users'}


class CampaignLog(DynamicDocument):
    meta = {'collection': 'campaign_logs'}