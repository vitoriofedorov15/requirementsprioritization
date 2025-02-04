from PyQt5.QtWidgets import QApplication, QFileDialog, QPushButton, QLabel, QVBoxLayout, QWidget


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.label = QLabel("Выберите CSV-файл с данными")
        layout.addWidget(self.label)

        self.btn_load = QPushButton("Загрузить файл", self)
        self.btn_load.clicked.connect(self.load_file)
        layout.addWidget(self.btn_load)

        self.setLayout(layout)
        self.setWindowTitle("Приоритизация требований")
        self.show()

    def load_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Выберите файл")
        self.label.setText(f"Выбран файл: {file_name}")


if __name__ == '__main__':
    app = QApplication([])
    ex = App()
    app.exec_()
