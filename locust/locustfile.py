from locust import HttpUser, task

class HelloWorldUser(HttpUser):
    @task
    def hello_world(self):
        #self.client.get("v0/players/")
        self.client.get("v0/players/?first_name=Bryce&last_name=Young")
        self.client.get("v0/players/2009/")
        #self.client.get("v0/performances/?skip=0&limit=20000&minimum_last_changed_date=2024-04-01")
        self.client.get("v0/leagues/5002/")
        #self.client.get("v0/leagues/?skip=0&limit=500")
        #self.client.get("v0/teams/?skip=0&limit=500")
        #self.client.get("v0/teams/?skip=0&limit=500&league_id=5001")
        self.client.get("v0/counts/")