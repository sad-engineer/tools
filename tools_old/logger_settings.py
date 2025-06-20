from service_for_my_projects.logger_settings import config

config['loggers'] = {
    'Finder': {'handlers': ['consoleHandler', 'fileHandler'], 'level': 'DEBUG', 'propagate': False},
    # INFO - выводить все сообщения,
    # ERROR - ошибки создания имени инструмента,
    # CRITICAL - отключить ошибки создания имени инструмента,
    'tool_names': {'handlers': ['consoleHandler', 'fileHandler'], 'level': 'CRITICAL', 'propagate': False},
}
