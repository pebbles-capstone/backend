import boto3
import numpy
import sklearn
import multiprocessing
import collections
import heapq

from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score


# dynamic route -> student data -> multiple cluster configurations in parallel -> pick best -> return top 10
# DONE              DONE            TODO (easy)                                     DONE        

def scanStudentData(dynamodb=None, test={}):
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
                except:
                    arr = [float(x) for x in student["interests"]]
            if arr != [0,0,0,0,0,0]:
                data.append((student["userId"], arr))
            test[student["userId"]] = student
        else:
            print(student)

    
    return data

class clustersMap:
    def __init__(self, data):
        self.ids = [x[0] for x in data]
        self.data = [x[1] for x in data]

        self.cluster_configs = []
        self.max_loss = 0.0

        self.optimal_cluster = None
        self.optimal_cluster_info = collections.defaultdict(list)

    def set_max_loss(self):
        for cluster in self.cluster_configs:
            self.max_loss = max(self.max_loss, cluster.loss)
    
    def genClusters(self, k=2):
        print("clusters START (" + str(k) + ")")
        
        data = self.data
        kmeans_cluster = cluster(k) # new cluster object
        km = KMeans(init="k-means++", n_clusters=k) #KMeans object
        
        # generate cluster info and populate cluster object
        kmeans_cluster.clusters = km.fit_predict(data) # generate cluster-data mapping
        kmeans_cluster.loss = km.inertia_ # loss
        kmeans_cluster.silhouette = silhouette_score(data, kmeans_cluster.clusters) # silhouette score

        self.cluster_configs.append(kmeans_cluster)
        self.max_loss = max(self.max_loss, kmeans_cluster.loss)

        print("clusters END (" + str(k) + ")")

    def scoreClusters(self):
        for cluster in self.cluster_configs:
            cluster.score += cluster.silhouette * 0.5 # normalized silhouette score
            cluster.score += (1.0 - (cluster.loss / self.max_loss)) * 0.5 # normalized loss

            if not self.optimal_cluster or self.optimal_cluster.score < cluster.score:
                self.optimal_cluster = cluster
        
        student = 0
        for student_cluster in self.optimal_cluster.clusters:
            self.optimal_cluster_info[student_cluster].append((self.ids[student], numpy.array(self.data[student])))
            student += 1

class cluster:
    def __init__(self, k):
        self.k = k # number of clusters
        self.clusters = [] # cluster mapping corresponding to data
        self.loss = 0.0 # loss calculated for cluster configuration
        
        # silhouette score calculated for cluster configuration
        # 1 -> more distinct segregated clusters (perfect clusters)
        # 0 -> clusters are less distinct (imperfect clusters)
        self.silhoutte = 0.0 

        # normalized rating for cluster configuration combining loss and silhoutte score
        self.score = 0.0

def student_heap_sort_return(student, other_students, k=10): # return list of n closest students to 'student' within 'other_students'
    heap = []
    
    if not other_students:
        return heap
    
    s_id, s_dp = student[0], student[1]
    for o_id, o_dp in other_students:
        curr_key = -numpy.linalg.norm(s_dp - o_dp)
        curr_id = o_id

        if len(heap) == k:
            top_key, top_id = heapq.heappop(heap)
            if -top_key < -curr_key:
                curr_key = top_key
                curr_id = top_id

        heapq.heappush(heap, (curr_key, curr_id))
    
    ret = []
    while heap:
        ret.insert(0, heapq.heappop(heap)[1]) # insert other student ids in order from nth closest to 1st closest

    return ret

if __name__ == '__main__':
    # fetch/format student data, load into clusterMap object
    student_data = scanStudentData()
    cluster_map = clustersMap(student_data)

    # TODO: This is working, need to mod function returns a bit
    # set up processes 
    # pool = multiprocessing.Pool(processes=4)
    # args = [k for k in range(2,15)]
    # ret = pool.map(cluster_map.genClusters, args)
    # print(ret)

    for k in range(2,15):
        cluster_map.genClusters(k)

    # print(cluster_map.cluster_configs)

    # print(student_data)
    cluster_map.scoreClusters()

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('RecsTable')

    for student_group in cluster_map.optimal_cluster_info.values():
        for i in range(len(student_group)):
            student, other_students = student_group[i], student_group[:i] + student_group[i+1:]

            student_rec = {
                "userId": student[0],
                "recs": student_heap_sort_return(student, other_students)
            }

            try:
                table.put_item(Item=student_rec)
            except:
                print('ERROR')




    # print(cluster_map.optimal_cluster_info[0])

    # c = cluster_map.optimal_cluster_info[0]

    # for s in range(len(c)):
    #     print(c[s])
    #     print(student_heap_sort_return(c[s], c[:s] + c[s+1:]))

    #     temp = []
    #     for other in c[:s] + c[s+1:]:
    #         temp.append((numpy.linalg.norm(c[s][1] - other[1]), other[0]))
    #     temp.sort(key=lambda x: x[0])
    #     print(temp)


    #     print()

    # iter through key, list (cluster id, and students within cluster)
        # Apply top n ranking to each student within cluster -> heap of size n
        # order key = numpy.linalg.norm(a-b)


    # for cluster in cluster_map.cluster_configs:
    #     print(cluster.k)
    #     print(cluster.score)
    #     print()

    # print(optimal_cluster.k)