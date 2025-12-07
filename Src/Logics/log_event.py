from datetime import datetime

class log_event:
    def __init__(self, category: str, message: str):
        self.category = category
        self.message = message
        self.time = datetime.now()
