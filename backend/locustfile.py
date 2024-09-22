from locust import HttpUser, task, between
from random import choice

class LearningPlatformUser(HttpUser):
    wait_time = between(1, 5)

    def on_start(self):
        response = self.client.post("/api/auth/login", json={
            "email": "testuser@example.com",
            "password": "password123"
        })
        self.token = response.json()["access_token"]

    @task
    def view_dashboard(self):
        self.client.get("/api/dashboard", headers={"Authorization": f"Bearer {self.token}"})

    @task
    def get_learning_materials(self):
        self.client.get("/api/learning-materials", headers={"Authorization": f"Bearer {self.token}"})

    @task
    def update_progress(self):
        self.client.post("/api/progress", json={
            "material_id": 1,
            "progress": 50
        }, headers={"Authorization": f"Bearer {self.token}"})

    @task
    def get_notifications(self):
        self.client.get("/api/notifications", headers={"Authorization": f"Bearer {self.token}"})

    @task
    def create_notification(self):
        self.client.post("/api/notifications", json={
            "message": "Test notification",
            "type": choice(["info", "alert", "warning"])
        }, headers={"Authorization": f"Bearer {self.token}"})

    @task
    def mark_notification_as_read(self):
        response = self.client.get("/api/notifications", headers={"Authorization": f"Bearer {self.token}"})
        notifications = response.json()
        if notifications:
            notification_id = notifications[0]["id"]
            self.client.put(f"/api/notifications/{notification_id}", headers={"Authorization": f"Bearer {self.token}"})