import json
import boto3

def loadProfData(data, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb')
        #arn:aws:dynamodb:ca-central-1:768427752868:table")

    table = dynamodb.Table('ProfTable')
    
    profId = 0
    for vec in data:
        for prof in data[vec]:
            profId+=1
            prof["Year"] = prof["id"]
            prof["id"] = str(profId)
            prof["Admin"] = str(prof["Admin"])
            prof["Interests"] = str(prof["Interests"])
            try:
                table.put_item(Item=prof)
            except:
                print(prof)
                print('wtf')
            # return

    # response = table.get_item(Key={'id': '2020-2021 Professor Interests 79'})
    # print(response['Item']['TagBVector'])


if __name__ == '__main__':
    f = open('./prof_json_data.json')
    data = json.load(f)
    
    loadProfData(data)

    f.close()