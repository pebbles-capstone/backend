import boto3
import numpy
import names
import random

def genStudentData(nStudents=250, data=[]):
    for i in range(nStudents):
        software = [0, 0, numpy.random.default_rng().uniform(0.02,0.25), numpy.random.default_rng().uniform(0.02,0.20), 0, numpy.random.default_rng().uniform(0.01,0.20)]
        data.append(software)
    return data

def loadStudentData(data, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb')

    table = dynamodb.Table('UserTable')

    disciplines = {
        0: "Computer Engineering",
        1: "Electrical Engineering"
    }

    userId = 120
    for student_vector in data:
        student_vector = [str(item) for item in student_vector]

        fname, lname = names.get_first_name(), names.get_last_name()

        student = {
            "userId": str(userId),
            "name": fname + " " + lname,
            "contact": fname.lower() + "." + lname.lower() + "@mail.utoronto.ca",
            "discipline": disciplines[random.randint(0, 1)],
            "about": "I am a fourth year student passionate about software. My dream is to work on systems.",
            "interest_vector": student_vector,
            "teamID": -1
        }
        
        try:
            table.put_item(Item=student)
        except:
            print('ERROR: new user could not be created')

        userId += 1

if __name__ == '__main__':
    student_dataset = genStudentData(nStudents=20)
    loadStudentData(student_dataset)