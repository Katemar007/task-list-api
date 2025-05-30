import pytest
from app.models.goal import Goal
from app.db import db


# @pytest.mark.skip(reason="No way to test this feature yet")
def test_get_goals_no_saved_goals(client):
    # Act
    response = client.get("/goals")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []


# @pytest.mark.skip(reason="No way to test this feature yet")
def test_get_goals_one_saved_goal(client, one_goal):
    # Act
    response = client.get("/goals")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body == [
        {
            "id": 1,
            "title": "Build a habit of going outside daily"
        }
    ]


# @pytest.mark.skip(reason="No way to test this feature yet")
def test_get_goal(client, one_goal):
    # Act
    response = client.get("/goals/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert "goal" in response_body
    assert response_body == {
        "goal": {
            "id": 1,
            "title": "Build a habit of going outside daily"
        }
    }


# @pytest.mark.skip(reason="test to be completed by student")
def test_get_goal_not_found(client):
    pass
    # Act
    response = client.get("/goals/1")
    response_body = response.get_json()

    # raise Exception("Complete test")
    # Assert
    assert response.status_code == 404
    assert response_body == {"message": f"Goal with 1 does not exist"}
    # ---- Complete Test ----
    # assertion 1 goes here
    # assertion 2 goes here
    # ---- Complete Test ----


# @pytest.mark.skip(reason="No way to test this feature yet")
def test_create_goal(client):
    # Act
    response = client.post("/goals", json={
        "title": "My New Goal"
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert "goal" in response_body
    assert response_body == {
        "goal": {
            "id": 1,
            "title": "My New Goal"
        }
    }


# @pytest.mark.skip(reason="test to be completed by student")
def test_update_goal(client, one_goal):
    # Act
    response = client.put("/goals/1", json={
        "title": "Updated Goal Title"
    })
    query = db.select(Goal).where(Goal.id == 1)
    goal = db.session.scalar(query)

    # Assert
    assert response.status_code == 204
    assert response.headers.get("Content-Length") == None
    assert goal.title == "Updated Goal Title"
    # Assert
    # ---- Complete Assertions Here ----
    # assertion 1 goes here
    # assertion 2 goes here
    # assertion 3 goes here
    # ---- Complete Assertions Here ----


# @pytest.mark.skip(reason="test to be completed by student")
def test_update_goal_not_found(client):
    response = client.get("/goals/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == {"message": f"Goal with 1 does not exist"}
    # ---- Complete Assertions Here ----
    # assertion 1 goes here
    # assertion 2 goes here
    # ---- Complete Assertions Here ----


# @pytest.mark.skip(reason="No way to test this feature yet")
def test_delete_goal(client, one_goal):
    # Act
    response = client.delete("/goals/1")

    # Assert
    assert response.status_code == 204

    # Check that the goal was deleted
    response = client.get("/goals/1")
    assert response.status_code == 404

    response_body = response.get_json()
    assert "message" in response_body
    assert response_body["message"] == "Goal with 1 does not exist"

    # raise Exception("Complete test with assertion about response body")
    # *****************************************************************
    # **Complete test with assertion about response body***************
    # *****************************************************************


# @pytest.mark.skip(reason="test to be completed by student")
def test_delete_goal_not_found(client):
    response = client.delete("/goals/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == {"message": f"Goal with 1 does not exist"}
    # ---- Complete Assertions Here ----
    # assertion 1 goes here
    # assertion 2 goes here
    # ---- Complete Assertions Here ----


# @pytest.mark.skip(reason="No way to test this feature yet")
def test_create_goal_missing_title(client):
    # Act
    response = client.post("/goals", json={})
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == {
        "details": "Invalid data"
    }
