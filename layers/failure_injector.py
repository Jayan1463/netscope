import time
import random

def inject_delay(enabled: bool, delay_ms: int):
    if enabled:
        time.sleep(delay_ms / 1000)

def inject_failure(enabled: bool, probability=0.3):
    if enabled and random.random() < probability:
        raise RuntimeError("Simulated failure injected")
