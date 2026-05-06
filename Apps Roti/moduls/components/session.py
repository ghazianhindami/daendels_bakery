class SessionManager:

    def __init__(self, session_state):
        self.state = session_state

    def logout(self):
        keys = [
            "self_service", "user", "full_name",
            "role", "branch_id", "branch_name"
        ]
        for k in keys:
            self.state[k] = None

