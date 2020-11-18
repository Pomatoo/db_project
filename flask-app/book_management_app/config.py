from configparser import ConfigParser


class Config:
    cf = ConfigParser()
    cf.read('./web_config.conf')
    # cf.read('/etc/web_conf.conf')
    mysql = cf.get('db', 'mysql')
    mongo = cf.get('db', 'mongo')

    SECRET_KEY = 'isTdSoo43'
    MONGO_URI = 'mongodb://admin:iStD-So.043-Database@%s:27017/test?authSource=admin' % mongo
    SQLALCHEMY_DATABASE_URI = 'mysql://root:iStD-So.043-Database@%s/testDB' % mysql
