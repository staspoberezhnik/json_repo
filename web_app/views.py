from flask import Response, Flask, render_template, redirect
from flask import request
import os
import shelve
from .utils import protect_name


def get_project_info():
    if request.method == 'GET':
        return render_template('base.html')


def get_storage_stat():
    if request.method == 'GET':
        with shelve.open('shelve_lib') as db:

            return render_template('upload.html', db=db)


def download_file():

    if request.method == 'GET':
        return render_template('update.html')

    elif request.method == 'POST':

        file = request.files['file_name']
        protected_filename = protect_name(file.filename)
        resp_data = [{'filename': file.filename,
                      'protected_name': protected_filename}]

        filepath = os.path.join('media', file.filename)
        file.save(filepath)

        with shelve.open('shelve_lib') as db:
            if request.form['tag'] in db:
                db[request.form['tag']] += resp_data
            else:
                db[request.form['tag']] = resp_data

        return redirect('/storage/files/')


def upload_files(tag):

    if request.method == 'GET':
        with shelve.open('shelve_lib') as db:
            if tag not in db:
                tag_files = []
            else:
                tag_files = db[tag][::2]
        return render_template('files_by_tag.html',
                               files_list=tag_files, tag=tag)


def update_file(tag, filename):
    if request.method == 'GET':
        with shelve.open('shelve_lib') as db:
            if tag not in db:
                tags = False
            else:
                tags = tag

        return render_template('update_by_tag.html',
                               tag=tags, filename=filename)
    elif request.method == 'PATCH':
        return render_template()
