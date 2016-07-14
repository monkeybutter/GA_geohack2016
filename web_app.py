from flask import Flask, request
import matplotlib
# Force matplotlib to not use any Xwindows backend.
matplotlib.use('Agg')
import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import pandas.io.sql as pdsql
from flask import send_file
import numpy as np
import cartopy
import cartopy.crs as ccrs
import os

app = Flask(__name__, static_url_path='/static')


conn_string = "host='150.203.254.19' dbname='nw_2010' user='dh8_conn_admin' password='ge0hack!'"
conn = psycopg2.connect(conn_string)
cursor = conn.cursor()

def plot(t1, t2):
    os.system('rm ./images/*.png')
    
    query = "SELECT REL_ID, TIME_, ST_X(geom), ST_Y(geom), ST_Z(geom) AS depth FROM nw_2010_01_26d10 WHERE TIME_ BETWEEN '{}'::timestamp AND '{}'::timestamp LIMIT 20000".format(t1, t2)   
    df = pdsql.read_sql(query, conn)
    
    time = df['time_'].unique()
    # The extents of the image we are plotting
    img_extent = (df['st_x'].min(), df['st_x'].max(), df['st_y'].min(), df['st_y'].max())
    ids = df['rel_id'].unique()
    cmap = cm.jet(np.arange(len(ids)))
    
    for i in range(0, len(time[:200])):
        print time[i]
        dfi = df[df['time_'] == time[i]]
        
        plt.figure(figsize=(12,6))

        # Setup the axes projection
        ax = plt.axes(projection=ccrs.PlateCarree())

        # Define the projection information of the image
        img_proj = ccrs.PlateCarree()

        # Extent of the axes in the plot
        extent = [img_extent[0]-3, img_extent[1]+3, img_extent[2]-.4, img_extent[3]+.4]
        ax.set_extent(extent)
        ax.gridlines()
        ax.coastlines(resolution='50m')
        ax.add_feature(cartopy.feature.OCEAN, alpha=.2)
        ax.set_xticks(np.linspace(extent[0], extent[1], 5))
        ax.set_yticks(np.linspace(extent[2], extent[3], 5))

        plt.scatter(dfi['st_x'], dfi['st_y'], c=cmap, marker='o', edgecolor=None)
        plt.xlabel('longitude (degrees)', fontsize=16)
        plt.ylabel('latitude (degrees)', fontsize=16)

        plt.title("Time: {}".format(time[i]), fontsize=18)
        
        plt.savefig('./images/img_'+ "{num:03d}".format(num=i)+'.png')
        ax.cla()
    plt.close()
    os.system('convert -delay 20 -loop 0 ./images/*.png static/animated.gif')

#### Backend
@app.route('/test')
def test():
    date1 = request.args.get('date1')
    date2 = request.args.get('date2')
    plot(date1, date2)
    return send_file("static/animated.gif", mimetype="image/gif")

#### Frontend
@app.route('/')
def root():
    return app.send_static_file('index.html')

if __name__ == '__main__':

    #app.run(port=5000)
    app.run(host="0.0.0.0", port=5000)
