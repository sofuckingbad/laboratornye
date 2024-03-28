import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from random import choices

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('form.ui', self)
        self.reset.clicked.connect(self.res)
        self.gener.clicked.connect(self.gen)

    def gen(self):
        DIGIT = '123456789'
        ALPHA_LOWER = 'qwertyiopasdfghjklzxcvbnm'
        ALPHA_UPPER = ALPHA_LOWER.upper()
        SYMBOL = '!@#$%^&*()_+<>'
        line = ''
        if self.digit.isChecked():
            line += DIGIT
        if self.alpha.isChecked():
            line += ALPHA_LOWER + ALPHA_UPPER
        if self.symbol.isChecked():
            line += SYMBOL
        data = []
        for elem in range(self.coun_pass.value()):
            data.append(''.join(choices(line, k=self.coun_sim.value())))
        fname, _ = QFileDialog.getSaveFileName(self, 'Сохранить', '/pass.txt')
        if fname:
            with open(fname, 'w') as f:
                for elem in data:
                    f.write(elem)
                    f.write('\n')

    def res(self):
        self.coun_pass.setValue(0)
        self.coun_sim.setValue(0)
        self.digit.setChecked(False)
        self.alpha.setChecked(False)
        self.symbol.setChecked(False)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())