import imp
import sys
import os
import subprocess
# comment added
#TODO:
#1)download all python packages
#2)Create emypty storage if it need it
#3)Create database file to track changes


def download_dependences():
    # check if dependencies not installed->install it
    # try:
    #     imp.find_module('flask')
    # except ImportError:
    #     print('Module flask not found')
    subprocess.run(['pip', 'install', 'flask'])


def initialize_env():
    #create directory, where we will save storage
    #create db file->shelve lib
    # print(os.getcwd())
    #print(os.path.exists('tests'))
    if not os.path.exists('media'):
        #print('Media is already created')
        os.mkdir('media')
        print('creating directory media')
        open('D:\\stas\\pycode\\proj 2\\media\\shelve_lib.db.txt', 'w')



def run_application():
    from web_app import application
    application.app.run()


if __name__ == "__main__":
    download_dependences()
    initialize_env()
    run_application()
