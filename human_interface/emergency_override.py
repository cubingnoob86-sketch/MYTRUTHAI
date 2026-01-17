from typing import Callable

class EmergencyOverride:
    """
    Allows human intervention for emergency bypasses or shutdown.
    """
    def __init__(self):
        self.override_enabled: bool = False
        self.kill_switch_engaged: bool = False
        self.override_log: list[dict] = []

    def enable_override(self, reason: str, actor: str):
        if self.kill_switch_engaged:
            return {"status": "error", "message": "Kill switch engaged; override blocked"}
        self.override_enabled = True
        self.override_log.append({"action": "enable", "reason": reason, "actor": actor})
        return {"status": "success", "message": "Override enabled"}

    def disable_override(self, actor: str):
        self.override_enabled = False
        self.override_log.append({"action": "disable", "actor": actor})
        return {"status": "success", "message": "Override disabled"}

    def engage_kill_switch(self, actor: str):
        self.kill_switch_engaged = True
        self.override_enabled = False
        self.override_log.append({"action": "kill_switch", "actor": actor})
        return {"status": "success", "message": "Kill switch engaged"}
