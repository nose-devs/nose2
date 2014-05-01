::
:: NOTE: requires virtualenvwrapper-win
::
call mkvirtualenv nose2
pip install -r requirements.txt
pip install tox
python setup.py develop
