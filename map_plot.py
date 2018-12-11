import sqlite3 as sqlite
import plotly.plotly as py
from plotly.graph_objs import *
from secret import PLOTLY_USERNAME, PLOTLY_API_KEY, MAPBOX_TOKEN
import plotly.graph_objs as go

def plot_data():
    conn = sqlite.connect('linkedin.sqlite')
    cur = conn.cursor()
    statement = '''
            SELECT People.Company, People.Location, Place.Lat, Place.Lng From People Join  Place where People.Location = Place.Place
         '''
    places = cur.execute(statement).fetchall()
    dic_company_locations = {}
    for place in places:
        company = place[0]
        lat = place[2]
        lng = place[3]
        if company in dic_company_locations:
            dic_company_locations[company]['lat'].append(lat)
            dic_company_locations[company]['lng'].append(lng)
        else:
            cur_dic ={'lat':[],
                      'lng':[]
                      }
            cur_dic['lat'].append(lat)
            cur_dic['lng'].append(lng)
            dic_company_locations[company]=cur_dic
    conn.commit()
    conn.close()
    return dic_company_locations

def plot():
    dic_company_locations = plot_data()
    data = []
    for company in dic_company_locations:
        cur_data = dic_company_locations[company]
        lat=cur_data['lat']
        lng=cur_data['lng']
        trace_cur = dict(
            type='scattergeo',
            locationmode='USA-states',
            lon=lng,
            lat=lat,
            text=company,
            name=company,
            mode='markers',
            marker=dict(
                size=15,
            ))
        print
        data.append(trace_cur)

    title = 'The Distribution of Working Places'
    layout = dict(
        title=title,
        geo=dict(
            scope='usa',
            projection=dict(type='albers usa'),
            showland=True,
            landcolor="rgb(250, 250, 250)",
            subunitcolor="rgb(100, 217, 217)",
            countrycolor="rgb(217, 100, 217)",
            # lataxis={'range': lat_axis},
            # lonaxis={'range': lon_axis},
            # center={'lat': center_lat, 'lon': center_lon},
            countrywidth=3,
            subunitwidth=3
        ),
    )
    fig = dict(data=data, layout=layout)
    py.plot(fig, validate=False, filename='test')

def plot_Histogram(num):
    conn = sqlite.connect('linkedin.sqlite')
    cur = conn.cursor()
    statement = '''
        select * from Skill order by Frequency Desc limit ?
    '''
    skills = cur.execute(statement, (num,)).fetchall()
    conn.close()
    x = []
    y = []
    for i in skills:
        x.append(i[1])
        y.append(str(i[2]))
    data = [
      go.Bar(
        y = y,
        x = x,
      )
    ]
    layout = go.Layout(
        title= "The top {} Skills".format(num),
        xaxis=dict(
            title='Skill Axis',
        ),
        yaxis=dict(
            title='Frequency',
        )
    )
    py.plot(data,filename='Top Skills', layout=layout)

def Main():
    plot()
