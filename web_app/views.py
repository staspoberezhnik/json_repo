from flask import Response, Flask, render_template, redirect
from flask import request
import os
import shelve


def get_project_info():
    if request.method == 'GET':

        # response_text = "<b>Hi. It's simple json repository based on Flask. Enjoy it.</b>"
        return render_template('base.html')


def get_storage_stat():
    if request.method == 'GET':
        with shelve.open('shelve_lib') as db:
            base = db
        # return Response(response=[{'<path_to_file>:<tag>'}],
        #             status=200,
        #             mimetype="application/json")
            return render_template('upload.html', db=base, status=200)


def download_file():
    # get file_content from request_obj
    if request.method == 'GET':
        return render_template('update.html')
        # print(request)
        # return Response(response="should be opened dialog to download file",
        #             status=200)
    elif request.method == 'POST':
        print(request.form)

        file = request.files['file_name']
        key = file.filename
        print(file.filename)
        filepath = os.path.join('media', file.filename)
        file.save(filepath)
        print(request.form['tag'])

        with shelve.open('shelve_lib') as db:
            # db[str(request.form['filename'])] = request.form['tag']
            db.update([(key, request.form['tag'])])
        with shelve.open('shelve_lib') as db:
            for val in db.values():
                print(val)

        return redirect('/storage/files/')


def upload_files(tag):
    # return Response(response="should upload file or files with specific tag")
    pass

def update_file(tag):
    if request.method == 'GET':
        return render_template('update.html')
    elif request.method == 'PUT':
        # get file_content from request_obj
        # return Response(response="should update file by specific tag")
        return render_template()
