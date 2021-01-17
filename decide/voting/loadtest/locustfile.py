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
VOTING = 1


class DefVisualizer(TaskSet):

    @task
    def index(self):
        self.client.get("/visualizer/{0}/".format(VOTING))


class DefVoters(SequentialTaskSet):

    def on_start(self):
        with open('voters.json') as f:
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


    #Tanto el add Census como la prueba de carga de realizar los votos se arregló para que funcionara con el proyecto
    #pero revisandolo vimos que a veces funcionaba y a veces no, por lo que hemos decidido comentarlo. Otros grupos
    #han ejecutado el mismo script y les ha funcionado,pero el grupo de Votaciones no ha sido capaz de ejecutar
    #este script en concreto correctamente.
    
    # @task
    # def voting(self):
    #     headers = {
    #         'Authorization': 'Token ' + self.token.get('token'),
    #         'content-type': 'application/json'
    #     }
    #     self.client.post("/store/", json.dumps({
    #         "token": self.token.get('token'),
            
    #         "vote": [{

    #             "a": "26766770314130064448264689161073846195046803359538529753921744094104381808669",
    #             "b": "43647514762102078828207848685222092192010819214482157652559720982397432213736"
    #         }],
    #         "voter": self.usr.get('id'),
    #         "voting": VOTING,
    #         'question_id': 1
    #     }), headers=headers)


    def on_quit(self):
        self.voter = None

class Visualizer(HttpUser):
    host = HOST
    tasks = [DefVisualizer]
    wait_time = between(3,5)



class Voters(HttpUser):
    host = HOST
    tasks = [DefVoters]
    wait_time= between(3,5)
