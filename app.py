from app import app

from app.controllers import user_controller, app_controller
from app.services import database

if __name__ == "__main__":
    app.run(debug=True)