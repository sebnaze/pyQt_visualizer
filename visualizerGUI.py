# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'visualizerGUI_v1.ui'
#
# Created: Thu Feb 14 01:00:03 2013
#      by: PyQt4 UI code generator 4.9.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Visualizer(object):
    def setupUi(self, Visualizer):
        Visualizer.setObjectName(_fromUtf8("Visualizer"))
        Visualizer.resize(1100, 623)
        Visualizer.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.groupBox = QtGui.QGroupBox(Visualizer)
        self.groupBox.setGeometry(QtCore.QRect(40, 70, 201, 521))
        self.groupBox.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(20, 60, 46, 13))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(20, 80, 46, 13))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_7 = QtGui.QLabel(self.groupBox)
        self.label_7.setGeometry(QtCore.QRect(20, 180, 46, 13))
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.doubleSpinBox_I1 = QtGui.QDoubleSpinBox(self.groupBox)
        self.doubleSpinBox_I1.setGeometry(QtCore.QRect(120, 60, 62, 16))
        self.doubleSpinBox_I1.setObjectName(_fromUtf8("doubleSpinBox_I1"))
        self.doubleSpinBox_I2 = QtGui.QDoubleSpinBox(self.groupBox)
        self.doubleSpinBox_I2.setGeometry(QtCore.QRect(120, 78, 62, 16))
        self.doubleSpinBox_I2.setMaximum(1.5)
        self.doubleSpinBox_I2.setSingleStep(0.1)
        self.doubleSpinBox_I2.setProperty("value", 0.9)
        self.doubleSpinBox_I2.setObjectName(_fromUtf8("doubleSpinBox_I2"))
        self.doubleSpinBox_gx1x1 = QtGui.QDoubleSpinBox(self.groupBox)
        self.doubleSpinBox_gx1x1.setEnabled(False)
        self.doubleSpinBox_gx1x1.setGeometry(QtCore.QRect(120, 97, 62, 16))
        self.doubleSpinBox_gx1x1.setObjectName(_fromUtf8("doubleSpinBox_gx1x1"))
        self.doubleSpinBox_gx1x2 = QtGui.QDoubleSpinBox(self.groupBox)
        self.doubleSpinBox_gx1x2.setGeometry(QtCore.QRect(120, 158, 62, 16))
        self.doubleSpinBox_gx1x2.setObjectName(_fromUtf8("doubleSpinBox_gx1x2"))
        self.doubleSpinBox_gx2x2 = QtGui.QDoubleSpinBox(self.groupBox)
        self.doubleSpinBox_gx2x2.setEnabled(False)
        self.doubleSpinBox_gx2x2.setGeometry(QtCore.QRect(120, 116, 62, 16))
        self.doubleSpinBox_gx2x2.setObjectName(_fromUtf8("doubleSpinBox_gx2x2"))
        self.doubleSpinBox_Ce = QtGui.QDoubleSpinBox(self.groupBox)
        self.doubleSpinBox_Ce.setEnabled(False)
        self.doubleSpinBox_Ce.setGeometry(QtCore.QRect(120, 137, 62, 16))
        self.doubleSpinBox_Ce.setProperty("value", 0.6)
        self.doubleSpinBox_Ce.setObjectName(_fromUtf8("doubleSpinBox_Ce"))
        self.doubleSpinBox_gx2x1 = QtGui.QDoubleSpinBox(self.groupBox)
        self.doubleSpinBox_gx2x1.setGeometry(QtCore.QRect(120, 177, 62, 16))
        self.doubleSpinBox_gx2x1.setObjectName(_fromUtf8("doubleSpinBox_gx2x1"))
        self.OkButton = QtGui.QPushButton(self.groupBox)
        self.OkButton.setGeometry(QtCore.QRect(110, 230, 75, 23))
        self.OkButton.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.OkButton.setObjectName(_fromUtf8("OkButton"))
        self.label_3 = QtGui.QLabel(Visualizer)
        self.label_3.setGeometry(QtCore.QRect(60, 170, 46, 13))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.label_4 = QtGui.QLabel(Visualizer)
        self.label_4.setGeometry(QtCore.QRect(60, 190, 46, 13))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.label_5 = QtGui.QLabel(Visualizer)
        self.label_5.setGeometry(QtCore.QRect(60, 210, 46, 13))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.label_6 = QtGui.QLabel(Visualizer)
        self.label_6.setGeometry(QtCore.QRect(60, 230, 46, 13))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.graphicsView = QtGui.QGraphicsView(Visualizer)
        self.graphicsView.setGeometry(QtCore.QRect(250, 50, 841, 521))
        self.graphicsView.setObjectName(_fromUtf8("graphicsView"))

        self.retranslateUi(Visualizer)
        QtCore.QMetaObject.connectSlotsByName(Visualizer)

    def retranslateUi(self, Visualizer):
        Visualizer.setWindowTitle(_translate("Visualizer", "Visualizer", None))
        self.groupBox.setTitle(_translate("Visualizer", "Parameters", None))
        self.label.setText(_translate("Visualizer", "I1", None))
        self.label_2.setText(_translate("Visualizer", "I2", None))
        self.label_7.setText(_translate("Visualizer", "g_x2x1", None))
        self.OkButton.setText(_translate("Visualizer", "Ok", None))
        self.label_3.setText(_translate("Visualizer", "g_x1x1", None))
        self.label_4.setText(_translate("Visualizer", "g_x2x2", None))
        self.label_5.setText(_translate("Visualizer", "Ce", None))
        self.label_6.setText(_translate("Visualizer", "g_x1x2", None))

