"""
Gateway service. This is an entrypoint to the API
"""

from src import create_app

if __name__ == "__main__":
    create_app().run(host="0.0.0.0", port=8080)
