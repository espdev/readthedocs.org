import os
import logging
import json
import yaml

from django.conf import settings
from django.template import Template, Context, loader as template_loader

from doc_builder.base import BaseBuilder, restoring_chdir
from projects.utils import run

log = logging.getLogger(__name__)


class Builder(BaseBuilder):

    """
    Mkdocs builder
    """
    type = 'mkdocs'

    def __init__(self, *args, **kwargs):
        super(Builder, self).__init__(*args, **kwargs)
        self.old_artifact_path = os.path.join(
            self.version.project.checkout_path(self.version.slug), 'site')

    @restoring_chdir
    def build(self, **kwargs):
        project = self.version.project
        os.chdir(project.checkout_path(self.version.slug))
        user_config = yaml.safe_load(open('mkdocs.yml', 'r'))
        docs_dir = user_config.get('docs_dir', 'docs')

        READTHEDOCS_DATA = {
            'project': project.slug,
            'version': self.version.slug,
            'language': project.language,
            'page': None,
            'theme': "readthedocs",
            'docroot': docs_dir,
            'source_suffix': ".md",
            'api_host': getattr(settings, 'SLUMBER_API_HOST', 'https://readthedocs.org'),
        }
        data_json = json.dumps(READTHEDOCS_DATA, indent=4)
        data_ctx = Context({
            'data_json': data_json,
            'current_version': READTHEDOCS_DATA['version'],
            'slug': READTHEDOCS_DATA['project'],
            'html_theme': READTHEDOCS_DATA['theme'],
            'pagename': None,
        })
        data_string = template_loader.get_template(
            'doc_builder/data.js.tmpl'
        ).render(data_ctx)

        data_file = open(os.path.join(docs_dir, 'readthedocs-data.js'), 'w+')
        data_file.write(data_string)
        data_file.close()

        include_ctx = Context({
            'global_analytics_code': getattr(settings, 'GLOBAL_ANALYTICS_CODE', 'UA-17997319-1'),
            'user_analytics_code': project.analytics_code,
        })
        include_string = template_loader.get_template(
            'doc_builder/include.js.tmpl'
        ).render(include_ctx)
        include_file = open(
            os.path.join(docs_dir, 'readthedocs-dynamic-include.js'), 'w+')
        include_file.write(include_string)
        include_file.close()

        MEDIA_URL = getattr(
            settings, 'MEDIA_URL', 'https://media.readthedocs.org')
        if 'extra_javascript' in user_config:
            user_config['extra_javascript'].append(
                '%sjavascript/jquery/jquery-2.0.3.min.js' % MEDIA_URL)
            user_config['extra_javascript'].append('readthedocs-data.js')
            user_config['extra_javascript'].append(
                'readthedocs-dynamic-include.js')
            user_config['extra_javascript'].append(
                '%sjavascript/readthedocs-doc-embed.js' % MEDIA_URL)
        else:
            user_config['extra_javascript'] = [
                '%sjavascript/jquery/jquery-2.0.3.min.js' % MEDIA_URL,
                'readthedocs-data.js',
                'readthedocs-dynamic-include.js',
                '%sjavascript/readthedocs-doc-embed.js' % MEDIA_URL,
            ]
        if 'extra_css' in user_config:
            user_config['extra_css'].append(
                'https://media.readthedocs.org/css/badge_only.css')
            user_config['extra_css'].append(
                'https://media.readthedocs.org/css/readthedocs-doc-embed.css')
        else:
            user_config['extra_css'] = [
                'https://media.readthedocs.org/css/badge_only.css',
                'https://media.readthedocs.org/css/readthedocs-doc-embed.css',
            ]
        yaml.dump(user_config, open('mkdocs.yml', 'w'))
        if project.use_virtualenv:
            build_command = "%s build --theme=mkdocs" % (
                project.venv_bin(version=self.version.slug,
                                 bin='mkdocs')
            )
        else:
            build_command = "mkdocs build --theme=mkdocs"
        results = run(build_command, shell=True)
        return results
