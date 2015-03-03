import os
import dotenv

PROJECT_PATH = os.path.dirname(os.path.dirname(__file__))

dotenv.load_dotenv(os.path.join(PROJECT_PATH, ".env"))
dotenv.load_dotenv(os.path.join(PROJECT_PATH, ".env_defaults"))

from disparity.settings import *  # NOQA
