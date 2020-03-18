import os   



class config:
    SQLALCHEMY_DATABASE_URI=os.getenv('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS=os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS',False)
    SECRET_KEY=os.getenv('SECRET_KEY')


class development(config):
    DEBUG=True

class Productino(config):
    DEBUG=False
