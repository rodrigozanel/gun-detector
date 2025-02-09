class NotificationDTO:
    def __init__(self, label, file_path, current_time, precision=None):
        self.label = label
        self.file_path = file_path
        self.current_time = current_time,
        self.precision = precision

    # add getter and setter methods
    def get_label(self):
        return self.label
    
    def get_file_path(self):
        return self.file_path
    
    def get_current_time(self):
        return self.current_time

    def get_precision(self):
        return self.precision
    
