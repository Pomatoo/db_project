from Utils import *
import json

log('Instances set up, ETA 10 mins')
aws_manager = AwsManager(system_type='analytics')

to_be_logged = {'created_instances': [],
                'access_key_name': aws_manager.get_access_key_name(),
                'security_group_name': aws_manager.get_security_group_name()
                }

config = ConfigParser()
config.read('aws_config.conf')
num_of_datanode = int(config.get('analytics-system', 'num_of_datanode'))
log('Number of data node: %s ' % num_of_datanode)

web_config = ConfigParser()
web_config.read('web_config.conf')
mysql_ip = web_config.get('db', 'mysql')
mongo_ip = web_config.get('db', 'mongo')

datanode_list = []

for i in range(num_of_datanode):
    node = WorkerThread(aws_manager, 'data_node_%s' % i)
    datanode_list.append(node)

name_node = WorkerThread(aws_manager, 'name_node', sh_file=['analytics_scripts', 'name_node.sh'])

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
ssh_client_name_node.put('./analytics_scripts/set_up_namenode.sh')
ssh_client_name_node.run(
    "sed -i 's/export MASTER/export MASTER=%s/g' ./set_up_namenode.sh" % name_node.get_instance_details()['private_ip'])
ssh_client_name_node.run(
    "sed -i 's/export WORKERS/export WORKERS=\"%s\"/g' ./set_up_namenode.sh" % data_node_private_ips)
ssh_client_name_node.run('chmod +x ./set_up_namenode.sh && ./set_up_namenode.sh')
# Configure TF-IDF script
ssh_client_name_node.put('./analytics_scripts/run_tfidf.sh')
ssh_client_name_node.put('./analytics_scripts/tfidf.py')
ssh_client_name_node.run("sed -i 's/$MYSQL_HOST/%s/g' ./run_tfidf.sh" % mysql_ip)
ssh_client_name_node.run("sed -i 's/$NAME_NODE_IP/%s/g' ./tfidf.py" % name_node.get_instance_details()['private_ip'])
ssh_client_name_node.run('chmod 777 ./tfidf.py')
ssh_client_name_node.run('chmod +x ./run_tfidf.sh')
# Configure Correlation script
ssh_client_name_node.put('./analytics_scripts/run_correlation.sh')
ssh_client_name_node.put('./analytics_scripts/correlation.py')
ssh_client_name_node.run("sed -i 's/$MYSQL_HOST/%s/g' ./run_correlation.sh" % mysql_ip)
ssh_client_name_node.run("sed -i 's/$MONGO_HOST/%s/g' ./run_correlation.sh" % mongo_ip)
ssh_client_name_node.run("sed -i 's/$NAME_NODE_IP/%s/g' ./correlation.py" % name_node.get_instance_details()['private_ip'])
ssh_client_name_node.run('chmod 777 ./correlation.py')
ssh_client_name_node.run('chmod +x ./run_correlation.sh')
ssh_client_name_node.close()

# Set Up Data Node
for data_node in datanode_list:
    node_details = data_node.get_instance_details()
    ssh_client_data_node = get_ssh_client(node_details['ip'], aws_manager.get_access_key_name())
    ssh_client_data_node.put('./analytics_scripts/set_up_datanode.sh')
    ssh_client_data_node.run('chmod +x ./set_up_datanode.sh && ./set_up_datanode.sh')
    ssh_client_data_node.close()

# RUN Hadoop and Spark
ssh_client_name_node = get_ssh_client(name_node.get_instance_details()['ip'], aws_manager.get_access_key_name())
ssh_client_name_node.run('/opt/hadoop-3.3.0/sbin/start-dfs.sh && /opt/hadoop-3.3.0/sbin/start-yarn.sh')
ssh_client_name_node.run('/opt/spark-3.0.1-bin-hadoop3.2/sbin/start-all.sh')
ssh_client_name_node.run('cd ~/result && nohup python3 -m http.server 8000 > /dev/null 2>&1 &')
ssh_client_name_node.close()
