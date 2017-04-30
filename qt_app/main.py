import sys
sys.path.append('./model')
sys.path.append('./view')
sys.path.append('./controller')

from model import Model
from view import View
from controller import Controller



import PyQt4.QtCore
import PyQt4.QtGui

class App(PyQt4.QtGui.QApplication):
    def __init__(self, sys_argv):
        super(App, self).__init__(sys_argv)

        self.model = Model()
        self.view = View()
        self.controller = Controller(self.model, self.view)
        self.view.set_defaults()



        self.view.show()

def main():
    app = App(sys.argv)
    app.exec_()
    sys.exit()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
