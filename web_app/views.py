from flask import Flask, render_template, redirect, send_from_directory
from flask import request
import unidecode
from werkzeug.exceptions import NotFound
import os
import shelve
from .utils import protect_name
DB_FILE_NAME = 'shelve_lib'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(
    os.path.dirname(__file__), os.path.pardir, 'media')


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

        filepath = os.path.join(app.config['UPLOAD_FOLDER'],
                                protected_filename)
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
            old_tag = False
            protected_filename = False
            file_name = False
            if tag in db:
                old_tag = tag
            else:
                raise NotFound
            for file in db[old_tag]:
                if file['filename'] == filename:
                    file_name = filename
                    protected_filename = file['protected_name']
                    break

            else:
                raise NotFound
        return render_template('update_by_tag.html',
                               oldtag=old_tag,
                               filename=file_name,
                               protectedname=protected_filename)
    elif request.method == 'POST':
        with shelve.open(DB_FILE_NAME) as db:
            counter = -1
            resp_data = [{'filename': request.form['file_name'],
                          'protected_name': request.form['protect_name']}]
            old_tag = request.form['old_tag']
            new_tag = request.form['tag']

            if new_tag in db:
                for files in db[new_tag]:
                    if (files['filename'] == request.form['file_name'] and
                            files['protected_name'] == request.form[
                                                    'protect_name']):
                        return redirect('/storage/stat/')
                else:
                    db[new_tag] += resp_data
            else:
                db[new_tag] = resp_data

            for files in db[old_tag]:
                counter += 1
                if (files['filename'] == request.form['file_name']
                    and files['protected_name'] == request.form[
                            'protect_name']):
                    break
            db[old_tag] = db[old_tag][:counter:] + db[old_tag][counter + 1::]

            if len(db[old_tag]) == 0:
                db.pop(old_tag)
            return redirect('/storage/files/{0}/{1}/'.format(
                                                new_tag,
                                                request.form['file_name']))


def return_file(filename):

    return send_from_directory(
        app.config['UPLOAD_FOLDER'],
        filename,
        as_attachment=True,
        attachment_filename=unidecode.unidecode(filename))
