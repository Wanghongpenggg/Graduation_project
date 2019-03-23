from app.views.auth.login import login_required
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, current_app
)
from . import back_blueprint as back_bp
from app.models.user_info import UserInfo
from app.models.identifier import Identifier
from app.models.identifier_type import IdentifierType
from app import db
import json


@back_bp.route('/manage-identifier', methods=['GET'])
@login_required
def manage_identifier():
    equipment_part = [IdentifierType.EQUIPMENT, IdentifierType.SENSOR, IdentifierType.SYSTEM]
    equipment_data_part = [IdentifierType.EQUIPMENT_DATA, IdentifierType.SENSOR_DATA, IdentifierType.SYSTEM_DATA]
    part = request.args.get('part', default='all')
    get_page = request.args.get('page', default=1, type=int)  # 当前页数
    if part == "all":
        pagination = Identifier.query.filter(Identifier.is_delete == 0, Identifier.user_id == g.user.id).order_by(
            Identifier.create_time.desc()).paginate(get_page, per_page=current_app.config['POSTS_PER_PAGE'],
                                                    error_out=True)
    elif part == "equipment":
        pagination = Identifier.query.filter(Identifier.is_delete == 0, Identifier.type in equipment_part,
                                             Identifier.user_id == g.user.id).order_by(
            Identifier.create_time.desc()).paginate(get_page, per_page=current_app.config['POSTS_PER_PAGE'],
                                                    error_out=True)
    elif part == "data":
        pagination = Identifier.query.filter(Identifier.is_delete == 0, Identifier.type in equipment_data_part,
                                             Identifier.user_id == g.user.id).order_by(
            Identifier.create_time.desc()).paginate(get_page, per_page=current_app.config['POSTS_PER_PAGE'],
                                                    error_out=True)
    render_dict = {
        "part": part,
        "pagination": pagination,
    }
    return render_template('back/company/manage_identifier.html', **render_dict)


@back_bp.route('/manage-identifier/add', methods=['GET', 'POST'])
@login_required
def add_identifier():
    if request.method == "GET":
        return render_template('back/company/manage_identifier_part/add_identifier.html')
    elif request.method == "POST":
        # print("=================================")
        register_type = request.form.get("type")
        metadata_dict = dict()
        for key in list(request.form.keys()):
            if key in ["handle", "type"]:
                continue
            metadata_dict[key] = request.form.get(key)
        new_identifier = Identifier()
        new_identifier.user_id = g.user.id
        new_identifier.handle = request.form.get("handle")
        new_identifier.the_metadata = json.dumps(metadata_dict)
        new_identifier.type = get_identifier_type_num(register_type)
        db.session.add(new_identifier)
        db.session.commit()
        return redirect(url_for('back.manage_identifier'))


@back_bp.route('/manage-identifier/<int:id>', methods=['GET'])
@login_required
def view_identifier(id):
    if request.method == "GET":
        # id = request.args.get("id")
        # print(id)
        identifier = Identifier.query.filter(Identifier.id == id).first()
        identifier.metadata = json.loads(identifier.the_metadata)
        return render_template('back/company/manage_identifier_part/view_identifier.html', identifier=identifier)


def get_identifier_type_num(register_type):
    if register_type == "sensor":
        return IdentifierType.SENSOR
    elif register_type == "equipment":
        return IdentifierType.EQUIPMENT
    elif register_type == "system":
        return IdentifierType.SYSTEM
    elif register_type == "sensor_data":
        return IdentifierType.SENSOR_DATA
    elif register_type == "equipment_data":
        return IdentifierType.EQUIPMENT_DATA
    elif register_type == "system_data":
        return IdentifierType.SYSTEM_DATA

# ---------------------------back for use---------------------------------------
# if register_type=="sensor":
#     pass
#     # metadata_dict["content"] = request.form.get("content")
#     # metadata_dict["sensorID"] = request.form.get("sensorID")
#     # metadata_dict["sensorNumber"] = request.form.get("sensorNumber")
#     # metadata_dict["sensorName"] = request.form.get("sensorName")
#     # metadata_dict["sensorCategory"] = request.form.get("sensorCategory")
#     # metadata_dict["sensorModel"] = request.form.get("sensorModel")
#     # metadata_dict["installationPosition"] = request.form.get("installationPosition")
#     # metadata_dict["lowAlarmValue"] = request.form.get("lowAlarmValue")
#     # metadata_dict["highAlarmValue"] = request.form.get("highAlarmValue")
#     # metadata_dict["applicationState"] = request.form.get("applicationState")
#     # metadata_dict["connectionChannel"] = request.form.get("connectionChannel")
#     # metadata_dict["lowErrorDifference"] = request.form.get("lowErrorDifference")
#     # metadata_dict["highErrorDifference"] = request.form.get("highErrorDifference")
#     # metadata_dict["lowCurrentValue"] = request.form.get("lowCurrentValue")
#     # metadata_dict["highCurrentValue"] = request.form.get("highCurrentValue")
#     # metadata_dict["rangeUnit"] = request.form.get("rangeUnit")
#     # metadata_dict["dateOfProduction"] = request.form.get("dateOfProduction")
#     # metadata_dict["installDate"] = request.form.get("installDate")
#     # metadata_dict["discardedDate"] = request.form.get("discardedDate")
#     # metadata_dict["storageDate"] = request.form.get("storageDate")
# elif register_type=="equipment":
#     pass
# elif register_type=="system":
#     pass
# else:
#     pass
