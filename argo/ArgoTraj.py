import xarray as xr
import numpy as np
import pandas as pd

DS=xr.open_dataset('../ArgoFloats_03e9_6ccd_bc4e.nc')
DS=DS.where((~np.isnan(DS.latitude))&(~np.isnan(DS.longitude)),drop=True)

#MED + BS
DS=DS.where((DS.latitude>29)&(DS.latitude<46)&(DS.longitude>-5)&(DS.longitude<40),drop=True)
#IGNORE SOME ATL FLOAT
DS=DS.where(~DS.platform_number.isin(['6901621','2902402','6902571']),drop=True)


platf=np.unique(DS.platform_number.values)
indz=1

for pl in range(len(platf)):    
    DSb=DS.where(DS.platform_number.isin([platf[pl]]),drop=True)      
    DSb=DSb.sortby('time')

    if(np.abs(DSb.longitude.max()-DSb.longitude.min())<100):
        print 'var data_'+str(indz)+'= ['
        for pos in range(len(DSb.row)):      
	        thistime=pd.to_datetime(DSb.time[pos].values)
	        print '{\"wmo\":\"'+platf[pl]+'\",\"latitude\":'+str(DSb.latitude[pos].values)+',\"longitude\":'+str(DSb.longitude[pos].values)+',\"time\":\"'+thistime.strftime('%Y-%m-%d %H:%M:%S')+'\"},'        
        print '{\"wmo\":\"'+platf[pl]+'\",\"latitude\":'+str(DSb.latitude[pos].values)+',\"longitude\":'+str(DSb.longitude[pos].values)+',\"time\":\"2018-12-31 23:59:59\"}'
        print '];'
        indz=indz+1

print 'var float_number = '+str(indz-1)+';'

