# Python standard library
import itertools

# Scipy
import numpy as np

class Controller():
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.setup_signals_slots()



    def setup_signals_slots(self):

        #rp_view._show_baseline_button.clicked.connect(lambda: \
            #self.toggle_show_baseline_ts(rp_model, rp_view))

        # Slider
        self.view.time_year_slider.sliderReleased.connect(self.time_slider_released)
        self.view.time_month_slider.sliderReleased.connect(self.time_slider_released)

        self.view.time_year_slider.valueChanged.connect(self.time_slider_value_changed)
        self.view.time_month_slider.valueChanged.connect(self.time_slider_value_changed)


        # ROI Buttons
        self.view.west_greenland_loc_button.clicked.connect(self.update_stats_plot)
        self.view.bering_loc_button.clicked.connect(self.update_stats_plot)
        self.view.hudson_loc_button.clicked.connect(self.update_stats_plot)
        self.view.severny_loc_button.clicked.connect(self.update_stats_plot)

        self.view.west_greenland_loc_button.clicked.connect(lambda: self.set_active_roi('west_greenland'))
        self.view.bering_loc_button.clicked.connect(lambda: self.set_active_roi('bering'))
        self.view.hudson_loc_button.clicked.connect(lambda: self.set_active_roi('hudson'))
        self.view.severny_loc_button.clicked.connect(lambda: self.set_active_roi('severny'))


        # ROI sliders
        self.view.roi_lat0_slider.sliderReleased.connect(self.update_stats_plot)
        self.view.roi_long0_slider.sliderReleased.connect(self.update_stats_plot)

        self.view.roi_lat0_slider.valueChanged.connect(self.update_roi_positions)
        self.view.roi_long0_slider.valueChanged.connect(self.update_roi_positions)

        self.view.roi_lat1_slider.sliderReleased.connect(self.update_stats_plot)
        self.view.roi_long1_slider.sliderReleased.connect(self.update_stats_plot)

        self.view.roi_lat1_slider.valueChanged.connect(self.update_roi_positions)
        self.view.roi_long1_slider.valueChanged.connect(self.update_roi_positions)


        # Globe plot (matplotlib signals and slots method!)
        self.view.globe_plot.mpl_connect('draw_event', self.update_roi_button_positions)


    def update_roi_positions(self):

        roi_name = self.model.active_roi

        lat0 = self.view.roi_lat0_slider.value()
        lat1 = self.view.roi_lat1_slider.value()
        long0 = self.view.roi_long0_slider.value()
        long1 = self.view.roi_long1_slider.value()

        if lat0 > lat1:
            temp = lat0
            lat0 = lat1
            lat1 = temp

        if long0 > long1:
            temp = long0
            long0 = long1
            long1 = temp

        new_roi = [lat0, lat1, long0, long1]

        self.model.rois[roi_name] = new_roi
        self.view.globe_plot.plot_roi_patch(roi_name, new_roi[0], new_roi[1], new_roi[2], new_roi[3])

        self.update_roi_button_positions(None)

        self.view.globe_plot.draw()



    def time_slider_released(self):
        self.update_globe_plot()

    def time_slider_value_changed(self):
        months = {0:'Jan',\
                  1:'Feb',\
                  2:'Mar',\
                  3:'Apr',\
                  4:'May',\
                  5:'Jun',\
                  6:'Jul',\
                  7:'Aug',\
                  8:'Sep',\
                  9:'Oct',\
                  10:'Nov',\
                  11:'Dec'}

        self.view.time_month_lineedit.setText(months[self.view.time_month_slider.value()])

        self.view.time_year_lineedit.setText(str(self.view.time_year_slider.value()))




    def update_globe_plot(self):
        index = self.get_index_from_sliders()
        globe_data = self.model.get_data_at_index(index)
        self.view.globe_plot.set_data(self.model.lats, self.model.lons, globe_data)

    def update_roi_button_positions(self, event):
        for key, value in self.model.rois.iteritems():
            roi = self.model.rois[key]
            coord = [(roi[2]+roi[3])/2,\
                    (roi[0]+roi[1])/2]

            pixel_coords = self.view.globe_plot.get_figure_coordinates(coord)

            if key == 'west_greenland':
                button = self.view.west_greenland_loc_button
            elif key == 'bering':
                button = self.view.bering_loc_button
            elif key == 'hudson':
                button = self.view.hudson_loc_button
            elif key == 'severny':
                button = self.view.severny_loc_button

            #+50/200
            if pixel_coords[0] < 0 or pixel_coords[0] > 565 or pixel_coords[1] < 0 or pixel_coords[1] > 565:
                button.setVisible(False)
            else:
                button.setVisible(True)
                button.move(pixel_coords[0]+50-button.width()/2, pixel_coords[1]+200-button.height()/2)



    def set_active_roi(self, roi_name):
        self.model.active_roi = roi_name
        roi = self.model.rois[roi_name]
        if roi_name == 'custom':
            roi_name = roi[0]+':'+roi[1]+','+roi[2]+':'+roi[3]
        self.view.active_roi_lineedit.setText(roi_name)

        self.view.roi_lat0_slider.setValue(roi[0])
        self.view.roi_lat1_slider.setValue(roi[1])
        self.view.roi_long0_slider.setValue(roi[2])
        self.view.roi_long1_slider.setValue(roi[3])

    def update_stats_plot(self):
        roi_name = self.model.active_roi
        roi = self.model.rois[roi_name]
        #TimeSeries_sea_ice_change_in_roi(lonmin, lonmax, latmin, latmax, selectMonth=False, Month=3, last_N_years=0):
        #data = self.model.TimeSeries_sea_ice_change_in_roi(roi[0],
        #    roi[1], roi[2], roi[3], selectMonth=True)#, Month=3, last_N_years=0)

        data = self.model.TimeSeries_sea_ice_change_in_roi(roi[2],roi[3], roi[0], roi[1], selectMonth=True, Month=[3,9], last_N_years=0)
        self.view.stats_plot_item_roi_mar.setData(np.hstack((data[0], data[1])))
        self.view.stats_plot_item_roi_sep.setData(np.hstack((data[0], data[2])))

    def get_index_from_sliders(self):
        return (self.view.time_year_slider.value()-self.view.time_year_slider.minimum())*12+\
                    self.view.time_month_slider.value()
