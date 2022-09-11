# !/usr/bin/python
# -*- coding: utf-8 -*-
from configparser import ConfigParser
from datetime import timedelta
from json import loads

from flask import Flask, request
from flask_cors import CORS, cross_origin
from flask_jwt_extended import JWTManager

from api.organization import showOrganization, createOrganization
from api.lesson import (
    createLesson,
    showLesson,
    updateLesson,
    dropLesson
)
from api.user import (
    createUser,
    activate,
    confirm_password,
    autentification,
    user_info,
    user_update
)
from api.group import (
    createGroup,
    viewGroup,
    createUserGroup,
    removeUserGroup
)
from api.timetable import (
    createTimetable,
    showTimetable,
    deleteTimetable
)
from api.journal import (
    addValueJournal,
    allValueJournal
)
from api.email import verificationUser, reset_password
from core.db.dbo import engine, Base


# ======================================================================
# ===================== Извлечение данных конфига ======================
# ======================================================================
conf = ConfigParser()
conf.read(filenames='settings.ini')
DEBUG = conf['WEB']['debug']
HOST = conf['WEB']['host']
PORT = conf['WEB']['port']
# ======================================================================
# ======================= Создание точки входа =========================
# ======================================================================
app = Flask(__name__)
# ======================================================================
# ========================= Создание миграций ==========================
# ======================================================================
Base.metadata.create_all(bind=engine)
# ======================================================================
# =========================== Настройка CORS ===========================
# ======================================================================
cors = CORS(app, resources={r"/*": {"origins": "*"}}, headers='Content-Type')
app.config['CORS_HEADERS'] = 'Content-Type'
# ======================================================================
# ====================== Настройка генератора JWT ======================
# ======================================================================
app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
jwt = JWTManager(app)
app.config["JWT_COOKIE_SECURE"] = False
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
app.config["JWT_SECRET_KEY"] = "super-secret"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)


# ======================================================================
# ======================= URL маршрутизация API ========================
# ======================================================================
@app.route('/api', methods=["GET"])
def api_index():
    pass


@app.route('/api/organization/create-organization', methods=["POST"])
@cross_origin()
def api_create_organization():
    return createOrganization.Api(organization_name=request.get_json().get('name')).save()


@app.route('/api/organization/show-organization', methods=["Get"])
@cross_origin()
def api_show_organization():
    return showOrganization.Api(organization_id=request.args.get('id')).show()


@app.route('/api/user/create-user', methods=["POST"])
@cross_origin()
def api_create_user():
    if request.get_json().get('add_personal'):
        """
        В случае если директор добавляет персонал,
        Id организации подставляется в organization_name
        """
        organization_id = request.get_json().get('organization_name')
    else:
        # В случае если регистрируется директор
        with createOrganization.Api(organization_name=request.get_json().get('organization_name')).save() as obj:
            data = loads(obj.data.decode('utf-8'))
            obj.close()

        organization_id = data[0]["message"]["id"]

    return createUser.Api(
        organization_name=organization_id,
        first_name=request.get_json().get('first_name'),
        last_name=request.get_json().get('last_name'),
        email=request.get_json().get('email'),
        role=request.get_json().get('role'),
        password=request.get_json().get('password'),
        group=request.get_json().get('group'),
        lesson_up=request.get_json().get('lesson_up')
    ).save()


@app.route('/api/user/activate', methods=["PUT"])
@cross_origin()
def api_activate():
    return activate.Api(user_id=request.args.get('id')).activate()


@app.route('/api/user/auth', methods=["POST"])
@cross_origin()
def api_auth():
    return autentification.Api(
        email=request.get_json().get('email'),
        password=request.get_json().get('password')
    ).auth()


@app.route('/api/user/update-user', methods=["PUT"])
@cross_origin()
def api_update_user():
    return user_update.Api(
        user_id=request.get_json().get('user_id'),
        first_name=request.get_json().get('first_name'),
        last_name=request.get_json().get('last_name'),
        role=request.get_json().get('role'),
        email=request.get_json().get('email')
    ).update()


@app.route('/api/user/user-info', methods=["GET"])
@cross_origin()
def api_user_info():
    return user_info.Api(access_token=request.args.get('access_token')).show()


@app.route('/api/user/all-user', methods=["GET"])
@cross_origin()
def api_all_user():
    print(request.args.get('group_id'))
    return user_info.Api(
        access_token='',
        role=request.args.get('role'),
        group_id=request.args.get('group_id'),
        lesson_id=request.args.get('lesson_id'),
        organization_id=request.args.get('organization_id'),
        year=request.args.get('year'),
        month=request.args.get('month'),
        mode=request.args.get('mode')
    ).all()


@app.route('/api/user/block-user', methods=["POST"])
@cross_origin()
def api_block_user():
    pass


@app.route('/api/email/send-verification', methods=["POST"])
@cross_origin()
def api_email_verification():
    return verificationUser.Api(
        email=request.get_json().get('email'),
        first_name=request.get_json().get('first_name')
    ).send()


@app.route('/api/email/reset-password', methods=["PUT"])
@cross_origin()
def api_reset_password():
    with confirm_password.Api(email=request.get_json().get('email')).abstract_new_password() as obj:
        data = loads(obj.data.decode('utf-8'))
        obj.close()

    new_password = data[0]["message"]

    return reset_password.Api(
        email=request.get_json().get('email'),
        password=new_password
    ).send()


@app.route('/api/lesson/create-lesson', methods=["POST"])
@cross_origin()
def api_create_lesson():
    return createLesson.Api(
        organization_id=request.get_json().get('organization_id'),
        lesson=request.get_json().get('lesson')
    ).add()


@app.route('/api/lesson/lesson-all', methods=["GET"])
@cross_origin()
def api_show_lesson():
    return showLesson.Api(
        organization_id=request.args.get('organization_id')
    ).show()


@app.route('/api/lesson/update-lesson', methods=["PUT"])
@cross_origin()
def api_update_lesson():
    return updateLesson.Api(
        id=request.get_json().get('id'),
        organization_id=request.get_json().get('organization_id'),
        lesson=request.get_json().get('lesson')
    ).update()


@app.route('/api/lesson/drop-lesson', methods=["DELETE"])
@cross_origin()
def api_drop_lesson():
    return dropLesson.Api(
        id=request.args.get('id'),
        organization_id=request.args.get('organization_id')
    ).drop()


@app.route('/api/group/create-group', methods=["POST"])
@cross_origin()
def api_create_group():
    return createGroup.Api(
        organization_id=request.get_json().get('organization_id'),
        user_id=request.get_json().get('user_id'),
        name=request.get_json().get('name')
    ).save()


@app.route('/api/group/all-group', methods=["GET"])
@cross_origin()
def api_all_group():
    return viewGroup.Api(
        organization_id=request.args.get('organization_id')
    ).all()


@app.route('/api/group/show-group', methods=["GET"])
@cross_origin()
def api_show_group():
    return viewGroup.Api(
        organization_id=request.args.get('organization_id'),
        group_id=request.args.get('group_id')
    ).show()


@app.route('/api/group/add-user', methods=["POST"])
@cross_origin()
def api_add_user():
    return createUserGroup.Api(
        group_id=request.get_json().get('group_id'),
        organization_id=request.get_json().get('organization_id'),
        user_id=request.get_json().get('user_id')
    ).save()


@app.route('/api/group/remove-user', methods=["DELETE"])
@cross_origin()
def api_remove_user():
    print(request.args.get('user_id'))
    return removeUserGroup.Api(
        user_id=request.args.get('user_id')
    ).remove()


@app.route('/api/timetable/create-timetable', methods=["POST"])
@cross_origin()
def api_create_timetable():
    return createTimetable.Api(
        organization_id=request.get_json().get('organization_id'),
        groups_id=request.get_json().get('groups_id'),
        lesson_id=request.get_json().get('lesson_id'),
        day=request.get_json().get('day'),
        time_start=request.get_json().get('time_start'),
        time_end=request.get_json().get('time_end'),
    ).save()


@app.route('/api/timetable/show-timetable', methods=["GET"])
@cross_origin()
def api_show_timetable():
    return showTimetable.Api(
        organization_id=request.args.get('organization_id'),
        groups_id=request.args.get('groups_id')
    ).show()


@app.route('/api/timetable/delete-timetable', methods=["DELETE"])
@cross_origin()
def api_delete_timetable():
    print(123)
    return deleteTimetable.Api(
        id=request.args.get('id')
    ).drop()


@app.route('/api/timetable/show-timetable/teacher', methods=["GET"])
@cross_origin()
def api_show_timetable_teacher():
    return showTimetable.Api(
        organization_id=request.args.get('organization_id'),
        user_id=request.args.get('user_id'),
        role=request.args.get('role')
    ).teacher_lesson()


@app.route('/api/journal/add', methods=["POST"])
@cross_origin()
def api_add_value_journal():
    print(request.get_json().get('value'))
    return addValueJournal.Api(
        organization_id=request.get_json().get('organization_id'),
        user_id=request.get_json().get('user_id'),
        groups_id=request.get_json().get('groups_id'),
        lesson_id=request.get_json().get('lesson_id'),
        value=request.get_json().get('value'),
        day=request.get_json().get('day'),
        month=request.get_json().get('month'),
        year=request.get_json().get('year'),
    ).add()


@app.route('/api/journal/all', methods=["GET"])
@cross_origin()
def api_all_journal():
    return showTimetable.Api(
        organization_id=request.args.get('organization_id'),
        lesson_id=request.args.get('lesson_id')
    ).all()