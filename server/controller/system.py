from flask import jsonify, request, url_for
from . import api
from .. import db
from ..model.system import Permission, App
from ..decorators import signature_required, permission_required, admin_required
from ..results import Success, Failed


@api.route("/apps/<int:app_id>", methods=["GET"])
@signature_required
@permission_required(Permission.READ)
def get_app(app_id):
    app = db.session.query(App).filter(App.id == app_id).first()
    if app is None:
        return jsonify(Failed(None).to_dict())
    return jsonify(Success(app.to_json()).to_dict())


@api.route("/apps", methods=["POST"])
@signature_required
@admin_required
def new_app():
    app = App.from_json(request.json)
    db.session.add(app)
    db.session.commit()
    return jsonify(Success(app.to_json()).to_dict()), 201, {"Location": url_for("api.get_app", app_id=app.id)}


@api.route("/apps/<int:app_id>", methods=["DELETE"])
@signature_required
@admin_required
def del_app(app_id):
    db.session.query(App).filter(App.id == app_id).delete()
    db.session.commit()
    return jsonify(Success(None).to_dict())
