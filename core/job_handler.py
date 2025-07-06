import time
from typing import Dict, List, Any

def handle_print_message(payload: Dict[str,str]):
    print(f"📝 {payload['message']}")
    time.sleep(1)

def handle_add(payload: Dict[str,int]):
    result = 0
    values = []
    for key, val in payload.items():
        result += val
        values.append(str(val))

    if len(values) == 1:
        values.append("0")
    calculation = " + ".join(values)
    print(f"➕ {calculation} = {result}")
    time.sleep(1)

def handle_reverse_string(payload: Dict[str,str]):
    text = payload["text"]
    reversed_text = (payload["text"][::-1])
    print(f"🔁 {text} → {reversed_text}")
    time.sleep(1)

def get_handler(job_type: str):
    handler = {
        "print_message": handle_print_message,
        "add": handle_add,
        "reverse_string": handle_reverse_string
    }
    return handler.get(job_type)


