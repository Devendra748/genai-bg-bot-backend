from fastapi.testclient import TestClient
from app import app
from search_data_module import SearchDataPayload

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to my chatbot app!"}

def test_search_data_handler():
    # Test case for a successful query with caching enabled
    payload = SearchDataPayload(
        question="Your test question",
        bot_name="YourBotName",
        language="English",
        chat_history=[
            {"question": "Previous question", "answer": "Previous answer"}
            # Add more chat history as needed
        ],
        enable_cache=True,
        similarity_cutoff=0.9
    )
    response = client.post("/bot/query", json=payload.dict())
    assert response.status_code == 200
    assert "result" in response.json()
    assert "status" in response.json()
    assert response.json()["status"]["code"] == 0
    assert "success" in response.json()["status"]["message"]

    # Add more assertions based on your expected response format and data

    # Test case for a successful query with caching disabled
    payload.enable_cache = False
    response = client.post("/bot/query", json=payload.dict())
    assert response.status_code == 200
    # Add assertions for response without caching
    
    # Add more test cases for different scenarios (e.g., invalid input, edge cases)

def test_search_data_handler():
    payload = {"question": "Test question", "bot_name": "TestBot", "language": "English"}
    response = client.post("/bot/query", json=payload)
    assert response.status_code == 200
    # Add more assertions based on your expected response


def test_delete_data_handler_invalid_input():
    # Test deleting a class with invalid input (e.g., empty classname)
    response = client.post("/delete_data", json={"classname": ""})
    assert response.status_code == 422
    # Add more assertions based on you

    # Add more test cases for different scenarios (e.g., invalid input, edge cases)

def test_search_data_handler_invalid_input():
    # Test case for invalid input (e.g., missing required fields)
    response = client.post("/bot/query", json={})
    assert response.status_code == 422
    # Add more assertions based on your expected response for invalid input


def test_delete_data_handler_invalid_input():
    # Test case for deleting data with invalid input (e.g., empty classname)
    response = client.post("/delete_data", json={"classname": ""})
    assert response.status_code == 422
    # Add more assertions based on your expected response for invalid input

def test_search_data_handler_no_history():
    # Test case for a successful query with no chat history
    payload = SearchDataPayload(
        question="Your test question",
        bot_name="YourBotName",
        language="English",
        enable_cache=True,
        similarity_cutoff=0.9
    )
    response = client.post("/bot/query", json=payload.dict())
    assert response.status_code == 200
    # Add assertions based on your expected response for a query with no chat history


def test_search_data_handler_low_similarity():
    # Test case for a query with low similarity
    payload = SearchDataPayload(
        question="Your test question",
        bot_name="YourBotName",
        language="English",
        chat_history=[
            {"question": "Previous question", "answer": "Previous answer"}
        ],
        enable_cache=True,
        similarity_cutoff=0.99  # Set a high similarity cutoff intentionally
    )
    response = client.post("/bot/query", json=payload.dict())
    assert response.status_code == 200
    # Add assertions based on your expected response for a query with low similarity

# Add more test functions as needed

