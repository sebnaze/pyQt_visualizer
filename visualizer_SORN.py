'''
Created on 13 feb. 2013

@author: Squirel
'''
import sys
from matplotlib import pylab as pb
from PyQt4 import QtCore, QtGui
import numpy as np
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg
import matplotlib
#matplotlib.use('Qt4Agg')
import h5py
from visualizerGUI_SORN import Ui_Visualizer
#sys.path.append('/home/naze/MGS/graphs/SORN/2018mar03/muIP0_001/ratioIP1_0/etaSTDP0_001/muHIP0_02/ratioHIP0_5')

path = '/home/naze/MGS/graphs/SORN/2018mar24/'
base1dir = 'muIP0_0001/ratioIP1_0/etaSTDP0_001/'
base2dir = 'muHIP0_01/ratioHIP0_5/muHIPi0_02/ratioHIPi0_5/' #'ratioIP1_0/etaSTDP0_001/muHIP0_02/ratioHIP0_5/'
base3dir = 'E2X0_05/I2X0_1/' #'muHIPi0_04/E2X0_05/I2X0_1/'
base4dir = ''

feature_4D_matrix = 'entropy_array_map.mat'

out_row_label = "g"
out_col_label = "tauSTDP"
in_row_label = "muDelay"
in_col_label = "ratioDelay"

out_row_vals = pb.array([1.0])
#out_row_vals = out_row_vals[::-1] #reverse array to have down -> axes up rather than down if needed
out_col_vals = pb.array([0.9, 0.99])
in_row_vals = pb.array([1, 2, 3, 5])
in_col_vals = pb.array([0.5, 1.0])

class mainVisual(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.ui = Ui_Visualizer()
        self.ui.setupUi(self)
        self.ui.setLabelNames(out_row_label, out_col_label, in_row_label, in_col_label)
        
        self.I1_idx = 0
        self.I1_s = pb.array([0, 1.5, 2.6, 2.9, 3.0, 3.1, 3.2, 3.5, 4.0, 5.0])
        self.I2_idx = 0
        self.I2_s = pb.array([0, 0.5, 0.8, 0.9, 1.0, 1.5])
        self.gx1x1_idx = 0
        self.gx1x1_s = pb.array([0, 0.2, 0.4, 0.6])
        self.gx2x2_idx = 0
        self.gx2x2_s = pb.array([0, 0.2, 0.4, 0.6])
        self.out_col_idx = 0
        self.out_col_s = out_col_vals
        self.in_row_idx = 0
        self.in_row_s = in_row_vals
        self.in_col_idx = 0
        self.in_col_s = in_col_vals
        self.out_row_idx = 0
        self.out_row_s = out_row_vals
        #self.x0_s=pb.array([-6, -5, -4, -3.5, -3, -2.5, -2, -1, 0]);
        
        #value initialization
        self.ui.doubleSpinBox_I2.setMaximum(self.I2_s.max())
        self.ui.doubleSpinBox_I2.setMinimum(self.I2_s.min())
        self.ui.doubleSpinBox_I2.setSingleStep(0.3)
        self.ui.doubleSpinBox_I2.setValue(self.I2_s[self.I2_idx])
        self.ui.doubleSpinBox_I2.setEnabled(False)

        self.ui.doubleSpinBox_I1.setMaximum(self.I1_s.max())
        self.ui.doubleSpinBox_I1.setMinimum(self.I1_s.min())
        self.ui.doubleSpinBox_I1.setSingleStep(1.0)
        self.ui.doubleSpinBox_I1.setValue(self.I1_s[self.I1_idx])
        self.ui.doubleSpinBox_I1.setEnabled(False)

        self.ui.doubleSpinBox_Ce.setMaximum(self.out_col_s.max())
        self.ui.doubleSpinBox_Ce.setMinimum(self.out_col_s.min())
        self.ui.doubleSpinBox_Ce.setSingleStep(0.01)
        self.ui.doubleSpinBox_Ce.setValue(self.out_col_s[self.out_col_idx])
        self.ui.doubleSpinBox_Ce.setEnabled(True)
        self.ui.doubleSpinBox_Ce.setDecimals(6)

        self.ui.doubleSpinBox_gx1x2.setMinimum(self.in_row_s.min())
        self.ui.doubleSpinBox_gx1x2.setMaximum(self.in_row_s.max())
        self.ui.doubleSpinBox_gx1x2.setSingleStep(0.1)
        self.ui.doubleSpinBox_gx1x2.setValue(self.in_row_s[self.in_row_idx])
        self.ui.doubleSpinBox_gx1x2.setEnabled(True)
        self.ui.doubleSpinBox_gx1x2.setDecimals(6)

        self.ui.doubleSpinBox_gx2x1.setMinimum(self.in_col_s.min())
        self.ui.doubleSpinBox_gx2x1.setMaximum(self.in_col_s.max())
        self.ui.doubleSpinBox_gx2x1.setSingleStep(0.1)
        self.ui.doubleSpinBox_gx2x1.setValue(self.in_col_s[self.in_col_idx])
        self.ui.doubleSpinBox_gx2x1.setEnabled(True)
        self.ui.doubleSpinBox_gx2x1.setDecimals(6)

        self.ui.doubleSpinBox_x0.setMaximum(self.out_row_s.max())
        self.ui.doubleSpinBox_x0.setMinimum(self.out_row_s.min())
        self.ui.doubleSpinBox_x0.setSingleStep(0.1)
        self.ui.doubleSpinBox_x0.setValue(self.out_row_s[self.out_row_idx])
        self.ui.doubleSpinBox_x0.setEnabled(True)
        
        #enability
        self.ui.doubleSpinBox_gx1x1.setEnabled(False)
        self.ui.doubleSpinBox_gx2x2.setEnabled(False)
        
        #events
        QtCore.QObject.connect(self.ui.OkButton, 
                               QtCore.SIGNAL("clicked()"), self.updateFields)
        QtCore.QObject.connect(self.ui.doubleSpinBox_I1,
                               QtCore.SIGNAL("valueChanged(double)"), self.updateFields)
        QtCore.QObject.connect(self.ui.doubleSpinBox_I2, 
                               QtCore.SIGNAL("valueChanged(double)"), self.updateFields)
        QtCore.QObject.connect(self.ui.doubleSpinBox_gx1x1,
                               QtCore.SIGNAL("valueChanged(double)"), self.updateFields)
        QtCore.QObject.connect(self.ui.doubleSpinBox_gx2x2,
                               QtCore.SIGNAL("valueChanged(double)"), self.updateFields)
        QtCore.QObject.connect(self.ui.doubleSpinBox_gx1x2,
                               QtCore.SIGNAL("valueChanged(double)"), self.updateFields)
        QtCore.QObject.connect(self.ui.doubleSpinBox_gx2x1,
                               QtCore.SIGNAL("valueChanged(double)"), self.updateFields)
        QtCore.QObject.connect(self.ui.doubleSpinBox_Ce, 
                               QtCore.SIGNAL("valueChanged(double)"), self.updateFields)
        QtCore.QObject.connect(self.ui.doubleSpinBox_x0, 
                               QtCore.SIGNAL("valueChanged(double)"), self.updateFields)
        
        # Graphics view for scatter plot
        scatter_pic = QtGui.QPixmap("/home/naze/Pictures/Hatosia.jpg")
        scatter_pic = scatter_pic.scaled(self.ui.graphicsView_scatter.size(),
                         QtCore.Qt.IgnoreAspectRatio, 
                         QtCore.Qt.SmoothTransformation)
        self.scatter_scene = QtGui.QGraphicsScene()
        self.scatter_scene.addPixmap(scatter_pic)
        self.ui.graphicsView_scatter.setScene(self.scatter_scene)
        self.ui.graphicsView_scatter.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.ui.graphicsView_scatter.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.ui.graphicsView_scatter.show()

        # Graphics view for Time Series
        ts_pic = QtGui.QPixmap("/home/naze/Pictures/fractal_eye.jpg")
        ts_pic = ts_pic.scaled(self.ui.graphicsView_ts.size(),
                                         QtCore.Qt.IgnoreAspectRatio,
                                         QtCore.Qt.SmoothTransformation)
        self.ts_scene = QtGui.QGraphicsScene()
        self.ts_scene.addPixmap(ts_pic)
        self.ui.graphicsView_ts.setScene(self.ts_scene)
        self.ui.graphicsView_ts.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.ui.graphicsView_ts.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.ui.graphicsView_ts.show()

        # Graphics view for correlation coefficient
        corr_pic = QtGui.QPixmap("/home/naze/Pictures/fractal_eye.jpg")
        corr_pic = corr_pic.scaled(self.ui.graphicsView_corr.size(),
                               QtCore.Qt.IgnoreAspectRatio,
                               QtCore.Qt.SmoothTransformation)
        self.corr_scene = QtGui.QGraphicsScene()
        self.corr_scene.addPixmap(corr_pic)
        self.ui.graphicsView_corr.setScene(self.corr_scene)
        self.ui.graphicsView_corr.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.ui.graphicsView_corr.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.ui.graphicsView_corr.show()

        # Graphics view for spectrum
        spect_pic = QtGui.QPixmap("/home/naze/Pictures/eye_visualizer.png")
        spect_pic = spect_pic.scaled(self.ui.graphicsView_spect.size(),
                                   QtCore.Qt.IgnoreAspectRatio,
                                   QtCore.Qt.SmoothTransformation)
        self.spect_scene = QtGui.QGraphicsScene()
        self.spect_scene.addPixmap(spect_pic)
        self.ui.graphicsView_spect.setScene(self.spect_scene)
        self.ui.graphicsView_spect.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.ui.graphicsView_spect.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.ui.graphicsView_spect.show()

        # Handle the parameter space map in a new window 
        self.mapWin = self.drawKOPmap()
        self.mapWin.show()
        self.mapWin.draw()
        self.previous_ax = [] #list of (normally only 1 or zero) axes object, referring to the last point seen in param space
        
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
        
        self.out_col_idx = self.adjustFieldValue(self.out_col_idx, self.ui.doubleSpinBox_Ce.value(), self.out_col_s)
        self.ui.doubleSpinBox_Ce.setValue(self.out_col_s[self.out_col_idx])
        
        self.in_row_idx = self.adjustFieldValue(self.in_row_idx, self.ui.doubleSpinBox_gx1x2.value(), self.in_row_s)
        self.ui.doubleSpinBox_gx1x2.setValue(self.in_row_s[self.in_row_idx])
        
        self.in_col_idx = self.adjustFieldValue(self.in_col_idx, self.ui.doubleSpinBox_gx2x1.value(), self.in_col_s)
        self.ui.doubleSpinBox_gx2x1.setValue(self.in_col_s[self.in_col_idx])
        
        self.out_row_idx = self.adjustFieldValue(self.out_row_idx, self.ui.doubleSpinBox_x0.value(), self.out_row_s)
        self.ui.doubleSpinBox_x0.setValue(self.out_row_s[self.out_row_idx])
        
        #print I1, I2, gx1x1, gx2x2, Ce, gx1x2, gx2x1
        self.drawPoint(self.in_row_idx, self.in_row_s, self.in_col_idx, self.in_col_s, 
                       self.out_row_idx, self.out_row_s, self.out_col_idx, self.out_col_s)
        
#        simpath = out_row_label + str(self.out_row_s[self.out_row_idx]).replace('.', '_') + '/' + \
#                   out_col_label + str(self.out_col_s[self.out_col_idx]).replace('.', '_') + '/' + \
#                   in_row_label + str(self.in_row_s[self.in_row_idx]).replace('.', '_') + '/' + \
#                   in_col_label + str(self.in_col_s[self.in_col_idx]).replace('.', '_') + '/' + '0/'
        #simpath = base1dir + out_col_label + str('{:f}'.format(self.out_col_s[self.out_col_idx]).rstrip('0')).replace('.', '_') + '/' + \
        simpath = base1dir + out_col_label + str(self.out_col_s[self.out_col_idx]).replace('.', '_') + '/' + \
                  base2dir + out_row_label + str(self.out_row_s[self.out_row_idx]).replace('.', '_') + '/' + \
                  base3dir + in_row_label + str(self.in_row_s[self.in_row_idx]).replace('.', '_') + '/' + \
                  base4dir + in_col_label + str(self.in_col_s[self.in_col_idx]).replace('.', '_') + '/' + '0/'
        print path + simpath

        # scatter
        scatter_pic = QtGui.QPixmap(path + simpath + 'SORN_scatter_1800_2000s_zoom.png')
        scatter_pic = scatter_pic.scaled(self.ui.graphicsView_scatter.size(),
                         QtCore.Qt.IgnoreAspectRatio, 
                         QtCore.Qt.SmoothTransformation)
        self.scatter_scene.addPixmap(scatter_pic)
        #self.ui.graphicsView_scatter.setScene()
        self.ui.graphicsView_scatter.show()

        # time series
        ts_pic = QtGui.QPixmap(path + simpath + 'SORN_mean_ts_1800_2000s_zoom.png')
        ts_pic = ts_pic.scaled(self.ui.graphicsView_ts.size(),
                               QtCore.Qt.IgnoreAspectRatio,
                               QtCore.Qt.SmoothTransformation)
        self.ts_scene.addPixmap(ts_pic)
        self.ui.graphicsView_ts.show()

        # Correlations
        corr_pic = QtGui.QPixmap(path + simpath + 'SORN_corrCoeff_1800_2000s.png')
        corr_pic = corr_pic.scaled(self.ui.graphicsView_corr.size(),
                               QtCore.Qt.IgnoreAspectRatio,
                               QtCore.Qt.SmoothTransformation)
        self.corr_scene.addPixmap(corr_pic)
        self.ui.graphicsView_corr.show()

        # Spectra
        spect_pic = QtGui.QPixmap(path + simpath + 'SORN_spectrum_1800_2000s.png')
        spect_pic = spect_pic.scaled(self.ui.graphicsView_spect.size(),
                                   QtCore.Qt.IgnoreAspectRatio,
                                   QtCore.Qt.SmoothTransformation)
        self.spect_scene.addPixmap(spect_pic)
        self.ui.graphicsView_spect.show()
        
    def adjustFieldValue(self, index, new_val, all_val):
        """adjust the value of the parameter from the spinboxes to existing values in parameter space"""
        if(new_val < all_val[index] and index > 0):
            index -= 1
        elif (new_val > all_val[index] and index < pb.size(all_val)):
            index += 1
        return index
            
    def drawPoint(self, in_y_index, in_y_s, in_x_index, in_x_s, out_y_index, out_y_s, out_x_index, out_x_s):
        """this function plots a point in the current map to know where we are in the parameter space"""
        # remove previous plotted point if there was one
        if len(self.previous_ax)!=0:
            del self.previous_ax[0].lines[:]
        #remember the out_y axes nay have been reversed so:
        #out_y_index = out_y_s.size-1 - out_y_index
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
        f = h5py.File(path + feature_4D_matrix)
        entropy = f['entropy']
        entropy = np.array(entropy)
        eshape = np.array(entropy.shape)
        while (eshape.shape[0] < 4):
            entropy = np.expand_dims(entropy, axis=-1)
            eshape = np.array(entropy.shape)
        entropy = entropy.reshape(out_row_vals.shape[0], out_col_vals.shape[0], in_row_vals.shape[0], in_col_vals.shape[0])
        fig = self.drawFig(entropy.transpose())
        mapWin = mapWindow()
        mapWin.set_figure(fig)
        return mapWin

    def drawFig(self, img_grid):
        # figure properties
        fig = pb.figure(figsize = (10, 6))
        row_length = len(out_row_vals)
        col_length = len(out_col_vals)
        gs = matplotlib.gridspec.GridSpec(row_length, col_length, wspace=.05, hspace=.05)  # +1 for the colormap area
        """figure processing"""
        img_grid_list = img_grid.tolist()
        # get min and max to set up colormap scale, and loop all again to plot images
        MIN = pb.array(img_grid).min()
        MAX = pb.array(img_grid).max()
        for out_row_index in range(len(out_row_vals)):
            for out_col_index in range(len(out_col_vals)):
                ax = fig.add_subplot(gs[row_length-1 - out_row_index, out_col_index])
                ax.hold(True)

                img_grid_list[out_row_index][out_col_index] = ax.contourf(img_grid[out_row_index][out_col_index],
                                                                             levels=pb.linspace(MIN, MAX, 50),
                                                                             extent=[in_col_vals.min(), in_col_vals.max(),
                                                                                     in_row_vals.min(), in_row_vals.max()],
                                                                             vmin=MIN, vmax=MAX)

                # set ticks and labels of axis (no number in legend for graphs not on borders):
                # for the x axis:
                xticks = in_col_vals
                ax.set_xticks(xticks)
                if (out_row_index > 0): #< row_length - 1):
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
        cbar = pb.colorbar(img_grid_list[0][0], ax)  # , ticks=ticksValues)
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
    
    
    