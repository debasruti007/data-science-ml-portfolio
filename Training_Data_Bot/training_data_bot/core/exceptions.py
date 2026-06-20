class TrainingDataBotError(Exception):
    pass

class ConfigurationError(TrainingDataBotError):
    pass

class DocumentLoadError(TrainingDataBotError):
    def __init__(self, message, file_path=None, cause=None):
        super().__init__(message)
        self.file_path = file_path
        self.cause = cause