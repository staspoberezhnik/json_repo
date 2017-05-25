from flask import Response, Flask, render_template, redirect, send_from_directory, make_response
from flask import request
import os
import shelve
from .utils import protect_name
DB_FILE_NAME = 'shelve_lib'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'D:/stas/pycode/proj 2/media'


def get_project_info():
    if request.method == 'GET':

        return render_template('base.html')


def get_storage_stat():
    if request.method == 'GET':
        with shelve.open(DB_FILE_NAME) as db:

            return render_template('upload.html', db=db)


def download_file():

    if request.method == 'GET':
        return render_template('update.html')

    elif request.method == 'POST':

        file = request.files['file_name']
        protected_filename = protect_name(file.filename)
        resp_data = [{'filename': file.filename,
                      'protected_name': protected_filename}]

        filepath = os.path.join('media', protected_filename)
        file.save(filepath)

        with shelve.open(DB_FILE_NAME) as db:

            if request.form['tag'] in db:
                db[request.form['tag']] += resp_data
            else:
                db[request.form['tag']] = resp_data
        return redirect('/storage/files/')


def upload_files(tag):

    if request.method == 'GET':
        with shelve.open(DB_FILE_NAME) as db:
            if tag not in db:
                tag_files = []
            else:
                tag_files = db[tag]
        return render_template('files_by_tag.html',
                               files_list=tag_files, tag=tag)


def update_file(tag, filename):
    if request.method == 'GET':
        with shelve.open(DB_FILE_NAME) as db:
            if tag not in db:
                tags = False
            else:
                tags = tag
            file_name = False
            protected_filename = False

            for file in db[tag]:
                if file['filename'] == filename:

                    file_name = filename
                    protected_filename = file['protected_name']
                    break

        return render_template('update_by_tag.html',
                               tag=tags, filename=file_name, protectedname=protected_filename)
    elif request.method == 'POST':

        # print(request.form['protected_filename'])

        return redirect('/storage/stat/')


def return_file(filename):
    response = make_response(send_from_directory(app.config['UPLOAD_FOLDER'], filename))
    response.headers['Content-Disposition'] = "attachment; filename=%s" % filename

    return response


    # print(filename)
    # return send_from_directory('/media', filename)
