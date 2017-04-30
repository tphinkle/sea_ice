# Scipy
import numpy as np

# netCDF4
import netCDF4


class Model():
    def __init__(self):
        self.locs = {}
        self.locs['greenland'] = [-38.152,83.545]
        self.locs['bering'] = [185, 65]


        self.load_data()

    def load_data(self):
        sea_ice = netCDF4.Dataset("../data/G10010_SIBT1850_v1.1.nc", 'r')
        lat = sea_ice.variables['latitude'][:]
        lon = sea_ice.variables['longitude'][:]

        lats = lat[:]
        lons = lon[:]

        self.lons, self.lats = np.meshgrid(lons,lats)


        self.seaice_conc = sea_ice.variables['seaice_conc'][:]





    def get_time_from_index(self, index):
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
        month = months[index%12]
        year = index/12+1850

        return month + ' ' + str(year)


    def get_data_at_index(self, time_index):
        return self.seaice_conc[time_index,:,:]
        #return self.seaice_conc[time_index,:,:]



    def get_data_mean(self):
        return self.seaice_conc[:,:,:].mean(axis = (1,2))



    def get_data_roi_mean(self, roi):
        '''
        lat0 = roi[0]
        lat1 = roi[1]
        long0 = roi[2]
        long1 = roi[3]
        '''

        lat0 = 0
        lat1 = 100
        long0 = 0
        long1 = 100

        return self.seaice_conc[:, lat0:lat1, long0:long1].mean(axis = (1,2))
