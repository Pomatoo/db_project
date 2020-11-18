import json

from Utils import *

with open('created_aws_instances.json', 'r') as f:
    content = json.loads(f.read())

created_instances = content['created_instances']
key_name = content['access_key_name']
security_group_name = content['security_group_name']

aws_manager = AwsManager(init_security_group_and_key=False)
log('Created instances are %s' % content)
for each_instance in created_instances:
    aws_manager.terminate_instances(each_instance['id'])

log('Waiting All Instances to be terminated ... ')
for each_instance in created_instances:
    while 1:
        state = aws_manager.get_instance_state(each_instance['id'])
        if state == 'terminated':
            break
        sleep(10)
log('All Instances are terminated')
aws_manager.remove_key_pair(key_name)
aws_manager.remove_security_group(security_group_name)
aws_manager.remove_key_pair(key_name)
log('Thank you!')
