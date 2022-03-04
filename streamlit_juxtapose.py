import streamlit.components.v1 as components

def juxtapose(img1: str, img2: str, label1: str, label2: str, height: int = 1000):  # data

    """Create a new timeline component.
    Parameters
    ----------
    height: int or None
        Height of the timeline in px
    Returns
    -------
    static_component: Boolean
        Returns a static component with a timeline
    """

    # load css + js
    cdn_path = "https://cdn.knightlab.com/libs/juxtapose/latest"
    css_block = f'<link rel="stylesheet" href="{cdn_path}/css/juxtapose.css">'
    js_block = f'<script src="{cdn_path}/js/juxtapose.min.js"></script>'

    # write html block
    htmlcode = (
        css_block
        + """ 
    """
        + js_block
        + """
        <div id="foo" style="width: 95%; height: """
        + str(height)
        + '''px; margin: 1px;"></div>
        <script>
        slider = new juxtapose.JXSlider('#foo',
            [
                {
                    src: "'''
        + img1
        + '''",
                    label: '{label1}',
                },
                {
                    src: "'''
        + img2
        + """",
                    label: '{label2}',
                }
            ],
            {
                animate: true,
                showLabels: true,
                showCredits: true,
                startingPosition: "50%",
                makeResponsive: true
            });
        </script>
    """
    )
    htmlcode = htmlcode.replace('{label1}', label1)
    htmlcode = htmlcode.replace('{label2}', label2)
    static_component = components.html(
        htmlcode,
        height=height,
    )
    return static_component
