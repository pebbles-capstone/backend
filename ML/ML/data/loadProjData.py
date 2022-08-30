import json
import boto3

def loadProjData(data, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb')
        #arn:aws:dynamodb:ca-central-1:768427752868:table")

    table = dynamodb.Table('ProjectTable')
    
    projId = 0
    for vec in data:
        for proj in data[vec]:
            projId+=1
            proj["Year"] = proj["id"]
            proj["id"] = str(projId)
            proj["Supervisor"] = str(proj["Supervisor"])
            proj["Project Title"] = str(proj["Project Title"])
            proj["Project Description"] = str(proj["Project Description"])
            proj["Students"] = str(proj["Students"])
            proj["TagA"] = str(proj["TagA"])
            proj["TagB"] = str(proj["TagB"])
            proj["ID"] = str(proj["ID"])
            try:
                table.put_item(Item=proj)
            except:
                print(proj)
                print('wtf')
            # return

    # response = table.get_item(Key={'id': '2020-2021 Professor Interests 79'})
    # print(response['Item']['TagBVector'])


if __name__ == '__main__':
    f = open('./proj_json_data.json')
    data = json.load(f)
    
    loadProjData(data)

    f.close()