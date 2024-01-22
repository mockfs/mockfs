import os
import sys

try:
    import furo
except ImportError:
    furo = None
try:
    import rst.linker as rst_linker
except ImportError:
    rst_linker = None

sys.path.insert(1, os.path.dirname(os.path.dirname(__file__)))

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
]

project = 'mockfs'
master_doc = 'index'

if furo:
    html_theme = 'furo'
else:
    html_theme = 'agogo'

# {package_url} can be provided py jaraco.packaging.sphinx but we
# expand the value manually to avoid the dependency.
package_url = 'https://github.com/mockfs/mockfs'

# Link dates and other references in the changelog
if rst_linker is not None:
    extensions += ['rst.linker']

link_files = {
    '../CHANGES.rst': dict(
        using=dict(GH='https://github.com', package_url=package_url),
        replace=[
            dict(
                pattern=r'(Issue #|\B#)(?P<issue>\d+)',
                url='{package_url}/issues/{issue}',
            ),
            dict(
                pattern=r'(?m:^((?P<scm_version>v?\d+(\.\d+){1,2}))\n[-=]+\n)',
                with_scm='{text}\n{rev[timestamp]:%d %b %Y}\n',
            ),
            dict(
                pattern=r'PEP[- ](?P<pep_number>\d+)',
                url='https://www.python.org/dev/peps/pep-{pep_number:0>4}/',
            ),
        ],
    )
}

# Be strict about any broken references
nitpicky = True

# export MOCKFS_SPHINX_INTERSPHINX_ENABLED=0 in the environment to disable
# the "sphinx.ext.intersphinx" sphinx extension.
intersphinx_enabled = os.environ.get('MOCKFS_SPHINX_INTERSPHINX_ENABLED', '1')
if intersphinx_enabled == '1':
    extensions += ['sphinx.ext.intersphinx']
    intersphinx_mapping = {
        'python': ('https://docs.python.org/3', None),
        'sphinx': ('https://www.sphinx-doc.org/en/stable/', None),
    }

# Preserve authored syntax for defaults
autodoc_preserve_defaults = True
