import redis
import json
import uuid
from time import time

# connect to redis server
r = redis.Redis(host='localhost', port='6379', db='0')

# submit a job to the queue
def submit_job(job_type, payload):
    # create a job object
    job = {
        'id': str(uuid.uuid4()),
        'type': job_type,           # 'test_job_name'
        'payload': payload,         # 'message': 'hello from Ben'
        'status': 'pending',        # 'pending', 'completed', 'failed'
        'created_at': time()        # timestamp in seconds
    }
    # push the job to the queue (list)
    r.hset("job_status", job["id"], "pending")
    r.rpush('job_queue', json.dumps(job))
    print(f"Job {job['id']} submitted successfully")

if __name__ == "__main__":
    payload = { 'message': 'hello from Ben' }
    submit_job('print_message', payload)

# job_queue: [job1, job2, job3]

# job1: 
# {
# "id": "58a04186-beb6-424c-bc18-00262dc01b35", 
# "type": "test_job_type",
# "payload": {"message": "hello from Ben"},
#  "status": "pending",
#  "created_at": 1751657076.7396019
# }



