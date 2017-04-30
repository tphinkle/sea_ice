# Python standard library
import sys
sys.path.append('./../pyqtgraph')

# Scipy
import matplotlib.backends.backend_qt4agg
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.patches import Polygon
from mpl_toolkits.basemap import Basemap
import numpy as np

# PyQt
import PyQt4.QtCore
import PyQt4.QtGui
import pyqtgraph as pg

class GlobePlot(matplotlib.backends.backend_qt4agg.FigureCanvas):
    def __init__(self, parent=None):

        self.fig = plt.figure(figsize=(3,3), dpi = 50)
        self.axes = self.fig.add_subplot(111)

        matplotlib.backends.backend_qt4agg.FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        matplotlib.backends.backend_qt4agg.FigureCanvas.setSizePolicy(self,
                                   PyQt4.QtGui.QSizePolicy.Expanding,
                                   PyQt4.QtGui.QSizePolicy.Expanding)
        matplotlib.backends.backend_qt4agg.FigureCanvas.updateGeometry(self)

        self.setup_map()

        self.width, self.height = self.get_width_height()

        self.plot_all_roi_patches()


    def setup_map(self):

        self.map = Basemap(projection='npstere',boundinglat=50,lon_0=270,resolution='l')
        self.toolbar = matplotlib.backends.backend_qt4agg.NavigationToolbar2QT(self, self)
        self.toolbar.hide()
        self.toolbar.pan()

        self.im1 = None

        self.map.drawparallels(np.arange(50.,90.,10.), labels=[0,0,0,0],zorder=50, color='grey', linewidth=0.8)
        self.map.drawmeridians(np.arange(-180.,181.,20.),latmax=90, labels=[0,0,0,0],zorder=50,color='grey', linewidth=0.8)
        self.map.drawcoastlines(linewidth=0.3)
        self.map.fillcontinents(color='chocolate',lake_color='lightblue', alpha=0.7, zorder=20)
        self.map.drawmapboundary(fill_color='brown', linewidth=0.1)



    def get_figure_coordinates(self, coords):
        xpt, ypt = self.map(coords[0], coords[1])

        xy_pixels = self.axes.transData.transform(np.vstack([xpt,ypt]).T)[0]

        return xy_pixels[0], self.height - xy_pixels[1]




    def set_data(self, lats, longs, data):

        if self.im1:
            self.im1.remove()

        self.im1 = self.map.pcolormesh(longs, lats, data,
                             shading='flat',
                             cmap=cm.seismic,
                             latlon=True,
                            zorder=0)

        self.colorbar = self.map.colorbar(self.im1, "bottom", size="5%", pad="2%")

        self.fig.tight_layout()
        self.draw()

    def plot_roi_patch(self, latmin,latmax,lonmin,lonmax, map):

        x1,y1 = map(lonmax, latmax)   # lon_max, lat_max
        x2,y2 = map(lonmax, latmin)   # lon_max, lat_min
        xmid1, ymid1 = map( (lonmax+lonmin)/2, latmin  )
        x3,y3 = map(lonmin, latmin)   # lon_min, lat_min
        x4,y4 = map(lonmin, latmax)  # lon_min, lat_max
        xmid2, ymid2 = map( (lonmax+lonmin)/2, latmax  )

        boundary=[]
        boundary.append([x1,y1])
        boundary.append([x2,y2])

        for n in range((lonmax-lonmin)*3):
            xx,yy = map(lonmax-(n+1)/3., latmin)
            boundary.append([xx,yy])

        boundary.append([x3,y3])
        boundary.append([x4,y4])

        for n in range((lonmax-lonmin)*3):
            xx,yy = map(lonmin+(n+1)/3., latmax)
            boundary.append([xx,yy])

        p = Polygon(boundary,
            facecolor='yellow', edgecolor='yellow',linewidth = 6, zorder = 1000, alpha = 0.35, ls = '-')
        plt.gca().add_patch(p)

    def plot_all_roi_patches(self):
        # West greenland
        latmin, latmax= 66,75
        lonmin, lonmax= 290,310 #220,240
        self.plot_roi_patch(latmin,latmax,lonmin,lonmax, self.map)

        # Hudson Bay
        latmin, latmax= 55,65
        lonmin, lonmax= 265,285
        self.plot_roi_patch(latmin,latmax,lonmin,lonmax, self.map)

        # Bering Strait
        latmin, latmax= 63,70
        lonmin, lonmax= 180,199
        self.plot_roi_patch(latmin,latmax,lonmin,lonmax, self.map)


class View(PyQt4.QtGui.QMainWindow):
    def __init__(self, parent = None):
        super(View, self).__init__(None)

        self.res = [1280,800]

        self.showFullScreen()
        #self.setGeometry(0,0,800,600)

        self.setup_layout()

        self.setup_time_widgets()
        self.setup_stats_roi_sliders()
        self.setup_globe_plot()
        self.setup_stats_plot()
        self.setup_loc_buttons()

        self.globe_plot.get_figure_coordinates([0,0])









    def set_defaults(self):
        # Time
        self.time_year_lineedit.setText('1850')
        self.time_month_lineedit.setText('Jan')



    def setup_layout(self):


        return

    def setup_time_widgets(self):
        # slider
        self.time_year_slider = PyQt4.QtGui.QSlider(parent = self, orientation = PyQt4.QtCore.Qt.Horizontal)
        self.time_year_slider.setGeometry(50,150,500,50)
        self.time_year_slider.setMinimum(1850)
        self.time_year_slider.setMaximum(2013)
        self.time_year_slider.show()

        self.time_month_slider = PyQt4.QtGui.QSlider(parent = self, orientation = PyQt4.QtCore.Qt.Horizontal)
        self.time_month_slider.setGeometry(50,100,500,50)
        self.time_month_slider.setMinimum(0)
        self.time_month_slider.setMaximum(11) # Total data points
        self.time_month_slider.show()



        # lineedit
        self.time_year_lineedit = PyQt4.QtGui.QLineEdit(parent = self)
        self.time_year_lineedit.setGeometry(550,150,100,65)
        self.time_year_lineedit.setAlignment(PyQt4.QtCore.Qt.AlignHCenter)
        self.time_year_lineedit.setStyleSheet("""
        .QLineEdit {
            border: 0px solid black;
            border-radius: 10px;
            background-color: rgba(255, 255, 255, 0);
            }
        """)
        self.time_year_lineedit.show()

        self.time_month_lineedit = PyQt4.QtGui.QLineEdit(parent = self)
        self.time_month_lineedit.setGeometry(550,100,100,65)
        self.time_month_lineedit.setAlignment(PyQt4.QtCore.Qt.AlignHCenter)
        self.time_month_lineedit.setStyleSheet("""
        .QLineEdit {
            border: 0px solid black;
            border-radius: 10px;
            background-color: rgba(255, 255, 255, 0);
            }
        """)
        self.time_month_lineedit.show()




    def setup_stats_roi_sliders(self):
        pass

    def setup_globe_plot(self):
        self.globe_plot = GlobePlot(self)
        self.globe_plot.setGeometry(50,200,565,565)
        self.globe_plot.show()


    def setup_stats_plot(self):
        self.stats_plot = pg.PlotWidget(parent = self)

        self.stats_plot.setLabel('left', text = 'Mean concentration (units)')
        self.stats_plot.setLabel('bottom', text = 'Time (s)')
        self.stats_plot.showGrid(x = True, y = True, alpha = 0.2)


        self.stats_plot.setGeometry(665,200,565,565)

        pen_0 = PyQt4.QtGui.QPen(PyQt4.QtGui.QColor(200,200,200))
        pen_1 = PyQt4.QtGui.QPen(PyQt4.QtGui.QColor(200,50,75))

        self.stats_plot_item_roi = pg.PlotDataItem()
        self.stats_plot_item_roi.setPen(pen_0)

        self.stats_plot.addItem(self.stats_plot_item_roi)

        self.stats_plot_item_full = pg.PlotDataItem()
        self.stats_plot_item_full.setPen(pen_1)

        self.stats_plot.addItem(self.stats_plot_item_full)

        self.stats_plot.show()



    def setup_loc_buttons(self):
        # Greenland
        self.greenland_loc_button = PyQt4.QtGui.QPushButton('X', self)
        self.greenland_loc_button.setStyleSheet('''
                            background-color: rgba(255,255,255,0);
                            color: green
                            ''' )
        self.greenland_loc_button.setFont(PyQt4.QtGui.QFont("Arial", 20, PyQt4.QtGui.QFont.Bold))
        self.greenland_loc_button.setMaximumWidth(30)
        self.greenland_loc_button.setMaximumHeight(30)

        self.greenland_loc_button.show()



        # Bering
        self.bering_loc_button = PyQt4.QtGui.QPushButton('X', self)
        self.bering_loc_button.setStyleSheet('''
                            background-color: rgba(255,255,255,0);
                            color: green
                            ''' )
        self.bering_loc_button.setFont(PyQt4.QtGui.QFont("Arial", 20, PyQt4.QtGui.QFont.Bold))
        self.bering_loc_button.setMaximumWidth(30)
        self.bering_loc_button.setMaximumHeight(30)

        self.bering_loc_button.show()
