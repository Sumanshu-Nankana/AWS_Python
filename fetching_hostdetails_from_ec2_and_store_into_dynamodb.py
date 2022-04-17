import boto3

stsClient = boto3.client('sts')
ec2Client = boto3.client('ec2')
dbClient = boto3.client('dynamodb')


def lambda_handler(event, context):
    # getting the account_id
    response = stsClient.get_caller_identity()
    print(f"Output of get_caller_identity is : {response}")
    account_id = response['Account']
    print(f"account id is : {account_id}")

    # get the ec2-instance-details
    response = ec2Client.describe_instances(InstanceIds=["i-0236e8b33545dbcd6"])
    response = response['Reservations']

    for li in response:
        instance_properties = li['Instances']

    for i in instance_properties:
        instance_id = i['InstanceId']
        instance_type = i['InstanceType']
        private_ip_address = i['PrivateIpAddress']

    print(f"Instance Id is : {instance_id}")
    print(f"Instance Type is : {instance_type}")
    print(f"Private IP address : {private_ip_address}")

    # update data into dynamo Db table
    try:
        response = dbClient.put_item(
            TableName="my_dynamodb_table",
            Item={
                'account_id': {'S': account_id},
                'instance_id': {'S': instance_id},
                'instance_type': {'S': instance_type},
                'private_ip_address': {'S': private_ip_address}
            })
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            print("Entry has been sucessfully added into the Dynamo DB Database")
    except Exception as e:
        print(e)