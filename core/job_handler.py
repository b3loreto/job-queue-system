import time

def handle_print_message(payload):
    print(f"📝 {payload["message"]}")
    time.sleep(1)

def handle_add(payload):
    result = payload["a"] + payload["b"]
    print(f"➕ {payload["a"]} + {payload["b"]} = {result}")
    time.sleep(1)

def handle_reverse_string(payload):
    print(payload["text"][::-1])
    time.sleep(1)

def get_handler(job_type):
    handler = {
        "print_message": handle_print_message,
        "add": handle_add,
        "reverse_string": handle_reverse_string
    }
    return handler.get(job_type)


