from config.default import *

SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'pybo.db'))
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = b'K\xc3\xa4\xf9R\x16\x8d\xd4\x96\xc9\xb1\xf2\xa06\xceZ'