# # \file /src/fast_api/external_client.py
# -*- coding: utf-8 -*-
# ! .pyenv/bin/python3

""".. module:: src.fast_api.external_client
    :platform: Windows, Unix
    :synopsis: Example XML-RPC client for managing the Fast API server from external code."""

import sys
from xmlrpc.client import ServerProxy
import time

def main():
    """The main function for managing the server through RPC from the external code."""
    rpc_client = ServerProxy("http://localhost:9000", allow_none=True)
    
    try:
        # Example: Starting the server on port 8001
        print("Starting server on port 8001...")
        rpc_client.start_server(8001, "127.0.0.1")
        time.sleep(1)
        
        # Example: Adding a new route /test_route
        print("Adding new route /test_route...")
        rpc_client.add_new_route("/test_route", 'lambda: {"message": "Hello from test_route"}', ["GET"])
        time.sleep(1)

        # Example: obtaining server status
        print("Getting server status...")
        rpc_client.status_servers()
        time.sleep(1)

       # Example: Stop server on port 8001
        print("Stopping server on port 8001...")
        rpc_client.stop_server(8001)
        time.sleep(1)
        
        # Example: obtaining server status
        print("Getting server status...")
        rpc_client.status_servers()
        time.sleep(1)

    except Exception as ex:
        print(f"An error occurred: {ex}")
    finally:
        print("Shutting down RPC server")
        rpc_client.shutdown()


if __name__ == "__main__":
    main()