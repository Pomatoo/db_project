from Utils import *
config1 = ConfigParser()
config1.read('analytics_config.conf')
name_node_ip = config1.get('name-node', 'name_node_public_ip')

config2 = ConfigParser()
config2.read('aws_config.conf')
key = config2.get('name-node', 'name_node_public_ip')

ssh_client_name_node = get_ssh_client(name_node_ip, key)
