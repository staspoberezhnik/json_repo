import os
import subprocess
# TODO:
# 1)download all python packages
# 2)Create emypty storage if it need it
# 3)Create database file to track changes


def download_dependences():
    subprocess.run(['pip', 'install', '-r', 'requirements.txt'])


def initialize_env():
    if not os.path.exists('media'):
        os.mkdir('media')
        print('creating directory media')
    pass


def run_application():
    from web_app import application
    application.app.run()


if __name__ == "__main__":
    download_dependences()
    initialize_env()
    run_application()
