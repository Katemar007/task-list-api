from flask import abort, make_response, Response
from ..db import db
import os
import requests
import logging


def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        response = {"message": f":{cls.__name__} with {model_id} invalid"}
        abort(make_response(response, 400))
    
    query = db.select(cls).where(cls.id == model_id)
    model = db.session.scalar(query)

    if not model:
        response = {"message": f"{cls.__name__} with {model_id} does not exist"}
        abort(make_response(response, 404))

    return model


def create_model(cls, model_data):
    try:
        new_model = cls.from_dict(model_data)
    except KeyError as error:
        response = {"details": "Invalid data"}
        # response = {"message": f"Invalid request: missing {error.args[0]}"}
        abort(make_response(response, 400))
        
    db.session.add(new_model)
    db.session.commit()

    return new_model.to_dict(), 201

def delete_model(cls, model_id):
    model = validate_model(cls, model_id)

    db.session.delete(model)
    db.session.commit()

    return Response(status=204, mimetype="application/json")
    

# Work in progress
def task_to_dict(Task, data):
    {
            "id": data.id,
            "title": data.title,
            "description": data.description,
            "is_complete": bool(data.completed_at),
            "goal": data.goal_id
    }

    return task_to_dict

def send_message_task_complete_slack(task_title):
    slack_url = os.environ.get("SLACK_BOT_PATH")
    slack_token = os.environ.get("SLACK_BOT_TOKEN")
    slack_channel = os.environ.get("SLACK_CHANNEL_ID")  # Can also be channel ID like "C01ABCXYZ"

    message = {
        "channel": slack_channel,
        "text": f"Someone just completed the task {task_title}"
    }

    headers = {
        "Authorization": f"Bearer {slack_token}",
        "Content-Type": "application/json"
    }

    response = requests.post(slack_url, json=message, headers=headers)

    if not response.ok:
        logger = logging.getLogger(__name__)
        logger.error(f"Slack message failed: {response.json()}")
