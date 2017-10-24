# coding: utf-8

import subprocess
import os
import shutil
import logging
from monty.shutil import decompress_dir

from custodian.custodian import Job
from custodian.utils import backup

"""
This module implements basic kinds of jobs for FEFF runs
"""

logger = logging.getLogger(__name__)

__author__ = "Chen Zheng"
__version__ = "0.1"
__maintainer__ = "Chen Zheng"
__email__ = "chz022@ucsd.edu"
__status__ = "Alpha"
__date__ = '10/20/17'

FEFF_INPUT_FILES = {"feff.inp"}
FEFF_BACKUP_FILES = {"ATOMS", "HEADER", "PARAMETERS", "POTENTIALS"}


class FeffJob(Job):
    """
    A basic FEFF job, run whatever is in the directory.
    """

    def __init__(self, feff_cmd, output_file="feff.out",
                 stderr_file="std_feff_err.txt", backup=True):
        """
        This constructor is used for a standard FEFF initialization
        Args:
            feff_cmd (str): the name of the full executable for running FEFF
            output_file (str): Name of file to direct standard out to.
                Defaults to "feff.out".
            stderr_file (str): Name of file direct standard error to.
                Defaults to "std_feff_err.txt".
            backup (bool): Indicating whether to backup the initial input files.
                If True, the feff.inp will be copied with a ".orig" appended.
                Defaults to True.
        """
        self.feff_cmd = feff_cmd
        self.output_file = output_file
        self.stderr_file = stderr_file
        self.backup = backup

    def setup(self):
        """
        Performs initial setup for FeffJob, do backing up.
        Returns:

        """
        decompress_dir('.')

        if self.backup:
            for f in FEFF_INPUT_FILES:
                shutil.copy(f, "{}.orig".format(f))

            for f in FEFF_BACKUP_FILES:
                if os.path.isfile(f):
                    shutil.copy(f, "{}.orig".format(f))

    def run(self):

        """
        Performs the actual FEFF run
        Returns:
            (subprocess.Popen) Used for monitoring.
        """
        cmd = list(self.feff_cmd)
        with open(self.output_file, "w") as f_std, \
                open(self.stderr_file, "w", buffering=1) as f_err:
            # Use line buffering for stderr
            p = subprocess.Popen(cmd, stdout=f_std, stderr=f_err, shell=True)

        return p

    def postprocess(self):
        pass
