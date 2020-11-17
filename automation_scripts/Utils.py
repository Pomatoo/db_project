import boto3
import os
import json
from time import strftime
from botocore.exceptions import ClientError
from configparser import ConfigParser
from time import sleep
from fabric import Connection


def log(msg):
    print('%s %s' % (strftime('[%a %m-%d-%y %H:%M:%S] '), msg))


def write_json(file_name, msg_in_dictionary):
    with open('%s.json' % file_name, 'w') as f:
        json_object = json.dumps(msg_in_dictionary, indent=4)
        f.write(json_object)


def get_ssh_client(ip, key):
    return Connection(
        host=ip,
        user="ubuntu",
        connect_kwargs={
            "key_filename": key + ".pem",
        }
    )


class AwsManager(object):

    def __init__(self, init_security_group_and_key=False):
        self.__config = ConfigParser()
        self.__config.read('aws_config.conf')
        params = ('aws_access_key_id', 'aws_secret_access_key', 'instance_type',
                  'instance_ami', 'access_key_name', 'security_group_name',
                  'aws_educate', 'region_name')
        for param in params:
            if param not in self.__config.options('aws-credentials'):
                raise Exception('Parameter %s cannot be found in aws_config.conf' % param)

        self.__is_aws_educate = int(self.__config.get('aws-credentials', 'aws_educate'))

        credentials = {
            'aws_access_key_id': self.__config.get('aws-credentials', 'aws_access_key_id'),
            'aws_secret_access_key': self.__config.get('aws-credentials', 'aws_secret_access_key'),
            'region_name': self.__config.get('aws-credentials', 'region_name')
        }
        if self.__is_aws_educate:
            log('Using AWS Educate Account')
            credentials['aws_session_token'] = self.__config.get('aws-credentials', 'aws_session_token')

        self.__ec_client = boto3.client('ec2', **credentials)
        self.__access_key_name = self.__config.get('aws-credentials', 'access_key_name')
        self.__security_group_id = None

        if init_security_group_and_key:
            self.__create_security_group()
            self.__create_access_key()

    def get_access_key_name(self):
        return self.__access_key_name

    def get_security_group_id(self):
        return self.__security_group_id

    def get_instance_status(self, instance_id):
        response = self.__ec_client.describe_instances(
            InstanceIds=[instance_id]
        )
        return response['Reservations'][0]['Instances'][0]['State']['Name']

    def terminate_instances(self, instance_id):
        log('Terminating Instance id:%s' % instance_id)
        response = self.__ec_client.terminate_instances(
            InstanceIds=[
                instance_id,
            ]
        )

    def remove_key_pair(self, key_name):
        response = self.__ec_client.delete_key_pair(
            KeyName=key_name,
        )
        log('Key pair %s is deleted' % key_name)

    def remove_security_group(self, group_id):
        response = self.__ec_client.delete_security_group(
            GroupId=group_id,
        )
        log('Security Group id:%s is deleted' % group_id)

    def create_an_instance(self):
        """
        Sample output:
        {'Groups': [], 'Instances': [{'AmiLaunchIndex': 0, 'ImageId': 'ami-00ddb0e5626798373', 'InstanceId': 'i-0f530309de61f982d', 'InstanceType': 't2.medium', 'KeyName': 'databaseProjectKey', 'LaunchTime': datetime.datetime(2020, 11, 16, 12, 48, 14, tzinfo=tzutc()), 'Monitoring': {'State': 'disabled'}, 'Placement': {'AvailabilityZone': 'us-east-1f', 'GroupName': '', 'Tenancy': 'default'}, 'PrivateDnsName': 'ip-172-31-67-248.ec2.internal', 'PrivateIpAddress': '172.31.67.248', 'ProductCodes': [], 'PublicDnsName': '', 'State': {'Code': 0, 'Name': 'pending'}, 'StateTransitionReason': '', 'SubnetId': 'subnet-849cfa8a', 'VpcId': 'vpc-2fe81052', 'Architecture': 'x86_64', 'BlockDeviceMappings': [], 'ClientToken': '635a9213-5717-4c26-92b2-e76a932b9af5', 'EbsOptimized': False, 'EnaSupport': True, 'Hypervisor': 'xen', 'NetworkInterfaces': [{'Attachment': {'AttachTime': datetime.datetime(2020, 11, 16, 12, 48, 14, tzinfo=tzutc()), 'AttachmentId': 'eni-attach-0f08e208461e61dc6', 'DeleteOnTermination': True, 'DeviceIndex': 0, 'Status': 'attaching'}, 'Description': '', 'Groups': [{'GroupName': 'Database_project', 'GroupId': 'sg-00de8805e27c31078'}], 'Ipv6Addresses': [], 'MacAddress': '16:ac:f8:63:e6:6b', 'NetworkInterfaceId': 'eni-0cd39199ec2838c36', 'OwnerId': '891842124584', 'PrivateDnsName': 'ip-172-31-67-248.ec2.internal', 'PrivateIpAddress': '172.31.67.248', 'PrivateIpAddresses': [{'Primary': True, 'PrivateDnsName': 'ip-172-31-67-248.ec2.internal', 'PrivateIpAddress': '172.31.67.248'}], 'SourceDestCheck': True, 'Status': 'in-use', 'SubnetId': 'subnet-849cfa8a', 'VpcId': 'vpc-2fe81052', 'InterfaceType': 'interface'}], 'RootDeviceName': '/dev/sda1', 'RootDeviceType': 'ebs', 'SecurityGroups': [{'GroupName': 'Database_project', 'GroupId': 'sg-00de8805e27c31078'}], 'SourceDestCheck': True, 'StateReason': {'Code': 'pending', 'Message': 'pending'}, 'VirtualizationType': 'hvm', 'CpuOptions': {'CoreCount': 2, 'ThreadsPerCore': 1}, 'CapacityReservationSpecification': {'CapacityReservationPreference': 'open'}, 'MetadataOptions': {'State': 'pending', 'HttpTokens': 'optional', 'HttpPutResponseHopLimit': 1, 'HttpEndpoint': 'enabled'}}], 'OwnerId': '891842124584', 'ReservationId': 'r-005ae25a3e1f7e597', 'ResponseMetadata': {'RequestId': '3945171c-037e-42fd-a64a-2d0ac2ae9d54', 'HTTPStatusCode': 200, 'HTTPHeaders': {'x-amzn-requestid': '3945171c-037e-42fd-a64a-2d0ac2ae9d54', 'content-type': 'text/xml;charset=UTF-8', 'content-length': '4891', 'vary': 'accept-encoding', 'date': 'Mon, 16 Nov 2020 12:48:14 GMT', 'server': 'AmazonEC2'}, 'RetryAttempts': 0}}
        """
        log('Creating Instance')
        ec2_instance = self.__ec_client.run_instances(
            ImageId=self.__config.get('aws-credentials', 'instance_ami'),
            MinCount=1,
            MaxCount=1,
            InstanceType=self.__config.get('aws-credentials', 'instance_type'),
            KeyName=self.__access_key_name,
            SecurityGroupIds=[self.__security_group_id]
        )
        instance_id = ec2_instance['Instances'][0]['InstanceId']
        sleep(3)
        while 1:
            if self.get_instance_status(instance_id) == 'running':
                break
            sleep(3)

        public_ip = self.__ec_client.describe_instances(
            InstanceIds=[instance_id]
        )['Reservations'][0]['Instances'][0]['PublicIpAddress']

        log('Instance is created, ip:%s, id:%s, key:%s, security-group:%s ' %
            (public_ip, instance_id, self.__access_key_name, self.__security_group_id))
        return {'id': instance_id, 'ip': public_ip}

    def __create_access_key(self):
        existing_key_paris = [key['KeyName'] for key in self.__ec_client.describe_key_pairs()['KeyPairs']]
        log('Existing Key Paris: %s' % existing_key_paris)
        if self.__access_key_name in existing_key_paris:
            raise Exception(
                'Error, Key-%s already exists, assign a new access_key_name in aws_config.conf' % self.__access_key_name)

        log('Creating Access Key %s' % self.__access_key_name)
        response = self.__ec_client.create_key_pair(
            KeyName=self.__access_key_name
        )
        key = response['KeyMaterial']
        log('Access Key %s is created successfully' % self.__access_key_name)

        with open('%s.pem' % self.__access_key_name, 'w') as f:
            f.write(key)
        log(os.getcwd() + os.path.sep + '%s.pem is created' % self.__access_key_name)
        if os.name != 'nt':
            os.chmod('%s.pem' % self.__access_key_name, 0o400)

    def __create_security_group(self):
        """
        For the sack of simplicity, all instances share the same security group in this project
        Following code snippet is from Boto3 Documentation
        """
        response = self.__ec_client.describe_vpcs()
        vpc_id = response.get('Vpcs', [{}])[0].get('VpcId', '')

        existing_groups = [group['GroupName'] for group in
                           self.__ec_client.describe_security_groups()['SecurityGroups']]
        log('Existing Security Groups: %s' % existing_groups)

        if self.__config.get('aws-credentials', 'security_group_name') in existing_groups:
            raise Exception(
                'Error, Group-%s already exists, assign a new security_group_name in aws_config.conf' % self.__config.get(
                    'aws-credentials', 'security_group_name'))
        log('Creating Security Group: %s' % self.__config.get('aws-credentials', 'security_group_name'))

        try:
            response = self.__ec_client.create_security_group(
                GroupName=self.__config.get('aws-credentials', 'security_group_name'),
                Description='Database project security group',
                VpcId=vpc_id)
            self.__security_group_id = response['GroupId']
            log('Security Group Created %s in vpc %s.' % (self.__security_group_id, vpc_id))

            data = self.__ec_client.authorize_security_group_ingress(
                GroupId=self.__security_group_id,
                IpPermissions=[
                    {'IpProtocol': 'tcp',
                     'FromPort': 80,
                     'ToPort': 80,
                     'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
                    {'IpProtocol': 'tcp',
                     'FromPort': 22,
                     'ToPort': 22,
                     'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
                    {'IpProtocol': 'tcp',
                     'FromPort': 27017,
                     'ToPort': 27017,
                     'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
                    {'IpProtocol': 'tcp',
                     'FromPort': 3306,
                     'ToPort': 3306,
                     'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}
                ])
            log('Ingress Successfully Set %s' % data)

        except ClientError as e:
            log(e)
            log('Failed to create security group')
            self.__create_security_group()


if __name__ == "__main__":
    aws_manager = AwsManager(init_security_group_and_key=True)
    instance = aws_manager.create_an_instance()
    log(instance)
    breakpoint()
    aws_manager = AwsManager()
    iid = instance['id']
    aws_manager.terminate_instances(iid)
    log('Waiting All Instances to be terminated ... ')
    while 1:
        status = aws_manager.get_instance_status(iid)
        if status == 'terminated':
            break
        sleep(10)

    aws_manager.remove_key_pair('databaseProjectKey')
    aws_manager.remove_security_group('Database_project')

    # Send cmd over SSH
    # from fabric import Connection
    #
    # c = Connection(
    #     host='18.206.15.56',
    #     user="ubuntu",
    #     connect_kwargs={
    #         "key_filename": "databaseProjectKey.pem",
    #     }
    # )
    # c.run()
