from __future__ import absolute_import
#from distutils.core import setup
from setuptools import setup

descr = """GO-Bayes: A simple Bayesian correction for GO overrepresentation.
"""

DISTNAME            = 'gobayes'
DESCRIPTION         = 'Bayesian correction for overrepresentation tests'
LONG_DESCRIPTION    = descr
MAINTAINER          = 'Juan Nunez-Iglesias'
MAINTAINER_EMAIL    = 'juan.n@unimelb.edu.au'
URL                 = 'https://github.com/jni/gobayes'
LICENSE             = 'BSD 3-clause'
DOWNLOAD_URL        = 'https://github.com/jni/gobayes'
VERSION             = '0.1-dev'
PYTHON_VERSION      = (3, 4)
INST_DEPENDENCIES   = {}


if __name__ == '__main__':

    setup(name=DISTNAME,
        version=VERSION,
        url=URL,
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        author=MAINTAINER,
        author_email=MAINTAINER_EMAIL,
        license=LICENSE,
        packages=['gobayes', 'gobayes.parsers'],
        package_data={},
        install_requires=INST_DEPENDENCIES,
        scripts=[]
    )

