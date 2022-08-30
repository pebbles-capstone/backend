import boto3
from botocore.exceptions import ClientError

def deleteUserTable(dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb')

    table = dynamodb.Table('UserTable')

    try:
        table.delete()
    except ClientError as e:
        print(e.response['Error']['Code'])
        if e.response['Error']['Code'] == "ConditionalCheckFailedException":
            print(e.response['Error']['Message'])
        elif e.response['Error']['Code'] == 'ResourceNotFoundException':
            print(e.response['Error']['Message'])
        else:
            raise

def createUserTable(dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb')

    table = dynamodb.create_table(
        TableName='UserTable',
        KeySchema=[
            {
                'AttributeName': 'userId',
                'KeyType': 'HASH'  # Partition key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'userId',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 1,
            'WriteCapacityUnits': 1
        }
    )

def flushStudentData(dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb')

    # deleteUserTable(dynamodb)
    # createUserTable(dynamodb)

    table = dynamodb.Table('UserTable')

    for userId in range(250):
        try:
            response = table.delete_item(
                Key={
                    'userId': str(userId)
                }
            )
        except ClientError as e:
            if e.response['Error']['Code'] == "ConditionalCheckFailedException":
                print(e.response['Error']['Message'])
            else:
                raise

if __name__ == '__main__':
    flushStudentData()