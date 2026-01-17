import hashlib
import time
from typing import Any

def merkle_hash(data: Any) -> str:
    """
    Simple hash for append-only logging
    """
    serialized = str(data).encode("utf-8")
    return hashlib.sha256(serialized).hexdigest()

def timestamp() -> float:
    return time.time()

def priority_score(material_score: float, scope: int, irreversible: bool) -> float:
    """
    Compute v9.5 priority for triage
    """
    return (10 if irreversible else 1) * scope * material_score

def chunk_list(lst: list, n: int):
    """
    Yield successive n-sized chunks from list
    """
    for i in range(0, len(lst), n):
        yield lst[i:i + n]
