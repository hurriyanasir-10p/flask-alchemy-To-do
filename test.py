import pytest
import requests
import json
BASE = "http://127.0.0.1:5000/"


@pytest.fixture
def userData():
    return {
        '1': {'name': 'Hurriya'},
        '2': {'name': 'Adil'},
        '3': {'name': 'Zaynab'},

    }


@pytest.fixture
def listData():
    return {
        "1": {"name": "Exams", "user_id": 2},
        "2": {"name": "Study", "user_id": 1},
        "3": {"name": "Today", "user_id": 2}
    }



@pytest.fixture
def taskData():
    return {

        "1": {"description": "presentation", "priority": "medium", "list_id": 1},
        "2": {"description": "quiz", "priority": "low", "list_id": 1},
        "3": {"description": "task 1", "priority": "high", "list_id": 2},
        "4": {"description": "Meeting", "priority": "medium", "list_id": 1},

    }


############# USER TESTS ###########

# Testing post for adding user
@pytest.mark.parametrize("id,output", [('1', {"id": 1, "name": 'Hurriya'}),
                                       ('2', {"id": 2, "name": 'Adil'}),
                                       ('3', {"id": 3, "name": 'Zaynab'}), ])
def test_user_post(output,userData,id):


    url = "http://127.0.0.1:5000/user"

    payload = json.dumps(userData[id])
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)

    assert response.json()==output

################ Testing put for user

@pytest.mark.parametrize("id,output", [
    ('2', {"id": 2, "name": 'Nasir'})])
def test_user_put(output, id):
    url = BASE+"user/"+id
    payload = json.dumps({
        "name": "Nasir"
    })
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("PUT", url, headers=headers, data=payload)
    print(response.text)
    assert response.json() == output


################ Testing get for user

@pytest.mark.parametrize("id,output", [
    ('1', {"id": 1,
           "name": "Hurriya"
           })])
def test_user_get(output, id):
    url = BASE + "user/" + id

    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("GET", url, headers=headers)
    print(response.text)
    assert response.json() == output

################ Testing delete for user

@pytest.mark.parametrize("id,output", [
    ('3', {"id": 3,
           "name": "Zaynab"
           })])
def test_user_delete(output, id):
    url = BASE + "user/" + id

    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("DELETE", url, headers=headers)
    print(response.text)
    assert response.json() == output


###########  LIST TESTS  ###########

@pytest.mark.parametrize("id,user_id,output1,output2", [('1','2', 'Exams', 2),
                                       ('2','1','Study',1 ),
                                       ('3','2','Today',2 ), ])
def test_list_post(output1,output2,listData,id,user_id):
    url = BASE+"list"
    payload = json.dumps(listData[id])
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)

    assert response.json()["name"]==output1
    assert response.json()["user_id"]==output2

################ Testing put for list

@pytest.mark.parametrize("id,output1,output2", [
    ('3', "Homework",2)])
def test_list_put(output1,output2, id):
    url = BASE+"list/"+id
    payload = json.dumps({
    "name": "Homework",
})
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("PUT", url, headers=headers, data=payload)
    assert response.json()["name"]==output1
    assert response.json()["user_id"]==output2


################ Testing get for list

@pytest.mark.parametrize("id,output1,output2", [
    ('3', 'Homework', 2)])
def test_list_get(output1,output2, id):
    url = BASE + "list/" + id

    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("GET", url, headers=headers)
    assert response.json()["name"]==output1
    assert response.json()["user_id"]==output2

################ Testing delete for list
#
@pytest.mark.parametrize("id,output1,output2", [
    ('3', 'Homework', 2)])
def test_list_delete(output1, output2, id):
    url = BASE + "list/" + id

    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("DELETE", url, headers=headers)
    assert response.json()["name"] == output1
    assert response.json()["user_id"] == output2


###########  TASKS TESTS  ###########

@pytest.mark.parametrize("id,output", [('1',{"id":1,"description": "presentation", "priority": "medium", "list_id":1}),
                                       ('2',{"id":2,"description": "quiz", "priority": "low", "list_id":1}, ),
                                       ('3',{"id":3,"description": "task 1", "priority": "high", "list_id":2}),
                                       ('4',{"id":4,"description": "Meeting", "priority": "medium", "list_id":1}),
                                       ])
def test_task_post(output,taskData,id):
    url = BASE+"task"
    payload = json.dumps(taskData[id])
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)

    assert response.json()==output


################ Testing put for tasks

@pytest.mark.parametrize("id,output", [
    ('1', {"id":1,"description": "presentation", "priority": "High", "list_id":1})])
def test_task_put(output, id):
    url = BASE+"task/"+id
    payload = json.dumps({
    "priority": "High",
})
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("PUT", url, headers=headers, data=payload)
    assert response.json()==output


################ Testing get for list

@pytest.mark.parametrize("id,output", [
    ('2',{"id":2,"description": "quiz", "priority": "low", "list_id":1} )])
def test_task_get(output, id):
    url = BASE + "task/" + id

    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("GET", url, headers=headers)
    assert response.json()==output
################ Testing delete for list

@pytest.mark.parametrize("id,output", [
    ('4', {"id": 4, "description": "Meeting", "priority": "medium", "list_id": 1})])
def test_task_delete(output, id):
    url = BASE + "task/" + id

    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("DELETE", url, headers=headers)
    assert response.json() == output


########### GET A USER'S LISTS (THROUGH USER ID) ###################

@pytest.mark.parametrize("id,output", [
    ('9', []),
    ('1', [{"id": 2,
            "last_edit": "Wed, 10 Aug 2022 13:05:06 -0000",
            "name": "Study",
            "start_date": "Wed, 10 Aug 2022 13:05:03 -0000",
            "user_id": 1}]),
    ('2', [{
        "id": 1,
        "last_edit": "Wed, 10 Aug 2022 13:05:06 -0000",
        "name": "Exams",
        "start_date": "Wed, 10 Aug 2022 13:05:03 -0000",
        "user_id": 2}]),

])
def test_user_list(output, id):
    url = BASE + id  # user id here

    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("GET", url, headers=headers)
    assert response.json() == output

########### GET A LIST'S TASKS (THROUGH LIST ID) ###################

@pytest.mark.parametrize("id,output", [
    ('7', []),

    ('1',[{
        "description": "quiz",
        "id": 2,
        "list_id": 1,
        "priority": "low"
    },
    {
        "description": "presentation",
        "id": 1,
        "list_id": 1,
        "priority": "High"
    }]),

    ('2', [{
        "description": "task 1",
        "id": 3,
        "list_id": 2,
        "priority": "high"
    }]),

])
def test_list_tasks(output, id):
    url = BASE+"tasks/" + id  # list id here

    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("GET", url, headers=headers)
    assert response.json() == output
