import boto3
import numpy as np
import sklearn
import multiprocessing
import collections
import json
import pickle
import ast

from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score
from sklearn.metrics.pairwise import cosine_similarity,cosine_distances

MODEL_BASE = "/home/ec2-user/mlapi/backend/ML/ML/models/"
DATA_BASE = "/home/ec2-user/mlapi/backend/ML/ML/data/"
prof_path = MODEL_BASE + "prof_model.pkl"
proj_path = MODEL_BASE + "prof_model.pkl"
prof_cluster_path = DATA_BASE + "prof_cluster_map.json"
prof_data_path = DATA_BASE + "prof_json_data.json"
proj_cluster_path = DATA_BASE + "proj_cluster_map.json"
proj_data_path = DATA_BASE + "proj_json_data.json"

kernels = {
           "Photonics and Semiconductor Physics": 0,
           "Electromagnetics and Energy Systems": 1,
           "Analog and Digital Electronics": 2,
           "Control, Communications and Signal Processing": 3,
           "Computer Hardware & Computer Networks": 4,
           "Software": 5
          }

def getStudentData(dynamodb=None, test={}):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb')

    table = dynamodb.Table('UserTable')
    response = table.scan()

    data = []
    for student in response["Items"]:
        if "interest_vector" in student:
            data.append((student["userId"], [float(x)
                        for x in student["interest_vector"]]))
            test[student["userId"]] = student
        elif "interests" in student and len(student["interests"]) == 6:
            arr = [float(x) for x in student["interests"]]
            if "projectCount" in student:
                cnt = float(student["projectCount"])
                try:
                    arr = [float(x)/cnt for x in student["interests"]]
                    if "f9c97aeb-cc50-4a1d-a561-8632faaa9b0f" == student["userId"]:
                        print("Inside:",arr)
                    if "area" in student:
                        for kernel, ind in kernels.items():
                            if kernel in student["area"]:
                                arr[ind] += 2
                                print("Increment!!")

                except:
                    arr = [float(x) for x in student["interests"]]
                    print(arr)
                    print("Error: Normalizing student data failed")
            data.append((student["userId"], arr))
            test[student["userId"]] = student
        else:
            print("failed")
            print(student)

    return data

def storeRecs(recs):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('RecsTable')
  
    for student_rec in recs:
        try:
            table.put_item(Item=student_rec)
        except:
            print('ERROR- Cound not save data' + str(student_rec))

def buildProfRecs(prof_key, v, prof_cluster_info, prof_data):
    #Container for recs per student
    prof_rec = []
    
    if prof_key in prof_cluster_info:
        points = prof_cluster_info[prof_key]

        #Container for sorted points
        weighted_p = []
    
        for point in points:
            try:
                arr = ast.literal_eval(point)
                weight = (calculateCosSim(v,arr),point)
                # print(weight)
                weighted_p.append(weight)
            except:
                print("Error: points eval failed for " + point)
        
        sorted(weighted_p,reverse=True)
        # print(weighted_p)
        for _,coord in weighted_p:
            if(len(prof_rec) > 100):
                break
            if coord in prof_data:
                data = prof_data[coord]
                prof_rec.extend(data)
            else:
                print("Error: this coord is not in prof " + coord)

    else:
        print("Error: this key failed " + prof_key)

    return prof_rec


def buildProjRecs(proj_key, v, proj_cluster_info, proj_data):
    #Container foQr recs per student
    proj_rec = []
    proj_key = "ALL"
    if proj_key in proj_cluster_info:
        points = proj_cluster_info["ALL"]

        #Container for sorted points
        weighted_p = []
        print("Points:", len(points))
        for point in points:
            try:
                arr = ast.literal_eval(point)
                weight = (calculateCosSim(v,arr),point)
                # print(weight)
                weighted_p.append(weight)
            except:
                print("Error: points eval failed for " + point)
        
        res = sorted(weighted_p, reverse=True)
        print(res)
        print(len(weighted_p))
        for _,coord in res:
            if coord in proj_data:
                data = proj_data[coord]
                proj_rec.extend(data)
            else:
                print("Error: this coord is not in prof " + coord)

    else:
        print("Error: this key failed " + proj_key)

    # print(len(proj_rec))

    return proj_rec

def calculateCosSim(a,b):
    A=np.array(a)
    B=np.array(b)
    result=cosine_similarity(A.reshape(1,-1),B.reshape(1,-1))
    return result[0][0]

def generateStaticRec():
    # Get all student data in correct format
    studentData = getStudentData()

    # Load in all models
    prof_model = loadModel(prof_path)
    proj_model = loadModel(proj_path)

    #Load in cluster data
    proj_cluster_info = loadJsonData(proj_cluster_path)
    prof_cluster_info = loadJsonData(prof_cluster_path)

    #Load in lookup table
    proj_data = loadJsonData(proj_data_path)
    prof_data = loadJsonData(prof_data_path)

    #Container for all recs
    recs = {}

    for (k,v) in studentData:
        #Container for recs per student
        prof_rec = []
        proj_rec = []

        #Skip index if len is too large
        if len(v) != 6: continue

        #Predict cluster spot for a point
        prof_index = prof_model.predict([v])
        proj_index = proj_model.predict([v])

        #Build keys and build data
        prof_key = str(prof_index[0])
        proj_key = str(proj_index[0])

        prof_rec = buildProfRecs(prof_key, v, prof_cluster_info, prof_data) 
        proj_rec = buildProjRecs(proj_key, v, proj_cluster_info, proj_data)

        recs[k] = {
            "prof": prof_rec,
            "proj": proj_rec
        }
    
    return recs


def loadModel(path):
    with open(path, "rb") as f:
        model = pickle.load(f)
        return model

def loadJsonData(path):
    with open(path) as json_file:
        data = json.load(json_file)
        return data

# if __name__ == '__main__':
#     recs = generateStaticRec()
