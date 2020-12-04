from Utils import *
import json

log('Instances set up, ETA 10 mins')
aws_manager = AwsManager(init_security_group_and_key=False, system_type='analytics')

to_be_logged = {'created_instances': [],
                'access_key_name': aws_manager.get_access_key_name(),
                'security_group_name': aws_manager.get_security_group_name()
                }

config = ConfigParser()
config.read('aws_config.conf')
num_of_datanode = int(config.get('analytics-system', 'num_of_datanode'))
log('Number of data node: %s ' % num_of_datanode)

datanode_list = []

for i in range(num_of_datanode):
    node = WorkerThread(aws_manager, 'data_node_%s' %i)
    datanode_list.append(node)

name_node = WorkerThread(aws_manager, 'name_node', sh_file='./analytics_scripts/name_node.sh')

for node in datanode_list:
    node.start()

name_node.start()
name_node.join()

for node in datanode_list:
    node.join()

cf = ConfigParser()

cf.add_section('name-node')
cf.set('name-node', 'name_node_public_ip', name_node.get_instance_details()['ip'])
cf.set('name-node', 'name_node_private_ip', name_node.get_instance_details()['private_ip'])

cf.add_section('data-node')
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
ssh_client_name_node = get_ssh_client(name_node.get_instance_details()['ip'], aws_manager.get_access_key_name())
ssh_client_name_node.get('.ssh/id_rsa.pub')

# Set public key for each data node
data_node_private_ips = ''
for data_node in datanode_list:
    node_details = data_node.get_instance_details()
    ssh_client_data_node = get_ssh_client(node_details['ip'], aws_manager.get_access_key_name())
    ssh_client_data_node.put('id_rsa.pub')
    ssh_client_data_node.run('cat id_rsa.pub >> ~/.ssh/authorized_keys')
    ssh_client_data_node.close()
    data_node_private_ips += '%s ' % node_details['private_ip']

# Set Up Name Node
ssh_client_name_node.run('echo "export MASTER=\'%s\'" >> ~/.bashrc && source ~/.bashrc' % name_node.get_instance_details()['ip'])
ssh_client_name_node.run('echo "export WORKERS=\'%s\'" >> ~/.bashrc && source ~/.bashrc' % data_node_private_ips)
ssh_client_name_node.put('set_up_namenode.sh')
ssh_client_name_node.run('./set_up_namenode.sh')
ssh_client_name_node.close()

# Set Up Data Node
for data_node in datanode_list:
    node_details = data_node.get_instance_details()
    ssh_client_data_node = get_ssh_client(node_details['ip'], aws_manager.get_access_key_name())
    ssh_client_data_node.put('data_node.sh')
    ssh_client_data_node.run('./data_node.sh')
    ssh_client_data_node.close()

# RUN
ssh_client_name_node = get_ssh_client(name_node.get_instance_details()['ip'], aws_manager.get_access_key_name())
ssh_client_name_node.run('/opt/hadoop-3.3.0/sbin/start-dfs.sh && /opt/hadoop-3.3.0/sbin/start-yarn.sh')
ssh_client_name_node.run('/opt/spark-3.0.1-bin-hadoop3.2/sbin/start-all.sh')
ssh_client_name_node.close()


# ssh ubuntu@35.153.98.254 -i myKey.pem "sudo cat /home/ubuntu/.ssh/id_rsa.pub" | ssh ubuntu@54.197.44.24 -i myKey.pem "sudo cat - | sudo tee -a /home/ubuntu/.ssh/authorized_keys"

# log(to_be_logged)
# with open('created_aws_instances.json', 'w') as f:
#     json.dump(to_be_logged, f, indent=4)


# Process:
# all data nodes run
# tar zxvf hadoop-3.3.0.tgz
# sudo mv hadoop-3.3.0 /opt/
# sudo mkdir -p /mnt/hadoop/datanode/
# sudo chown -R ubuntu:ubuntu /mnt/hadoop/datanode/
#
# tar zxvf spark-3.0.1-bin-hadoop3.2.tgz
# sudo mv spark-3.0.1-bin-hadoop3.2 /opt/
# sudo chown -R ubuntu:ubuntu /opt/spark-3.0.1-bin-hadoop3.2
