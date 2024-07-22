import logging
import logging.handlers

app_logger = logging.getLogger('tummytime')

def setup_logger():
    
    app_logger.setLevel(logging.DEBUG)
    
    #Shared handler
    handler = logging.handlers.RotatingFileHandler(
        filename='tummy.log',
        encoding='utf-8',
        maxBytes=32 * 1024 * 1024,  # 32 MiB
        backupCount=5,  # Rotate through 5 files
    )
    
    dt_fmt = '%Y-%m-%d %H:%M:%S'
    formatter = logging.Formatter('[{asctime}] [{levelname:<8}] {name}: {message}', dt_fmt, style='{')
    handler.setFormatter(formatter)
    
    #Discord logger
    discord_logger = logging.getLogger('discord')
    discord_logger.setLevel(logging.INFO)
    
    #SQLAlchemy logger
    sql_logger = logging.getLogger('sqlalchemy.engine')
    sql_logger.setLevel(logging.INFO)

    sql_logger.addHandler(handler)
    discord_logger.addHandler(handler)
    app_logger.addHandler(handler)
