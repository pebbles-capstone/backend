from flask import Flask
import boto3
from routes.staticModel import generateStaticRec
from routes.dynModel import scanStudentData, clustersMap, student_heap_sort_return

app = Flask(__name__)


@app.route("/")
def home():
    return "<p>Hello, World!</p>"


@app.route("/status")
def status():
    return "<p>Healthy</p>"

@app.route("/rec/<id>")
def startRec(id):
    try:
        demo = {}
        staticRecs = generateStaticRec()

        student_data = scanStudentData(test=demo)
        cluster_map = clustersMap(student_data)

        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('RecsTable')

        for k in range(2,15):
            cluster_map.genClusters(k)

        # print(cluster_map.cluster_configs)

        # print(student_data)
        cluster_map.scoreClusters()

        recs = {}
        final_rec = {}
        for student_group in cluster_map.optimal_cluster_info.values():
            for i in range(len(student_group)):
                student, other_students = student_group[i], student_group[:i] + student_group[i+1:]

                student_rec2 = {
                    "userId": student[0],
                    "recs": student_heap_sort_return(student, other_students)
                }
                arr = student_heap_sort_return(student, other_students)
                
                recs[student[0]] = [demo[x] for x in arr]

                for proj in staticRecs[student[0]]["proj"]:
                    proj["id"] = str(proj["id"])
                    proj["Supervisor"] = str(proj["Supervisor"])
                    proj["Project Title"] = str(proj["Project Title"])
                    proj["Project Description"] = str(proj["Project Description"])
                    proj["Students"] = str(proj["Students"])
                    if "TagA" in proj:
                        proj["TagA"] = str(proj["TagA"])
                    if "TagB" in proj:
                        proj["TagB"] = str(proj["TagB"])
                    proj["ID"] = str(proj["ID"])
                    proj["TagBVector"] = str(proj["TagBVector"])

                for x in staticRecs[student[0]]["prof"]:
                    x["TagBVector"] = str(x["TagBVector"])
                    if "TagA" in x:
                        x["TagA"] = str(x["TagA"])
                    if "TagB" in x:
                        x["TagB"] = str(x["TagB"])
                    x["Admin"] = str(x["Admin"])
                    x["Interests"] = str(x["Interests"])

                student_rec = {
                    "userId": student[0],
                    "recs": {
                        "userRec": [demo[x] for x in arr],
                        "profRec": staticRecs[student[0]]["prof"],
                        "projectRec": staticRecs[student[0]]["proj"]
                    }
                }
                final_rec[student[0]] = student_rec
                try:
                    if id == student[0]:
                        table.put_item(Item=student_rec)
                except Exception as e:
                    print(e)
                    cnt = 0
                    if(cnt == 0):
                        print(student[0])
                    cnt+=1
                    print('ERROR')

    except Exception as e:
        print(e)
        return "Error: Something went wrong while building recs!"

    return final_rec[id]


@app.route("/staticRec")
def staticRec():
    recs = generateStaticRec()
    return recs
    # return "<p>Starting rec!</p>"


@app.route("/dynamicRec")
def dynamicRec():
    student_data = scanStudentData()
    cluster_map = clustersMap(student_data)

    for k in range(2,15):
        cluster_map.genClusters(k)

    # print(cluster_map.cluster_configs)

    # print(student_data)
    cluster_map.scoreClusters()

    recs = {}

    for student_group in cluster_map.optimal_cluster_info.values():
        for i in range(len(student_group)):
            student, other_students = student_group[i], student_group[:i] + student_group[i+1:]

            # student_rec = {
            #     "userId": student[0],
            #     "recs": student_heap_sort_return(student, other_students)
            # }
            recs[student[0]] = student_heap_sort_return(student, other_students)

    return recs


if __name__ == "__main__":
    app.run(host='0.0.0.0', port="5000", debug=True)
