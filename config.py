import logging
import os

BOT_ROOT = os.getcwd()
BACKEND = 'Text'  # Errbot will start in text mode

BOT_DATA_DIR = os.path.join(BOT_ROOT, 'errbot_data')
BOT_EXTRA_PLUGIN_DIR = os.path.join(BOT_ROOT, 'plugins')
BOT_LOG_FILE = os.path.join(BOT_ROOT, 'errbot.log')
BOT_LOG_LEVEL = logging.DEBUG

BOT_ADMINS = ('@CHANGE_ME', )
