from locust import HttpLocust, TaskSet
import json

def conjugate(l):
    headers = {"Content-Type": "application/json"}
    l.client.get('/api/v1/conjugate?verb=athonte&patient=1-sg', headers=headers)

def index(l):
    l.client.get("/")

def affix(l):
    l.client.get("/api/v1/affixes")

def aspect(l):
    l.client.get("/api/v1/aspect_affixes")

def tmp(l):
    l.client.get("/api/v1/tmp_affixes")

def verb(l):
    l.client.get("/api/v1/verbs")

def pronoun(l):
    l.client.get("/api/v1/pronouns")

class UserBehavior(TaskSet):
    tasks = {index: 2, pronoun: 1, affix: 3, tmp: 2}

    def on_start(self):
        conjugate(self)

class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 5000
    max_wait = 9000