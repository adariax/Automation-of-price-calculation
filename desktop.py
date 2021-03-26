import sys

from desktop import QApplication, Application

if __name__ == '__main__':
    desktop_app = QApplication(sys.argv)
    ex = Application()
    ex.show()
    sys.exit(desktop_app.exec_())
