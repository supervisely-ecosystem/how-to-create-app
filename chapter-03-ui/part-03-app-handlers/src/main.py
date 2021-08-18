import supervisely_lib as sly
from dotenv import load_dotenv  # pip install python-dotenv
                                # don't forget to add to requirements.txt!

load_dotenv("../debug.env")
load_dotenv("../secret_debug.env", override=True)

app = sly.AppService()
logger = sly.logger


@app.callback('normal_handler')
def normal_handler(api: sly.Api, task_id, context, state, app_logger):
    logger.info('normal handler called')


@app.callback('error_handler')
@app.ignore_errors_and_show_dialog_window()
def error_handler(api: sly.Api, task_id, context, state, app_logger):
    logger.info('normal handler called')
    raise SystemError('there could be an error message here')


def main():
    logger.info('Application starting...')
    app.run()


if __name__ == "__main__":
    sly.main_wrapper("main", main)
