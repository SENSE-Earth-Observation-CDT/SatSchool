import streamlit as st
import apps.streamlit_book as stb
import geemap#.foliumap as geemap
import ee

m = geemap.Map(locate_control=False)
m.add_basemap("HYBRID")

def app():
    st.markdown(
    "<h1 style='text-align: center; color: #565656; background: #90ee90'> Land 🌲</h1>",
    unsafe_allow_html=True)

    stb.set_book_config(path="apps/land",toc=False, button='top', book_id='land')

    # import extra_streamlit_components as stx
    # val = stx.stepper_bar(steps=["Ready", "Get Set", "Almost", "Are we there yet?", "Go"])
    # st.info(f"Phase #{val}")


    # collection = ee.ImageCollection('MODIS/006/MOD13A2') \
    # .filterDate('2015-01-01', '2019-12-31') \
    # .select('NDVI')

    # # Convert the image collection to an image.
    # image = collection.toBands()

    # ndvi_vis = {
    # 'min': 0.0,
    # 'max': 9000.0,
    # 'palette': [
    #     'FFFFFF', 'CE7E45', 'DF923D', 'F1B555', 'FCD163', '99B718', '74A901',
    #     '66A000', '529400', '3E8601', '207401', '056201', '004C00', '023B01',
    #     '012E01', '011D01', '011301'
    # ]
    # }

    # m1 = geemap.Map()
    # m1.addLayer(image.select(0), ndvi_vis, 'MODIS NDVI VIS')
    # m1.add_layer_control()
    # m1.to_streamlit(height=700)
