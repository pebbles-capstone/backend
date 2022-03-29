import boto3
import numpy
import sklearn
import multiprocessing
import collections
import heapq

from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score


def getStudentData(dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb')

    table = dynamodb.Table('UserTable')
    response = table.scan()

    data = []
    for student in response["Items"]:
        data.append((student["userId"], [float(x)
                    for x in student["interest_vector"]]))

    return data


def buildProfRecs():
    raise NotImplementedError


def buildProjRecs():
    raise NotImplementedError


def generateStaticRec():
    studentData = getStudentData()
    prof_rec = buildProfRecs(studentData)
    proj_rec = buildProjRecs(studentData)
