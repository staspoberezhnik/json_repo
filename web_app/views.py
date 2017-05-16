from flask import Response
from flask import request


def get_project_info():
    response_text = "<b>Hi. It's simple json repository based on Flask. Enjoy it.</b>"
    return Response(response=response_text,
                    status=200)


def get_storage_stat():
    return Response(response=[{'<path_to_file>:<tag>'}],
                    status=200,
                    mimetype="application/json")


def download_file(tag):
    #get file_content from request_obj
    print(request)
    return Response(response="should be opened dialog to download file",
                    status=200)


def upload_files(tag):
    return Response(response="should upload file or files with specific tag")


def update_file(tag):
    #get file_content from request_obj
    return Response(response="should update file by specific tag")
