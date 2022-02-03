from tkinter import N
import geemap.foliumap as geemap
import ee
import eemont
import streamlit.components.v1 as components
import datetime
import pandas as pd
import streamlit as st

st.title("Sea Surface Temperature")
df = pd.read_csv('ocean_sst_all.csv')

cola, colb = st.columns([0.25,1])

with cola:
    #radio_choice = st.radio(
    #    "View",
    #    ('Sea Surface Temperature', 'Chlorophyll-a concentration'),
    #)

    start_date=datetime.datetime(2002, 7, 4)
    end_date=datetime.datetime(2021, 5, 28)

    ## Range selector
    format = 'MMM YYYY'  # format output

    slider = st.slider('Select date', min_value=start_date, max_value=end_date, format=format)

    min_val, max_val = st.select_slider(
        'Select a temperature range to display',
        options=range(-20,51,1),
        value=(-5, 40))
    st.write('You selected sea surface temperatures between', str(min_val), 'and', str(max_val), '°C on', slider.strftime("%B %Y."))
    #date = st.date_input('Select date', min_value=start_date, max_value=end_date, value=start_date)
    #color1 = st.color_picker('Min colour', value='#0000ff'
    #color2 = st.color_picker('Max colour', value='#ff0000')
    chla_check_cont = st.container()

with colb:
    m = geemap.Map(locate_control=True,zoom=1)
    m.add_basemap("HYBRID")

    #NOAA/CDR/SST_WHOI/V2
    dataset = ee.ImageCollection('NASA/OCEANDATA/MODIS-Aqua/L3SMI') \
                .filterDate(slider.strftime('%Y-%m-%d'), (slider+datetime.timedelta(days=31)).strftime('%Y-%m-%d'))
    sst = dataset.select(['sst']).median()
    chla = dataset.select(['chlor_a']).median()
    #st.write(sst.getInfo())
    palette = ['#0000ff', '#00ffff', '#ffff00', '#ff0000']
    remoteSensingReflectanceVis = {'min': min_val, 'max': max_val, 'palette': palette}

    m.addLayer(
        sst, remoteSensingReflectanceVis,
        'Sea Surface Temperature')

    with st.spinner('Loading...'):
        atlantic_region = ee.Geometry.Point([-41.1328, 24.8466])
        indian_region = ee.Geometry.Point([71.0156, -2.4602])
        pacific_region = ee.Geometry.Point([-140.6250, 7.7110])
        arctic_region = ee.Geometry.Point([8.4375, 72.7119])

        atlantic_region = atlantic_region.buffer(100000).bounds()
        indian_region = indian_region.buffer(100000).bounds()
        pacific_region = pacific_region.buffer(100000).bounds()
        arctic_region = arctic_region.buffer(100000).bounds()

        # atlantic_ts = ee.ImageCollection('NASA/OCEANDATA/MODIS-Aqua/L3SMI').filterDate(datetime.datetime(2020,1,1), datetime.datetime(2022,1,25))\
        #     .getTimeSeriesByRegion(
        #     geometry = atlantic_region,
        #     bands = ['sst'],
        #     reducer = [ee.Reducer.median(), ee.Reducer.stdDev()],
        #     scale=100
        # )
        # indian_ts = ee.ImageCollection('NASA/OCEANDATA/MODIS-Aqua/L3SMI').filterDate(datetime.datetime(2020,1,1), datetime.datetime(2022,1,25))\
        #     .getTimeSeriesByRegion(
        #     geometry = indian_region,
        #     bands = ['sst'],
        #     reducer = [ee.Reducer.median(), ee.Reducer.stdDev()],
        #     scale=100
        # )
        # pacific_ts = ee.ImageCollection('NASA/OCEANDATA/MODIS-Aqua/L3SMI').filterDate(datetime.datetime(2020,1,1), datetime.datetime(2022,1,25))\
        #     .getTimeSeriesByRegion(
        #     geometry = pacific_region,
        #     bands = ['sst'],
        #     reducer = [ee.Reducer.median(), ee.Reducer.stdDev()],
        #     scale=100
        # )
        # arctic_ts = ee.ImageCollection('NASA/OCEANDATA/MODIS-Aqua/L3SMI').filterDate(datetime.datetime(2020,1,1), datetime.datetime(2022,1,25))\
        #     .getTimeSeriesByRegion(
        #     geometry = arctic_region,
        #     bands = ['sst'],
        #     reducer = [ee.Reducer.median(), ee.Reducer.stdDev()],
        #     scale=100
        # )

        # atlantic_df = geemap.ee_to_pandas(atlantic_ts)
        # indian_df = geemap.ee_to_pandas(indian_ts)
        # pacific_df = geemap.ee_to_pandas(pacific_ts)
        # arctic_df = geemap.ee_to_pandas(arctic_ts)

        # atlantic_df['Atlantic'] = atlantic_df['sst']
        # atlantic_df = atlantic_df.loc[atlantic_df['reducer'] == 'median']
        # atlantic_df = atlantic_df.drop(columns=['sst', 'reducer'])
        # indian_df['Indian'] = indian_df['sst']
        # indian_df = indian_df.loc[indian_df['reducer'] == 'median']
        # indian_df = indian_df.drop(columns=['sst', 'reducer'])
        # pacific_df['Pacific'] = pacific_df['sst']
        # pacific_df = pacific_df.loc[pacific_df['reducer'] == 'median']
        # pacific_df = pacific_df.drop(columns=['sst', 'reducer'])
        # arctic_df['Arctic'] = arctic_df['sst']
        # arctic_df = arctic_df.loc[arctic_df['reducer'] == 'median']
        # arctic_df = arctic_df.drop(columns=['sst', 'reducer'])
        # df = pd.merge(atlantic_df, indian_df, on='date')
        # df = pd.merge(df, pacific_df, on='date')
        # df = pd.merge(df, arctic_df, on='date')

    #labels = [str(min_val), f"{min_val + 0.25*(max_val-min_val):.2f}", f"{(min_val + 0.75*(max_val-min_val)):.2f}", str(max_val)]
    #color can be defined using either hex code or RGB (0-255, 0-255, 0-255)
    # colors = [(255, 0, 0), (127, 255, 0), (127, 18, 25), (36, 70, 180), (96, 68, 123)]
    m.add_colorbar(colors=palette, vmin=min_val, vmax=max_val, caption='Sea Surface Temperature (°C)')

    if chla_check_cont.checkbox(label='View Chlorophyll-a concentration'):
        m.addLayer(
            chla, {'min': 0, 'max': 1, 'palette': ['F2F2F2','00A600'],},
            'Chlorophyll-a', True)
        m.add_colorbar(colors=['F2F2F2','00A600'], vmin=0, vmax=1, caption='Chlorophyll-a concentration (milligrammes per cubic metre)')
    #m.add_legend(title='Legend', labels=labels, colors=colors)

    m.addLayer(atlantic_region,{},'North Atlantic')
    m.addLayer(indian_region,{},'Indian')
    m.addLayer(pacific_region,{},'Pacific')
    m.addLayer(arctic_region,{},'Arctic')

    m.addLayerControl()

    m.to_streamlit(height=700)

#st.dataframe(df)
df_data = df[['Atlantic', 'Indian', 'Pacific', 'Arctic', 'date']]
df_data['date'] = pd.to_datetime(df_data['date'])
df_data['date'] = df_data['date'].apply(lambda t: t.floor('d'))
#df_data = df_data.loc[df_data['Indian'] > 5]
#df_data = df_data.loc[df_data['Atlantic'] > 5]
#df_data = df_data.loc[df_data['Pacific'] > 5]
#df_data = df_data.loc[df_data['Arctic'] > 5]

import altair as alt
import numpy as np

df_data_pacific = df_data[['date', 'Pacific']]
#df_data_pacific['Pacific'] = df_data_pacific['Pacific'].rolling(window=30).mean()
st.dataframe(df_data_pacific)
c = alt.Chart(df_data_pacific).mark_line().encode(
    x=alt.X('date', axis=alt.Axis(tickCount=30, labelOverlap="greedy",grid=False, labelExpr="datum.value % 100 ? null : datum.label")), y='Pacific', tooltip=['date', 'Pacific'])

st.altair_chart(c, use_container_width=True)