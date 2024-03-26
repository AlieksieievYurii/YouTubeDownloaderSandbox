from src import create_app

if __name__ == "__main__":
    # This is essential to set host to 0.0.0.0
    # if we want to make the server listen to external incoming requests
    create_app().run("0.0.0.0", port=5000)
