import redis
import json
import time
import logging
import sys
import os

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.job_handler import get_handler

r = redis.Redis(host="localhost", port=6379, db=0)

logging.basicConfig(
    filename="logs/job_worker.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def run_worker():
    print("🚀 Worker started ")
    while True:
        _, job_data = r.blpop("job_queue")
        job = json.loads(job_data)
        job_id = job["id"]
        job_type = job["type"]
        payload = job["payload"]

        try:
            handler = get_handler(job_type)
            if not handler:
                raise ValueError(f"Unknown job type: {job_type}")
            handler(payload)
            r.hset("job_status", job["id"], "completed")
            logging.info(f"✅ Completed job {job_id}")
        except Exception as e:
            logging.error(f"❌ Failed job {job_id}: {e}")
            retries = int(job.get("retries", 0))
            if retries < 3:
                job["retries"] = retries + 1
                r.rpush("job_queue", json.dumps(job))
                logging.warning(f"🔁 Retrying job {job_id} (attempt {retries+1})")
            else:
                r.hset("job_status", job_id, "failed")

if __name__ == "__main__":
    run_worker()