class Cart:

    def __init__(self, session_state):
        self.session_state = session_state
        if "cart" not in self.session_state:
            self.session_state.cart = []
            
    def clear(self):
        self.session_state.cart = []