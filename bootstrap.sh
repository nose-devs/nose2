#!/bin/bash
#
# NOTE: requires virtualenvwrapper
#
mkvirtualenv nose2
pip install -r requirements.txt
python setup.py develop
