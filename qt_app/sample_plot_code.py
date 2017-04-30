import netCDF4
import pandas as pd
import matplotlib.cm as cm
import matplotlib
import numpy as np
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

sea_ice = netCDF4.Dataset('data/G10010_SIBT1850_v1.1.nc','r')


lat = sea_ice.variables['latitude'][:]
lon = sea_ice.variables['longitude'][:]
seaice_conc = sea_ice.variables['seaice_conc'][:]
seaice_source = sea_ice.variables['seaice_source'][:]
time = sea_ice.variables['time'][:]


def time_slice(t):
    # t ranges from -55138 to 4731
    # return 240x1440 array of concentration at lon/lat at the given time
    if t in time:
        t_index = np.where( time==t )
        return seaice_conc[t_index][0]
    else:
        closest_neighbor = np.abs(time-t).min()
        t_index = np.where( time==closest_neighbor )

        return seaice_conc[t_index][0]

t = 4731

lats = lat[:]
lons = lon[:]
lons, lats = np.meshgrid(lons,lats)

map= Basemap(projection='npstere',boundinglat=50,lon_0=270,resolution='l')


fig = plt.figure(figsize=(9,9))
ax=fig.add_subplot(111)

#ax.annotate(r'10',
#                xy=(0.5,0.6),
#                xycoords='axes fraction',horizontalalignment='right',size=14, zorder=20)
#                 bbox=dict(facecolor='white', pad=9, edgecolor='grey'), backgroundcolor='white')

im1 = map.pcolormesh(lons,lats, time_slice(t),
                     shading='flat',
                     cmap=cm.seismic,
                     latlon=True,
                    zorder=0)
cb = map.colorbar(im1,"bottom", size="5%", pad="2%")


map.drawparallels(np.arange(50.,90.,10.), labels=[0,0,0,0])
map.drawmeridians(np.arange(-180.,181.,20.),latmax=90, labels=[0,0,0,0])
map.drawcoastlines(linewidth=0.3)
map.fillcontinents(color='chocolate',lake_color='lightblue', alpha=0.7, zorder=20)
map.drawmapboundary(fill_color='brown', linewidth=0.1)

plt.show()
