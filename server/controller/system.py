from flask import jsonify, request, url_for
from . import api
from .. import db
from ..model.system import Permission, App
from ..decorators import signature_required, permission_required, admin_required
from ..results import Success


@api.route("/apps/<int:app_id>", methods=["GET"])
@signature_required
@permission_required(Permission.READ)
def get_app(app_id):
    app = App.query.get_or_404(app_id)
    return jsonify(Success(app.to_json()).to_dict())


@api.route("/apps", methods=["POST"])
@signature_required
@admin_required
def new_app():
    app = App.from_json(request.json)
    db.session.add(app)
    db.session.commit()
    return jsonify(Success(app.to_json()).to_dict()), 201, {"Location": url_for("api.get_app", app_id=app.id)}
