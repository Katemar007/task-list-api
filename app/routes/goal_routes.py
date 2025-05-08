from flask import Blueprint, abort, make_response, request, Response
from app.models.goal import Goal
from app.models.task import Task
from ..db import db
from .route_utilities import validate_model, create_model
from datetime import datetime
from datetime import timezone
import requests
import os

bp = Blueprint("goals_bp", __name__, url_prefix="/goals")


@bp.post("")
def create_goal():
    request_body = request.get_json()
    new_goal, status_code = create_model(Goal, request_body)

    return {"goal": new_goal}, status_code


@bp.get("")
def get_all_goals():
    query = db.select(Goal)

    title_param = request.args.get("title")
    if title_param:
        query = query.where(Goal.title.ilike(f"%{title_param}%"))

    # sort_param = request.args.get("sort")
    # if sort_param == "asc":
    #     query = query.order_by(Task.title.asc())
    # elif sort_param == "desc":
    #     query = query.order_by(Task.title.desc())

    query = query.order_by(Goal.id)
    goals = db.session.scalars(query)

    goals_response = []
    for goal in goals:
        goals_response.append(goal.to_dict())
    
    return goals_response


@bp.get("/<goal_id>")
def get_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    return {"goal": goal.to_dict()}


@bp.put("/<goal_id>")
def update_one_goal(goal_id):
    task = validate_model(Goal, goal_id)
    request_body = request.get_json()
    
    task.title = request_body["title"]

    db.session.commit()

    return Response(status=204, mimetype="application/json")


@bp.delete("/<goal_id>")
def delete_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    db.session.delete(goal)
    db.session.commit()

    return Response(status=204, mimetype="application/json")

@bp.post("/<goal_id>/tasks")
def tasks_to_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    
    request_body = request.get_json()
    task_list = request_body.get("task_ids", [])

    for task_id in task_list:
        task = validate_model(Task, task_id)
        task.goal_id = goal.id

    db.session.commit()

    return {
        "id": goal.id,
        "task_ids": task_list
    }