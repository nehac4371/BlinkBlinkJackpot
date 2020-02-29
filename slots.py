from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import queue
import time
import random
import os
import sys
import threading
import subprocess
import WidgetMachine as SlotM
from blinking import q,CamTracker
from cv import camera


class MyImageViewerWidget(QFrame):
    def __init__(self,*args):
        super(MyImageViewerWidget, self).__init__(*args)
        self.setGeometry(0, 0, 800, 600)
        self.ui = SlotM.Ui_Form()
        self.ui.setupUi(self)
        self.cpt = 0
        ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(ROOT_DIR, "slot_machine_symbols.png")
        self.px = QPixmap(path)

        self.x = [0, 0, 0, 300, 300, 300, 600, 600, 600]
        self.y = [0, 300, 600, 0, 300, 600, 0, 300, 600]

        rect = QRect(0, 0, 300, 300)
        cropped = self.px.copy(rect)
        self.ui.mLabel.setPixmap(cropped)
        self.ui.mLabel2.setPixmap(cropped)
        self.ui.mLabel3.setPixmap(cropped)


        

    def spin(self):
        q_cnt = 0
        for i in range(0, 200):
            time.sleep((50 + 25 * 9) / 1000)
            
            
            if q.empty() == False:
                q_cnt = q.get() 
            
            #print('slots q_cnt:',q_cnt)
            if q_cnt < 1:
                #print('Blink 1:',q_cnt)

                a = random.randint(0, len(self.x) - 1)
                self.rect = QRect(self.x[a], self.y[a], 300, 300)
                cropped = self.px.copy(self.rect)
                self.ui.mLabel.setPixmap(cropped)

                b = random.randint(0, len(self.x) - 1)
                self.rect = QRect(self.x[b], self.y[b], 300, 300)
                cropped = self.px.copy(self.rect)
                self.ui.mLabel2.setPixmap(cropped)

                c = random.randint(0, len(self.x) - 1)
                self.rect = QRect(self.x[c], self.y[c], 300, 300)
                cropped = self.px.copy(self.rect)
                self.ui.mLabel3.setPixmap(cropped)

            elif q_cnt < 2:
                #print('Blink 2:',q_cnt)
                b = random.randint(0, len(self.x) - 1)
                self.rect = QRect(self.x[b], self.y[b], 300, 300)
                cropped = self.px.copy(self.rect)
                self.ui.mLabel2.setPixmap(cropped)

                c = random.randint(0, len(self.x) - 1)
                self.rect = QRect(self.x[c], self.y[c], 300, 300)
                cropped = self.px.copy(self.rect)
                self.ui.mLabel3.setPixmap(cropped)

            elif q_cnt < 3:
                #print('Blink 3:',q_cnt)

                c = random.randint(0, len(self.x) - 1)
                self.rect = QRect(self.x[c], self.y[c], 300, 300)
                cropped = self.px.copy(self.rect)
                self.ui.mLabel3.setPixmap(cropped)
                
            elif q_cnt >=3:
                break
            QApplication.processEvents()
        
        
        self.cpt += 1
        if a == b and c == b:
            print("===============")
            print("=== JACKPOT ===")
            print("===============")

        else:
            print("game over, " + str(self.cpt) + " games played")
        
        if self.cpt >1:
            return
            


class MyMainWindow(QMainWindow):

    def __init__(self , parent=None):
        
        QWidget.__init__(self, parent=parent)
        # attributs de la fenetre principale
        #self.q = queue.Queue()
        self.setGeometry(500, 450, 940, 320)
        self.setFixedSize(940, 320)
        self.setWindowTitle('Slot Machine')

        self.mDisplay = MyImageViewerWidget(self)

    

    def keyPressEvent(self, e):
        #print('inside KeyPress')
        if e.key() == QtCore.Qt.Key_Space:
            self.mDisplay.spin()



def QTWin():
    app = QApplication(sys.argv)
    w = MyMainWindow()
    #w.get_que(q)
    w.show()
    app.exec_()


C = CamTracker()
c1 = camera()

t1 = threading.Thread(target = C.start)
t2 = threading.Thread(target = QTWin)
t3 = threading.Thread(target = c1.start)

t2.start()
t1.start()
t3.start()

t2.join() 
t1.join()  