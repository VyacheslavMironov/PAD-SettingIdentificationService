from api.app import app, DEBUG, PORT, HOST


if __name__ == "__main__":
    app.run(host=HOST, port=PORT, debug=DEBUG)
