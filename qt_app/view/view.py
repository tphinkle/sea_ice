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

        self.fig = plt.figure(figsize=(3,3), dpi = 10)
        self.axes = self.fig.add_subplot(111)

        self.patches = {'west_greenland': None,\
            'bering': None,\
            'severny': None,\
            'hudson': None,\
            'custom': None}

        matplotlib.backends.backend_qt4agg.FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        matplotlib.backends.backend_qt4agg.FigureCanvas.setSizePolicy(self,
                                   PyQt4.QtGui.QSizePolicy.Expanding,
                                   PyQt4.QtGui.QSizePolicy.Expanding)
        matplotlib.backends.backend_qt4agg.FigureCanvas.updateGeometry(self)

        self.setup_map()

        self.width, self.height = 565, 565

        self.plot_all_roi_patches()










    def setup_map(self):

        self.map = Basemap(projection='npstere',boundinglat=50,lon_0=270,resolution='l')
        self.toolbar = matplotlib.backends.backend_qt4agg.NavigationToolbar2QT(self, self)
        self.toolbar.hide()
        self.toolbar.pan()

        self.im1 = None

        self.map.drawparallels(np.arange(50.,90.,10.), labels=[0,0,0,0],zorder=50, color='grey', linewidth=5)
        self.map.drawmeridians(np.arange(-180.,181.,20.),latmax=90, labels=[0,0,0,0],zorder=50,color='grey', linewidth=5)
        self.map.drawcoastlines(linewidth=1)
        self.map.fillcontinents(color='chocolate',lake_color='lightblue', alpha=1, zorder=20)
        self.map.drawmapboundary(fill_color='brown', linewidth=1)



    def get_figure_coordinates(self, coords):
        xpt, ypt = self.map(coords[0], coords[1])


        xy_pixels = self.axes.transData.transform([xpt,ypt])
        #xy_pixels = self.fig.transFigure.transform()

        #xy_pixels = self.fig.transFigure.inverted().transform(xy_pixels)

        fig_x = xy_pixels[0]
        fig_y = self.height - xy_pixels[1]


        return fig_x, fig_y




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

    def plot_roi_patch(self, roi_name, latmin, latmax, lonmin, lonmax):

        x1,y1 = self.map(lonmax, latmax)   # lon_max, lat_max
        x2,y2 = self.map(lonmax, latmin)   # lon_max, lat_min
        xmid1, ymid1 = self.map( (lonmax+lonmin)/2, latmin  )
        x3,y3 = self.map(lonmin, latmin)   # lon_min, lat_min
        x4,y4 = self.map(lonmin, latmax)  # lon_min, lat_max
        xmid2, ymid2 = self.map( (lonmax+lonmin)/2, latmax  )

        boundary=[]
        boundary.append([x1,y1])
        boundary.append([x2,y2])

        for n in range((lonmax-lonmin)*3):
            xx,yy = self.map(lonmax-(n+1)/3., latmin)
            boundary.append([xx,yy])

        boundary.append([x3,y3])
        boundary.append([x4,y4])

        for n in range((lonmax-lonmin)*3):
            xx,yy = self.map(lonmin+(n+1)/3., latmax)
            boundary.append([xx,yy])

        if self.patches[roi_name]:
            self.patches[roi_name].remove()

        self.patches[roi_name] = Polygon(boundary,
            facecolor='yellow', edgecolor='yellow',linewidth = 6, zorder = 1000, alpha = 0.35, ls = '-')
        plt.gca().add_patch(self.patches[roi_name])


    def plot_all_roi_patches(self):
        # West greenland
        latmin, latmax= 66,75
        lonmin, lonmax= 290,310 #220,240
        self.plot_roi_patch('west_greenland', latmin,latmax,lonmin,lonmax)

        # Hudson Bay
        latmin, latmax= 55,65
        lonmin, lonmax= 265,285
        self.plot_roi_patch('hudson', latmin,latmax,lonmin,lonmax)

        # Bering Strait
        latmin, latmax= 63,70
        lonmin, lonmax= 180,199
        self.plot_roi_patch('bering', latmin,latmax,lonmin,lonmax)

        # Severny
        latmin, latmax = 70, 80
        lonmin, lonmax = 50, 75
        self.plot_roi_patch('severny', latmin, latmax, lonmin, lonmax)

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
        self.setup_roi_sliders()
        self.setup_conc_labels()

        self.globe_plot.get_figure_coordinates([0,0])





        self.setup_roi_sliders()


    def setup_conc_labels(self):
        self.conc_0_lineedit = PyQt4.QtGui.QLineEdit('0', parent = self)
        self.conc_0_lineedit.setGeometry(50,800,50,55)
        self.conc_0_lineedit.setStyleSheet("""
            .QLineEdit {
                border: 0px solid black;
                border-radius: 10px;
                background-color: rgba(0, 0, 255, 0);
                }
                """)
        self.conc_0_lineedit.show()

        self.conc_50_lineedit = PyQt4.QtGui.QLineEdit('50', parent = self)
        self.conc_50_lineedit.setGeometry(50+565/2,800,50,55)
        self.conc_50_lineedit.setStyleSheet("""
            .QLineEdit {
                border: 0px solid black;
                border-radius: 10px;
                background-color: rgba(255, 255, 255, 0);
                }
                """)
        self.conc_50_lineedit.show()

        self.conc_100_lineedit = PyQt4.QtGui.QLineEdit('100', parent = self)
        self.conc_100_lineedit.setGeometry(50+565,800,50,55)
        self.conc_100_lineedit.setStyleSheet("""
            .QLineEdit {
                border: 0px solid black;
                border-radius: 10px;
                background-color: rgba(255, 0, 0, 0);
                }
                """)
        self.conc_100_lineedit.show()







    def setup_roi_sliders(self):
        self.roi_lat0_slider = PyQt4.QtGui.QSlider(parent = self, orientation = PyQt4.QtCore.Qt.Horizontal)
        self.roi_lat0_slider.setGeometry(715,150,250,50)
        self.roi_lat0_slider.setMinimum(40)
        self.roi_lat0_slider.setMaximum(90)
        self.roi_lat0_slider.show()


        self.roi_long0_slider = PyQt4.QtGui.QSlider(parent = self, orientation = PyQt4.QtCore.Qt.Horizontal)
        self.roi_long0_slider.setGeometry(715,100,250,50)
        self.roi_long0_slider.setMinimum(0)
        self.roi_long0_slider.setMaximum(360) # Total data points
        self.roi_long0_slider.show()

        self.roi_lat1_slider = PyQt4.QtGui.QSlider(parent = self, orientation = PyQt4.QtCore.Qt.Horizontal)
        self.roi_lat1_slider.setGeometry(980,150,250,50)
        self.roi_lat1_slider.setMinimum(40)
        self.roi_lat1_slider.setMaximum(90)
        self.roi_lat1_slider.show()


        self.roi_long1_slider = PyQt4.QtGui.QSlider(parent = self, orientation = PyQt4.QtCore.Qt.Horizontal)
        self.roi_long1_slider.setGeometry(980,100,250,50)
        self.roi_long1_slider.setMinimum(0)
        self.roi_long1_slider.setMaximum(360) # Total data points
        self.roi_long1_slider.show()

        self.roi_lat_lineedit = PyQt4.QtGui.QLineEdit('LAT', parent = self)
        self.roi_lat_lineedit.setGeometry(665,150,50,65)
        self.roi_lat_lineedit.show()

        self.roi_long_lineedit = PyQt4.QtGui.QLineEdit('LONG', parent = self)
        self.roi_long_lineedit.setGeometry(665,100,50,65)
        self.roi_long_lineedit.show()

        self.active_roi_lineedit = PyQt4.QtGui.QLineEdit('', parent = self)
        self.active_roi_lineedit.setGeometry(665,50,200,65)
        self.active_roi_lineedit.show()

        for le in [self.roi_long_lineedit, self.roi_lat_lineedit, self.active_roi_lineedit]:
            le.setStyleSheet("""
            .QLineEdit {
                border: 0px solid black;
                border-radius: 10px;
                background-color: rgba(255, 255, 255, 0);
                }
                """)



    def set_defaults(self):
        # Time

        self.severny_loc_button.clicked.emit(True)


        self.time_month_slider.setSliderPosition(2)
        self.time_month_slider.sliderReleased.emit()


        self.time_year_slider.setSliderPosition(1950)
        self.time_year_slider.sliderReleased.emit()



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

        pen_0 = PyQt4.QtGui.QPen(PyQt4.QtGui.QColor(238,50,50))
        pen_1 = PyQt4.QtGui.QPen(PyQt4.QtGui.QColor(50,175,238))

        self.stats_plot_item_roi_mar = pg.PlotDataItem(name = 'Mar')
        self.stats_plot_item_roi_mar.setPen(pen_1)

        self.stats_plot.addItem(self.stats_plot_item_roi_mar)

        self.stats_plot_item_roi_sep = pg.PlotDataItem(name = 'Sep')
        self.stats_plot_item_roi_sep.setPen(pen_0)

        self.stats_plot.addItem(self.stats_plot_item_roi_sep)

        self.stats_plot.addLegend()


        #self.stats_plot_item_full = pg.PlotDataItem()
        #self.stats_plot_item_full.setPen(pen_1)

        #self.stats_plot.addItem(self.stats_plot_item_full)

        self.stats_plot.show()



    def setup_loc_buttons(self):
        # West greenland
        self.west_greenland_loc_button = PyQt4.QtGui.QPushButton('X', self)
        self.west_greenland_loc_button.setStyleSheet('''
                            background-color: rgba(255,255,255,0);
                            color: green
                            ''' )
        self.west_greenland_loc_button.setFont(PyQt4.QtGui.QFont("Arial", 20, PyQt4.QtGui.QFont.Bold))
        self.west_greenland_loc_button.setMaximumWidth(30)
        self.west_greenland_loc_button.setMaximumHeight(30)

        self.west_greenland_loc_button.show()



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

        # Hudson
        self.hudson_loc_button = PyQt4.QtGui.QPushButton('X', self)
        self.hudson_loc_button.setStyleSheet('''
                            background-color: rgba(255,255,255,0);
                            color: green
                            ''' )
        self.hudson_loc_button.setFont(PyQt4.QtGui.QFont("Arial", 20, PyQt4.QtGui.QFont.Bold))
        self.hudson_loc_button.setMaximumWidth(30)
        self.hudson_loc_button.setMaximumHeight(30)

        self.hudson_loc_button.show()

        # Severny
        self.severny_loc_button = PyQt4.QtGui.QPushButton('X', self)
        self.severny_loc_button.setStyleSheet('''
                            background-color: rgba(255,255,255,0);
                            color: green
                            ''' )
        self.severny_loc_button.setFont(PyQt4.QtGui.QFont("Arial", 20, PyQt4.QtGui.QFont.Bold))
        self.severny_loc_button.setMaximumWidth(30)
        self.severny_loc_button.setMaximumHeight(30)

        self.severny_loc_button.show()
