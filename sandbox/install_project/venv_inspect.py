# -*- coding: utf-8 -*-
"""
Created by chiesa on 18.01.16

Copyright 2015 Alpes Lasers SA, Neuchatel, Switzerland
"""
import json
import subprocess
from tempfile import NamedTemporaryFile

__author__ = 'chiesa'
__copyright__ = "Copyright 2015, Alpes Lasers SA" 


def get_entry_points(venv_python_path, project_name):
    f = NamedTemporaryFile(delete=False)
    f.write('import pkg_resources\n')
    f.write('import json\n\n')
    f.write('print json.dumps(pkg_resources.get_entry_map(\'{0}\').get(\'console_scripts\', {{}}).keys())\n'.format(project_name))
    f.close()
    return json.loads(subprocess.check_output([venv_python_path, f.name]))


def get_project_version(venv_python_path, project_name):
    f = NamedTemporaryFile(delete=False)
    f.write('import pkg_resources\n')
    f.write('import json\n\n')
    f.write('print json.dumps(pkg_resources.get_distribution(\'{0}\').version)\n'.format(project_name))
    f.close()
    return json.loads(subprocess.check_output([venv_python_path, f.name]))