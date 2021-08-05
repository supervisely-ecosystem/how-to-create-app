import supervisely_lib as sly
import time
from dotenv import load_dotenv  # pip install python-dotenv

# don't forget to add to requirements.txt!

load_dotenv("../debug.env")
load_dotenv("../secret_debug.env", override=True)

app = sly.AppService()
app_api = app.public_api
logger = sly.logger


@app.callback('start_timer')
def start_timer(api: sly.Api, task_id, context, state, app_logger):
    timer_value = app_api.app.get_field(task_id=task_id,
                                        field='state.timerValue')  # getting field
    app_api.app.set_field(task_id=task_id,
                          field='state.timerStarted',
                          payload=True)  # setting field

    starting_time = time.time()

    while time.time() - starting_time < timer_value:
        time_left = timer_value - (time.time() - starting_time)
        app_api.app.set_field(task_id=task_id,
                              field='data.timeLeft',
                              payload=time_left)
        time.sleep(1)

    app_api.app.set_field(task_id=task_id,
                          field='data.timeLeft',
                          payload=0)


def main():
    state = {}
    data = {}

    # initialize required fields here
    state['timerValue'] = 0
    data['timeLeft'] = None

    app.run(data=data, state=state)

    logger.info('Application starting...')
    app.run()


if __name__ == "__main__":
    sly.main_wrapper("main", main)
