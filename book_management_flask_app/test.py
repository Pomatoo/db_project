# import boto3
# from botocore.exceptions import ClientError
# from Utils import Config
#
# aws_config = Config('./aws_config.cfg')
#
# aws_client = boto3.client(
#     'ec2',
#     aws_access_key_id=aws_config.get_aws_access_key_id(),
#     aws_secret_access_key=aws_config.get_aws_secret_access_key(),
#     aws_session_token=aws_config.get_aws_session_token(),
#     region_name=aws_config.get_region_name()
# )
#
#
# ec2 = boto3.resource('ec2')
# instance = ec2.create_instances(
#     ImageId='ami-0817d428a6fb68645',
#     MinCount=1,
#     MaxCount=1,
#     InstanceType='t2.micro',
#     KeyName='awsKey'
# )
#
# # Retrieve instance information
# reservations = ec2.describe_instances()['Reservations']
# for instance in reservations:
#     print(instance)
#     # output of instance:
#     #{'Groups': [], 'Instances': [{'AmiLaunchIndex': 0, 'ImageId': 'ami-0817d428a6fb68645', 'InstanceId': 'i-0098a96b65d8512c0', 'InstanceType': 't2.micro', 'KeyName': 'awsKey', 'LaunchTime': datetime.datetime(2020, 10, 20, 16, 18, 14, tzinfo=tzutc()), 'Monitoring': {'State': 'disabled'}, 'Placement': {'AvailabilityZone': 'us-east-1a', 'GroupName': '', 'Tenancy': 'default'}, 'PrivateDnsName': '', 'ProductCodes': [], 'PublicDnsName': '', 'State': {'Code': 48, 'Name': 'terminated'}, 'StateTransitionReason': 'User initiated (2020-10-20 16:29:42 GMT)', 'Architecture': 'x86_64', 'BlockDeviceMappings': [], 'ClientToken': '540ab1c7-e071-4c47-933b-bb6722ed3c95', 'EbsOptimized': False, 'EnaSupport': True, 'Hypervisor': 'xen', 'NetworkInterfaces': [], 'RootDeviceName': '/dev/sda1', 'RootDeviceType': 'ebs', 'SecurityGroups': [], 'StateReason': {'Code': 'Client.UserInitiatedShutdown', 'Message': 'Client.UserInitiatedShutdown: User initiated shutdown'}, 'VirtualizationType': 'hvm', 'CpuOptions': {'CoreCount': 1, 'ThreadsPerCore': 1}, 'CapacityReservationSpecification': {'CapacityReservationPreference': 'open'}, 'HibernationOptions': {'Configured': False}, 'MetadataOptions': {'State': 'pending', 'HttpTokens': 'optional', 'HttpPutResponseHopLimit': 1, 'HttpEndpoint': 'enabled'}}], 'OwnerId': '891842124584', 'ReservationId': 'r-005260d506e12b50a'}
#     #{'Groups': [], 'Instances': [{'AmiLaunchIndex': 0, 'ImageId': 'ami-0817d428a6fb68645', 'InstanceId': 'i-00675425b2c16029f', 'InstanceType': 't2.micro', 'KeyName': 'awsKey', 'LaunchTime': datetime.datetime(2020, 10, 16, 9, 56, 34, tzinfo=tzutc()), 'Monitoring': {'State': 'disabled'}, 'Placement': {'AvailabilityZone': 'us-east-1b', 'GroupName': '', 'Tenancy': 'default'}, 'PrivateDnsName': '', 'ProductCodes': [], 'PublicDnsName': '', 'State': {'Code': 48, 'Name': 'terminated'}, 'StateTransitionReason': 'User initiated (2020-10-20 16:18:53 GMT)', 'Architecture': 'x86_64', 'BlockDeviceMappings': [], 'ClientToken': 'aa27b71b-5e1a-4caa-a68e-3fbd07b7603a', 'EbsOptimized': False, 'EnaSupport': True, 'Hypervisor': 'xen', 'NetworkInterfaces': [], 'RootDeviceName': '/dev/sda1', 'RootDeviceType': 'ebs', 'SecurityGroups': [], 'StateReason': {'Code': 'Client.UserInitiatedShutdown', 'Message': 'Client.UserInitiatedShutdown: User initiated shutdown'}, 'VirtualizationType': 'hvm', 'CpuOptions': {'CoreCount': 1, 'ThreadsPerCore': 1}, 'CapacityReservationSpecification': {'CapacityReservationPreference': 'open'}, 'HibernationOptions': {'Configured': False}, 'MetadataOptions': {'State': 'pending', 'HttpTokens': 'optional', 'HttpPutResponseHopLimit': 1, 'HttpEndpoint': 'enabled'}}], 'OwnerId': '891842124584', 'ReservationId': 'r-0590e5e1fa6024d39'}
#
# response = ec2.describe_vpcs()
# vpc_id = response.get('Vpcs', [{}])[0].get('VpcId', '')
#
# try:
#     response = ec2.create_security_group(GroupName='SECURITY_GROUP_NAME',
#                                          Description='DESCRIPTION',
#                                          VpcId=vpc_id)
#     security_group_id = response['GroupId']
#     print('Security Group Created %s in vpc %s.' % (security_group_id, vpc_id))
#
#     data = ec2.authorize_security_group_ingress(
#         GroupId=security_group_id,
#         IpPermissions=[
#             {'IpProtocol': 'tcp',
#              'FromPort': 80,
#              'ToPort': 80,
#              'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
#             {'IpProtocol': 'tcp',
#              'FromPort': 22,
#              'ToPort': 22,
#              'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
#             {'IpProtocol': 'tcp',
#              'FromPort': 27017,
#              'ToPort': 27017,
#              'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
#             {'IpProtocol': 'tcp',
#              'FromPort': 3306,
#              'ToPort': 3306,
#              'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}
#         ])
#     print('Ingress Successfully Set %s' % data)
# except ClientError as e:
#     print(e)

# Create security group
# Mongo

import pymongo
import json

client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['test']
collection = db['book_meta']

# data_ls = []
# file = open(r'C:\Users\Tomatoo\Desktop\meta_Kindle_Store.json', 'r')
# for each_line in file:
#     data_dictionary = eval(each_line)
#     data_ls.append(data_dictionary)
# file.close()
#
# # insert_many takes a list and insert all data in one shot
# x = collection.insert_many(data_ls)
# print(x.inserted_ids)

for i in collection.find({'asin': 'B000F83STC'}):
    print(i)
client.close()


# Read CSV
# import csv
#
# with open('kindle_reviews.csv', mode='r') as csv_file:
#     csv_reader = csv.reader(csv_file)
#     for row in csv_reader:
#         print(row)
#         break



# Dump Data to MySQL
# import pymysql
# import csv
# import datetime
#
# print(datetime.datetime.now())
# conn = pymysql.connect('localhost', user="root", passwd="1234")
# # conn = pymysql.connect('130.211.235.92', user="root", passwd="Wrn3h7^`")
#
# cursor = conn.cursor()
#
# cursor.execute('CREATE DATABASE IF NOT EXISTS testDB DEFAULT CHARSET utf8 COLLATE utf8_general_ci;')
#
# conn.select_db('testDB')
#
# cursor.execute('drop table if exists user')
#
# sql = """CREATE TABLE IF NOT EXISTS `review` (\
# 	  `id` int(11) NOT NULL AUTO_INCREMENT,\
# 	  `asin` varchar(255) NOT NULL,\
# 	  `helpful` varchar(255) ,\
# 	  `overall` varchar(255) ,\
# 	  `review_text` text ,\
# 	  `review_time` varchar(255) ,\
# 	  `reviewer_id` varchar(255) NOT NULL,\
# 	  `reviewer_name` varchar(255) ,\
# 	  `summary` varchar(1000) ,\
# 	  `unix_review_time` int(11) NOT NULL,\
# 	  PRIMARY KEY (`id`),\
# 	  INDEX idx_asin (asin)
# 	) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=0"""
#
# cursor.execute(sql)
#
# with open(r'C:\Users\Tomatoo\Desktop\kindle_reviews.csv', mode='r') as csv_file:
#     csv_reader = csv.reader(x.replace('\0', '') for x in csv_file)
#     next(csv_reader)
#     usersvalues = []
#     for row in csv_reader:
#         usersvalues.append((row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9]))
#
#     cursor.executemany(
#         "insert into review(asin,helpful,overall,review_text, review_time, reviewer_id, reviewer_name, summary,"
#         "unix_review_time) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)",
#         usersvalues)
#
# cursor.close()
#
# conn.commit()
#
# conn.close()
# print(datetime.datetime.now())

# LOAD DATA LOCAL INFILE 'C:\Users\Tomatoo\Desktop\kindle_reviews.csv' INTO TABLE testdb.review FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 ROWS;
