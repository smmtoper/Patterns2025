from datetime import datetime

class log_event:
    def __init__(self, category, message):
        self.category = category
        self.message = message
        self.time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
