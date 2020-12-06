from Utils import *
import json

with open('created_aws_instances.json', 'r') as f:
    content = json.loads(f.read())

created_instances = content['created_instances']
name_node_ip = ''
for instance in created_instances:
    if instance['instance_name'] == 'name_node':
        name_node_ip = instance['ip']
        break

key_name = content['access_key_name']

log('Running TF-IDF Job')
ssh_client_name_node = get_ssh_client(name_node_ip, key_name)
ssh_client_name_node.run('./run_tfidf.sh')
ssh_client_name_node.close()
log('Completed TF-IDF Job')
log('Please go to http://%s:8000 to view results.' % name_node_ip)