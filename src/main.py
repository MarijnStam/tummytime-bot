from log import setup_logger, app_logger
from db_helper import create_db
from version import *
from discord_bot import start_bot

def main():
    setup_logger()
    app_logger.info(f"Starting tummytime-bot V{APP_VERSION_MAJOR}.{APP_VERSION_MINOR}")
    create_db()
    start_bot()
    
if __name__ == "__main__":
    main()