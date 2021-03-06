#coding=utf-8

"""
Module provides a backend for Perforce VCS

You should use this backend for build projects from Perforce VCS.

.. warning::
    Firstly you must create Perforce config (see Perforce documentation)::

        - P4USER
        - P4PASSWD
        - P4PORT
        - P4CLIENT

This backend uses a client (workspace). A client must be created
for your Perforce environment (user/server).

You should set ``Repo`` in the project settings as::

    //<depot_name>/<...>/<project_name>

Where::

    <depot_name> -- name of Perforce depot
    <...> -- path to project dir in depot
    <project_name> -- name of your project dir

.. note::

    * This backend supports versions as perforce labels.
    * This backend uses p4 console client and P4Python API.

"""

import os

from projects.exceptions import ProjectImportError
from vcs_support.base import BaseVCS, VCSVersion

try:
    from P4 import P4, P4Exception
except ImportError:
    raise ProjectImportError((
        'Cannot import P4Python. You must install Perforce p4 console client and Python API.\n'
        + 'See: http://www.perforce.com/perforce/doc.current/manuals/p4script/03_python.html'
    ))


class Backend(BaseVCS):
    """Class is a backend for Perforce VCS
    """

    supports_tags = True
    supports_branches = False
    fallback_branch = '#head'

    def __init__(self, project, version):
        super(Backend, self).__init__(project, version)

        p4 = P4()   # P4 Python API

        try:
            if not p4.connected():
                p4.connect()
        except P4Exception as err:
            raise ProjectImportError(
                'Cannot connect to Perforce server.\n{}'.format(err))

        try:
            p4.run_login()
        except P4Exception as err:
            # Oops... any problems о_О
            raise ProjectImportError(
                'Cannot login to Perforce server.\n{}'.format(err))

        self.p4 = p4

    def __del__(self):
        try:
            self.p4.disconnect()
        except P4Exception:
            pass

    def update(self):
        super(Backend, self).update()

        self._update_client()
        self.co()

    @property
    def tags(self):
        try:
            labels = self.p4.run_labels(self._get_depot_url())
        except P4Exception:
            return []
        return self.parse_tags(labels)

    def parse_tags(self, labels):
        vcs_tags = []

        for label in labels:
            label_name = label['label']
            vcs_tags.append(VCSVersion(self, '@'+label_name, label_name))

        return vcs_tags

    @property
    def commit(self):
        info = self.p4.run('changes', '-s', 'submitted', '-m', '1',
                           '{}/...#have'.format(self.working_dir))
        try:
            stdout = info[0]['change']
        except Exception:
            stdout = 'Unknown'
        return stdout

    def co(self, identifier=None):
        self._revert()
        self.make_clean_working_dir()
        info = self._sync(identifier)

        return info

    def checkout(self, identifier=None):
        super(Backend, self).checkout()

        retcode = 0
        stderr = ''

        try:
            self._update_client()
            info = self.co(identifier)
            stdout = '{} files have been synchronized'.format(len(info))
        except ProjectImportError as err:
            retcode = 1
            stdout = 'Files have not been synchronized'
            stderr = '{}'.format(err)

        return retcode, stdout, stderr

    def _update_client(self):
        try:
            # Change client root for current project
            client = self.p4.fetch_client()
            client['Root'] = self.working_dir

            self.p4.save_client(client)
        except P4Exception as err:
            raise ProjectImportError(
                'Failed to update client "{}".\n{}\n'.format(
                    self.p4.client, err))

    def _get_depot_url(self):
        depot_url = self.repo_url.rstrip('/')

        if not depot_url.endswith('/...'):
            # A canonical depot url for view to all files
            depot_url += '/...'
        return depot_url

    def _revert(self):
        try:
            self.p4.run_revert(self._get_depot_url())
        except P4Exception:
            pass

    def _sync(self, identifier):
        depot_url = self._get_depot_url()

        if identifier:
            # Use a specified changelist or label
            depot_url += identifier

        try:
            info = self.p4.run_sync('-f', depot_url)
        except P4Exception as err:
            raise ProjectImportError(
                "Failed to sync code from '{}'. Error:\n{}\n".format(
                    depot_url, err)
            )

        for rootdir, dirnames, filenames in os.walk(self.working_dir):
            for fname in filenames:
                pname = os.path.join(rootdir, fname)
                os.chmod(pname, 0o777)

        return info
