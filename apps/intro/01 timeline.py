import streamlit as st
import streamlit.components.v1 as components

# parameters
CDN_LOCAL = False
CDN_PATH = 'https://cdn.knightlab.com/libs/timeline3/latest'
CSS_PATH = 'timeline3/css/timeline.css'
JS_PATH = 'timeline3/js/timeline.js'

SOURCE_TYPE = 'gdocs' # json or gdocs
GDOCS_PATH = 'https://docs.google.com/spreadsheets/u/1/d/1xuY4upIooEeszZ_lCmeNx24eSFWe0rHe9ZdqH2xqVNk/pubhtml' # example url
JSON_PATH = 'timeline_nlp.json' # example json

TL_HEIGHT = 800 # px


# load data
json_text = ''
if SOURCE_TYPE == 'json':
    with open(JSON_PATH, "r") as f:
        json_text = f.read()
        source_param = 'timeline_json'
        source_block = f'var {source_param} = {json_text};'
elif SOURCE_TYPE == 'gdocs':
    source_param = f'"{GDOCS_PATH}"'
    source_block = ''


# load css + js
if CDN_LOCAL:
    with open(CSS_PATH, "r") as f:
        css_text = f.read()
        css_block = f'<head><style>{css_text}</style></head>'

    with open(JS_PATH, "r") as f:
        js_text = f.read()
        js_block  = f'<script type="text/javascript">{js_text}</script>'
else:
    css_block = f'<link title="timeline-styles" rel="stylesheet" href="{CDN_PATH}/css/timeline.css">'
    js_block  = f'<script src="{CDN_PATH}/js/timeline.js"></script>'


# write html block
htmlcode = css_block + ''' 
''' + js_block + '''
    <div id='timeline-embed' style="width: 95%; height: '''+str(TL_HEIGHT)+'''px; margin: 1px;"></div>
    <script type="text/javascript">
        var additionalOptions = {
            start_at_end: false, is_embed:true,
        }
        '''+source_block+'''
        timeline = new TL.Timeline('timeline-embed', '''+source_param+''', additionalOptions);
    </script>'''

components.html(htmlcode, height=TL_HEIGHT,)

components.iframe('https://demos.mapbox.com/scrollytelling/', height=800, scrolling=True)

components.iframe('https://storymaps.arcgis.com/stories/4faf6d052c8f41b3b9b99c506642bca5', height=800, scrolling=True)