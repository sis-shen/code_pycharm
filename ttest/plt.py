import matplotlib.pyplot as plt
from random import *
import numpy as np
import pandas as pd

from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d import axes3d
from mpl_toolkits.mplot3d import Axes3D

data = pd.read_csv('haiti\Haiti.csv')
data = data[(data.LATITUDE>18)&(data.LATITUDE<20)&(data.LONGITUDE>-75)&(data.LONGITUDE<-70)&data.CATEGORY.notnull()]
def get_all_categories(cat_series):
    cat_sets=(set(to_cat_list(x)) for x in cat_series) #生成器表达式
    return sorted(set.union(*cat_sets))
def to_cat_list(catstr):
    stripped=(x.strip() for x in catstr.split(','))
    return [x for x in stripped if x]
def get_english(cat):
    code,names=cat.split('.')
    if '|' in names:
        names=names.split('|')[1]
    return code,names.strip()
get_english('2.  Urgences logistique |Vital Lines')

all_cats=get_all_categories(data.CATEGORY)
english_mapping=dict(get_english(x) for x in all_cats)

def get_code(seq):
    return [x.split('.')[0] for x in seq if x]
all_codes=get_code(all_cats)
code_index=pd.Index(np.unique(all_codes))
dummy_frame=pd.DataFrame(np.zeros((len(data),len(code_index))),index=data.index,columns=code_index)
for row, cat in zip(data.index,data.CATEGORY):
    codes=get_code(to_cat_list(cat))
    dummy_frame.loc[row,codes]=1
    data = data.join(dummy_frame.add_prefix('category_'))
from mpl_toolkits.basemap import Basemap
def basic_haiti_map(ax=None, lllat = 17.25,urlat = 20.25,lllon = -75,urlon=-71):
    m = Basemap(ax=ax,projection = 'stere',
                lon_0=(urlon+lllon)/2,
                lat_0 = (urlat+lllat)/2,
                llcrnrlat = lllat,urcrnrlat=urlat,
                llcrnrlon = lllon,urcrnrlon = urlon,
                resolution = 'f')
    m.drawcoastlines()
    m.drawstates()
    m.drawcountries()
    return m

fig,axes = plt.subplots(nrows = 2,ncols =2,figsize=(12,10))
fig.subplots_adjust(hspace =0.05,wspace=0.05)
to_plot = ['2a','1','3c','7a']
lllat =17.25
urlat=20.25
lllon =-75
urlon=-71
for code,ax in zip(to_plot,axes.flat):
    m = basic_haiti_map(ax,lllat=lllat,urlat=urlat,lllon=lllon,urlon=urlon)
    cat_data=data[data['category_%s' % code] ==1]
    x, y = m(cat_data.LONGITUDE.values, cat_data.LATITUDE.values)
    m.plot(x,y,'k.',alpha = 0.5)
    ax.set_title('%s:%s' % (code, english_mapping[code]))
plt.show()