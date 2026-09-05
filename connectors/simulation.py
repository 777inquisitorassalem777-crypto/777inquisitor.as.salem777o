class SimulationConnector:
    """
    Safe robotics/game/sensor connector.
    Exposes state and simulation events, not weapon control.
    """
    def __init__(self):
        self.state = {"x": 0.0, "y": 0.0, "battery": 1.0}

    def observe(self):
        return self.state.copy()

    def step(self, action):
        allowed = {"move", "stop", "inspect", "rescue_simulation"}
        if action.get("type") not in allowed:
            return {"accepted": False, "reason": "unsupported simulation action"}
        return {"accepted": True, "action": action}
