import requests
import json

class XAI:
    def __init__(self, api_key):
        """The initialization of the XII class.

        : Param API_KEY: API key for authentication."""
        self.api_key = api_key
        self.base_url = "https://api.x.ai/v1"  # Basic URL API
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def _send_request(self, method, endpoint, data=None):
        """Sending a request to the API X.Ai.

        : Param Method: HTTP method (Get, Post, Put, Delete).
        : Param Endpoint: end point API.
        : Param Data: Data for sending a request in the body (for Post and PUT).
        : Return: answer from the API."""
        url = f"{self.base_url}/{endpoint}"
        response = requests.request(method, url, headers=self.headers, json=data)
        response.raise_for_status()  # Throws an exception if the status of an answer is not 2xx
        return response.json()

    def chat_completion(self, messages, model="grok-beta", stream=False, temperature=0):
        """Request to complete the chat.

        : Param Messages: Chat Messages List.
        : Param Model: Model for use.
        : Param Stream: flag for turning on stream gear.
        : Param Temperature: The temperature for generating an answer.
        : Return: answer from the API."""
        endpoint = "chat/completions"
        data = {
            "messages": messages,
            "model": model,
            "stream": stream,
            "temperature": temperature
        }
        response = self._send_request("POST", endpoint, data)
        return response

    def stream_chat_completion(self, messages, model="grok-beta", temperature=0):
        """Request to complete the chat with streaming.

        : Param Messages: Chat Messages List.
        : Param Model: Model for use.
        : Param Temperature: The temperature for generating an answer.
        : Return: The flow of answers from the API."""
        endpoint = "chat/completions"
        data = {
            "messages": messages,
            "model": model,
            "stream": True,
            "temperature": temperature
        }
        url = f"{self.base_url}/{endpoint}"
        response = requests.post(url, headers=self.headers, json=data, stream=True)
        response.raise_for_status()
        return response.iter_lines(decode_unicode=True)

# An example of using the XII class
if __name__ == "__main__":
    api_key = "your_api_key_here"  # Replace with your real API key
    xai = XAI(api_key)

    messages = [
        {
            "role": "system",
            "content": "You are Grok, a chatbot inspired by the Hitchhikers Guide to the Galaxy."
        },
        {
            "role": "user",
            "content": "What is the answer to life and universe?"
        }
    ]

    # Non -flowing request
    completion_response = xai.chat_completion(messages)
    print("Non-streaming response:", completion_response)

    # Streaming request
    stream_response = xai.stream_chat_completion(messages)
    print("Streaming response:")
    for line in stream_response:
        if line.strip():
            print(json.loads(line))