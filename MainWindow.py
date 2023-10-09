# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'form.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(749, 590)
        self.gridLayoutWidget = QtWidgets.QWidget(MainWindow)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(30, 30, 691, 80))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.buttonSave = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.buttonSave.setObjectName("buttonSave")
        self.gridLayout_2.addWidget(self.buttonSave, 0, 2, 1, 1)
        self.buttonEditNew = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.buttonEditNew.setObjectName("buttonEditNew")
        self.gridLayout_2.addWidget(self.buttonEditNew, 1, 2, 1, 1)
        self.buttonOpen = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.buttonOpen.setObjectName("buttonOpen")
        self.gridLayout_2.addWidget(self.buttonOpen, 1, 0, 1, 1)
        self.label_Error = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_Error.setText("")
        self.label_Error.setAlignment(QtCore.Qt.AlignCenter)
        self.label_Error.setObjectName("label_Error")
        self.gridLayout_2.addWidget(self.label_Error, 0, 1, 2, 1)
        self.buttonLena = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.buttonLena.setObjectName("buttonLena")
        self.gridLayout_2.addWidget(self.buttonLena, 0, 0, 1, 1)
        self.origImage = QtWidgets.QLabel(MainWindow)
        self.origImage.setGeometry(QtCore.QRect(30, 110, 342, 299))
        self.origImage.setFrameShape(QtWidgets.QFrame.Box)
        self.origImage.setText("")
        self.origImage.setScaledContents(True)
        self.origImage.setAlignment(QtCore.Qt.AlignCenter)
        self.origImage.setObjectName("origImage")
        self.newImage = QtWidgets.QLabel(MainWindow)
        self.newImage.setGeometry(QtCore.QRect(380, 110, 342, 299))
        self.newImage.setFrameShape(QtWidgets.QFrame.Box)
        self.newImage.setText("")
        self.newImage.setScaledContents(True)
        self.newImage.setAlignment(QtCore.Qt.AlignCenter)
        self.newImage.setObjectName("newImage")
        self.horizontalLayoutWidget = QtWidgets.QWidget(MainWindow)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(30, 420, 691, 170))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.formLayout_3 = QtWidgets.QFormLayout()
        self.formLayout_3.setObjectName("formLayout_3")
        self.label_1 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label_1.setObjectName("label_1")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.input_x = QtWidgets.QLineEdit(self.horizontalLayoutWidget)
        self.input_x.setObjectName("input_x")
        self.horizontalLayout.addWidget(self.input_x)
        self.input_y = QtWidgets.QLineEdit(self.horizontalLayoutWidget)
        self.input_y.setObjectName("input_y")
        self.horizontalLayout.addWidget(self.input_y)
        self.formLayout_3.setLayout(0, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout)
        self.label_2 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.formLayout_3.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.inputAlgo = QtWidgets.QComboBox(self.horizontalLayoutWidget)
        self.inputAlgo.setObjectName("inputAlgo")
        self.inputAlgo.addItem("")
        self.inputAlgo.addItem("")
        self.inputAlgo.addItem("")
        self.inputAlgo.addItem("")
        self.formLayout_3.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.inputAlgo)
        self.label_3 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.formLayout_3.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.inputBits = QtWidgets.QComboBox(self.horizontalLayoutWidget)
        self.inputBits.setObjectName("inputBits")
        self.inputBits.addItem("")
        self.inputBits.addItem("")
        self.inputBits.addItem("")
        self.inputBits.addItem("")
        self.inputBits.addItem("")
        self.inputBits.addItem("")
        self.inputBits.addItem("")
        self.inputBits.addItem("")
        self.inputBits.addItem("")
        self.formLayout_3.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.inputBits)
        self.label_4 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label_4.setObjectName("label_4")
        self.formLayout_3.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.inputHistoEq = QtWidgets.QComboBox(self.horizontalLayoutWidget)
        self.inputHistoEq.setObjectName("inputHistoEq")
        self.inputHistoEq.addItem("")
        self.inputHistoEq.addItem("")
        self.inputHistoEq.addItem("")
        self.formLayout_3.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.inputHistoEq)
        self.label_5 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label_5.setObjectName("label_5")
        self.formLayout_3.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_5)
        self.input_histoSize = QtWidgets.QLineEdit(self.horizontalLayoutWidget)
        self.input_histoSize.setObjectName("input_histoSize")
        self.formLayout_3.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.input_histoSize)
        self.horizontalLayout_2.addLayout(self.formLayout_3)
        spacerItem = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.buttonConfirm = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.buttonConfirm.setObjectName("buttonConfirm")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.buttonConfirm)
        self.inputFilter = QtWidgets.QComboBox(self.horizontalLayoutWidget)
        self.inputFilter.setObjectName("inputFilter")
        self.inputFilter.addItem("")
        self.inputFilter.addItem("")
        self.inputFilter.addItem("")
        self.inputFilter.addItem("")
        self.inputFilter.addItem("")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.inputFilter)
        self.label_7 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label_7.setObjectName("label_7")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_7)
        self.label_8 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label_8.setObjectName("label_8")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_8)
        self.input_filterSize = QtWidgets.QLineEdit(self.horizontalLayoutWidget)
        self.input_filterSize.setObjectName("input_filterSize")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.input_filterSize)
        self.label = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label.setObjectName("label")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label)
        self.lineEdit = QtWidgets.QLineEdit(self.horizontalLayoutWidget)
        self.lineEdit.setObjectName("lineEdit")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.lineEdit)
        self.horizontalLayout_2.addLayout(self.formLayout)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Widget"))
        self.buttonSave.setText(_translate("MainWindow", "Save Image"))
        self.buttonEditNew.setText(_translate("MainWindow", "Edit New Image"))
        self.buttonOpen.setText(_translate("MainWindow", "Open Image"))
        self.buttonLena.setText(_translate("MainWindow", "Open Lena"))
        self.label_1.setText(_translate("MainWindow", "Dimensions (x, y)"))
        self.label_2.setText(_translate("MainWindow", "Algorithm"))
        self.inputAlgo.setItemText(0, _translate("MainWindow", "Select One"))
        self.inputAlgo.setItemText(1, _translate("MainWindow", "Nearest Neighbor"))
        self.inputAlgo.setItemText(2, _translate("MainWindow", "Linear Interpolation"))
        self.inputAlgo.setItemText(3, _translate("MainWindow", "Bilinear Interpolation"))
        self.label_3.setText(_translate("MainWindow", "Bits"))
        self.inputBits.setItemText(0, _translate("MainWindow", "Select One"))
        self.inputBits.setItemText(1, _translate("MainWindow", "1"))
        self.inputBits.setItemText(2, _translate("MainWindow", "2"))
        self.inputBits.setItemText(3, _translate("MainWindow", "3"))
        self.inputBits.setItemText(4, _translate("MainWindow", "4"))
        self.inputBits.setItemText(5, _translate("MainWindow", "5"))
        self.inputBits.setItemText(6, _translate("MainWindow", "6"))
        self.inputBits.setItemText(7, _translate("MainWindow", "7"))
        self.inputBits.setItemText(8, _translate("MainWindow", "8"))
        self.label_4.setText(_translate("MainWindow", "Histogram Eq."))
        self.inputHistoEq.setItemText(0, _translate("MainWindow", "Select One"))
        self.inputHistoEq.setItemText(1, _translate("MainWindow", "Local"))
        self.inputHistoEq.setItemText(2, _translate("MainWindow", "Global"))
        self.label_5.setText(_translate("MainWindow", "Mask Size ( m^2 )"))
        self.input_histoSize.setText(_translate("MainWindow", "3"))
        self.buttonConfirm.setText(_translate("MainWindow", "Confirm"))
        self.inputFilter.setItemText(0, _translate("MainWindow", "Select One"))
        self.inputFilter.setItemText(1, _translate("MainWindow", "Smoothing"))
        self.inputFilter.setItemText(2, _translate("MainWindow", "Median"))
        self.inputFilter.setItemText(3, _translate("MainWindow", "Sharpening Laplacian"))
        self.inputFilter.setItemText(4, _translate("MainWindow", "High-boosting "))
        self.label_7.setText(_translate("MainWindow", "Filtering "))
        self.label_8.setText(_translate("MainWindow", "Filter Size( m^2 )"))
        self.label.setText(_translate("MainWindow", "Bitplane Removal"))
