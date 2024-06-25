# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 6.6.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QFormLayout, QGridLayout,
    QGroupBox, QLabel, QLineEdit, QMainWindow,
    QPushButton, QSizePolicy, QStatusBar, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(407, 502)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_2 = QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        font = QFont()
        font.setPointSize(10)
        self.groupBox.setFont(font)
        self.formLayout_3 = QFormLayout(self.groupBox)
        self.formLayout_3.setObjectName(u"formLayout_3")
        self.cbBoxDevice = QComboBox(self.groupBox)
        self.cbBoxDevice.setObjectName(u"cbBoxDevice")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cbBoxDevice.sizePolicy().hasHeightForWidth())
        self.cbBoxDevice.setSizePolicy(sizePolicy)
        self.cbBoxDevice.setMinimumSize(QSize(250, 0))
        font1 = QFont()
        font1.setPointSize(14)
        font1.setBold(True)
        self.cbBoxDevice.setFont(font1)

        self.formLayout_3.setWidget(1, QFormLayout.LabelRole, self.cbBoxDevice)

        self.connectButton = QPushButton(self.groupBox)
        self.connectButton.setObjectName(u"connectButton")
        self.connectButton.setFont(font1)

        self.formLayout_3.setWidget(1, QFormLayout.FieldRole, self.connectButton)

        self.disconnectButton = QPushButton(self.groupBox)
        self.disconnectButton.setObjectName(u"disconnectButton")
        self.disconnectButton.setFont(font1)

        self.formLayout_3.setWidget(2, QFormLayout.FieldRole, self.disconnectButton)


        self.gridLayout_2.addWidget(self.groupBox, 0, 0, 1, 1)

        self.groupBox_2 = QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName(u"groupBox_2")
        font2 = QFont()
        font2.setBold(True)
        self.groupBox_2.setFont(font2)
        self.formLayout = QFormLayout(self.groupBox_2)
        self.formLayout.setObjectName(u"formLayout")
        self.label = QLabel(self.groupBox_2)
        self.label.setObjectName(u"label")
        font3 = QFont()
        font3.setPointSize(10)
        font3.setBold(True)
        self.label.setFont(font3)

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label)

        self.readLineEdit = QLineEdit(self.groupBox_2)
        self.readLineEdit.setObjectName(u"readLineEdit")
        self.readLineEdit.setFont(font1)

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.readLineEdit)

        self.readButton = QPushButton(self.groupBox_2)
        self.readButton.setObjectName(u"readButton")
        self.readButton.setFont(font1)

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.readButton)

        self.label_2 = QLabel(self.groupBox_2)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setFont(font3)

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_2)

        self.writeLineEdit = QLineEdit(self.groupBox_2)
        self.writeLineEdit.setObjectName(u"writeLineEdit")
        self.writeLineEdit.setFont(font1)

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.writeLineEdit)

        self.writeButton = QPushButton(self.groupBox_2)
        self.writeButton.setObjectName(u"writeButton")
        self.writeButton.setFont(font1)

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.writeButton)


        self.gridLayout_2.addWidget(self.groupBox_2, 1, 0, 1, 1)

        self.groupBox_3 = QGroupBox(self.centralwidget)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.groupBox_3.setFont(font2)
        self.formLayout_2 = QFormLayout(self.groupBox_3)
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.label_3 = QLabel(self.groupBox_3)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setFont(font)

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.label_3)

        self.readNoteLineEdit = QLineEdit(self.groupBox_3)
        self.readNoteLineEdit.setObjectName(u"readNoteLineEdit")
        font4 = QFont()
        font4.setPointSize(14)
        self.readNoteLineEdit.setFont(font4)

        self.formLayout_2.setWidget(0, QFormLayout.FieldRole, self.readNoteLineEdit)

        self.readNoteButton = QPushButton(self.groupBox_3)
        self.readNoteButton.setObjectName(u"readNoteButton")
        self.readNoteButton.setFont(font4)

        self.formLayout_2.setWidget(1, QFormLayout.FieldRole, self.readNoteButton)

        self.label_4 = QLabel(self.groupBox_3)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setFont(font)

        self.formLayout_2.setWidget(2, QFormLayout.LabelRole, self.label_4)

        self.writeNoteLineEdit_2 = QLineEdit(self.groupBox_3)
        self.writeNoteLineEdit_2.setObjectName(u"writeNoteLineEdit_2")
        self.writeNoteLineEdit_2.setFont(font4)

        self.formLayout_2.setWidget(2, QFormLayout.FieldRole, self.writeNoteLineEdit_2)

        self.writeNoteButton = QPushButton(self.groupBox_3)
        self.writeNoteButton.setObjectName(u"writeNoteButton")
        self.writeNoteButton.setFont(font4)

        self.formLayout_2.setWidget(3, QFormLayout.FieldRole, self.writeNoteButton)


        self.gridLayout_2.addWidget(self.groupBox_3, 2, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusBar = QStatusBar(MainWindow)
        self.statusBar.setObjectName(u"statusBar")
        MainWindow.setStatusBar(self.statusBar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"SIS Tools", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Device", None))
        self.connectButton.setText(QCoreApplication.translate("MainWindow", u"Connect", None))
        self.disconnectButton.setText(QCoreApplication.translate("MainWindow", u"Disconnect", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"Command - Coin Value", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Read  :  ", None))
        self.readButton.setText(QCoreApplication.translate("MainWindow", u"CMD", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Write  :  ", None))
        self.writeButton.setText(QCoreApplication.translate("MainWindow", u"CMD", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("MainWindow", u"Command - Note Box", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Read :", None))
        self.readNoteButton.setText(QCoreApplication.translate("MainWindow", u"CMD", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Write :", None))
        self.writeNoteButton.setText(QCoreApplication.translate("MainWindow", u"CMD", None))
    # retranslateUi

