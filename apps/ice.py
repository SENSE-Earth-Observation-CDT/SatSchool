from pdb import line_prefix
import streamlit as st
import geemap.foliumap as geemap
#from streamlit_metrics import metric, metric_row
from streamlit_ace import st_ace
import pandas as pd
import ee
import extra_streamlit_components as stx
import re

def app():
    if 'well_done' not in st.session_state:
        st.session_state.well_done = False

    st.markdown(
    "<h1 style='text-align: center; color: #565656; background: #99FFFF'> Ice 🧊</h1>",
    unsafe_allow_html=True)

    chosen_id = stx.tab_bar(data=[
        stx.TabBarItemData(id=1, title="Code exercise 1", description="Sentinel 1 difference"),
        stx.TabBarItemData(id=2, title="Code exercise 2", description="Ice mass balance"),
        stx.TabBarItemData(id=3, title="Code exercise 3", description="Another one"),
    ], default=1)
    #st.info(f"{chosen_id=}")

    display, editor = st.columns((1, 1))

    INITIAL_CODE = """print('if you print something it goes onto the page!')
print('Subtract the bedrock topography of Antartica from the elevation of the South Pole')

###############
bedrock = ee.Image('NOAA/NGDC/ETOPO1').select('bedrock')
Map.addLayer(bedrock, {'min':-10898, 'max':1000}, 'bedrock')

###############
lima_mosaic = ee.Image('USGS/LIMA/MOSAIC')
antarctica = lima_mosaic.select(['B3', 'B2', 'B1'])
antarcticaVis = {
  'min': 0.0,
  'max': 10000.0,
}
Map.addLayer(lima_mosaic, antarcticaVis, 'Antartica Imagery (RGB)')

###############
cryosat_dem = ee.Image('CPOM/CryoSat2/ANTARCTICA_DEM').select('elevation')

visualisation = {
'min': 0.0,
'max': 10000.0,
'palette': ['001fff', '00ffff', 'fbff00', 'ff0000']
}

Map.addLayer(cryosat_dem, visualisation, 'Cryosat DEM')

############### PUT SOMETHING BELOW HERE TO SHOW THE SUBTRACTED IMAGE
Map.addLayer(cryosat_dem.subtract(bedrock), {'min': -4000,'max': 4000,'palette': ['001fff', '00ffff', 'fbff00', 'ff0000']}, 'ice-bedrock difference')

Map.setCenter(0, 0, 4)
"""

    with editor:
        corr = 3
        ans = st.text_input('How far (in km) has the ice moved in the radar images from 2016 to 2022?', help='something helpful goes here', max_chars=4)
        if ans.replace('.','',1).isdigit():
            ans = float(ans)
            if ans < corr+corr*0.1 and ans > corr-corr*0.1:
                st.success('Well done!')
                if st.session_state.well_done is False:
                    st.balloons()
                st.session_state.well_done = True
            else:
                st.error('Incorrect. Try again.')
                st.session_state.well_done = False

        st.write('### Code editor')

        st.caption('The code in the box below is given for you. It gives the images that you will be using as code variables.')
        st.code('''#These are the radar images that you will be using. 
#They are from the Sentinel-1 satellite and can see through clouds.
s1_2016 = ee.Image('COPERNICUS/S1_GRD/S1A_EW_GRDM_1SSH_20160602T051612_20160602T051716_011527_011973_749B').select('HH')
s1_2022 = ee.Image('COPERNICUS/S1_GRD/S1B_IW_GRDH_1SSH_20210321T095950_20210321T100015_026111_031D9E_1D62').select('HH')

#You can add the images to the map like this:
#Make sure you set a minimum and maximum value for the image.
Map.addLayer(s1_2016, {'min':-25, 'max':0}, '2016')
Map.addLayer(s1_2022, {'min':-25, 'max':0}, '2022')

#You can subtract the images like this:
difference = s1_2022.subtract(s1_2016)

#You can add the difference to the map like this:
Map.addLayer(difference, {'min':-5, 'max':5, 'palette': ['001fff', '00ffff', 'fbff00', 'ff0000']}, 'diff')
''')

        st.caption('The code in the box below is run in the browser. You can edit it and see the results on the left.')
        code = st_ace(
                value= INITIAL_CODE,
                language="python",
                theme="github",
                keybinding="vim",
                font_size=18,
                tab_size=4,
                show_gutter=True,
                key="ace",
            )
            
        st.write('Hit `CTRL+ENTER` to refresh')
        st.write('*Remember to save your code separately!*')

    with display:
        Map = geemap.Map(locate_control=True, draw_export=False, plugin_Draw=True, add_google_map = False, tiles=None)
        #Map.add_basemap("HYBRID")

        code = code.replace('print(','st.write(')

        executable_code = []
        proj_change = ".changeProj('EPSG:3031', 'EPSG:3857')"
        for line in code.split('\n'):
            if 'Map.addLayer(' in line:
                if proj_change not in line:
                    line_suffix = ''.join(line.split('Map.addLayer(')[1:])
                    COMMA_MATCHER = re.compile(r",(?=(?:[^\"']*[\"'][^\"']*[\"'])*[^\"']*$)")
                    args = COMMA_MATCHER.split(line_suffix)
                    #st.write(args)
                    first_arg = args[0] + proj_change + ','
                    new_line = 'Map.addLayer(' + first_arg + ','.join(args[1:])
                    #st.write('line', line)
                    #st.write(new_line)
                    executable_code.append(new_line)
            else:
                executable_code.append(line)
        executable_code = '\n'.join(executable_code)
        #st.code(executable_code)
        exec(executable_code)

        Map.to_streamlit(height=600)
