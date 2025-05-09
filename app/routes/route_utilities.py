from flask import abort, make_response
from ..db import db

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