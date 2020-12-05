from Utils import *
import json

log('Instances set up, ETA 10 mins')
aws_manager = AwsManager(init_security_group_and_key=True, system_type='production')

to_be_logged = {'created_instances': [],
                'access_key_name': aws_manager.get_access_key_name(),
                'security_group_name': aws_manager.get_security_group_name()
                }

mysql_worker = WorkerThread(aws_manager, 'MySQL', sh_file='production_scripts/mysql_setup.sh')
mongo_worker = WorkerThread(aws_manager, 'Mongo', sh_file='production_scripts/mongo_setup.sh')
web_worker = WorkerThread(aws_manager, 'Web', sh_file='web_setup.sh')

mysql_worker.start()
mongo_worker.start()
web_worker.start()

web_worker.join()
mysql_worker.join()
mongo_worker.join()

mysql_instance = mysql_worker.get_instance_details()
mongo_instance = mongo_worker.get_instance_details()
web_instance = web_worker.get_instance_details()

cf = ConfigParser()
cf.add_section('db')
cf.set('db', 'mysql', mysql_instance['ip'])
cf.set('db', 'mongo', mongo_instance['ip'])

with open('web_config.conf', 'w') as f:
    cf.write(f)

log('Instances set up complete!')
log('Starting Web Application')
while 1:
    try:
        ssh_client = get_ssh_client(web_instance['ip'], aws_manager.get_access_key_name())
        ssh_client.put('web_config.conf')
        ssh_client.put('./production_scripts/run_app.sh')
        ssh_client.run('chmod 777 ~/web_config.conf ~/run_app.sh')
        ssh_client.run('bash ~/run_app.sh')
    except:
        sleep(3)
    else:
        break
log('Web Application is running now.')
log('>>>>>>>>>> Web: http://%s:8080' % web_instance['ip'])

to_be_logged['created_instances'] = [mysql_instance, mongo_instance, web_instance]
log(to_be_logged)
with open('created_aws_instances.json', 'w') as f:
    json.dump(to_be_logged, f, indent=4)
