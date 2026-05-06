class SessionManager:

    def __init__(self, session_state):
        self.state = session_state

    def logout(self):
        for key in list(self.state.keys()):
            del self.state[key]