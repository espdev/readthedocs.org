#coding=utf-8

from projects.exceptions import ProjectImportError
from vcs_support.base import BaseVCS, VCSVersion

try:
    from P4 import P4, P4Exception
except ImportError:
    raise ProjectImportError((
        'Cannot import P4Python. You must install Perforce Python API.\n'
        + 'See: http://www.perforce.com/perforce/doc.current/manuals/p4script/03_python.html'
    ))


CLIENT_TEMPLATE = 'espdev-rtd-srv-main'   # tmp


class Backend(BaseVCS):
    supports_tags = True
    supports_branches = False
    fallback_branch = ''

    def __init__(self, project, version):
        super(Backend, self).__init__(project, version)

        print 'I am PERFORCE BACKEND'

        print 'PROJECT NAME: {}'.format(self.name)
        print 'PROJECT WORKING DIR: {}'.format(self.working_dir)

        p4 = P4()   # P4 API

        try:
            if not p4.connected():
                p4.connect()
            p4.run_login()
        except P4Exception as err:
            raise ProjectImportError('{}'.format(err))

        self.p4 = p4

    def __del__(self):
        print 'DISCONNECT PERFORCE BACKEND'

        try:
            self.p4.disconnect()
        except P4Exception as err:
            print err

    def update(self):
        super(Backend, self).update()

        print 'PERFORCE UPDATE'

        self._update_client()
        self.sync()

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
            vcs_tags.append(VCSVersion(self, label['label'], label['label']))

        return vcs_tags

    def sync(self, identifier=None):
        depot_url = self._get_depot_url()

        if identifier:
            # Use a specified changelist or label
            depot_url += '@{}'.format(identifier)

        try:
            self.p4.run_revert(self._get_depot_url())
        except P4Exception as err:
            print err

        try:
            info = self.p4.run_sync('-f', depot_url)
        except P4Exception as err:
            raise ProjectImportError(
                "Failed to get code from '{}'. Error:\n{}\n".format(
                    self.repo_url, err)
            )

        try:
            self.p4.run_edit(self._get_depot_url())
        except P4Exception as err:
            raise ProjectImportError(
                "Failed to edit code from '{}'. Error:\n{}\n".format(
                    self.repo_url, err)
            )

        return info

    def checkout(self, identifier=None):
        super(Backend, self).checkout()

        print 'PERFORCE CHECKOUT'

        self._update_client()
        info = self.sync(identifier)

        return 0, '{}'.format(info), ''

    def _update_client(self):
        try:
            self.p4.client = CLIENT_TEMPLATE

            client = self.p4.fetch_client('-t', CLIENT_TEMPLATE)
            client['Root'] = self.working_dir
            self.p4.save_client(client)

        except P4Exception as err:
            raise ProjectImportError(
                'Failed to create project client.\n{}\n'.format(err))

    def _get_depot_url(self):
        depot_url = self.repo_url.rstrip('/')

        if not depot_url.endswith('/...'):
            depot_url += '/...'

        return depot_url
