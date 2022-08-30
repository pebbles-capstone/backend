import json
import boto3

def editTable(dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb')

    table = dynamodb.Table('ProjectTable')
    for i in range(1, 89):
        print(i)
        response = table.get_item(Key={'id': i})
        print(response)

    # projId = 0
    # for vec in data:
    #     for proj in data[vec]:
    #         projId+=1
    #         proj["Year"] = proj["id"]
    #         proj["id"] = str(projId)
    #         proj["Supervisor"] = str(proj["Supervisor"])
    #         proj["Project Title"] = str(proj["Project Title"])
    #         proj["Project Description"] = str(proj["Project Description"])
    #         proj["Students"] = str(proj["Students"])
    #         proj["TagA"] = str(proj["TagA"])
    #         proj["TagB"] = str(proj["TagB"])
    #         proj["ID"] = str(proj["ID"])
    #         try:
    #             table.put_item(Item=proj)
    #         except:
    #             print(proj)
    #             print('wtf')
            # return

    # response = table.get_item(Key={'id': '2020-2021 Professor Interests 79'})
    # print(response['Item']['TagBVector'])


if __name__ == '__main__':
    editTable()

    f.close()