from flask import Blueprint, abort, make_response, request, Response
from app.models.task import Task
from app.models.goal import Goal
from ..db import db
from .route_utilities import validate_model, create_model
from datetime import datetime
from datetime import timezone
import requests
import os
from dotenv import load_dotenv

load_dotenv()

bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")


#Wave 1
@bp.post("")
def create_task():
    request_body = request.get_json()
    new_task, status_code = create_model(Task, request_body)

    return {"task": new_task}, status_code

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

    sort_param = request.args.get("sort")
    if sort_param == "asc":
        query = query.order_by(Task.title.asc())
    elif sort_param == "desc":
        query = query.order_by(Task.title.desc())

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

#Wave 1
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

#Wave 1
@bp.delete("/<task_id>")
def delete_one_task(task_id):
    task = validate_model(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    return Response(status=204, mimetype="application/json")
    
# Wave 3
@bp.patch("/<task_id>/mark_complete")
def completed_task(task_id):
    task = validate_model(Task, task_id)
    task.completed_at = datetime.now(timezone.utc)
    task_title = task.title
    send_request_to_slackbot(task_title)

    db.session.commit()

    return Response(status=204, mimetype="application/json")

def send_request_to_slackbot(data):
    bot_path = os.environ.get("SLACK_BOT_PATH")
    bot_token = os.environ.get("SLACK_BOT_TOKEN")
    channel_id = os.environ.get("SLACK_CHANNEL_ID")
    message = "Restoration attempt #3 {data}"

    token = f"Bearer {bot_token}"
    headers = {
        "Content-type": "application/json", 
        "Authorization": token}
    request_body = {
        "channel": channel_id,
        "text": message
        }

# Wave 3
@bp.patch("/<task_id>/mark_incomplete")
def incomplete_task(task_id):
    task = validate_model(Task, task_id)
    task.completed_at = None

    db.session.commit()
    return Response(status=204, mimetype="application/json")

# Wave 3
@bp.patch("/<task_id>/mark_complete")
def completed_on_complete_task(task_id):
    task = validate_model(Task, task_id)
    task.completed_at = datetime.now(timezone.utc)

    db.session.commit()
    return Response(status=204, mimetype="application/json")

# Wave 3
@bp.patch("/<task_id>/mark_incomplete")
def incompleted_on_incomplete_task(task_id):
    task = validate_model(Task, task_id)
    task.completed_at = None

    db.session.commit()
    return Response(status=204, mimetype="application/json")

# Wave 4
# @bp.patch("/<task_id>/mark_complete")
def completed_task_notification_by_API(task_id):
    task = validate_model(Task, task_id)
    task.title = "My Beautiful Task"
    task.completed_at = datetime.now(timezone.utc)
    db.session.commit()

    # Send Slack message
    slack_url = "https://slack.com/api/chat.postMessage"
    slack_token = os.environ.get("SLACK_BOT_TOKEN")
    slack_channel = "task-notifications"  # Can also be channel ID like "C01ABCXYZ"

    message = {
        "channel": slack_channel,
        "text": f"Someone just completed the task {task.title}"
    }

    headers = {
        "Authorization": f"Bearer {slack_token}",
        "Content-Type": "application/json"
    }

    response = requests.post(slack_url, json=message, headers=headers)

    if not response.ok:
        print("Slack message failed:", response.json())

    return Response(status=204)

# @bp_child.post("")
# def tasks_to_goal(goal_id,list_id):
#     goal = validate_model(Goal, goal_id)
    
#     task_ids = []
#     for task_id in list_id:
#         task = validate_model(Task, task_id)
#         task.goal_id = goal.goal_id
#         task_ids.append(task.task_id)

#     db.session.commit()

#     return {
#         "id": goal.goal_id,
#         "task_ids": task_ids
#     }, 200

