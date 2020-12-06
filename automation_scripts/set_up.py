from Utils import *
import json

log('Instances set up, ETA 10 mins')
production_manager = AwsManager(system_type='production')
analytics_manager = AwsManager(system_type='analytics')

# Log created aws objects (instances, key, security_group)
to_be_logged = {'created_instances': [],
                'access_key_name': production_manager.get_access_key_name(),
                'security_group_name': production_manager.get_security_group_name()
                }

aws_config = ConfigParser()
aws_config.read('aws_config.conf')
num_of_datanode = int(aws_config.get('analytics-system', 'num_of_datanode'))
log('Number of data node: %s ' % num_of_datanode)

# Production instances
mysql_worker = WorkerThread(production_manager, 'MySQL', sh_file=['production_scripts', 'mysql_setup.sh'])
mongo_worker = WorkerThread(production_manager, 'Mongo', sh_file=['production_scripts', 'mongo_setup.sh'])
web_worker = WorkerThread(production_manager, 'Web', sh_file=['production_scripts', 'web_setup.sh'])

# Analytics instance
datanode_list = []
for i in range(num_of_datanode):
    node = WorkerThread(analytics_manager, 'data_node_%s' % i, sh_file=['analytics_scripts', 'data_node.sh'])
    datanode_list.append(node)
name_node = WorkerThread(analytics_manager, 'name_node', sh_file=['analytics_scripts', 'name_node.sh'])

# Start threads
mysql_worker.start()
mongo_worker.start()
web_worker.start()
for data_node in datanode_list:
    data_node.start()
name_node.start()

name_node.join()
web_worker.join()
mysql_worker.join()
mongo_worker.join()
for data_node in datanode_list:
    data_node.join()

# Configuration for Production system
# get_instance_details() => {'id': instance_id, 'ip': public_ip, 'private_ip': private_ip, 'instance_name': instance_name}
mysql_instance = mysql_worker.get_instance_details()
mongo_instance = mongo_worker.get_instance_details()
web_instance = web_worker.get_instance_details()

# web_config will be sent to Web server, it contains IPs of the database servers
web_config = ConfigParser()
web_config.add_section('db')
web_config.set('db', 'mysql', mysql_instance['ip'])
web_config.set('db', 'mongo', mongo_instance['ip'])
with open('web_config.conf', 'w') as f:
    web_config.write(f)

# Configuration for Analytics system
# Grab public key to local machine
name_node_instance = name_node.get_instance_details()
ssh_client_name_node = get_ssh_client(name_node_instance['ip'], analytics_manager.get_access_key_name())
ssh_client_name_node.get('.ssh/id_rsa.pub')

# Set public key for each data node
# Format => data_node_private_ips = "ip1 ip2 ip3 ..."
log('Adding public key to data nodes')
data_node_private_ips = ''
for data_node in datanode_list:
    node_details = data_node.get_instance_details()
    ssh_client_data_node = get_ssh_client(node_details['ip'], analytics_manager.get_access_key_name())
    ssh_client_data_node.put('id_rsa.pub')
    ssh_client_data_node.run('cat id_rsa.pub >> ~/.ssh/authorized_keys')
    ssh_client_data_node.close()
    data_node_private_ips += '%s ' % node_details['private_ip']

# Configuration for Name Node
log('Configuring Name node')
ssh_client_name_node.put('./analytics_scripts/set_up_namenode.sh')
ssh_client_name_node.run("sed -i 's/export MASTER/export MASTER=%s/g' ./set_up_namenode.sh" % name_node_instance['private_ip'])
ssh_client_name_node.run("sed -i 's/export WORKERS/export WORKERS=\"%s\"/g' ./set_up_namenode.sh" % data_node_private_ips)
ssh_client_name_node.run('chmod +x ./set_up_namenode.sh && ./set_up_namenode.sh')
# Configure TF-IDF script
ssh_client_name_node.put('./analytics_scripts/run_tfidf.sh')
ssh_client_name_node.put('./analytics_scripts/tfidf.py')
ssh_client_name_node.run("sed -i 's/$MYSQL_HOST/%s/g' ./run_tfidf.sh" % mysql_instance['ip'])
ssh_client_name_node.run("sed -i 's/$NAME_NODE_IP/%s/g' ./tfidf.py" % name_node_instance['private_ip'])
ssh_client_name_node.run('chmod 777 ./tfidf.py')
ssh_client_name_node.run('chmod +x ./run_tfidf.sh')
# Configure Correlation script
ssh_client_name_node.put('./analytics_scripts/run_correlation.sh')
ssh_client_name_node.put('./analytics_scripts/correlation.py')
ssh_client_name_node.run("sed -i 's/$MYSQL_HOST/%s/g' ./run_correlation.sh" % mysql_instance['ip'])
ssh_client_name_node.run("sed -i 's/$MONGO_HOST/%s/g' ./run_correlation.sh" % mongo_instance['ip'])
ssh_client_name_node.run("sed -i 's/$NAME_NODE_IP/%s/g' ./correlation.py" % name_node_instance['private_ip'])
ssh_client_name_node.run('chmod 777 ./correlation.py')
ssh_client_name_node.run('chmod +x ./run_correlation.sh')
# Configure HTTP server
ssh_client_name_node.put('./analytics_scripts/http_server.py')
ssh_client_name_node.run('chmod 777 ./http_server.py')
ssh_client_name_node.close()

# Set Up Data Node
log('Configuring data nodes')
for data_node in datanode_list:
    node_details = data_node.get_instance_details()
    ssh_client_data_node = get_ssh_client(node_details['ip'], analytics_manager.get_access_key_name())
    ssh_client_data_node.put('./analytics_scripts/set_up_datanode.sh')
    ssh_client_data_node.run('chmod +x ./set_up_datanode.sh && ./set_up_datanode.sh')
    ssh_client_data_node.close()

log('Instances set up complete!')
log('Starting Hadoop + Spark')
# RUN Hadoop and Spark
ssh_client_name_node = get_ssh_client(name_node.get_instance_details()['ip'], analytics_manager.get_access_key_name())
ssh_client_name_node.run('/opt/hadoop-3.3.0/sbin/start-dfs.sh && /opt/hadoop-3.3.0/sbin/start-yarn.sh')
ssh_client_name_node.run('/opt/spark-3.0.1-bin-hadoop3.2/sbin/start-all.sh')
ssh_client_name_node.run('nohup python3 http_server.py > /dev/null 2>&1 &')
ssh_client_name_node.close()
log('Hadoop and Spark are running Now!')

log('Starting Web Application')
ssh_client = get_ssh_client(web_instance['ip'], production_manager.get_access_key_name())
ssh_client.put('web_config.conf')
ssh_client.put('./production_scripts/run_app.sh')
ssh_client.run('chmod 777 ~/web_config.conf ~/run_app.sh')
ssh_client.run('bash ~/run_app.sh')
log('Web Application is running now.')
log('>>>>>>>>>> Web: http://%s:8080' % web_instance['ip'])

to_be_logged['created_instances'].append(mysql_instance)
to_be_logged['created_instances'].append(mongo_instance)
to_be_logged['created_instances'].append(web_instance)
to_be_logged['created_instances'].append(name_node_instance)
for data_node in datanode_list:
    data_node_instance = data_node.get_instance_details()
    to_be_logged['created_instances'].append(data_node_instance)

log(to_be_logged)
with open('created_aws_instances.json', 'w') as f:
    json.dump(to_be_logged, f, indent=4)
