from cv2 import merge
import geemap.foliumap as geemap
import ee
import eemont
import streamlit.components.v1 as components
import datetime
import pandas as pd
import streamlit as st
import requests

from streamlit_lottie import st_lottie_spinner

@st.cache()
def load_lottieurl(url: str):
  import requests
  r = requests.get(url)
  if r.status_code != 200:
      return None
  return r.json()

lottie_url_download = "https://assets8.lottiefiles.com/packages/lf20_nay3rc6w.json"
lottie_download = load_lottieurl(lottie_url_download)

# INSTRUCTION
st.info("You are mapping deforestation in Brazil in 2018. This is **really cool** and there should be some information\
          here about it.")
st.write("Rainforests have decreased in size primarily due to deforestation. Despite reductions in the deforestation rate\
   over the last ten years, the Amazon rainforest will be reduced by 40% by 2030 at the current rate. Between May 2000\
      and August 2006, Brazil lost nearly 150,000 square kilometres (58,000 sq mi) of forest, an area larger than Greece.\
         According to the Living Planet Report 2010, deforestation continues at an alarming rate.\
           At the Convention on Biological Diversity's 9th Conference, 67 ministers signed up to help achieve zero net\
              deforestation by 2020. Due to deforestation the Amazon was a net emitter of greenhouse gas in the 2010s.")

cola, colb = st.columns((0.5, 1))
with cola:
  st.write('')
  with st.form("Add training points"):
    lon = st.text_input("Longitude")
    lat = st.text_input("Latitude")
    label_class = st.radio("What is your label?", ['forest', 'not forest'])
    submitted = st.form_submit_button(label="Add point", help=None, on_click=None, args=None, kwargs=None) 

    if submitted:
      if lon.replace('.','',1).replace('-','',1).isdigit():
        lon = float(lon)
        if lat.replace('.','',1).replace('-','',1).isdigit():
          lat = float(lat)

          if lon > -180 and lon < 180 and lat > -90 and lat < 90:
            st.info(f"added lon: {lon:.2f}, lat: {lat:.2f}, class: {label_class}")

            if 'points' not in st.session_state:
              st.session_state.points = []
            st.session_state.points.append({'lon': lon, 'lat': lat, 'class': label_class})

          else:
            st.error("Invalid coordinates")
        else:
          st.error('Invalid latitude given.')
      else:
        st.error('Invalid longitude given.')

  reset_points = st.button('Reset points')
  df_cont = st.container()

  protected_area_check = st.checkbox('Show protected areas on the map')
  measurement_reg_check = st.checkbox('Show region we are measuring deforestation in on the map')

  if reset_points:
    st.session_state.points = []
  classifier_button = st.button('🪄 Run classifier! 🪄')

with colb:
  Map = geemap.Map(zoom=1)

  # Define a region of interest as a point.  Change the coordinates
  # to get a classification of any place where there is imagery.
  roi = ee.Geometry.Point(-122.3942, 37.7295)

  l8 = ee.ImageCollection('LANDSAT/LC08/C01/T1')
  image = ee.Algorithms.Landsat.simpleComposite(**{
    'collection': l8.filterDate('2018-01-01', '2018-12-31'),
    'asFloat': True,
  })

  bands = ['B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B10', 'B11']

  forest_coords = [(-63.0187, -9.3958), (-62.7688, -9.1735)]
  notforest_coords = [(-62.7921, -9.4486), (-62.6788, -9.044)]

  if 'points' in st.session_state:
    for c in st.session_state.points[:15]:
      if c['class'] == 'forest':
        forest_coords.append((c['lon'], c['lat']))
      else:
        notforest_coords.append((c['lon'], c['lat']))

  # Make a FeatureCollection from the hand-made geometries
  notforest_points_lst = []
  for c in notforest_coords:
    notforest_points_lst.append(ee.Geometry.Point(c))
  notforest_points = ee.FeatureCollection(notforest_points_lst)

  forest_points_lst = []
  for c in forest_coords:
    forest_points_lst.append(ee.Geometry.Point(c))
    forest_points = ee.FeatureCollection(forest_points_lst)
  
  # all_points = ee.FeatureCollection([
  #     ee.Feature(notforest_points_lst[0], {'class': 0}),
  #     ee.Feature(notforest_points_lst[1], {'class': 0}),
  #     ee.Feature(forest_points_lst[0], {'class': 1}),
  #     ee.Feature(forest_points_lst[1], {'class': 1}),
  # ])

  all_points_df = []
  for c in notforest_coords:
    all_points_df.append({'lon': c[0], 'lat': c[1], 'class': 'not forest'})
  for c in forest_coords:
    all_points_df.append({'lon': c[0], 'lat': c[1], 'class': 'forest'})
  # if 'points' in st.session_state:
  #   all_points_df += st.session_state.points

  all_points = []
  for row in all_points_df:
    point = ee.Geometry.Point((row['lon'], row['lat']))
    all_points.append( ee.Feature(point, {'class': 0 if row['class'] == 'not forest' else 1}) )
  all_points = ee.FeatureCollection(all_points)

  df = pd.DataFrame(all_points_df)
  if len(df) > 15:
    df_cont.error('Too many points! Reset points to add new points.')

  df[['lon','lat']] = df[['lon','lat']].round(2)
  with df_cont:
    # CSS to inject contained in a string
    hide_table_row_index = """
                <style>
                tbody th {display:none}
                .blank {display:none}
                </style>
                """

    # Inject CSS with Markdown
    st.markdown(hide_table_row_index, unsafe_allow_html=True)

    st.table(df)

  # Display the classification result and the input image.
  Map.setCenter(-62.836, -9.2399, 9)
  Map.addLayer(image, {'bands': ['B4', 'B3', 'B2'], 'max': 0.5, 'gamma': 2}, 'Cloudless Landsat-8 imagery 2018')

  Map.addLayer(forest_points, {'color':'#90EE90'}, 'training forest points')
  Map.addLayer(notforest_points, {'color':'red'}, 'training not-forest points')

  if protected_area_check:
    dataset = ee.FeatureCollection('WCMC/WDPA/current/polygons')
    Map.addLayer(dataset, {'color': 'green'}, 'WDPA Protected Areas', True, 0.85)

  gaul = ee.FeatureCollection("FAO/GAUL/2015/level2");
  jamari = gaul.filter(ee.Filter.eq("ADM2_NAME", 'Jamari'))
  cujubim = gaul.filter(ee.Filter.eq("ADM2_NAME", 'Cujubim'))
  candeias_do_jamari = gaul.filter(ee.Filter.eq("ADM2_NAME", 'Candeias Do Jamari'))
  alto_paraiso = gaul.filter(ee.Filter.eq("ADM2_NAME", 'Alto Paraiso'))
  rio_crespo = gaul.filter(ee.Filter.eq("ADM2_NAME", 'Rio Crespo'))
  ariquemes = gaul.filter(ee.Filter.eq("ADM2_NAME", 'Ariquemes'))

  styleParams = {
    'fillColor': 'b5ffb4',
    'color': '00909F',
    'width': 1.0
  };
  merged_area = jamari.merge(cujubim).merge(candeias_do_jamari).merge(alto_paraiso).merge(rio_crespo).merge(ariquemes)

  if measurement_reg_check:
    Map.addLayer(merged_area.style(**styleParams), {'opacity': 0.5}, 'measurement region')

  if classifier_button:
    #with st.spinner('Doing some classification magic...'):
    with st_lottie_spinner(lottie_download, key="classification magic", width=200):
      # Get the values for all pixels in each polygon in the training.

      training = image.sampleRegions(**{
        # Get the sample from the polygons FeatureCollection.
        'collection': all_points,
        # Keep this list of properties from the polygons.
        'properties': ['class'],
        # Set the scale to get Landsat pixels in the polygons.
        'scale': 30
      })

      # Create an SVM classifier with custom parameters.
      classifier = ee.Classifier.libsvm(**{
        'kernelType': 'RBF',
        'gamma': 0.5,
        'cost': 10
      })

      # Train the classifier.
      trained = classifier.train(training, 'class', bands)

      # Classify the image.
      classified = image.classify(trained)

      areaImage = classified.multiply(ee.Image.pixelArea());
      # Calculate the area of loss pixels in the merged area.
      stats = areaImage.reduceRegion(**{
        'reducer': ee.Reducer.sum(),
        'geometry': merged_area.geometry(),
        'scale': 30,
        'maxPixels': 1e9
      })

      
      Map.addLayer(classified,
                  {'min': 0, 'max': 1, 'palette': ['red', 'green']},
                  'deforestation')

  Map.addLayerControl()
  Map.to_streamlit()

with colb:
  # rel_counts = pd.DataFrame(data=df_data, columns=["atlantic"])
  # st.table(rel_counts.style.format("{:.2f}"))
  labels_ = ['forest', 'not forest']
  import numpy as np
  import altair as alt

  if classifier_button:
    st.write(f"You used {len(df)} points to classify deforestation, with {len(df[df['class'] == 'not forest'])} points\
           being labelled as forest and {len(df[df['class'] == 'forest'])} points being labelled as not forest.\
           Can you see where the classification has done well, and where it hasn't done well? Why do you think this?")
    # Get a confusion matrix representing train accuracy.
    trainAccuracy = trained.confusionMatrix()

    # # Get a confusion matrix representing expected accuracy.
    # testAccuracy = validated.errorMatrix('Land_Cover_Type_1', 'classification')
    # st.write('Validation error matrix: ', testAccuracy.getInfo())
    # st.write('Validation overall accuracy: ', testAccuracy.accuracy().getInfo())

    # with st.expander('test'):
    #   st.write('Resubstitution error matrix: ', trainAccuracy.getInfo())
    train_acc_result = trainAccuracy.accuracy().getInfo()*100
    st.write(f'The overall (training) accuracy is {train_acc_result:.0f}%. This means that the points you used for the\
      classifier are {train_acc_result:.0f}% accurate when compared to the map produced by the classifier.')

    with st.expander('Read more about your accuracy results:'):
      cm = np.array(trainAccuracy.getInfo()) #confusion_matrix(y_true, y_pred)
      cm = (cm.astype('float') / cm.sum(axis=1)[:, np.newaxis])
      labels_repeated = []
      for _ in range(np.unique(labels_).shape[0]):
          labels_repeated.append(np.unique(labels_))
      source = pd.DataFrame({'predicted class': np.transpose(np.array(labels_repeated)).ravel(),
                          'true class': np.array(labels_repeated).ravel(),
                          'fraction': np.round(cm.ravel(), 2)})
      #st.dataframe(source)
      heat = alt.Chart(source, height=500, width=500, title="confusion matrix").mark_rect(opacity=0.7).encode(
          x='predicted class:N',
          y='true class:N',
          color=alt.Color('fraction:Q', scale=alt.Scale(scheme='blues')),
          tooltip="fraction")

      st.info('This is a confusion matrix. It shows the number of times a prediction was made for a given class,\
              and the number of times the prediction was correct. The diagonal shows the number of times the prediction\
                was correct for that class. The off-diagonal shows the number of times the prediction was correct for a\
                  different class. The higher the number in the diagonal, the better the prediction. The lower the number\
                    in the off-diagonal, the better the prediction.')

      st.altair_chart(heat)

    st.subheader('According to your deforestation classifier:')
    total_area = 24225
    forest_area = stats.getInfo()['classification']*1e-6
    st.metric(label="Amount of area marked as forested in measurement region", value=f'{forest_area:.0f} square kilometres ({forest_area/total_area*100:.0f}%)')
    st.metric(label="Total area of the measurement region", value=f'{total_area:.0f} square kilometres')
    #stateArea = merged_area.geometry().area()
    #stateAreaSqKm = ee.Number(stateArea).divide(1e6).round()
    #st.write(stateAreaSqKm.getInfo())

  area_ans = st.number_input('How much area in the measured region is not forest? (in sqkm)', step=100, help='Nearest 100 sqkm')
  if area_ans == 8200: #total_area - forest_area
    st.success('You are correct!')
    st.balloons()