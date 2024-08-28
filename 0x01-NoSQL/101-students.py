#!/usr/bin/env python3
"""
101-students.py
"""


def top_students(mongo_collection):
    """Python function that returns all students sorted by average score"""
    if not mongo_collection:
        return []
    docs = mongo_collection.find()
    my_list = [doc for doc in docs]
    for ele in my_list:
        scores = [topic['score'] for topic in ele['topics']]
        average = sum(scores) / len(scores)
        ele['averageScore'] = average
    return sorted(my_list, key=lambda student: student['averageScore'], reverse=True)
