# -*- coding: utf-8 -*-
"""
Created by chiesa on 02.03.15
"""

from contextlib import closing
import logging
from apscheduler.schedulers.blocking import BlockingScheduler
from sandbox.scheduler.dynimp import dynimport
from sandbox.scheduler.mapping import Jobs

__author__ = 'chiesa'


def get_connection():
    """
    Returns a connection to the database
    :return:
    """


def run():
    dbConnection = get_connection()
    with closing(dbConnection.get_session()) as session:
        jobs = {j.name: j for j in session.query(Jobs).filter_by(active=True).all()}
    sched = BlockingScheduler()
    fns = {}
    for j in jobs.values():
        try:
            fns[j.name] = dynimport(j.job_path)
        except Exception:
            logging.error('failed to import job {0}'.format(j.name), exc_info=1)
    for jname, f in fns.items():
        try:
            job_kargs = jobs[jname].job_kargs
            if not 'kwargs' in job_kargs:
                job_kargs['kwargs'] = {}
            job_kargs['kwargs'].update({'connection': dbConnection})
            sched.add_job(f, name=jname, **job_kargs)
            logging.info('added job {0}: {1}'.format(jname, job_kargs))
        except Exception as e:
            logging.exception(e)
    sched.start()

