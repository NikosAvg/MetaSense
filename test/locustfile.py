from locust import HttpUser, task, between

class StressTestUser(HttpUser):
    wait_time = between(1, 5)  # Wait time between tasks (1 to 5 seconds)

    @task(2)
    def get_projects(self):
        """Stress test the GET /projects endpoint."""
        self.client.get("/api/projects")

    @task(2)
    def get_sensors(self):
        """Stress test the GET /sensors endpoint."""
        self.client.get("/api/sensors")

    @task(1)
    def create_project(self):
        """Stress test the POST /projects endpoint."""
        self.client.post(
            "/api/projects",
            json={"name": "Stress Test Project", "description": "Created during stress test"}
        )

    @task(1)
    def create_sensor(self):
        """Stress test the POST /sensors endpoint."""
        # Fetch a project ID to associate with the sensor
        response = self.client.get("/api/projects")
        if response.status_code == 200 and response.json():
            project_id = response.json()[0]["id"]  # Use the first project
            self.client.post(
                "/api/sensors",
                json={
                    "name": "Stress Test Sensor",
                    "type": "Temperature",
                    "project_id": project_id,
                    "extra_data": '{"unit": "Celsius"}'
                }
            )

    @task(1)
    def create_sensor_data(self):
        """Stress test the POST /sensor_data endpoint."""
        # Fetch a sensor ID to associate with the sensor data
        response = self.client.get("/api/sensors")
        if response.status_code == 200 and response.json():
            sensor_id = response.json()[0]["id"]  # Use the first sensor
            self.client.post(
                "/api/sensor_data",
                json={
                    "sensor_id": sensor_id,
                    "timestamp": "2024-01-01T12:00:00",
                    "value": 25.5,
                    "unit": "Celsius",
                    "extra_data": '{"location": "Room 1"}'
                }
            )

    @task(1)
    def delete_project(self):
        """Stress test the DELETE /projects endpoint."""
        response = self.client.get("/api/projects")
        if response.status_code == 200 and response.json():
            project_id = response.json()[0]["id"]  # Use the first project
            self.client.delete(f"/api/projects/{project_id}")
