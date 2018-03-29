# -*- coding:utf-8 -*-

import os
import sys
import logging

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


CMD_RESULT = {
    "name":"cmd_result",
    "path":os.path.join(BASE_DIR,"log","cmd_result"),
}



LOG_LEVEL = logging.INFO
LOG_TYPES = {
    "cmd_history":"cmd_history.log",
    'system': 'system.log',
}