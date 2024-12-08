from locust import HttpUser, between, task
from bs4 import BeautifulSoup  # For extracting CSRF token if needed

class MyUser(HttpUser):
    host = "http://127.0.0.1:5000"  # Specify your Flask app's host here
    wait_time = between(1, 5)

    @task
    def login(self):
        # Step 1: First, retrieve the login page to get any CSRF token
        response = self.client.get("/login")
        soup = BeautifulSoup(response.text, "html.parser")

        # Step 2: Extract CSRF token if present
        csrf_token = None
        csrf_input = soup.find("input", {"name": "csrf_token"})  # Adjust if needed
        if csrf_input:
            csrf_token = csrf_input["value"]

        # Step 3: Prepare login data
        data = {
            "name": "testuser",  # Adjust the username as needed
            "password": "password123",  # Adjust the password as needed
        }

        # Include CSRF token if necessary
        if csrf_token:
            data["csrf_token"] = csrf_token

        # Step 4: Send the login request with the form data
        response = self.client.post("/login", data=data)

        # Step 5: Check if login was successful
        if response.status_code == 200:
            print("Login successful")
            self.leaderboard()  # If login is successful, access the leaderboard page
        else:
            print(f"Login failed with status code {response.status_code}")
            print(f"Response body: {response.text}")

    @task
    def leaderboard(self):
        # Step 6: After logging in, access the leaderboard page
        response = self.client.get("/leaderboard")
        if response.status_code == 200:
            print("Leaderboard fetched successfully")
        else:
            print(f"Failed to fetch leaderboard: {response.status_code}")

    @task
    def some_other_page(self):
        self.client.get("/register")  # Example of another page to test
