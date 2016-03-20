from __future__ import with_statement
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 17 21:47:44 2016

@author: YOSI
"""

def clear_all():
    """Clears all the variables from the workspace of the spyder application."""
    gl = globals().copy()
    for var in gl:
        if var[0] == '_': continue
        if 'func' in str(globals()[var]): continue
        if 'module' in str(globals()[var]): continue

        del globals()[var]
if __name__ == "__main__":
    clear_all()
    
clear_all()

from sys import argv
from datetime import datetime
from datetime import timedelta
import numpy as np
import re

yyyy = []; mo = []; dd = []; hh = []; mm = []; ss = []
Bx = []; By = []; Bz = []; Bf = []

Bx = list(np.tile(np.nan,86400))
By = list(np.tile(np.nan,86400))
Bz = list(np.tile(np.nan,86400))
Bf = list(np.tile(np.nan,86400))
x_mean=np.zeros(1440)
y_mean=np.zeros(1440)
z_mean=np.zeros(1440)
f_mean=np.zeros(1440)

try:
    script, filename = argv
except ValueError:
    print "Usage: lemi2iaga <namafileinput>"
    print "\nlemi2iaga - LEMI-018 to IAGA-2002 converter, Version 0.0.1"
    print "(c) 2015-2016 Yosi Setiawan"
    quit()

#Initialization
with open('lemi2iaga.ini') as f_ini:
    init = f_ini.readlines()
    staname_init = re.split('=|\n',init[0])
    stacode_init = re.split('=|\n',init[1])
    lat_init = re.split('=|\n',init[2])
    lon_init = re.split('=|\n',init[3])
    elev_init = re.split('=|\n',init[4])

#Import data Lemi   
namafile = filename
try:
    with open(namafile) as f_lemi:
        content = f_lemi.readlines()
        for i in range(0,len(content)):
            data = re.split('\s+',content[i])
            yyyy = int(data[0])
            mo = int(data[1])
            dd = int(data[2])
            hh = int(data[3])
            mm = int(data[4])
            ss = int(data[5])
            index = (hh*3600)+(mm*60)+ss
            Bx[index] = float(data[6])
            By[index] = float(data[7])
            Bz[index] = float(data[8])
            Bf[index] = np.sqrt((Bx[index]**2)+(By[index]**2)+(Bz[index]**2))

except IOError:
    print "Input file does not exist\nUsage: lemi2iaga <namafileinput>"
    print "\nlemi2iaga - LEMI-018 to IAGA-2002 converter, Version 0.0.1"
    print "(c) 2015-2016 Yosi Setiawan"
    quit()
    
#Membuat waktu selama 24 jam interval 1 detik
tahun = np.tile(yyyy,86400)
bulan = np.tile(mo,86400)
tanggal = np.tile(dd,86400)
jam = np.sort(np.tile(range(0,24),3600))
menit = np.tile(np.sort(np.tile(range(0,60),60)),24)
detik = np.tile(range(0,60),1440)

date1 = datetime(year=yyyy,month=mo,day=dd,hour=0,minute=0,second=0)

#Hitung rata-rata satu menit
for k in range(0,1440):
    if np.count_nonzero(np.isnan(Bx[(0+(60*k)):((60+(60*k)))])) <= 6:
        x_mean[k]=np.nanmean(Bx[(0+(60*k)):((60+(60*k)))])
    else:
        x_mean[k]=99999.00
    if np.count_nonzero(np.isnan(By[(0+(60*k)):((60+(60*k)))])) <= 6:
        y_mean[k]=np.nanmean(By[(0+(60*k)):((60+(60*k)))])
    else:
        y_mean[k]=99999.00
    if np.count_nonzero(np.isnan(Bz[(0+(60*k)):((60+(60*k)))])) <= 6:
        z_mean[k]=np.nanmean(Bz[(0+(60*k)):((60+(60*k)))])
    else:
        z_mean[k]=99999.00
    if np.count_nonzero(np.isnan(Bf[(0+(60*k)):((60+(60*k)))])) <= 6:
        f_mean[k]=np.nanmean(Bf[(0+(60*k)):((60+(60*k)))])
    else:
        f_mean[k]=99999.00

#Menyimpan file output
fileout = stacode_init[1]+str(yyyy)+str(mo).zfill(2)+str(dd).zfill(2)+'vmin'+'.min'
f_iaga = open(fileout, 'w')

f_iaga.write(' Format                 IAGA-2002                                    |\n')
f_iaga.write(' Source of Data         BMKG                                         |\n')
f_iaga.write(' Station Name           %s                                    |\n' %staname_init[1])
f_iaga.write(' IAGA Code              %s                                          |\n' %stacode_init[1])
f_iaga.write(' Geodetic Latitude      %s                                        |\n' %lat_init[1])
f_iaga.write(' Geodetic Longitude     %s                                       |\n' %lon_init[1])
f_iaga.write(' Elevation              %s                                           |\n' %elev_init[1])
f_iaga.write(' Reported               XYZF                                         |\n')
f_iaga.write(' Sensor Orientation     XYZ                                          |\n')
f_iaga.write(' Digital Sampling       1 second                                     |\n')
f_iaga.write(' Data Interval Type     Filtered 1-minute (00:15-01:45)              |\n')
f_iaga.write(' Data Type              variation                                    |\n')
f_iaga.write('DATE       TIME         DOY     TUNX      TUNY      TUNZ      TUNF   |\n')

for j in range(0,1440):
    body_iaga = '%s     %8.2f  %8.2f  %8.2f  %8.2f\n' %((date1+timedelta(minutes=j)).strftime("%Y-%m-%d %H:%M:%S.000 %j"),x_mean[j],y_mean[j],z_mean[j],f_mean[j])
    f_iaga.write(body_iaga)
f_iaga.write(' ')
f_iaga.close()

print '%s converted to %s' %(filename,fileout)
