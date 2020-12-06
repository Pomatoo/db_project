from configparser import ConfigParser

# To assign IPs of MongoDB and Mysql
class Config:
    cf = ConfigParser()
    # Local path
    # cf.read('./web_config.conf')
    # Server Path
    cf.read('/home/ubuntu/web_config.conf')
    mysql = cf.get('db', 'mysql')
    mongo = cf.get('db', 'mongo')

    SECRET_KEY = 'isTdSoo43'
    MONGO_URI = 'mongodb://admin:iStD-So.043-Database@%s:27017/test?authSource=admin' % mongo
    SQLALCHEMY_DATABASE_URI = 'mysql://root:iStD-So.043-Database@%s/testDB' % mysql
