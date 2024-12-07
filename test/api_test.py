import unittest
import requests

BASE_URL = "http://localhost:5000/api"


class APITestCase(unittest.TestCase):
    def setUp(self):
        """Set up test data"""
        self.project_data = {"name": "Test Project", "description": "A project for testing"}
        self.sensor_data = {
            "name": "Test Sensor",
            "type": "Temperature",
            "project_id": None,  # Assigned dynamically
            "extra_data": "{\"unit\": \"Celsius\"}"
        }
        self.sensor_data_entry = {
            "sensor_id": None,  # Assigned dynamically
            "timestamp": "2024-01-01T12:00:00",
            "value": 23.5,
            "unit": "Celsius",
            "extra_data": "{\"location\": \"Room 1\"}"
        }

    def test_project_crud(self):
        """Test CRUD operations for projects"""
        # Create a project
        response = requests.post(f"{BASE_URL}/projects", json=self.project_data)
        print("Create Project Response:", response.json())
        project_id = response.json().get("id")
        if not project_id:
            self.fail(f"Failed to create project: {response.json()}")

        # Read the project
        response = requests.get(f"{BASE_URL}/projects/{project_id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], self.project_data["name"])

        # Update the project
        updated_data = {"name": "Updated Project", "description": "Updated description"}
        response = requests.put(f"{BASE_URL}/projects/{project_id}", json=updated_data)
        self.assertEqual(response.status_code, 200)

        # Verify the update
        response = requests.get(f"{BASE_URL}/projects/{project_id}")
        self.assertEqual(response.json()["name"], "Updated Project")

        # Delete the project
        response = requests.delete(f"{BASE_URL}/projects/{project_id}")
        self.assertEqual(response.status_code, 200)

        # Verify deletion
        response = requests.get(f"{BASE_URL}/projects/{project_id}")
        self.assertEqual(response.status_code, 404)

    def test_sensor_crud(self):
        """Test CRUD operations for sensors"""
        # Create a project for the sensor
        response = requests.post(f"{BASE_URL}/projects", json=self.project_data)
        project_id = response.json().get("id")
        if not project_id:
            self.fail(f"Failed to create project: {response.json()}")
        self.sensor_data["project_id"] = project_id

        # Create a sensor
        response = requests.post(f"{BASE_URL}/sensors", json=self.sensor_data)
        print("Create Sensor Response:", response.json())
        sensor_id = response.json().get("id")
        if not sensor_id:
            self.fail(f"Failed to create sensor: {response.json()}")

        # Read the sensor
        response = requests.get(f"{BASE_URL}/sensors/{sensor_id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], self.sensor_data["name"])

        # Update the sensor
        updated_data = {"name": "Updated Sensor", "type": "Humidity", "project_id": project_id, "extra_data": "{}"}
        response = requests.put(f"{BASE_URL}/sensors/{sensor_id}", json=updated_data)
        self.assertEqual(response.status_code, 200)

        # Verify the update
        response = requests.get(f"{BASE_URL}/sensors/{sensor_id}")
        self.assertEqual(response.json()["name"], "Updated Sensor")

        # Delete the sensor
        response = requests.delete(f"{BASE_URL}/sensors/{sensor_id}")
        self.assertEqual(response.status_code, 200)

        # Verify deletion
        response = requests.get(f"{BASE_URL}/sensors/{sensor_id}")
        self.assertEqual(response.status_code, 404)

    def test_sensor_data_crud(self):
        """Test CRUD operations for sensor data"""
        # Create a project and sensor for the sensor data
        project_response = requests.post(f"{BASE_URL}/projects", json=self.project_data)
        project_id = project_response.json().get("id")
        if not project_id:
            self.fail(f"Failed to create project: {project_response.json()}")
        self.sensor_data["project_id"] = project_id

        sensor_response = requests.post(f"{BASE_URL}/sensors", json=self.sensor_data)
        sensor_id = sensor_response.json().get("id")
        if not sensor_id:
            self.fail(f"Failed to create sensor: {sensor_response.json()}")
        self.sensor_data_entry["sensor_id"] = sensor_id

        # Create sensor data
        response = requests.post(f"{BASE_URL}/sensor_data", json=self.sensor_data_entry)
        print("Create Sensor Data Response:", response.json())
        data_id = response.json().get("id")
        if not data_id:
            self.fail(f"Failed to create sensor data: {response.json()}")

        # Read sensor data
        response = requests.get(f"{BASE_URL}/sensor_data/{data_id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["value"], self.sensor_data_entry["value"])

        # Update sensor data
        updated_data = {
            "sensor_id": sensor_id,
            "timestamp": "2024-01-01T13:00:00",
            "value": 25.0,
            "unit": "Celsius",
            "extra_data": "{}"
        }
        response = requests.put(f"{BASE_URL}/sensor_data/{data_id}", json=updated_data)
        self.assertEqual(response.status_code, 200)

        # Verify the update
        response = requests.get(f"{BASE_URL}/sensor_data/{data_id}")
        self.assertEqual(response.json()["value"], 25.0)

        # Delete sensor data
        response = requests.delete(f"{BASE_URL}/sensor_data/{data_id}")
        self.assertEqual(response.status_code, 200)

        # Verify deletion
        response = requests.get(f"{BASE_URL}/sensor_data/{data_id}")
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
