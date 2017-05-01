# Scipy
import numpy as np

# netCDF4
import netCDF4


class Model():
    def __init__(self):
        self.locs = {}
        #self.locs['west_greenland'] = [70.,300.]
        #self.locs['hudson'] = [60.,275.]
        #self.locs['bering'] = [66.,190.]
        self.active_roi = 'west_greenland'

        self.locs['west_greenland'] = [300.,70.]
        self.locs['hudson'] = [275.,60.]
        self.locs['bering'] = [190.,66.]
        self.locs['severny'] = [62.5, 75]

        self.rois = {}
        self.rois['west_greenland'] = [66,75,290,310]
        self.rois['hudson'] = [55,65,265,285]
        self.rois['bering'] = [63,70,180,199]
        self.rois['severny'] = [70,80,50,75]
        self.load_data()

    def load_data(self):
        sea_ice = netCDF4.Dataset("../data/G10010_SIBT1850_v1.1.nc", 'r')
        self.lat = sea_ice.variables['latitude'][:]
        self.lon = sea_ice.variables['longitude'][:]
        self.time = sea_ice.variables['time'][:]

        self.lats = self.lat[:]
        self.lons = self.lon[:]

        self.lons, self.lats = np.meshgrid(self.lons,self.lats)


        self.seaice_conc = sea_ice.variables['seaice_conc'][:]


    def TimeSeries_sea_ice_change_in_roi(self, lonmin, lonmax, latmin, latmax, selectMonth=False, Month=[3,9], last_N_years=0):
        # if selectMonth=True, only returns ice concentration for the selected Month (1=Jan, 2=Feb, etc.)
        minlat_index = np.argmin(abs(self.lat-latmin))
        maxlat_index = np.argmin(abs(self.lat-latmax))
        minlon_index = np.argmin(abs(self.lon-lonmin))
        maxlon_index = np.argmin(abs(self.lon-lonmax))

        roi_conc_cube = self.seaice_conc[:,maxlat_index:minlat_index,minlon_index:maxlon_index]

        time_arr = []
        conc_time_series=[]
        if len(Month)>1:
            for m in Month:
                conc_time_series.append([])

        num_points = 0  #roi_conc_cube.shape[1] * roi_conc_cube.shape[2]
        N_years = int(len(self.time)/12)

        if selectMonth==False:
            xdim, ydim = roi_conc_cube[0].shape[0], roi_conc_cube[0].shape[1]

            for t in range(roi_conc_cube.shape[0]):
                time_arr.append( self.time[t] )
                sum=0.
                Npoints=0

                for x in range(xdim):
                    for y in range(ydim):
                        elem = roi_conc_cube[t][x][y]
                        if elem > -0.1:
                            sum+=elem
                            Npoints+=1
                conc_time_series.append( sum/Npoints )
        else:


            xdim, ydim = roi_conc_cube[0].shape[0], roi_conc_cube[0].shape[1]

            seaice_conc_temptemp = self.seaice_conc[:,latmin:latmax, lonmin:lonmax]

            for m in range(len(Month)):
                for yr in range(0,N_years):
                    index = yr*12 + Month[m]
                    if m==0:
                        time_arr.append( self.time[index] )
                    sum=0.
                    Npoints=0

                    indices = np.where(seaice_conc_temptemp[index,:,:] > -0.1)
                    seaice_conc_temp = seaice_conc_temptemp[index, indices[0], indices[1]]
                    Npoints = seaice_conc_temp.shape[0]
                    conc_time_series[m].append(np.mean(seaice_conc_temp))


            '''
            xdim, ydim = roi_conc_cube[0].shape[0], roi_conc_cube[0].shape[1]
            for m in range(len(Month)):
                for yr in range(0,N_years):
                    index = yr*12 + Month[m]
                    if m==0:
                        time_arr.append( self.time[index] )
                    sum=0.
                    Npoints=0



                    for x in range(xdim):
                        for y in range(ydim):
                            elem = roi_conc_cube[index,x,y] #roi_conc_cube[index][x][y]
                            if elem > -0.1:
                                sum+=elem
                                Npoints+=1
                    conc_time_series[m].append( sum/Npoints )
                #conc_time_series.append( roi_conc_cube[index].sum() / num_points )
            '''

        #adjusted_time, conc_time_series = TS[0], TS[1]
        adjusted_time = time_arr - np.min(time_arr)

        time_years = []
        for d in range(len(adjusted_time)):
            time_years.append(1850+d)


        time_years = np.array(time_years).reshape(-1,1)
        conc_time_series1 = np.array(conc_time_series[0]).reshape(-1,1)
        conc_time_series2 = np.array(conc_time_series[1]).reshape(-1,1)


        return time_years, conc_time_series1, conc_time_series2





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
        lat0 = roi[2]
        lat1 = roi[3]
        long0 = roi[0]
        long1 = roi[1]

        return self.seaice_conc[:, lat0:lat1, long0:long1].mean(axis = (1,2))
