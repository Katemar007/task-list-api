from flask import Blueprint, abort, make_response, request, Response
from app.models.task import Task
from ..db import db
from .route_utilities import validate_model

bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

#Wave 1
@bp.post("")
def create_task():
    request_body = request.get_json()
    
    try:
        new_task = Task.from_dict(request_body)

    except KeyError as error:
        if "description" not in request_body  or "title" not in request_body:
            response = {"details": "Invalid data"}
        else:
            response = {"details": f"Invalid request: missing {error.args[0]}"}

        abort(make_response(response, 400))

    db.session.add(new_task)
    db.session.commit()

    return {"task": new_task.to_dict()}, 201

#Wave 3 and Wave 5
@bp.get("")
def get_all_tasks():
    query = db.select(Task)
    description_param = request.args.get("description")
    if description_param:
        query = query.where(Task.description.ilike(f"%{description_param}%"))
        
    completed_at_param = request.args.get("completed_at")
    if completed_at_param:
        query = query.where(Task.completed_at.like=={completed_at_param})
        
    query = query.order_by(Task.id)
    tasks = db.session.scalars(query)

    tasks_response = []
    for task in tasks:
        tasks_response.append(task.to_dict())
    
    return tasks_response

#Wave 1
@bp.get("/<task_id>")
def get_one_task(task_id):
    task = validate_model(Task, task_id)
    return {"task": task.to_dict()}

#Wave 4
@bp.put("/<task_id>")
def update_one_task(task_id):
    task = validate_model(Task, task_id)
    request_body = request.get_json()
    
    task.title = request_body["title"]
    task.description = request_body["description"]
    task.completed_at = request_body.get("completed_at")
    db.session.commit()
    # needs fixing
    return Response(status=204, mimetype="application/json")

#Wave 4
@bp.delete("/<task_id>")
def delete_one_task(task_id):
    task = validate_model(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    return Response(status=204, mimetype="application/json")
    