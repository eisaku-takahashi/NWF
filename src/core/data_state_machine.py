class DataStateMachine:
    def __init__(self):
        self.current_state = "IDLE"
    def transition_to(self, new_state: str):
        self.current_state = new_state
        return True
