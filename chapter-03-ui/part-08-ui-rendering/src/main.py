import supervisely_lib as sly
from dotenv import load_dotenv  # pip install python-dotenv
                                # don't forget to add to requirements.txt!

load_dotenv("../debug.env")
load_dotenv("../secret_debug.env", override=True)

app = sly.AppService()


def main():
    sly.logger.info('Application starting...')
    app.run()


if __name__ == "__main__":
    sly.main_wrapper("main", main)
