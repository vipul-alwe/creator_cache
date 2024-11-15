from __init__ import create_app  # Import create_app from __init__.py

app = create_app('development')  # Use 'production' for production environment

if __name__ == '__main__':
    app.run()
