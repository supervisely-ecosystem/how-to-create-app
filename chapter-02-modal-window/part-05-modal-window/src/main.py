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


print(f'Hello modal world!')

