import redis
import time
import json

r = redis.Redis(host='localhost', port='6379', db='0')

def process_job(job):
    job_type = job["type"]
    if job_type == 'print_message':
        print(f"🛠️ Job {job['id']}: {job['payload']['message']}")
        time.sleep(2)
    else:
        print(f"❌ Unknown job type: {job_type}")

def run_worker():
    print("🚀 Worker started ")
    while True:
        _, job_data = r.blpop("job_queue")
        job = json.loads(job_data)
        process_job(job)
        r.hset("job_status", job["id"], "completed")
        print(f"✅ Job {job['id']} marked complete")

if __name__ == "__main__":
    run_worker()

