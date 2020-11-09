'''
Created on 13 feb. 2013

@author: Squirel
'''
import sys
import pylab as pb
from PyQt4 import QtCore, QtGui
from visualizerGUI_v2 import Ui_Visualizer


from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg

from popEpi_HMR_FHN import paramSpace_4D



class mainVisual(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.ui = Ui_Visualizer()
        self.ui.setupUi(self)
        
        self.I1_idx=5; 
        self.I1_s=pb.array([0, 1.5, 2.6, 2.9, 3.0, 3.1, 3.2, 3.5, 4.0, 5.0]);
        self.I2_idx=3; 
        self.I2_s=pb.array([0, 0.5, 0.8, 0.9, 1.0, 1.5]);
        self.gx1x1_idx=0;
        self.gx1x1_s=pb.array([0.3]) 
        self.gx2x2_idx=0;
        self.gx2x2_s=pb.array([0.3])
        self.Ce_idx=0;
        self.Ce_s=pb.array([0.6])
        self.gx1x2_idx=2
        self.gx1x2_s=pb.array([0.05, 0.1, 0.15, 0.2, 0.3]);
        self.gx2x1_idx=2
        self.gx2x1_s=pb.array([0.05, 0.1, 0.15, 0.2, 0.3]);
        
        #value initialization
        self.ui.doubleSpinBox_I2.setMaximum(self.I2_s.max())
        self.ui.doubleSpinBox_I2.setMinimum(self.I2_s.min())
        self.ui.doubleSpinBox_I2.setSingleStep(0.1)
        self.ui.doubleSpinBox_I2.setValue(self.I2_s[self.I2_idx])
        self.ui.doubleSpinBox_I1.setMaximum(self.I1_s.max())
        self.ui.doubleSpinBox_I1.setMinimum(self.I1_s.min())
        self.ui.doubleSpinBox_I1.setSingleStep(0.1)
        self.ui.doubleSpinBox_I1.setValue(self.I1_s[self.I1_idx])
        self.ui.doubleSpinBox_Ce.setValue(self.Ce_s[self.Ce_idx])
        self.ui.doubleSpinBox_gx1x2.setMinimum(self.gx1x2_s.min())
        self.ui.doubleSpinBox_gx1x2.setMaximum(self.gx1x2_s.max())
        self.ui.doubleSpinBox_gx1x2.setSingleStep(0.05)
        self.ui.doubleSpinBox_gx1x2.setValue(self.gx1x2_s[self.gx1x2_idx])
        self.ui.doubleSpinBox_gx2x1.setMinimum(self.gx2x1_s.min())
        self.ui.doubleSpinBox_gx2x1.setMaximum(self.gx2x1_s.max())
        self.ui.doubleSpinBox_gx2x1.setSingleStep(0.05)
        self.ui.doubleSpinBox_gx2x1.setValue(self.gx2x1_s[self.gx2x1_idx])
        
        #events
        QtCore.QObject.connect(self.ui.OkButton, 
                               QtCore.SIGNAL("clicked()"), self.updateFields)
        QtCore.QObject.connect(self.ui.doubleSpinBox_I1, 
                               QtCore.SIGNAL("valueChanged(double)"), self.updateFields)
        QtCore.QObject.connect(self.ui.doubleSpinBox_I2, 
                               QtCore.SIGNAL("valueChanged(double)"), self.updateFields)
        QtCore.QObject.connect(self.ui.doubleSpinBox_gx1x2, 
                               QtCore.SIGNAL("valueChanged(double)"), self.updateFields)
        QtCore.QObject.connect(self.ui.doubleSpinBox_gx2x1, 
                               QtCore.SIGNAL("valueChanged(double)"), self.updateFields)
        
        #Graphics view
        pic = QtGui.QPixmap(
            "C:/Users/Public/Pictures/Sample Pictures/Hatosia.jpg")
        pic = pic.scaled(self.ui.graphicsView_ts.size(), 
                         QtCore.Qt.IgnoreAspectRatio, 
                         QtCore.Qt.SmoothTransformation)
        self.scene = QtGui.QGraphicsScene()
        self.scene.addPixmap(pic)
        self.ui.graphicsView_ts.setScene(self.scene)
        self.ui.graphicsView_ts.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.ui.graphicsView_ts.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.ui.graphicsView_ts.show()
        
        self.previous_ax=[] #list of (normally only 1 or zero) axes object, refering to the last point seen in param space 
        
    def updateFields(self):
        """update all fields from the canvas when a parameter is changed"""
        self.I1_idx = self.adjustFieldValue(self.I1_idx, self.ui.doubleSpinBox_I1.value(), self.I1_s)
        self.ui.doubleSpinBox_I1.setValue(self.I1_s[self.I1_idx])
        
        self.I2_idx = self.adjustFieldValue(self.I2_idx, self.ui.doubleSpinBox_I2.value(), self.I2_s)
        self.ui.doubleSpinBox_I2.setValue(self.I2_s[self.I2_idx])
        
        self.gx1x1_idx = self.adjustFieldValue(self.gx1x1_idx, self.ui.doubleSpinBox_gx1x1.value(), self.gx1x1_s)
        self.ui.doubleSpinBox_gx1x1.setValue(self.gx1x1_s[self.gx1x1_idx])
        
        self.gx2x2_idx = self.adjustFieldValue(self.gx2x2_idx, self.ui.doubleSpinBox_gx2x2.value(), self.gx2x2_s)
        self.ui.doubleSpinBox_gx1x1.setValue(self.gx2x2_s[self.gx2x2_idx])
        
        self.Ce_idx = self.adjustFieldValue(self.Ce_idx, self.ui.doubleSpinBox_Ce.value(), self.Ce_s)
        self.ui.doubleSpinBox_Ce.setValue(self.Ce_s[self.Ce_idx])
        
        self.gx1x2_idx = self.adjustFieldValue(self.gx1x2_idx, self.ui.doubleSpinBox_gx1x2.value(), self.gx1x2_s)
        self.ui.doubleSpinBox_gx1x2.setValue(self.gx1x2_s[self.gx1x2_idx])
        
        self.gx2x1_idx = self.adjustFieldValue(self.gx2x1_idx, self.ui.doubleSpinBox_gx2x1.value(), self.gx2x1_s)
        self.ui.doubleSpinBox_gx2x1.setValue(self.gx2x1_s[self.gx2x1_idx])
        
        #print I1, I2, gx1x1, gx2x2, Ce, gx1x2, gx2x1
        self.drawPoint(self.gx1x2_idx, self.gx2x1_idx, self.I1_idx, self.I2_idx)
        
        filename = 'epilepton_40_HMR_40_ML_CpES_' +str(int(self.Ce_s[self.Ce_idx]*100))+ \
                    '_I1_'+str(int(self.I1_s[self.I1_idx]*10))+'_gx1x2_'+str(int(self.gx1x2_s[self.gx1x2_idx]*100))+ \
                    '_I2_'+str(int(self.I2_s[self.I2_idx]*10))+'_gx2x1_'+str(int(self.gx2x1_s[self.gx2x1_idx]*100))+'_10s.png'
        path = "C://Users/Squirel/workspace/HC-Septum-Network/popEpi_HMR_FHN/img_28jan/"
        print path+filename
        pic = QtGui.QPixmap(path+filename)
        pic = pic.scaled(self.ui.graphicsView_ts.size(), 
                         QtCore.Qt.IgnoreAspectRatio, 
                         QtCore.Qt.SmoothTransformation)
        self.scene.addPixmap(pic)
        #self.ui.graphicsView_ts.setScene()
        self.ui.graphicsView_ts.show()
        
    def adjustFieldValue(self, index, new_val, all_val):
        """adjust the value of the parameter from the spinboxes to existing values in parameter space"""
        if(new_val<all_val[index] and index > 0):
            index-=1
        elif (new_val>all_val[index] and index < pb.size(all_val)):
            index+=1
        return index
            
    def drawPoint(self, in_y_index, in_x_index, out_y_index, out_x_index):
        """this function plots a point in the current map to know where we are in the parameter space"""
        # remove previous plotted point if there was one
        if len(self.previous_ax)!=0:
            del self.previous_ax[0].lines[:]
        #remember the out_y axes has been reversed so:
        out_y_index = self.I1_s.size-1 - out_y_index
        #select the Axes object on which to plot the point
        axs = self.ui.mplwidget.canvas.fig.get_axes()
        ax = axs[out_y_index*self.I2_s.size + out_x_index]
        ax.hold(True)
        ax.autoscale(enable=False) #avoid the plot to change the ticks and scale and all
        ax.plot(self.gx2x1_s[in_x_index], self.gx1x2_s[in_y_index], 'ow')
        #replace the previous axe to the new axe
        if len(self.previous_ax)!=0:
            self.previous_ax[0]=ax
        else:
            self.previous_ax.append(ax)
        self.ui.mplwidget.canvas.draw()
        
            
        
        
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = mainVisual()
    myapp.show()
    sys.exit(app.exec_())
    
    
    