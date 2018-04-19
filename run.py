from app import create_app

config_name = 'development'

app = create_app(config_name)

if __name__ == '__main__':
    app.run(debug=False, use_debugger=False, port=8083)
