from Utils import *
from configparser import SafeConfigParser

log('Instances set up')
aws_manager = AwsManager(init_security_group_and_key=True)

to_be_logged = {'created_instances': [],
                'access_key_name': aws_manager.get_access_key_name(),
                'security_group_id': aws_manager.get_security_group_id()
                }

mysql_worker = WorkerThread(aws_manager, 'MySQL', 'mysql_setup.sh')
mongo_worker = WorkerThread(aws_manager, 'Mongo', 'mongo_setup.sh')

mysql_worker.start()
mongo_worker.start()
mysql_worker.join()
mongo_worker.join()

mysql_instance = mysql_worker.get_instance_details()
mongo_instance = mongo_worker.get_instance_details()

cf = ConfigParser()
cf.add_section('db')
cf.set('db', 'mysql', mysql_instance['ip'])
cf.set('db', 'mongo', mongo_worker['ip'])

with open('web_config.conf', 'w') as f:
    cf.write(f)

log('Creating Web-server instance')
web_worker = WorkerThread(aws_manager, 'Web', 'web_setup.sh')
web_worker.start()
web_worker.join()
web_instance = mysql_worker.get_instance_details()
log('Instances set up complete!')
log('>>>>>>>>>> Web: http://%s:8080' % web_instance['ip'])

to_be_logged['created_instances'].append([mysql_instance['ip'], web_instance['ip']])
log(to_be_logged)



###########################################################################
# mysql_instance = aws_manager.create_an_instance()
# mongo_instance = aws_manager.create_an_instance()
# web_instance = aws_manager.create_an_instance()

# Store all created AWS instances

# to_be_logged['created_instances'].append(mongo_instance['id'])
# to_be_logged['created_instances'].append(web_instance['id'])


# bash_mysql_instance = get_ssh_client('3.236.222.176', 'databaseProjectKey')
# bash_mongo_instance = get_ssh_client(mongo_instance['ip'], key)
# bash_web_instance = get_ssh_client(web_instance['ip'], key)

# bash_mysql_instance.put('./web_setup.sh')
# bash_mysql_instance.run('chmod 777 web_setup.sh')
# bash_mysql_instance.sudo('bash ./web_setup.sh')

# breakpoint()

# aws_manager = AwsManager()
# # instance_id_list = [mysql_instance['id'], mongo_instance['id'], web_instance['id']]
# instance_id_list = ['i-060054221c22a2dd1']
# for iid in instance_id_list:
#     aws_manager.terminate_instances(iid)
# log('Waiting All Instances to be terminated ... ')
#
# for iid in instance_id_list:
#     while 1:
#         status = aws_manager.get_instance_status(iid)
#         if status == 'terminated':
#             log('Instance %s is terminated' % iid)
#             break
#         sleep(10)
#
# aws_manager.remove_key_pair('databaseProjectKey')
# aws_manager.remove_security_group(security_group_id)
