# -*- coding: utf-8 -*-
"""
Created by chiesa on 02.03.15

Copyright 2015 Alpes Lasers SA, Neuchatel, Switzerland
"""
import logging
import cjson
from sqlalchemy.ext.declarative.api import declarative_base
import sqlalchemy.types as sqlTypes
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import String, Boolean, Integer
import types


__author__ = 'chiesa'
__copyright__ = "Copyright 2015, Alpes Lasers SA"

BASE = declarative_base()


class MyJSON(sqlTypes.TypeDecorator):
    impl = sqlTypes.Text

    def process_bind_param(self, value, dialect):
        if type(value) in types.StringTypes:
            # Protect against badly formatted json
            cjson.decode(value)
            return value
        if type(value) == types.DictType:
            # Cast to JSON if it's a dict
            return cjson.encode(value)

    def process_result_value(self, value, dialect):
        if value:
            try:
                return cjson.decode(value)
            except Exception, e:
                logging.exception(e)
                return {}
        else:
            return {}


class Jobs(BASE):
    __tablename__ = 'jobs'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    job_path = Column(String)    # the path to the job
    job_kargs = Column(MyJSON)   # injected into Advanced Scheduler and into the function
    active = Column(Boolean, server_default='true')


