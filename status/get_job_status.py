import redis
import sys

r = redis.Redis(host='localhost',port=6379, db=0)

def get_status(job_id: str):
    status = r.hget("job_status", job_id)
    if status:
        print(f"🧾 Job {job_id} status: {status})")
    else:
        print("⚠️ Job not found.")

if __name__ == "__main__":
    job_id = sys.argv[1]
    get_status(job_id)