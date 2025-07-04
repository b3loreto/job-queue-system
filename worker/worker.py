import redis
import time
import json

r = redis.Redis(host='localhost', port='6379', db='0')

def process_job(job):
    job_type = job['name']
