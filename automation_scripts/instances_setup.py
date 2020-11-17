from Utils import *
from time import sleep
from fabric import Connection


# log('Instances set up')
# aws_manager = AwsManager(init_security_group_and_key=True)
# key = aws_manager.get_access_key_name()
# security_group_id = aws_manager.get_security_group_id()
#
# mysql_instance = aws_manager.create_an_instance()
# # mongo_instance = aws_manager.create_an_instance()
# # web_instance = aws_manager.create_an_instance()
#
# # Store all created AWS instances
# to_be_logged = {'created_instances': [], 'access_key_name': key, 'security_group_id': security_group_id}
# to_be_logged['created_instances'].append(mysql_instance['id'])
# # to_be_logged['created_instances'].append(mongo_instance['id'])
# # to_be_logged['created_instances'].append(web_instance['id'])

# bash_mysql_instance = get_ssh_client('3.238.135.181', 'databaseProjectKey')
# # bash_mongo_instance = get_ssh_client(mongo_instance['ip'], key)
# # bash_web_instance = get_ssh_client(web_instance['ip'], key)
#
# bash_mysql_instance.put('./web_setup.sh')
# bash_mysql_instance.run('chmod 777 web_setup.sh')
# bash_mysql_instance.sudo('bash ./web_setup.sh')

breakpoint()

aws_manager = AwsManager()
# instance_id_list = [mysql_instance['id'], mongo_instance['id'], web_instance['id']]
instance_id_list = ['i-060054221c22a2dd1']
for iid in instance_id_list:
    aws_manager.terminate_instances(iid)
log('Waiting All Instances to be terminated ... ')

for iid in instance_id_list:
    while 1:
        status = aws_manager.get_instance_status(iid)
        if status == 'terminated':
            log('Instance %s is terminated' % iid)
            break
        sleep(10)

aws_manager.remove_key_pair('databaseProjectKey')
aws_manager.remove_security_group('Database_project')
