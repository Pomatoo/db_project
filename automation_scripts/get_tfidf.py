from Utils import *
# This parser is to get public ip of MySQL server
config1 = ConfigParser()
config1.read('analytics_config.conf')
name_node_ip = config1.get('name-node', 'name_node_public_ip')

# This parser is to get ssh key name
config2 = ConfigParser()
config2.read('aws_config.conf')
key = config2.get('aws-credentials', 'access_key_name')

log('Running TF-IDF Job')
ssh_client_name_node = get_ssh_client(name_node_ip, key)
ssh_client_name_node.run('./run_tfidf.sh')
ssh_client_name_node.close()
log('Completed TF-IDF Job')
log('Please go to http://%s:8000 to view results.' % name_node_ip)