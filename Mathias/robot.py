import sys
import os
# sys.path.append("../zAxis/Python") # Adds higher directory to python modules path.
# sys.path.append("~/Documents/Buffer") # Adds higher directory to python modules path.
# sys.path.append("../../Buffer") # Adds higher directory to python modules path.
import time
from PyQt5 import QtWidgets, uic , QtCore  
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from portRecognition import findArduinoPort
from sc import usbCommunication

class WorkerSignals(QObject):
    '''
    Defines the signals available from a running worker thread.

    Supported signals are:

    finished
        No data
    
    error
        `tuple` (exctype, value, traceback.format_exc() )
    
    result
        `object` data returned from processing, anything

    progress
        `int` indicating % progress 

    '''
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    progress = pyqtSignal(int)

class Worker(QRunnable):
    '''
    Worker thread

    Inherits from QRunnable to handler worker thread setup, signals and wrap-up.

    :param callback: The function callback to run on this worker thread. Supplied args and 
                     kwargs will be passed through to the runner.
    :type callback: function
    :param args: Arguments to pass to the callback function
    :param kwargs: Keywords to pass to the callback function

    '''

    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()

        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()    

        # Add the callback to our kwargs
        #self.kwargs['progress_callback'] = self.signals.progress        

    @pyqtSlot()
    def run(self):
        '''
        Initialise the runner function with passed args, kwargs.
        '''
        
        # Retrieve args/kwargs here; and fire processing using them
        try:
            result = self.fn(*self.args, **self.kwargs)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)  # Return the result of the processing
        finally:
            self.signals.finished.emit()  # Done


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self,resWidth,resHeight, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        #Load the UI Page
        uic.loadUi('robot.ui', self)
        try:
            SerialNumber = "757353036313511191B2" #zAxis serial number. 
            BAUD_RATE = 500000
            self.arduino = usbCommunication(SerialNumber, BAUD_RATE)
        except Exception as e:
            print("Arduino error")
            print(e)


        # Start worker threds
        self.threadpool = QThreadPool()
        print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())
        # self.startWorkers()   
        # self.dial.sliderPressed.connect(self.dialChange)    
        self.dial.valueChanged.connect(self.dialChange)
        self.verticalSlider.valueChanged.connect(self.sliderChange)
        self.show()

        #-------------------TIMERS--------------------------------------------------------------------
        # timer for handling slider to set Velocity Limits
        self.timer = QTimer()
        self.timer.setInterval(100)
        # self.timer.timeout.connect(self.checkAnalogValue)
        # self.timer.start()
        # self.startWorkers()

        ## Måns
        self.pushButton_sendDegrees1.clicked.connect(self.sendDegrees)
        #self.pushButton_sendDegrees2.clicked.connect(lambda: self.sendDegrees(2))
    # def startWorkers(self):
    #     worker_checkAnalogValue = Worker(self.checkAnalogValue)
    #     self.threadpool.start(worker_checkAnalogValue)
    #     worker_checkAnalogValue.signals.finished.connect(self.startWorkers)

    def sendDegrees(self):
        stepper_0_angle=self.spinBox.value()
        stepper_1_angle=self.spinBox_2.value()
        angle_value_list = [str(stepper_0_angle),str(stepper_1_angle)]    
        send_string = ','.join(angle_value_list)
        send_string += "\n"

        self.lcdA1.display(self.spinBox.value())

        self.lcdA2.display(self.spinBox_2.value())
        

    def dialChange(self):
        # print(self.dial.value())
        msg = "p"+str(self.dial.value())
        # print(msg)
        self.arduino.sendMessage(msg) 
        # self.arduino.readMessage()

    def sliderChange(self):
        # print(self.verticalSlider.value())
        msg = "p"+str(self.verticalSlider.value())
        # print(msg)
        self.arduino.sendMessage(msg) 
        # self.arduino.readMessage()

    # def meassurePin(self,pin):
    #     self.arduino.sendMessage(pin)
    #     msg = self.arduino.returnMessage()
    #     print("msg=",msg)
    #     msg = self.arduino.returnMessage()
    #     print("msg=",msg)
    #     try:
    #         msg2=int(msg)   
    #         return msg2*5/1023         
    #         # print("msg2=",msg2)
    #     except Exception as exp:
    #         print(exp)
        

    # def checkAnalogValue(self):
    #     self.arduino.readMessage()
    #     self.lcdA1.display(self.meassurePin("A1"))
    #     # self.arduino.sendMessage("A1\r\n") 
    #     # time.sleep(0.1)
    #     # msg = self.arduino.returnMessage()
    #     # print("msg=",msg)
    #     # if (msg == "A1"):
    #     #     msg = self.arduino.returnMessage()
    #     #     print("msg1=",msg)
    #     #     # print(type(msg))
    #     #     try:
    #     #         msg2=int(msg)
    #     #         self.lcdA1.display((msg2*5/1023))
    #     #         # print("msg2=",msg2)
    #     #     except Exception as exp:
    #     #         print(exp)
    #     time.sleep(0.2)
        
        # self.lcdNumber.display(2)

def main():
    global window
    app = QtWidgets.QApplication(sys.argv)
    screen_resolution = app.desktop().screenGeometry()
    width, height = screen_resolution.width(), screen_resolution.height()
    print(width)
    print(height)
    window = MainWindow(width,height)
    # window.setMaximumWidth(width)
    # window.setMaximumHeight(height)
    # window.setMinimumWidth(width)
    # window.setMinimumHeight(height)
    
    #global b 
    #b = MainWindow()
    #b= QtWidgets.QApplication.processEvents()
    #window.show()       
    sys.exit(app.exec_())    
    
if __name__ == '__main__':   
    #while(True):
     #   print("hej")     
    # timer = QTimer()
    # timer.timeout.connect(lambda: None)
    # timer.start(100)
    main()
