from Utils import *
import json

log('Instances set up, ETA 10 mins')

to_be_logged = {'created_instances': [],
                'access_key_name': aws_manager.get_access_key_name(),
                'security_group_name': aws_manager.get_security_group_name()
                }

aws_manager = AwsManager(init_security_group_and_key=False, system_type='analytics')

config = ConfigParser()
config.read('aws_config.conf')
num_of_datanode = int(config.get('analytics-system', 'num_of_datanode'))

log('Number of data node: %s ' % num_of_datanode)

datanode_list = []

for i in range(num_of_datanode):
    node = WorkerThread(aws_manager, 'data_node', 'data_node.sh')
    datanode_list.append(node)

name_node = WorkerThread(aws_manager, 'name_node', 'name_node.sh')

for node in datanode_list:
    node.start()

name_node.start()
name_node.join()

for node in datanode_list:
    node.join()

cf = ConfigParser()
cf.add_section('data-node')
cf.add_section('name-node')
cf.set('name-node', 'name_node_public_ip', name_node['ip'])
cf.set('name-node', 'name_node_private_ip', name_node['private_ip'])
cf.set('data-node', 'num_of_datanode', '%s' % len(datanode_list))

for index, node in enumerate(datanode_list):
    node_details = node.get_instance_details()
    cf.set('data-node', 'node_%s_public_ip' % index, node_details['ip'])
    cf.set('data-node', 'node_%s_private_ip' % index, node_details['private_ip'])

with open('analytics_config.conf', 'w') as f:
    cf.write(f)

log('Name node and data nodes set up successfully')

log('Setting public key for data nodes ... ')

# Grab public key to local machine
ssh_client_name_node = get_ssh_client(name_node['ip'], aws_manager.get_access_key_name())
ssh_client_name_node.get('.ssh/id_rsa.pub')

# Set public key for each data node
for data_node in datanode_list:
    ssh_client_data_node = get_ssh_client(data_node['ip'], aws_manager.get_access_key_name())
    ssh_client_data_node.put('id_rsa.pub')
    ssh_client_data_node.run('cat id_rsa.pub >> ~/.ssh/authorized_keys')

# Start Hadoop
ssh_client_name_node.run('')
ssh_client_name_node.put('run_hadoop.sh')

ssh_client_name_node.run('/opt/hadoop-3.3.0/sbin/start-dfs.sh && /opt/hadoop-3.3.0/sbin/start-yarn.sh')
ssh_client_name_node.close()

# ssh ubuntu@35.153.98.254 -i myKey.pem "sudo cat /home/ubuntu/.ssh/id_rsa.pub" | ssh ubuntu@54.197.44.24 -i myKey.pem "sudo cat - | sudo tee -a /home/ubuntu/.ssh/authorized_keys"


log('Instances set up complete!')
log('Starting Web Application')
while 1:
    try:
        ssh_client = get_ssh_client(web_instance['ip'], aws_manager.get_access_key_name())
        ssh_client.put('web_config.conf')
        ssh_client.put('run_app.sh')
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
