from website import create_app

app = create_app()

# entry point to app
if __name__ == '__main__':
    app.run(debug=True, port="1111")