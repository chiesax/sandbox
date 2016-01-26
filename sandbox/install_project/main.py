# -*- coding: utf-8 -*-

"""

Install an application from the AL repository.

CFG requirements:

- /PackageURL
- /VirtualEnv/WorkonHome/machine (machine=macosx or linux)
- /project/Python/machine: Optional, for the path to the python binary,
  if specific version is requested
- /CommonPath/machine

Created on Jan 15, 2014

@author: stephanep
"""
import os
import pkg_resources
import socket
import logging
import subprocess
from sandbox.install_project.venv_inspect import get_entry_points, get_project_version


VENV_BASE_PATH = os.path.join('/', 'opt', 'python')
SCRIPTS_PREFIX = 'mypy_'


class InPackageDirectory(Exception):
    pass


def find_python():
    """ Utility to locate where python is, given the current environment
    """
    path = subprocess.check_output(["which", "python"]).strip()
    return path


def notify_installation_success(project, version, host, last_version_after=None,
                                last_version_before=None):
    """A hook to be executed on installation success.
    Should return immediately and not block code execution."""
    pass


class InstallProject(object):
    """ Class holding and running the installation steps.
    """

    def __init__(self, requirement):
        """
        Constructor
        """
        self.log = logging.getLogger(self.__class__.__name__)
        self._host = socket.gethostname()
        self._requirement = pkg_resources.Requirement.parse(requirement)
        self._project = self._requirement.project_name
        # Check if we are currently in a package. If yes, blow up
        if os.path.exists("setup.py") and os.path.exists("setup.cfg") and os.path.exists("requirements.txt"):
            raise InPackageDirectory("You cannot run this while in a package directory.")
        self._version = 'last'
        self._last_version_before = None
        self._last_version_after = None
        self._betatest = False
        self._virtual_env_base_path = VENV_BASE_PATH
        self._virtual_env_full_path = None
        self._python_path = self._default_python_path()
        self._force = False

    def set_betatest(self):
        """Do not update symlinks"""
        self._betatest = True

    def set_force(self):
        self._force = True

    def set_python(self, path):
        """ Set the python binary to use in the virtual environment
        """
        self._python_path = path
        if not os.path.exists(self._python_path):
            self.log.exception("Missing python")
            raise EnvironmentError("Missing python")

    @property
    def _python_name(self):
        return os.path.basename(self._python_path)

    @property
    def _venv_bin_path(self):
        return os.path.join(self._virtual_env_full_path, 'bin')

    @property
    def _venv_pip_path(self):
        return os.path.join(self._venv_bin_path, 'pip')

    @property
    def _venv_python_path(self):
        return os.path.join(self._venv_bin_path, self._python_name)

    def run(self):
        """ Run the thing
        """
        if not self._project:
            raise ValueError("Project MUST be specified!")
        if not self._requirement.specs:
            self._version = 'last'
        else:
            self._version = ''.join(self._requirement.specs[0])
        if self._virtual_env_full_path is None:
            self._virtual_env_full_path = os.path.join(self._virtual_env_base_path,
                                                       self._project,
                                                       self._version,
                                                       self._python_name)
        if self._version == 'last':
           self._last_version_before = self._get_installed_project_version()
        if self._version != 'last':
            if self._check_exists():
                if not self._force:
                    print "Project already installed, doing nothing."
                    self._final_message()
                    return
        if not self._check_exists():
            self._setup_env()
        self._install()
        self._create_run_scripts()
        if self._version == 'last':
            self._last_version_after = self._get_installed_project_version()
        else:
            self._version = self._get_installed_project_version()
        self._final_message()
        notify_installation_success(project=self._project,
                                    version=self._version,
                                    host=self._host,
                                    last_version_after=self._last_version_after,
                                    last_version_before=self._last_version_before)

    def _default_python_path(self):
        return find_python()

    def _check_exists(self):
        return os.path.isdir(self._virtual_env_full_path)

    def _setup_env(self):
        subprocess.check_call(['virtualenv', '--system-site-packages',
                               '-p', self._python_path, self._virtual_env_full_path])

    def _install(self):
        if self._version == 'last':
            subprocess.check_call([self._venv_pip_path,
                                   'install', '--upgrade', '--no-deps',
                                   self._project])
            subprocess.check_call([self._venv_pip_path,
                                   'install', self._project])
        else:
            subprocess.check_call([self._venv_pip_path,
                                   'install', str(self._requirement)])

    def _get_entry_points(self):
        return get_entry_points(self._venv_python_path, self._project)

    def _get_installed_project_version(self):
        if not os.path.exists(self._venv_python_path):
            return None
        try:
            return get_project_version(self._venv_python_path, self._project)
        except Exception as e:
            logging.warning(e, exc_info=1)
            return None

    def _get_script_name(self, app):
        return '{0}_{1}'.format(SCRIPTS_PREFIX, app)

    def _create_run_scripts(self):
        """ Create the run scripts and symlinks
        """
        try:
            project_entry_points = self._get_entry_points()
        except Exception as e:
            logging.exception(e)
            project_entry_points = []
            for app in os.listdir(self._venv_bin_path):  # collect the entry points.
                if not os.path.basename(app).count(self._project):
                    self.log.info('ignoring creation of run script for {0} as it does not look like '
                                  'an entry point.'.format(app))
                project_entry_points.append(app)

        for app in project_entry_points:
            app_path = os.path.join(self._venv_bin_path, app)
            if not os.path.exists(app_path):
                logging.error('entry point path {0} does not exist, skip creation of entry point'.format(app_path))
                continue
            scriptname = os.path.join(self._virtual_env_base_path, "bin", "{0}_{1}".format(self._get_script_name(app),
                                                                                           self._version))
            with open(scriptname, "w") as script:
                script.write("#!/bin/bash\n")
                script.write('{0} "$@"\n'.format(app_path))
            os.chmod(scriptname, 0755)
            if not self._betatest:
                if os.path.exists(os.path.join(self._virtual_env_base_path, "bin", self._get_script_name(app))):
                    os.unlink(os.path.join(self._virtual_env_base_path, "bin", self._get_script_name(app)))
                try:
                    os.symlink(scriptname, os.path.join(self._virtual_env_base_path, "bin", self._get_script_name(app)))
                except OSError as e:
                    self.log.exception(e)

    def _final_message(self):
        """ Final message
        """
        messages = ["Installation of {0} completed.".format(self._project),
                    'The Virtualenv is called {0}'.format(self._virtual_env_full_path)]
        max_lengths = max([len(mess) for mess in messages])
        print max_lengths * "="
        for mess in messages:
            print mess
        print max_lengths * "="

