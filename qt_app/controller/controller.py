# Python standard library
import itertools

class Controller():
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.setup_signals_slots()
        self.update_stats_plot('greenland')

    def setup_signals_slots(self):

        #rp_view._show_baseline_button.clicked.connect(lambda: \
            #self.toggle_show_baseline_ts(rp_model, rp_view))

        # Slider
        self.view.time_year_slider.sliderReleased.connect(self.time_slider_released)
        self.view.time_month_slider.sliderReleased.connect(self.time_slider_released)

        self.view.time_year_slider.valueChanged.connect(self.time_slider_value_changed)
        self.view.time_month_slider.valueChanged.connect(self.time_slider_value_changed)


        # ROI Buttons
        self.view.greenland_loc_button.clicked.connect(lambda: self.update_stats_plot('greenland'))
        self.view.bering_loc_button.clicked.connect(lambda: self.update_stats_plot('bering'))



        # Globe plot (matplotlib signals and slots method!)
        self.view.globe_plot.mpl_connect('draw_event', self.update_roi_button_positions)




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
        i = 0
        for key, value in self.model.locs.iteritems():
            i = i + 1
            pixel_coords = self.view.globe_plot.get_figure_coordinates(value)

            if key == 'greenland':
                button = self.view.greenland_loc_button
            if key == 'bering':
                button = self.view.bering_loc_button


            button.move(pixel_coords[0]+button.width()/2, pixel_coords[1]+630-button.height()/2)




        #greenland_coords = self.model.greenland_coords
        #greenland_pixel_coords = self.view.globe_plot.get_figure_coordinates(greenland_coords)

    def update_stats_plot(self, roi_name):
        #self.view.stats_plot.set
        pass

    def get_index_from_sliders(self):
        return (self.view.time_year_slider.value()-self.view.time_year_slider.minimum())*12+\
                    self.view.time_month_slider.value()
