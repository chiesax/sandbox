# -*- coding: utf-8 -*-
"""
Created by stephanep on 09.06.15

Copyright 2015 Alpes Lasers SA, Neuchatel, Switzerland
"""
import argparse
from ProjectManager.install_project.main import InstallProject
from ProjectManager.utils.pip_utils import check_pip_config_files

__author__ = 'stephanep'
__copyright__ = "Copyright 2015, Alpes Lasers SA"


def main():
    """ Main entry point
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-b", "--betatest", dest="betatest", action="store_true",
                        help="If used, then do not update the symlinks with this version's entry points")
    parser.add_argument("--python", dest="pythonbin",
                        help="In case you need a specific python to run the project, specify its path here")
    parser.add_argument("-f", "--force", dest="force", action="store_true",
                        help="Force the reinstallation of a package as by default, if the directory exists, nothing is "
                             "done.")
    options, args = parser.parse_known_args()
    if not args:
        print 'Specify at least the project name'
        parser.print_help()
        return
    project = args[0]
    install_proj = InstallProject(project)
    if options.pythonbin:
        install_proj.set_python(options.pythonbin)
    if options.betatest:
        install_proj.set_betatest()
    if options.force:
        install_proj.set_force()
    check_pip_config_files(ignore_upload=True)  # The upload part isn't needed for install only, but localshop is
    # mandatory
    install_proj.run()

if __name__ == '__main__':
    main()
