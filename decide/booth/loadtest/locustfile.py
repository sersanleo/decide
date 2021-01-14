import json
import datetime
from django.utils import timezone

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
        username, pwd = self.voter
        self.token = self.client.post("/authentication/login/", {
            "username": username,
            "password": pwd,
        }).json()

    @task
    def getuser(self):
        self.usr= self.client.post("/authentication/getuser/", self.token).json()
        print( str(self.user))

    # @task
    # def suggestion(self):
    #     headers = {
    #         'Authorization': 'Token ' + self.token.get('token'),
    #         'content-type': 'application/json'
    #     }
    #     self.client.post("/booth/suggesting/", json.dumps({
    #         "token": self.token.get('token'),
    #         "suggesting": {
    #             "user_id" : self.usr.get('id', None),
    #             "title" : "test",
    #             "suggesting_date" : "2021-12-12T00:00:00.000",
    #             "content" : "test",
    #             "send_date" : "2021-01-14T00:00:00.000"
    #         }
    #     }), headers=headers)


    def on_quit(self):
        self.voter = None



class Suggestions(HttpUser):
    host = HOST
    tasks = [DefSuggestions]
    wait_time= between(3,5)
