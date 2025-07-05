import redis
import json
import time
import logging
import sys
import os

# Add the project root to Python path so we can import from the core module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import our custom job handler function that processes different job types
from core.job_handler import get_handler

# Initialize Redis connection to localhost on default port 6379, database 0
r = redis.Redis(host="localhost", port=6379, db=0)

# Configure logging to write to a file with timestamp, log level, and message format
logging.basicConfig(
    filename="logs/job_worker.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def run_worker():
    """
    Main worker function that continuously processes jobs from the Redis queue.
    Runs in an infinite loop, waiting for new jobs to arrive and processing them.
    """
    print("🚀 Worker started ")
    while True:
        # Block and wait for a job from the queue (BLPOP = Blocking Left POP)
        # Returns a tuple: (key_name, job_data) - we only need the job_data
        _, job_data = r.blpop("job_queue")
        
        # Parse the JSON job data into a Python dictionary
        job = json.loads(job_data)
        
        # Extract job details from the parsed data
        job_id = job["id"]          # Unique identifier for the job
        job_type = job["type"]      # Type of job (e.g., "print_message", "add")
        payload = job["payload"]    # Job-specific data/parameters

        try:
            # Get the appropriate handler function for this job type
            handler = get_handler(job_type)
            
            # If no handler found for this job type, raise an error
            if not handler:
                raise ValueError(f"Unknown job type: {job_type}")
            
            # Execute the job handler with the payload
            handler(payload)
            
            # Mark job as completed in Redis status hash
            r.hset("job_status", job["id"], "completed")
            logging.info(f"✅ Completed job {job_id}")
            
        except Exception as e:
            # Log the error that occurred during job processing
            logging.error(f"❌ Failed job {job_id}: {e}")
            
            # Get current retry count (default to 0 if not set)
            retries = int(job.get("retries", 0))
            
            # If we haven't exceeded maximum retries (3), retry the job
            if retries < 3:
                # Increment retry count
                job["retries"] = retries + 1
                # Put job back in queue for retry (RPUSH = Right PUSH to end of queue)
                r.rpush("job_queue", json.dumps(job))
                logging.warning(f"🔁 Retrying job {job_id} (attempt {retries+1})")
            else:
                # Maximum retries exceeded, mark job as failed
                r.hset("job_status", job_id, "failed")

# Worker script is executed directly (not imported as a module)
if __name__ == "__main__":
    run_worker()