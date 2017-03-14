#! c:\Python27\python.exe
from __future__ import with_statement
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 17 21:47:44 2016
@author: YOSI
"""

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
Bh = list(np.tile(np.nan,86400))
Bd = list(np.tile(np.nan,86400))
x_mean=np.zeros(1440)
y_mean=np.zeros(1440)
z_mean=np.zeros(1440)
h_mean=np.zeros(1440)
d_mean=np.zeros(1440)

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
    staname_init=list(np.tile(' ',45))
    staname_a = list(re.split('=|\n',init[0]))
    staname_a = staname_a[1]
    for q in range(0,len(staname_a)): staname_init[q]=staname_a[q]
    staname = ''.join(staname_init)
    
    stacode_init=list(np.tile(' ',45))
    stacode_a = list(re.split('=|\n',init[1]))
    stacode_a = stacode_a[1]
    for q in range(0,len(stacode_a)): stacode_init[q]=stacode_a[q]
    stacode = ''.join(stacode_init)
    
    lat_init=list(np.tile(' ',45))
    lat_a = list(re.split('=|\n',init[2]))
    lat_a = lat_a[1]
    for q in range(0,len(lat_a)): lat_init[q]=lat_a[q]
    lat = ''.join(lat_init)
    
    lon_init=list(np.tile(' ',45))
    lon_a = list(re.split('=|\n',init[3]))
    lon_a = lon_a[1]
    for q in range(0,len(lon_a)): lon_init[q]=lon_a[q]
    lon = ''.join(lon_init)
    
    elev_init=list(np.tile(' ',45))
    elev_a = list(re.split('=|\n',init[4]))
    elev_a = elev_a[1]
    for q in range(0,len(elev_a)): elev_init[q]=elev_a[q]
    elev = ''.join(elev_init)

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
            Bh[index] = np.sqrt((Bx[index]**2)+(By[index]**2))
            Bd[index] = 60 * np.degrees(np.arcsin(By[index] / Bh[index]))

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

for k in range(0,1440):
    if np.count_nonzero(np.isnan(Bh[(0+(60*k)):((60+(60*k)))])) <= 6:
        h_mean[k]=np.nanmean(Bh[(0+(60*k)):((60+(60*k)))])
    else:
        h_mean[k]=99999.00
    if np.count_nonzero(np.isnan(Bd[(0+(60*k)):((60+(60*k)))])) <= 6:
        d_mean[k]=np.nanmean(Bd[(0+(60*k)):((60+(60*k)))])
    else:
        d_mean[k]=99999.00
    if np.count_nonzero(np.isnan(Bz[(0+(60*k)):((60+(60*k)))])) <= 6:
        z_mean[k]=np.nanmean(Bz[(0+(60*k)):((60+(60*k)))])
    else:
        z_mean[k]=99999.00

#Menyimpan file output
fileout = stacode[0:3]+str(yyyy)+str(mo).zfill(2)+str(dd).zfill(2)+'.min'
f_iaga = open(fileout, 'w')

f_iaga.write(' Format                 IAGA-2002                                    |\n')
f_iaga.write(' Source of Data         BMKG                                         |\n')
f_iaga.write(' Station Name           %s|\n' %staname)
f_iaga.write(' IAGA Code              %s|\n' %stacode)
f_iaga.write(' Geodetic Latitude      %s|\n' %lat)
f_iaga.write(' Geodetic Longitude     %s|\n' %lon)
f_iaga.write(' Elevation              %s|\n' %elev)
f_iaga.write(' Reported               HDZF                                         |\n')
f_iaga.write(' Sensor Orientation     XYZ                                          |\n')
f_iaga.write(' Digital Sampling       1 second                                     |\n')
f_iaga.write(' Data Interval Type     Filtered 1-minute (00:15-01:45)              |\n')
f_iaga.write(' Data Type              variation                                    |\n')
f_iaga.write('DATE       TIME         DOY     %sH      %sD      %sZ      %sF   |\n' %(stacode[0:3],stacode[0:3],stacode[0:3],stacode[0:3]))

for j in range(0,1440):
    body_iaga = '%s    %9.2f %9.2f %9.2f %9.2f\n' %((date1+timedelta(minutes=j)).strftime("%Y-%m-%d %H:%M:%S.000 %j"),h_mean[j],d_mean[j],z_mean[j],88888)
    f_iaga.write(body_iaga)
f_iaga.close()

print '%s converted to %s' %(filename,fileout)
