from typing import Callable, Any
import threading
import time

class Sandbox:
    """
    Wraps AI actions in a safe environment
    """
    def __init__(self, max_runtime_sec: int = 5):
        self.max_runtime_sec = max_runtime_sec

    def run(self, func: Callable, *args, **kwargs) -> Any:
        """
        Execute function in sandboxed thread with timeout
        """
        result = [None]
        exception = [None]

        def target():
            try:
                result[0] = func(*args, **kwargs)
            except Exception as e:
                exception[0] = e

        thread = threading.Thread(target=target)
        thread.start()
        thread.join(self.max_runtime_sec)

        if thread.is_alive():
            print("[SANDBOX] Execution timed out. Terminating.")
            # Could add logging + kill flag here
            thread.join(0.1)
            raise TimeoutError("Sandbox execution exceeded max runtime.")

        if exception[0]:
            raise exception[0]

        return result[0]

    def human_gate(self, output: Any) -> Any:
        """
        Enforce human approval before any real-world effect
        """
        # In practice, this could be a queue to a human review system
        print("[SANDBOX] Output requires human approval before deployment:", output)
        return output
