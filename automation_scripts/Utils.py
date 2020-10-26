import boto3
from botocore.exceptions import ClientError


class Config(object):
    def __init__(self, cfg_path):
        self.configs = {}

        with open(cfg_path) as f:
            for i in f:
                if i.strip() != '' and i.strip()[0] != '#' and len(i.strip().split('=', 1)) == 2:
                    params = i.strip().split('=', 1)
                    self.configs[params[0]] = params[1]

        self.validation()

    def get_aws_access_key_id(self):
        return self.configs['aws_access_key_id']

    def get_aws_secret_access_key(self):
        return self.configs['aws_secret_access_key']

    def get_aws_session_token(self):
        return self.configs['aws_session_token']

    def get_region_name(self):
        return self.configs['region_name']

    def validation(self):
        params = ['aws_access_key_id', 'aws_secret_access_key', 'aws_session_token', 'region_name']
        for param in params:
            if param not in self.configs.keys() or self.configs[param] == '':
                raise Exception('%s not found or empty' % param)


class AwsManager(object):

    def __init__(self):
        self.__config = Config()
        self.ec2 = boto3.client(
            'ec2',
            aws_access_key_id=self.__config.get_aws_access_key_id(),
            aws_secret_access_key=self.__config.get_aws_secret_access_key(),
            aws_session_token=self.__config.get_aws_session_token(),
            region_name=self.__config.get_region_name()
        )
        self.__set_up_security_group()

    def get_instance_status(self):
        return None

    def create_instance(self):
        pass

    def __create_security_group(self):
        response = self.ec2.describe_vpcs()
        vpc_id = response.get('Vpcs', [{}])[0].get('VpcId', '')

        try:
            response = self.ec2.create_security_group(GroupName='Database_project',
                                                 Description='Database project security group',
                                                 VpcId=vpc_id)
            security_group_id = response['GroupId']
            print('Security Group Created %s in vpc %s.' % (security_group_id, vpc_id))

            data = self.ec2.authorize_security_group_ingress(
                GroupId=security_group_id,
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
            print('Ingress Successfully Set %s' % data)
        except ClientError as e:
            print(e)
            self.__create_security_group()
        else:
            return
