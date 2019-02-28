# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets


class Widget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        layout = QtWidgets.QVBoxLayout()
        items = [(0, 'Python'), (1, 'Golang'), (2, 'JavaScript'), (3, 'Ruby')]
        for id_, txt in items:
            checkBox = QtWidgets.QCheckBox(txt, self)
            checkBox.id_ = id_
            checkBox.stateChanged.connect(self.checkLanguage)  # 1
            layout.addWidget(checkBox)

        self.lMessage = QtWidgets.QLabel(self)
        layout.addWidget(self.lMessage)
        self.setLayout(layout)

    def checkLanguage(self, state):
        checkBox = self.sender()
        if state == QtCore.Qt.Unchecked:
            self.lMessage.setText(u'取消选择了{0}: {1}'.format(
                checkBox.id_, checkBox.text()))
        elif state == QtCore.Qt.Checked:
            self.lMessage.setText(u'选择了{0}: {1}'.format(
                checkBox.id_, checkBox.text()))


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    widget = Widget()
    widget.show()
    sys.exit(app.exec_())
