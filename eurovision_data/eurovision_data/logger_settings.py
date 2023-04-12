class LoggerSettings:

    log_location = ''

    def __init__(self, location):
        self.log_location = location

    def get_location(self):
        return self.log_location

    def set_location(self, location):
        self.log_location = location

    def get_logger_settings(self):
        log_settings = {
            'version': 1,
            'disable_existing_loggers': False,

            # The root logger is apparently special in Django, and needs to be higher up than the usual loggers.
            'root': {
                'handlers': ['debug_file', 'errors_file', 'info_file', 'console'],
                # 'handlers': ['debug_file', 'errors_file', 'info_file'],
                # the logger needs to have a level but it doesn't do anything, the level parameter in
                # the handler is what determines what logger level gets written in what log.
                'level': 'DEBUG',
            },
            'formatters': {
                'large': {
                    'format': '%(asctime)s - %(name)s.%(funcName)s.%(lineno)d - %(levelname)s - %(message)ss'
                },
                'tiny': {
                    # 'format': '%(asctime)s  %(message)s'
                    'format': '%(asctime)s  %(module)s  %(message)s'
                }
            },
            'handlers': {
                'errors_file': {
                    'level': 'ERROR',
                    'class': 'logging.handlers.TimedRotatingFileHandler',
                    'when': 'midnight',
                    'interval': 1,
                    'filename': self.log_location + '/ErrorLog.log',
                    'formatter': 'large',
                },
                'info_file': {
                    'level': 'INFO',
                    'class': 'logging.handlers.TimedRotatingFileHandler',
                    'when': 'midnight',
                    'interval': 1,
                    'filename': self.log_location + '/InfoLog.log',
                    'formatter': 'large',
                },
                'debug_file': {
                    'level': 'DEBUG',
                    'class': 'logging.handlers.TimedRotatingFileHandler',
                    'when': 'midnight',
                    'interval': 1,
                    'filename': self.log_location + '/DebugLog.log',
                    'formatter': 'large',
                },
                'console': {
                    'level': 'DEBUG',
                    'class': 'logging.StreamHandler',
                    'formatter': 'tiny',
                },
            },
            'loggers': {
                # '': {
                #     'handlers': ['debug_file', 'errors_file', 'info_file', 'console'],
                #     # 'handlers': ['debug_file', 'errors_file', 'info_file'],
                #     # the logger needs to have a level but it doesn't do anything, the level parameter in
                #     # the handler is what determines what logger level gets written in what log.
                #     'level': 'DEBUG',
                # },

            },
        }

        return log_settings
