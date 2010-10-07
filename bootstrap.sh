#!/bin/bash
#
# NOTE: requires virtualenvwrapper
#
mkvirtualenv nose2
pip install -r requirements.txt
python setup.py develop
pushd docs
git clone http://github.com/mitsuhiko/flask-sphinx-themes.git _themes
popd
