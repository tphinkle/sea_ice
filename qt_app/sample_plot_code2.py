
# west Greenland
latmin, latmax= 66,75
lonmin, lonmax= 290,310  

# Hudson Bay
latmin, latmax= 55,65
lonmin, lonmax= 265,285   

# Bering Strait
latmin, latmax= 63,70
lonmin, lonmax= 180,199 


def TimeSeries_sea_ice_change_in_roi(lonmin, lonmax, latmin, latmax, selectMonth=False, Month=3, last_N_years=0):
    # if selectMonth=True, only returns ice concentration for the selected Month (1=Jan, 2=Feb, etc.)
    minlat_index = np.argmin(abs(lat-latmin))
    maxlat_index = np.argmin(abs(lat-latmax))
    minlon_index = np.argmin(abs(lon-lonmin))
    maxlon_index = np.argmin(abs(lon-lonmax))

    roi_conc_cube = seaice_conc[:,maxlat_index:minlat_index,minlon_index:maxlon_index]
    
    time_arr = []
    conc_time_series=[]
    
    num_points = 0  #roi_conc_cube.shape[1] * roi_conc_cube.shape[2]
    N_years = int(len(time)/12)
  
    if selectMonth==False:
        xdim, ydim = roi_conc_cube[0].shape[0], roi_conc_cube[0].shape[1]
        
        for t in range(roi_conc_cube.shape[0]):
            time_arr.append(time[t])
            sum=0.
            Npoints=0
            
            for x in range(xdim):
                for y in range(ydim):
                    elem = roi_conc_cube[t][x][y]
                    if elem>-0.1:
                        sum+=elem
                        Npoints+=1
            conc_time_series.append( sum/Npoints )
    else:
        xdim, ydim = roi_conc_cube[0].shape[0], roi_conc_cube[0].shape[1]
        for y in range(0,N_years):
            index = y*12 + Month
            time_arr.append( time[index] )
            sum=0.
            Npoints=0

            for x in range(xdim):
                for y in range(ydim):
                    elem = roi_conc_cube[index][x][y]
                    if elem>-0.1:
                        sum+=elem
                        Npoints+=1
            conc_time_series.append( sum/Npoints )
            #conc_time_series.append( roi_conc_cube[index].sum() / num_points ) 
            
    #adjusted_time, conc_time_series = TS[0], TS[1]
    adjusted_time = time_arr - np.min(time_arr)

    time_years = []
    for d in range(len(adjusted_time)):
        time_years.append(1850+d)

    fig=plt.figure(figsize=(8,5))
    ax=fig.add_subplot(111)
    ax.set_xlabel('Year')
    ax.set_ylabel('Average Ice Concentration [%]')
    #ax.set_xscale('log')
    ax.plot(time_years[-last_N_years:], conc_time_series[-last_N_years:], 'o')
    month_arr= ['January','February', 'March', 'April', 'May', 'June','July','August','September','October','November','December']
    if selectMonth==True:
        ax.set_title(month_arr[Month-1])



def plot_roi_patch(latmin,latmax,lonmin,lonmax, map):

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
        facecolor='red',edgecolor='blue',linewidth=2)
    plt.gca().add_patch(p) 
    

map = Basemap(projection='npstere',boundinglat=50,lon_0=270,resolution='l') 

map.fillcontinents(color='coral',lake_color='lightblue', alpha=0.9, zorder=-20)
map.drawcoastlines() 
map.drawmapboundary(fill_color='lightblue')
map.drawparallels(np.arange(40.,90.,10))
map.drawmeridians(np.arange(-180.,181.,20.),latmax=90)


# west Greenland
latmin, latmax= 66,75
lonmin, lonmax= 290,310 #220,240    
plot_roi_patch(latmin,latmax,lonmin,lonmax, map)
plt.show() 

TimeSeries_sea_ice_change_in_roi(lonmin, lonmax, latmin, latmax, selectMonth=True, Month=9, last_N_years=60)
TimeSeries_sea_ice_change_in_roi(lonmin, lonmax, latmin, latmax, selectMonth=True, Month=3, last_N_years=60)



map = Basemap(projection='npstere',boundinglat=50,lon_0=270,resolution='l') 

map.fillcontinents(color='coral',lake_color='lightblue', alpha=0.9, zorder=-20)
map.drawcoastlines() 
map.drawmapboundary(fill_color='lightblue')
map.drawparallels(np.arange(40.,90.,10))
map.drawmeridians(np.arange(-180.,181.,20.),latmax=90)
# Hudson Bay
latmin, latmax= 55,65
lonmin, lonmax= 265,285   

plot_roi_patch(latmin,latmax,lonmin,lonmax, map)

TimeSeries_sea_ice_change_in_roi(lonmin, lonmax, latmin, latmax, selectMonth=True, Month=9, last_N_years=60)
TimeSeries_sea_ice_change_in_roi(lonmin, lonmax, latmin, latmax, selectMonth=True, Month=3, last_N_years=60)

plt.show() 
