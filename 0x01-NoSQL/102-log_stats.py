#!/usr/bin/env python3
"""
12-log_stats.py Improved
"""


from pymongo import MongoClient
from collections import Counter


def log_nginx_stats(mongo_collection):
    """provides some stats about Nginx logs"""
    print(f"{mongo_collection.estimated_document_count()} logs")

    print("Methods:")
    for method in ["GET", "POST", "PUT", "PATCH", "DELETE"]:
        count = mongo_collection.count_documents({"method": method})
        print(f"\tmethod {method}: {count}")

    number_of_gets = mongo_collection.count_documents(
        {"method": "GET", "path": "/status"})
    print(f"{number_of_gets} status check")
    # ==========
    print('IPs:')
    docs = mongo_collection.find()
    IPs_list = [doc['ip'] for doc in docs]
    IPs_list_counted = [{'ip': key, 'count': count}
                        for key, count in Counter(IPs_list).items()]
    IPs_list_counted_sorted = sorted(
        IPs_list_counted, key=lambda ip: ip['count'], reverse=True)

    for ip in IPs_list_counted_sorted[0:10]:
        count = mongo_collection.count_documents({"ip": ip['ip']})
        print(f"\t{ip['ip']}: {count}")


if __name__ == "__main__":
    mongo_collection = MongoClient('mongodb://172.17.0.2:27017').logs.nginx
    log_nginx_stats(mongo_collection)
