import mongoengine
mongoengine.connect('pluma-example')

import os
PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = '1zb7w)@e0v%_iz@a^123sbdk%%0jc-teewcg@v46v3$%mwx1lz'


