import uuid
from src import common

logger = common.Logger(log_file_name=uuid.uuid4(), log_mode='a')

