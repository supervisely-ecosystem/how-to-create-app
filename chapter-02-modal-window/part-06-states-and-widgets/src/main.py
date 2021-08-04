import supervisely_lib as sly
import time

import os
from dotenv import load_dotenv  # pip install python-dotenv
                                # don't forget to add to requirements.txt!

# Loading env files
load_dotenv("../debug.env")
load_dotenv("../secret_debug.env", override=True)

# Extracting variables
address = os.environ['SERVER_ADDRESS']
token = os.environ['API_TOKEN']

team_id = int(os.environ['context.teamId'])
workspace_id = int(os.environ['context.workspaceId'])

# Extracting world name from modal window
timer_value = int(os.environ['modal.state.timerValue'])


sly_logger = sly.logger
starting_time = time.time()

while time.time() - starting_time < timer_value:
    sly_logger.info(f'Time left {timer_value - (time.time() - starting_time)}')
    time.sleep(1)

sly_logger.warning(f'The timer has rang! DZZZZ')





