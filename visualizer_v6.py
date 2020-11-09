'''
Created on 13 feb. 2013

@author: Squirel
'''
import sys
from matplotlib import pylab as pb
from PyQt4 import QtCore, QtGui
from numpy import load
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg
import matplotlib
matplotlib.use('Qt4Agg')
from visualizerGUI_v3 import Ui_Visualizer
sys.path.append('/media/naze/COMPATIBLE/Squirrel_INS_backup_mai2015/workspace/HC-Septum-Network/popEpi_variableParamaters')
import paramSpace_4D_v6 as paramSpace4D


in_row_label = ""
in_col_label = ""
out_row_label = ""
out_col_label = ""

in_row_vals = pb.array([])
in_col_vals = pb.array([])
out_row_vals = pb.array([])
out_col_vals = pb.array([])


class mainVisual(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.ui = Ui_Visualizer()
        self.ui.setupUi(self)
        
        self.I1_idx=0
        self.I1_s=pb.array([0, 1.5, 2.6, 2.9, 3.0, 3.1, 3.2, 3.5, 4.0, 5.0])
        self.I2_idx=0
        self.I2_s=pb.array([0, 0.5, 0.8, 0.9, 1.0, 1.5])
        self.gx1x1_idx=0
        self.gx1x1_s=pb.array([0, 0.2, 0.4, 0.6])
        self.gx2x2_idx=0
        self.gx2x2_s=pb.array([0, 0.2, 0.4, 0.6])
        self.Ce_idx=0
        self.Ce_s=pb.array([0, 0.2, 0.4, 0.6, 0.8, 1])
        self.gx1x2_idx=0
        self.gx1x2_s=pb.array([0, 0.1, 0.2, 0.3])
        self.gx2x1_idx=0
        self.gx2x1_s=pb.array([0, 0.1, 0.2, 0.3])
        self.x0_idx=0
        self.x0_s=pb.array([2, 2.5, 3, 3.5, 4])
        #self.x0_s=pb.array([-6, -5, -4, -3.5, -3, -2.5, -2, -1, 0]);
        
        #value initialization
        self.ui.doubleSpinBox_I2.setMaximum(self.I2_s.max())
        self.ui.doubleSpinBox_I2.setMinimum(self.I2_s.min())
        self.ui.doubleSpinBox_I2.setSingleStep(0.3)
        self.ui.doubleSpinBox_I2.setValue(self.I2_s[self.I2_idx])
        self.ui.doubleSpinBox_I1.setMaximum(self.I1_s.max())
        self.ui.doubleSpinBox_I1.setMinimum(self.I1_s.min())
        self.ui.doubleSpinBox_I1.setSingleStep(1.0)
        self.ui.doubleSpinBox_I1.setValue(self.I1_s[self.I1_idx])
        self.ui.doubleSpinBox_Ce.setValue(self.Ce_s[self.Ce_idx])
        self.ui.doubleSpinBox_Ce.setMaximum(self.Ce_s.max())
        self.ui.doubleSpinBox_Ce.setMinimum(self.Ce_s.min())
        self.ui.doubleSpinBox_gx1x2.setMinimum(self.gx1x2_s.min())
        self.ui.doubleSpinBox_gx1x2.setMaximum(self.gx1x2_s.max())
        self.ui.doubleSpinBox_gx1x2.setSingleStep(0.1)
        self.ui.doubleSpinBox_gx1x2.setValue(self.gx1x2_s[self.gx1x2_idx])
        self.ui.doubleSpinBox_gx2x1.setMinimum(self.gx2x1_s.min())
        self.ui.doubleSpinBox_gx2x1.setMaximum(self.gx2x1_s.max())
        self.ui.doubleSpinBox_gx2x1.setSingleStep(0.1)
        self.ui.doubleSpinBox_gx2x1.setValue(self.gx2x1_s[self.gx2x1_idx])
        self.ui.doubleSpinBox_x0.setValue(self.x0_s[self.x0_idx])
        self.ui.doubleSpinBox_x0.setMaximum(self.x0_s.max())
        self.ui.doubleSpinBox_x0.setMinimum(self.x0_s.min())
        
        #enability
        self.ui.doubleSpinBox_I1.setEnabled(False)
        self.ui.doubleSpinBox_I2.setEnabled(False)
        self.ui.doubleSpinBox_gx1x1.setEnabled(False)
        self.ui.doubleSpinBox_gx2x2.setEnabled(False)
        
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
        QtCore.QObject.connect(self.ui.doubleSpinBox_Ce, 
                               QtCore.SIGNAL("valueChanged(double)"), self.updateFields)
        QtCore.QObject.connect(self.ui.doubleSpinBox_x0, 
                               QtCore.SIGNAL("valueChanged(double)"), self.updateFields)
        
        #Graphics view for Time Series
        pic = QtGui.QPixmap(
            "/home/naze/Pictures/Hatosia.jpg")
            #"/media/naze/COMPATIBLE/Squirrel_INS_backup_mai2015/Pictures/sveta-dorosheva-10.jpg")
        pic = pic.scaled(self.ui.graphicsView_ts.size(), 
                         QtCore.Qt.IgnoreAspectRatio, 
                         QtCore.Qt.SmoothTransformation)
        self.scene = QtGui.QGraphicsScene()
        self.scene.addPixmap(pic)
        self.ui.graphicsView_ts.setScene(self.scene)
        self.ui.graphicsView_ts.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.ui.graphicsView_ts.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.ui.graphicsView_ts.show()
        
        # Handle the parameter space map in a new window 
        self.mapWin = self.drawKOPmap()
        self.mapWin.show()
        self.mapWin.draw()
        self.previous_ax=[] #list of (normally only 1 or zero) axes object, referring to the last point seen in param space 
        
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
        
        self.x0_idx = self.adjustFieldValue(self.x0_idx, self.ui.doubleSpinBox_x0.value(), self.x0_s)
        self.ui.doubleSpinBox_x0.setValue(self.x0_s[self.x0_idx])
        
        #print I1, I2, gx1x1, gx2x2, Ce, gx1x2, gx2x1
        self.drawPoint(self.gx1x2_idx, self.gx1x2_s, self.gx2x1_idx, self.gx2x1_s, 
                       self.x0_idx, self.x0_s, self.Ce_idx, self.Ce_s)
        
        filename = 'epilepton_40_HMR_40_ML_CpES_' +str(int(self.Ce_s[self.Ce_idx]*100))+ \
                    '_gx1x2_'+str(int(self.gx1x2_s[self.gx1x2_idx]*100))+ \
                    '_gx2x1_'+str(int(self.gx2x1_s[self.gx2x1_idx]*100))+ \
                    '_x0_'+str(int(self.x0_s[self.x0_idx]*100))+'_10s.png'
        path = "/media/naze/COMPATIBLE/Squirrel_INS_backup_mai2015/workspace/HC-Septum-Network/popEpi_HMR_FHN/img_22feb/"
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
            
    def drawPoint(self, in_y_index, in_y_s, in_x_index, in_x_s, out_y_index, out_y_s, out_x_index, out_x_s):
        """this function plots a point in the current map to know where we are in the parameter space"""
        # remove previous plotted point if there was one
        if len(self.previous_ax)!=0:
            del self.previous_ax[0].lines[:]
        #remember the out_y axes has been reversed so:
        out_y_index = out_y_s.size-1 - out_y_index
        #select the Axes object on which to plot the point
        axs = self.mapWin.figure.get_axes()
        ax = axs[out_y_index*out_x_s.size + out_x_index] #get the current ax from the 1D array
        ax.hold(True)
        ax.autoscale(enable=False) #avoid the plot to change the ticks and scale and all

        ax.plot(in_x_s[in_x_index], in_y_s[in_y_index], 'ow', markersize=10, markeredgewidth=2)
        #replace the previous axe to the new axe
        if len(self.previous_ax)!=0:
            self.previous_ax[0]=ax
        else:
            self.previous_ax.append(ax)
        self.mapWin.figure.canvas.draw()
        #self.mapWin.pause(0.001)
        
    def drawKOPmap(self):
        """Draw the dialog window with the KOP map parameter space"""
        out_img_grid = load('/media/naze/COMPATIBLE/Squirrel_INS_backup_mai2015/workspace/HC-Septum-Network/popEpi_variableParamaters/outImgGridMean_v5.npy')
        out_img_grid_KOP = load('/media/naze/COMPATIBLE/Squirrel_INS_backup_mai2015/workspace/HC-Septum-Network/popEpi_variableParamaters/outImgGridKOP_v5.npy')
        #out_img_grid_KOP2 = load('C://Users/Squirel/workspace/HC-Septum-Network/popEpi_HMR_FHN/outImgGridKOP2_v3.npy')
        print out_img_grid.shape
        print out_img_grid_KOP.shape
        #print out_img_grid_KOP2.shape
        fig = paramSpace4D.drawFig(out_img_grid_KOP) #, out_img_grid_KOP)
        #fig.show()
        mapWin = mapWindow()
        mapWin.set_figure(fig)
        return mapWin


    def drawFig(img_grid):
        # figure properties
        fig = pb.figure(figsize=(10, 6))
        row_length = len(out_row_vals)
        col_length = len(out_col_vals)
        gs = matplotlib.gridspec.GridSpec(row_length, col_length, wspace=.05, hspace=.05)  # +1 for the colormap area
        """figure processing"""
        img_grid = img_grid.tolist()
        # get min and max to set up colormap scale, and loop all again to plot images
        MIN = pb.array(img_grid).min()
        MAX = pb.array(img_grid).max()
        for out_row_index in range(len(out_row_vals)):
            for out_col_index in range(len(out_col_vals)):
                ax = fig.add_subplot(gs[out_row_index, out_col_index])
                ax.hold(True)

                img_grid[out_row_index][out_col_index] = ax.contourf(img_grid[out_row_index][out_col_index],
                                                                             levels=pb.linspace(MIN, MAX, 50),
                                                                             extent=[in_col_vals.min(), in_col_vals.max(),
                                                                                     in_row_vals.min(), in_row_vals.max()],
                                                                             vmin=MIN, vmax=MAX)

                # set ticks and labels of axis (no number in legend for graphs not on borders):
                # for the x axis:
                xticks = in_col_vals
                ax.set_xticks(xticks)
                if (out_row_index < row_length - 1):
                    ax.set_xticklabels([])
                else:
                    ax.set_xlabel(
                        in_col_label + "\n\n" + out_col_label + "=" + str(out_col_vals[out_col_index]))  # , fontsize='xx-large')
                    ax.set_xticklabels(map(str, xticks))  # , fontsize='xx-large') #in_col_val

                # for the y axis:
                yticks = in_row_vals  # from in_row_val
                ax.set_yticks(yticks)
                if (out_col_index > 0):
                    ax.set_yticklabels([])
                else:
                    ax.set_ylabel("|" + out_row_label + "|=" + str(out_row_vals[out_row_index]) + '      ' + in_row_label,
                                  rotation='horizontal')  # , fontsize='xx-large')
                    ax.set_yticklabels(map(str, yticks))  # , fontsize='xx-large') #in_row_val

        # setup colorbar
        ax = pb.axes([0.92, 0.1, 0.01, 0.8])  # guess [left, bottom, width, heigth]. in percents
        cbar = pb.colorbar(img_grid[0][0], ax)  # , ticks=ticksValues)
        pb.ion()
        return fig

class mapWindow(QtGui.QDialog, FigureCanvasQTAgg):
    """Small class that displays the parameter space map on a new window"""
    def __init__(self, *args, **kwargs):
        QtGui.QDialog.__init__(self, *args, **kwargs)        
        self.setObjectName("Map Visualizer")
        self.resize(1000, 500)
        self.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        
    def set_figure(self, fig):
        self.canvas = FigureCanvasQTAgg.__init__(self, fig)

        
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = mainVisual()
    myapp.show()
    sys.exit(app.exec_())
    
    
    