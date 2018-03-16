import mimetypes
import os

from flask import redirect, render_template, jsonify
from flask_login import login_required, current_user, current_app
from flask import make_response
from flask import send_file, url_for
from flask_restful.reqparse import RequestParser

from compair.core import event
on_get_file = event.signal('GET_FILE')

attachment_download_parser = RequestParser()
attachment_download_parser.add_argument('name', default=None)

def register_api_blueprints(app):
    # Initialize rest of the api modules
    from .course import course_api
    app.register_blueprint(
        course_api,
        url_prefix='/api/courses')

    from .classlist import classlist_api
    app.register_blueprint(
        classlist_api,
        url_prefix='/api/courses/<course_uuid>/users')

    from .course_group import course_group_api
    app.register_blueprint(
        course_group_api,
        url_prefix='/api/courses/<course_uuid>/groups')

    from .course_group_user import course_group_user_api
    app.register_blueprint(
        course_group_user_api,
        url_prefix='/api/courses/<course_uuid>/users')

    from .login import login_api
    app.register_blueprint(login_api)

    from .lti_launch import lti_api
    app.register_blueprint(
        lti_api,
        url_prefix='/api/lti')

    from .lti_course import lti_course_api
    app.register_blueprint(
        lti_course_api,
        url_prefix='/api/lti/course')

    from .lti_consumers import lti_consumer_api
    app.register_blueprint(
        lti_consumer_api,
        url_prefix='/api/lti/consumers')

    from .users import user_api
    app.register_blueprint(
        user_api,
        url_prefix='/api/users')

    from .assignment import assignment_api
    app.register_blueprint(
        assignment_api,
        url_prefix='/api/courses/<course_uuid>/assignments')

    from .answer import answers_api
    app.register_blueprint(
        answers_api,
        url_prefix='/api/courses/<course_uuid>/assignments/<assignment_uuid>/answers')

    from .file import file_api
    app.register_blueprint(
        file_api,
        url_prefix='/api/attachment')

    from .assignment_comment import assignment_comment_api
    app.register_blueprint(
        assignment_comment_api,
        url_prefix='/api/courses/<course_uuid>/assignments/<assignment_uuid>/comments')

    from .answer_comment import answer_comment_api
    app.register_blueprint(
        answer_comment_api,
        url_prefix='/api/courses/<course_uuid>/assignments/<assignment_uuid>')

    from .criterion import criterion_api
    app.register_blueprint(
        criterion_api,
        url_prefix='/api/criteria')

    from .comparison import comparison_api
    app.register_blueprint(
        comparison_api,
        url_prefix='/api/courses/<course_uuid>/assignments/<assignment_uuid>/comparisons')

    from .comparison_example import comparison_example_api
    app.register_blueprint(
        comparison_example_api,
        url_prefix='/api/courses/<course_uuid>/assignments/<assignment_uuid>/comparisons/examples')

    from .report import report_api
    app.register_blueprint(
        report_api,
        url_prefix='/api/courses/<course_uuid>/report')

    from .gradebook import gradebook_api
    app.register_blueprint(
        gradebook_api,
        url_prefix='/api/courses/<course_uuid>/assignments/<assignment_uuid>/gradebook')

    from .common import timer_api
    app.register_blueprint(
        timer_api,
        url_prefix='/api/timer')

    from .healthz import healthz_api
    app.register_blueprint(healthz_api)

    @app.route('/app/')
    def route_app():
        if app.debug or app.config.get('TESTING', False):
            return render_template(
                'index-dev.html',
                ga_tracking_id=app.config['GA_TRACKING_ID'],
                attachment_extensions=list(app.config['ATTACHMENT_ALLOWED_EXTENSIONS']),
                attachment_upload_limit=app.config['ATTACHMENT_UPLOAD_LIMIT'],
                app_login_enabled=app.config['APP_LOGIN_ENABLED'],
                cas_login_enabled=app.config['CAS_LOGIN_ENABLED'],
                lti_login_enabled=app.config['LTI_LOGIN_ENABLED'],
                kaltura_enabled=app.config['KALTURA_ENABLED'],
                kaltura_extensions=list(app.config['KALTURA_ATTACHMENT_EXTENSIONS']),
                expose_email_to_instructor=app.config['EXPOSE_EMAIL_TO_INSTRUCTOR'],
                allow_student_change_name=app.config['ALLOW_STUDENT_CHANGE_NAME'],
                allow_student_change_display_name=app.config['ALLOW_STUDENT_CHANGE_DISPLAY_NAME'],
                allow_student_change_student_number=app.config['ALLOW_STUDENT_CHANGE_STUDENT_NUMBER'],
                allow_student_change_email=app.config['ALLOW_STUDENT_CHANGE_EMAIL'],
                notifications_enabled=app.config['MAIL_NOTIFICATION_ENABLED'],
                xapi_enabled=app.config['XAPI_ENABLED'],
                xapi_app_base_url=app.config.get('XAPI_APP_BASE_URL'),
                demo=app.config.get('DEMO_INSTALLATION'),
            )

        # running in prod mode, figure out asset location
        assets = app.config['ASSETS']
        prefix = app.config['ASSET_PREFIX']

        return render_template(
            'index.html',
            bower_js_libs=prefix + assets['bowerJsLibs.js'],
            compair_js=prefix + assets['compair.js'],
            compair_css=prefix + assets['compair.css'],
            static_img_path=prefix,
            ga_tracking_id=app.config['GA_TRACKING_ID'],
            attachment_extensions=list(app.config['ATTACHMENT_ALLOWED_EXTENSIONS']),
            attachment_upload_limit=app.config['ATTACHMENT_UPLOAD_LIMIT'],
            app_login_enabled=app.config['APP_LOGIN_ENABLED'],
            cas_login_enabled=app.config['CAS_LOGIN_ENABLED'],
            lti_login_enabled=app.config['LTI_LOGIN_ENABLED'],
            kaltura_enabled=app.config['KALTURA_ENABLED'],
            kaltura_extensions=list(app.config['KALTURA_ATTACHMENT_EXTENSIONS']),
            expose_email_to_instructor=app.config['EXPOSE_EMAIL_TO_INSTRUCTOR'],
            allow_student_change_name=app.config['ALLOW_STUDENT_CHANGE_NAME'],
            allow_student_change_display_name=app.config['ALLOW_STUDENT_CHANGE_DISPLAY_NAME'],
            allow_student_change_student_number=app.config['ALLOW_STUDENT_CHANGE_STUDENT_NUMBER'],
            allow_student_change_email=app.config['ALLOW_STUDENT_CHANGE_EMAIL'],
            notifications_enabled=app.config['MAIL_NOTIFICATION_ENABLED'],
            xapi_enabled=app.config['XAPI_ENABLED'],
            xapi_app_base_url=app.config.get('XAPI_APP_BASE_URL'),
            demo=app.config.get('DEMO_INSTALLATION'),
        )

    @app.route('/')
    def route_root():
        return redirect("/app/")

    @app.route('/app/pdf')
    def route_pdf_viewer():
        if app.debug or app.config.get('TESTING', False):
            return render_template(
                'pdf-viewer.html',
                pdf_lib_folder=url_for('static', filename='lib/pdf.js-viewer')
            )

        # running in prod mode, figure out asset location
        assets = app.config['ASSETS']
        prefix = app.config['ASSET_PREFIX']

        return render_template(
            'pdf-viewer.html',
            pdf_lib_folder=prefix + 'pdf.js-viewer'
        )

    @app.route('/app/<regex("attachment|report"):file_type>/<file_name>')
    @login_required
    def file_retrieve(file_type, file_name):
        file_dirs = {
            'attachment': app.config['ATTACHMENT_UPLOAD_FOLDER'],
            'report': app.config['REPORT_FOLDER']
        }
        file_path = '{}/{}'.format(file_dirs[file_type], file_name)

        if not os.path.exists(file_path):
            return make_response('invalid file name', 404)

        # TODO: add bouncer
        mimetype, encoding = mimetypes.guess_type(file_name)
        attachment_filename = None
        as_attachment = False

        if file_type == 'attachment' and mimetype != "application/pdf":
            params = attachment_download_parser.parse_args()
            attachment_filename = params.get('name') #optionally set the download file name
            as_attachment = True

        on_get_file.send(
            current_app._get_current_object(),
            event_name=on_get_file.name,
            user=current_user,
            file_type=file_type,
            file_name=file_name,
            data={'file_path': file_path, 'mimetype': mimetype})

        return send_file(file_path, mimetype=mimetype,
            attachment_filename=attachment_filename, as_attachment=as_attachment)

    return app

def register_statement_api_blueprints(app):
    from .statements import statement_api
    app.register_blueprint(
        statement_api,
        url_prefix='/api/statements')

    return app

def register_demo_api_blueprints(app):
    from .demo import demo_api
    app.register_blueprint(
        demo_api,
        url_prefix='/api/demo')

    return app

def log_events(log):
    # user events
    from .users import on_user_modified, on_user_get, on_user_list_get, on_user_create, on_user_course_get, \
        on_user_password_update, on_user_edit_button_get, on_teaching_course_get, on_user_notifications_update, \
        on_user_course_status_get, on_user_lti_users_get, on_user_lti_user_unlink, on_user_third_party_users_get, \
        on_user_third_party_user_delete
    on_user_modified.connect(log)
    on_user_get.connect(log)
    on_user_list_get.connect(log)
    on_user_create.connect(log)
    on_user_course_get.connect(log)
    on_teaching_course_get.connect(log)
    on_user_edit_button_get.connect(log)
    on_user_notifications_update.connect(log)
    on_user_password_update.connect(log)
    on_user_course_status_get.connect(log)
    on_user_lti_users_get.connect(log)
    on_user_lti_user_unlink.connect(log)
    on_user_third_party_users_get.connect(log)
    on_user_third_party_user_delete.connect(log)

    # course events
    from .course import on_course_modified, on_course_get, on_course_list_get, on_course_create, \
        on_course_delete, on_course_duplicate
    on_course_modified.connect(log)
    on_course_get.connect(log)
    on_course_delete.connect(log)
    on_course_list_get.connect(log)
    on_course_create.connect(log)
    on_course_duplicate.connect(log)

    # assignment events
    from .assignment import on_assignment_modified, on_assignment_get, on_assignment_list_get, on_assignment_create, \
        on_assignment_delete, on_assignment_list_get_status, on_assignment_get_status, \
        on_assignment_user_comparisons_get, on_assignment_users_comparisons_get
    on_assignment_modified.connect(log)
    on_assignment_get.connect(log)
    on_assignment_list_get.connect(log)
    on_assignment_create.connect(log)
    on_assignment_delete.connect(log)
    on_assignment_list_get_status.connect(log)
    on_assignment_get_status.connect(log)
    on_assignment_user_comparisons_get.connect(log)
    on_assignment_users_comparisons_get.connect(log)

    # assignment comment events
    from .assignment_comment import on_assignment_comment_modified, on_assignment_comment_get, \
        on_assignment_comment_list_get, on_assignment_comment_create, on_assignment_comment_delete
    on_assignment_comment_modified.connect(log)
    on_assignment_comment_get.connect(log)
    on_assignment_comment_list_get.connect(log)
    on_assignment_comment_create.connect(log)
    on_assignment_comment_delete.connect(log)

    # answer events
    from .answer import on_answer_modified, on_answer_get, on_answer_list_get, on_answer_create, on_answer_flag, \
        on_set_top_answer, on_answer_delete, on_user_answer_get
    on_answer_modified.connect(log)
    on_answer_get.connect(log)
    on_answer_list_get.connect(log)
    on_answer_create.connect(log)
    on_answer_flag.connect(log)
    on_set_top_answer.connect(log)
    on_answer_delete.connect(log)
    on_user_answer_get.connect(log)

    # answer comment events
    from .answer_comment import on_answer_comment_modified, on_answer_comment_get, on_answer_comment_list_get, \
        on_answer_comment_create, on_answer_comment_delete
    on_answer_comment_modified.connect(log)
    on_answer_comment_get.connect(log)
    on_answer_comment_list_get.connect(log)
    on_answer_comment_create.connect(log)
    on_answer_comment_delete.connect(log)

    # criterion events
    from .criterion import on_criterion_get, on_criterion_update, on_criterion_list_get, on_criterion_create
    on_criterion_get.connect(log)
    on_criterion_update.connect(log)
    on_criterion_list_get.connect(log)
    on_criterion_create.connect(log)

    # comparison events
    from .comparison import on_comparison_get, on_comparison_create, on_comparison_update
    on_comparison_get.connect(log)
    on_comparison_create.connect(log)
    on_comparison_update.connect(log)

    # comparison example events
    from .comparison_example import on_comparison_example_create, on_comparison_example_delete, \
        on_comparison_example_list_get, on_comparison_example_modified
    on_comparison_example_create.connect(log)
    on_comparison_example_delete.connect(log)
    on_comparison_example_list_get.connect(log)
    on_comparison_example_modified.connect(log)

    # classlist events
    from .classlist import on_classlist_get, on_classlist_upload, on_classlist_enrol, on_classlist_unenrol, \
        on_classlist_instructor_label, on_classlist_instructor, on_classlist_student, \
        on_classlist_update_users_course_roles
    on_classlist_get.connect(log)
    on_classlist_upload.connect(log)
    on_classlist_enrol.connect(log)
    on_classlist_unenrol.connect(log)
    on_classlist_instructor_label.connect(log)
    on_classlist_instructor.connect(log)
    on_classlist_student.connect(log)
    on_classlist_update_users_course_roles.connect(log)

    # course group events
    from .course_group import on_course_group_get, on_course_group_members_get
    on_course_group_get.connect(log)
    on_course_group_members_get.connect(log)

    # course user group events
    from .course_group_user import on_course_group_user_create, on_course_group_user_delete, \
        on_course_group_user_list_create, on_course_group_user_list_delete
    on_course_group_user_create.connect(log)
    on_course_group_user_delete.connect(log)
    on_course_group_user_list_create.connect(log)
    on_course_group_user_list_delete.connect(log)

    # report event
    from .report import on_export_report
    on_export_report.connect(log)

    # file attachment event
    from .file import on_save_file, on_get_kaltura_token, on_save_kaltura_file
    on_save_file.connect(log)
    on_get_kaltura_token.connect(log)
    on_save_kaltura_file.connect(log)

    # gradebook event
    from .gradebook import on_gradebook_get
    on_gradebook_get.connect(log)

    # lti launch event
    from .lti_course import on_lti_course_link_create, on_lti_course_membership_update, \
        on_lti_course_membership_status_get, on_lti_course_unlink
    on_lti_course_link_create.connect(log)
    on_lti_course_membership_update.connect(log)
    on_lti_course_membership_status_get.connect(log)

    # lti consumer event
    from .lti_consumers import on_consumer_create, on_consumer_get, \
        on_consumer_list_get, on_consumer_update
    on_consumer_create.connect(log)
    on_consumer_get.connect(log)
    on_consumer_list_get.connect(log)
    on_consumer_update.connect(log)

    # misc
    on_get_file.connect(log)


def log_demo_events(log):
    # demo events
    from .demo import on_user_demo_create
    on_user_demo_create.connect(log)
