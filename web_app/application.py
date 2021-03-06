from flask import Flask

app = Flask(__name__)
app.debug = True


def _init_routes(web_app):
    from . import views
    web_app.add_url_rule('/',
                         methods=['GET'],
                         view_func=views.get_project_info)
    web_app.add_url_rule('/storage/stat/',
                         methods=['GET'],
                         view_func=views.get_storage_stat)
    web_app.add_url_rule('/storage/files/',
                         methods=['GET', 'POST'],
                         view_func=views.download_file)
    web_app.add_url_rule('/storage/files/<tag>/',
                         methods=['GET', 'POST'],
                         view_func=views.upload_files)
    web_app.add_url_rule('/storage/files/<tag>/<filename>/',
                         methods=['GET', 'POST'],
                         view_func=views.update_file)
    web_app.add_url_rule('/storage/return/<filename>/', methods=['GET'],
                         view_func=views.return_file)


_init_routes(app)
