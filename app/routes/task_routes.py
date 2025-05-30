from flask import Blueprint, abort, make_response, request, Response
from app.models.task import Task
from app.models.goal import Goal
from ..db import db
from .route_utilities import validate_model, create_model, send_message_task_complete_slack
from datetime import datetime
from datetime import timezone
import requests
import os


bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")


@bp.post("")
def create_task():
    request_body = request.get_json()
    new_task, status_code = create_model(Task, request_body)

    return {"task": new_task}, status_code


@bp.get("")
def get_all_tasks():
    query = db.select(Task)

    description_param = request.args.get("description")
    if description_param:
        query = query.where(Task.description.ilike(f"%{description_param}%"))
        
    completed_at_param = request.args.get("completed_at")
    if completed_at_param:
        query = query.where(Task.completed_at.like=={completed_at_param})

    sort_param = request.args.get("sort")
    if sort_param == "asc":
        query = query.order_by(Task.title.asc())
    elif sort_param == "desc":
        query = query.order_by(Task.title.desc())

    query = query.order_by(Task.id)
    tasks = db.session.scalars(query)

    tasks_response = [task.to_dict() for task in tasks]
    
    return tasks_response


@bp.get("/<task_id>")
def get_one_task(task_id):
    task = validate_model(Task, task_id)
    return {"task": task.to_dict()}


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


@bp.delete("/<task_id>")
def delete_one_task(task_id):
    task = validate_model(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    return Response(status=204, mimetype="application/json")
    
# Wave 3
# @bp.patch("/<task_id>/mark_complete")
# def completed_task(task_id):
#     task = validate_model(Task, task_id)
#     task.completed_at = datetime.now(timezone.utc)
#     print(f'********* mark_complete {task_id} {task.completed_at}')
#     task_title = task.title
#     send_request_to_slackbot(task_title)

#     db.session.commit()

#     return Response(status=204, mimetype="application/json")

# def send_request_to_slackbot(data):
#     print(f'********* request_to_slackbot')
#     bot_path = os.environ.get("SLACK_BOT_PATH")
#     bot_token = os.environ.get("SLACK_BOT_TOKEN")
#     channel_id = os.environ.get("SLACK_CHANNEL_ID")
#     message = "Restoration attempt #3 {data}"

#     token = f"Bearer {bot_token}"
#     headers = {
#         "Content-type": "application/json", 
#         "Authorization": token}
#     request_body = {
#         "channel": channel_id,
#         "text": message
#         }

# CORRECTED YELLOW ISSUE #2 (There are two route handlers registered for /tasks/id/mark_incomplete)
@bp.patch("/<task_id>/mark_incomplete")
def incomplete_task(task_id):
    task = validate_model(Task, task_id)
    task.completed_at = None

    db.session.commit()
    return Response(status=204, mimetype="application/json")


# @bp.patch("/<task_id>/mark_complete")
# def completed_on_complete_task(task_id):
#     task = validate_model(Task, task_id)
#     task.completed_at = datetime.now(timezone.utc)

#     db.session.commit()
#     return Response(status=204, mimetype="application/json")



@bp.patch("/<task_id>/mark_complete")
def completed_task_notification_by_API(task_id):
    task = validate_model(Task, task_id)
    task.completed_at = datetime.now(timezone.utc)
    db.session.commit()

    send_message_task_complete_slack(task.title)

    # ADDED mimetype to fix json
    return Response(status=204, mimetype="application/json")
