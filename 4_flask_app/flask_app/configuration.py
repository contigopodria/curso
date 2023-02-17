import random
class BaseConfig(object):
    'Base configuracion'
    SECRET_KEY = 'Key'
    DEBUG = True
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root@localhost:3306/pyalmacen'
    #RECAPTCHA_PUBLIC_KEY= aquí hay que poner la llave pública de google entre comillas
    # RECAPTCHA_PRIVATE_KEY=aquí hay que poner la llave privada secreta de google entre comillas
    #WTF_CSRF_TIME_LIMIT = 600
class ProductionConfig(BaseConfig):
    'Produccion configuracion'
    DEBUG = False
class DevelopmentConfig(BaseConfig):
    'Desarrollo configuracion'
    DEBUG = True
    TESTING = True
    #palabra = random._urandom(24)
    #print(palabra)
    SECRET_KEY = "b'+W\xe8 Q\x08\xc7\xd1J\xcdk\xdf\xa2\x1f\x13\xeb\xa2G\xc9.\xc5\xb2\x86"
