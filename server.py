from app import app
from constants_creating import constants_into_db

if __name__ == '__main__':
    constants_into_db()

    app.run(port=5000, debug=True, use_reloader=False)
