import maestro
import servo
import face
from PyQt5.QtWidgets import QMainWindow, QApplication
from marie_curie_gui import Ui_MainWindow

class MarieGui(Ui_MainWindow):
    def __init__(self, controller, window):
        Ui_MainWindow.__init__(self)
        self.setupUi(window)
        self.controller = controller
        self.face = face.Face(self.controller)
        expression_names = [name.capitalize() for name in self.face.get_expression_names()]
        self.expressionComboBox.addItems(expression_names)
        self.pushButton.clicked.connect(self.user_rq_expression_perf)

    def user_rq_expression_perf(self):
        print('in callback')
        exp_name = self.expressionComboBox.currentText().lower()
        print(exp_name)
        self.face.perform_expression(exp_name)


def main():
    app = QApplication([])
    controller = maestro.Controller()
    window = QMainWindow()
    ui = MarieGui(controller, window)
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()
    