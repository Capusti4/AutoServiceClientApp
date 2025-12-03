from PySide6.QtWidgets import QApplication

from WorkerApp.router import Router

if __name__ == "__main__":
    app = QApplication([])
    router = Router()
    router.show()

    app.exec()
