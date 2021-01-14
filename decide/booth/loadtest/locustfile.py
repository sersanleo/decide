import json

from random import choice

from locust import (
    HttpUser,
    SequentialTaskSet,
    TaskSet,
    task,
    between
)


HOST = "http://localhost:8000"


class DefSuggestions(SequentialTaskSet):

    def on_start(self):
        with open('users.json') as f:
            self.voters = json.loads(f.read())
        self.voter = choice(list(self.voters.items()))


    @task
    def login(self):
        response = self.client.get("/booth/")
        username, pwd = self.voter
        csrftoken = response.cookies['csrftoken']
        self.client.post("/booth/dashboard/", {'username': username, 'password': pwd, "csrfmiddlewaretoken": csrftoken},
                          headers={"X-CSRFToken": csrftoken},
                          cookies={"csrftoken": csrftoken})

    @task
    def suggestion(self):
        response = self.client.get('/booth/suggesting/')
        csrftoken = response.cookies['csrftoken']
        data = {'suggesting-title': 'Suggestsing', 'suggesting-date': "2025-12-12", 'suggesting-content': 'Full suggesting content...', "csrfmiddlewaretoken": csrftoken}
        self.client.post("/booth/suggesting/send/", data,
                            headers={"X-CSRFToken": csrftoken},
                            cookies={"csrftoken": csrftoken})


    def on_quit(self):
        self.voter = None



class Suggestions(HttpUser):
    host = HOST
    tasks = [DefSuggestions]
    wait_time= between(3,5)
