import sys
from threading import Thread

from constants_creating import constants_into_db

from app import app
from desktop import QApplication, Application

if __name__ == '__main__':
    constants_into_db()

    server_thread = Thread(target=app.run, daemon=True, kwargs={'port': 5000,
                                                                'threaded': True,
                                                                'debug': True,
                                                                'use_reloader': False}).start()

    desktop_app = QApplication(sys.argv)
    ex = Application()
    ex.show()
    sys.exit(desktop_app.exec_())
