import os
import sys
import re 
from sys import platform
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QDialog, QMainWindow, QPushButton
from PyQt6.QtWidgets import QMessageBox
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6 import uic
from PySide6.QtCore import QFile, QIODevice
from PyQt6.QtGui import QFont
from logging import DEBUG
from util import logger
from util import convert
from controller.device import Device
from model.device_model import CARD_RESPONSE_CODE
log = logger.get_logger("App")

class MainWindow(QtWidgets.QMainWindow):
    
    def __init__(self, *args, **kwargs):
        log.info("__init__")   
        super().__init__(*args, **kwargs)
        app_path = os.path.dirname(os.path.abspath(sys.argv[0]))
        ui_path = os.path.join(app_path, "ui")
        ui_full_file_name = os.path.join(ui_path, "main.ui")
        self.device = Device()
        self.deviceList = self.device.get_device_list()
        self.ui = uic.loadUi(ui_full_file_name, self)
        
        # opening window in maximized size
        if platform == "linux" or platform == "linux2" or platform == "darwin":
            # linux
            # self.showFullScreen()
            self.setFont(QFont('.AppleSystemUIFont', 9))
        elif platform == "win32":
            # Windows...
            # self.showMaximized()
            self.setFont(QFont('MS Shell Dlg 2', 8))
            
        self.ui.disconnectButton.setEnabled(False)
        self.ui.readButton.setEnabled(False)
        self.ui.writeButton.setEnabled(False)
            
        self.fill_combo_box()
        """
        click connect to card
        """
        self.ui.connectButton.clicked.connect(self.worker_start)
        """
        click disconnect to card
        """
        self.ui.disconnectButton.clicked.connect(self.worker_stop)
        """
        click read button command
        """
        self.ui.readButton.clicked.connect(self.read_command)
        """
        click write button command
        """
        self.ui.writeButton.clicked.connect(self.write_command)
        
    def show_popup(self):
        msg = QMessageBox(text="Hello and Good Morning!",parent=self)
        msg.setIcon(QMessageBox.Icon.Question)
        msg.setStandardButtons(QMessageBox.StandardButton.Ok|
                               QMessageBox.StandardButton.Cancel)
        msg.setDefaultButton(QMessageBox.StandardButton.Ok)
 
        msg.setInformativeText("This is some extra informative text")
        msg.setDetailedText("Some Extra details.....\nCan be multi-line text")
 
        ret = msg.exec()
        
    def show_popup_tap_a_card(self):
        msg = QMessageBox(text="please tap a card from reader",parent=self)
        msg.setIcon(QMessageBox.Icon.Question)
        msg.setStandardButtons(QMessageBox.StandardButton.Ok|
                               QMessageBox.StandardButton.Cancel)
        ret = msg.exec()
        
    def show_popup_remove_card(self):
        msg = QMessageBox(text="please remove on card from reader",parent=self)
        msg.setIcon(QMessageBox.Icon.Question)
        msg.setStandardButtons(QMessageBox.StandardButton.Ok|
                               QMessageBox.StandardButton.Cancel)
        ret = msg.exec()
        
    def show_popup_write_success(self):
        msg = QMessageBox(text="write card success, please remove on card from reader",parent=self)
        msg.setIcon(QMessageBox.Icon.Question)
        msg.setStandardButtons(QMessageBox.StandardButton.Ok|
                               QMessageBox.StandardButton.Cancel)
        ret = msg.exec()
        
    def show_popup_write_error(self):
        msg = QMessageBox(text="write card error, please remove on card from reader",parent=self)
        msg.setIcon(QMessageBox.Icon.Question)
        msg.setStandardButtons(QMessageBox.StandardButton.Ok|
                               QMessageBox.StandardButton.Cancel)
        ret = msg.exec()

        
    def fill_combo_box(self):
        """
        fille reader list 
        """
        for readerIndex, readerItem in enumerate(self.deviceList):
            log.debug(f"fillCombox : get index {readerIndex} = {str(readerItem)}")
            # adding list of items to combo box
            self.ui.cbBoxDevice.addItem(str(readerItem))
            
    def worker_start(self):
        """
        work start control
        """
        self.ui.connectButton.setText("Connection")
        self.ui.connectButton.setEnabled(False)
        self.ui.disconnectButton.setEnabled(True)
        self.ui.readButton.setEnabled(True)
        self.ui.writeButton.setEnabled(True)
        
    def worker_stop(self):
        """
        work stop control
        """
        self.ui.connectButton.setText("Connect")
        self.ui.connectButton.setEnabled(True)
        self.ui.disconnectButton.setEnabled(False)
        self.ui.readButton.setEnabled(False)
        self.ui.writeButton.setEnabled(False)
        
    def read_command(self):
        """
        read command control
        """
        log.debug(f"read_command() : start")
        result, eventState = self.device.polling_card_detected()
        log.debug(f"read_command() : result = {result} , event state = {eventState}")
        if eventState == 'Card Present' :
            if not result : 
                self.ui.readLineEdit.setText('0')
            else:
                # uuidInt = convert.uuid_to_decimal(result)
                # log.debug(f"read_command() : uuid int = {str(uuidInt)}")
                log.debug(f"read_command() : tag info = {result} , type = {type(result)}")
                # # Remove leading 0 from Strings List
                # result.lstrip('0') 
                # zeros from a string  
                #regex = "^0+(?!$)"
                # Replaces the matched  
                # value with given string  
                #result = re.sub(regex, "", result)
                result = result.strip()[:5]
                self.ui.readLineEdit.setText(result)
            
        self.show_popup_remove_card()
            
        # if eventState == 'Card Present' :
        #     uuidInt = convert.uuid_to_decimal(result)
        #     log.debug(f"read_command() : uuid int = {str(uuidInt)}")
        #     self.ui.readLineEdit.setText(str(uuidInt))
            # self.device.load_auth_key()
        # if result != None:
        #     # call get card map to server
        #     log.debug(
        #         "call get Key from server to load authen key to reader")
        #     log.debug(f"result = {self.reader.loadAuthkey(testKey)}")
    

    def write_command(self):
        """
        write command control
        """
        value = self.ui.writeLineEdit.text()
        log.debug(f"write_command() : start with value {value}")
        resultCode, cardEvent = self.device.polling_write_tag(value)
        log.debug(f"write_command() : get a result {resultCode} , type = {type(resultCode)}")
        if resultCode != '144':
            self.show_popup_write_error()
        else:
            self.show_popup_write_success()
        # self.show_popup_remove_card()
        
        

app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()



