#-*- coding: utf-8 -*-

from multiprocessing import freeze_support
import sys
import main_window_gui


def main(self):
    global app
    app = main_window_gui.App(self)
    app.exec_()


if __name__ == '__main__':
    freeze_support()
    main(sys.argv)


