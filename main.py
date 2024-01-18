import streamlit as st

if "showChart" not in st.session_state:
    st.session_state.showChart = False

if "readVealues" not in st.session_state:
    st.session_state.readVealues = False    

def intro():
    import streamlit as st

    st.write("# Welcome to Streamlit! 👋")
    st.sidebar.success("Select a demo above.")

    st.markdown(
        """
        Streamlit is an open-source app framework built specifically for
        Machine Learning and Data Science projects.

        **👈 Select a demo from the dropdown on the left** to see some examples
        of what Streamlit can do!

        ### Want to learn more?

        - Check out [streamlit.io](https://streamlit.io)
        - Jump into our [documentation](https://docs.streamlit.io)
        - Ask a question in our [community
          forums](https://discuss.streamlit.io)

        ### See more complex demos

        - Use a neural net to [analyze the Udacity Self-driving Car Image
          Dataset](https://github.com/streamlit/demo-self-driving)
        - Explore a [New York City rideshare dataset](https://github.com/streamlit/demo-uber-nyc-pickups)
    """
    )

def mapping_demo():
    import streamlit as st
    import pandas as pd
    import pydeck as pdk

    from urllib.error import URLError

    st.markdown(f"# {list(page_names_to_funcs.keys())[2]}")
    st.write(
        """
        This demo shows how to use
[`st.pydeck_chart`](https://docs.streamlit.io/library/api-reference/charts/st.pydeck_chart)
to display geospatial data.
"""
    )

    @st.cache_data
    def from_data_file(filename):
        url = (
            "http://raw.githubusercontent.com/streamlit/"
            "example-data/master/hello/v1/%s" % filename
        )
        return pd.read_json(url)

    try:
        ALL_LAYERS = {
            "Bike Rentals": pdk.Layer(
                "HexagonLayer",
                data=from_data_file("bike_rental_stats.json"),
                get_position=["lon", "lat"],
                radius=200,
                elevation_scale=4,
                elevation_range=[0, 1000],
                extruded=True,
            ),
            "Bart Stop Exits": pdk.Layer(
                "ScatterplotLayer",
                data=from_data_file("bart_stop_stats.json"),
                get_position=["lon", "lat"],
                get_color=[200, 30, 0, 160],
                get_radius="[exits]",
                radius_scale=0.05,
            ),
            "Bart Stop Names": pdk.Layer(
                "TextLayer",
                data=from_data_file("bart_stop_stats.json"),
                get_position=["lon", "lat"],
                get_text="name",
                get_color=[0, 0, 0, 200],
                get_size=15,
                get_alignment_baseline="'bottom'",
            ),
            "Outbound Flow": pdk.Layer(
                "ArcLayer",
                data=from_data_file("bart_path_stats.json"),
                get_source_position=["lon", "lat"],
                get_target_position=["lon2", "lat2"],
                get_source_color=[200, 30, 0, 160],
                get_target_color=[200, 30, 0, 160],
                auto_highlight=True,
                width_scale=0.0001,
                get_width="outbound",
                width_min_pixels=3,
                width_max_pixels=30,
            ),
        }
        st.sidebar.markdown("### Map Layers")
        selected_layers = [
            layer
            for layer_name, layer in ALL_LAYERS.items()
            if st.sidebar.checkbox(layer_name, True)
        ]
        if selected_layers:
            st.pydeck_chart(
                pdk.Deck(
                    map_style="mapbox://styles/mapbox/light-v9",
                    initial_view_state={
                        "latitude": 37.76,
                        "longitude": -122.4,
                        "zoom": 11,
                        "pitch": 50,
                    },
                    layers=selected_layers,
                )
            )
        else:
            st.error("Please choose at least one layer above.")
    except URLError as e:
        st.error(
            """
            **This demo requires internet access.**

            Connection error: %s
        """
            % e.reason
        )

def plotting_demo():
    import streamlit as st
    import time
    import numpy as np

    st.markdown(f'# {list(page_names_to_funcs.keys())[1]}')
    st.write(
        """
        This demo illustrates a combination of plotting and animation with
Streamlit. We're generating a bunch of random numbers in a loop for around
5 seconds. Enjoy!
"""
    )

    progress_bar = st.sidebar.progress(0)
    status_text = st.sidebar.empty()
    last_rows = np.random.randn(1, 1)
    chart = st.line_chart(last_rows)

    for i in range(1, 101):
        new_rows = last_rows[-1, :] + np.random.randn(5, 1).cumsum(axis=0)
        status_text.text("%i%% Complete" % i)
        chart.add_rows(new_rows)
        progress_bar.progress(i)
        last_rows = new_rows
        time.sleep(0.05)

    progress_bar.empty()

    # Streamlit widgets automatically run the script from top to bottom. Since
    # this button is not connected to any other logic, it just causes a plain
    # rerun.
    st.button("Re-run")


def data_frame_demo():
    import streamlit as st
    import pandas as pd
    import altair as alt

    from urllib.error import URLError

    st.markdown(f"# {list(page_names_to_funcs.keys())[3]}")
    st.write(
        """
        This demo shows how to use `st.write` to visualize Pandas DataFrames.

(Data courtesy of the [UN Data Explorer](http://data.un.org/Explorer.aspx).)
"""
    )

    @st.cache_data
    def get_UN_data():
        AWS_BUCKET_URL = "http://streamlit-demo-data.s3-us-west-2.amazonaws.com"
        df = pd.read_csv(AWS_BUCKET_URL + "/agri.csv.gz")
        return df.set_index("Region")

    try:
        df = get_UN_data()
        countries = st.multiselect(
            "Choose countries", list(df.index), ["China", "United States of America"]
        )
        if not countries:
            st.error("Please select at least one country.")
        else:
            data = df.loc[countries]
            data /= 1000000.0
            st.write("### Gross Agricultural Production ($B)", data.sort_index())

            data = data.T.reset_index()
            data = pd.melt(data, id_vars=["index"]).rename(
                columns={"index": "year", "value": "Gross Agricultural Product ($B)"}
            )
            chart = (
                alt.Chart(data)
                .mark_area(opacity=0.3)
                .encode(
                    x="year:T",
                    y=alt.Y("Gross Agricultural Product ($B):Q", stack=None),
                    color="Region:N",
                )
            )
            st.altair_chart(chart, use_container_width=True)
    except URLError as e:
        st.error(
            """
            **This demo requires internet access.**

            Connection error: %s
        """
            % e.reason
        )

def startValuesReadings():
    st.session_state.showChart = True
    st.session_state.readVealues = True

def stopValuesReadings():    
    st.session_state.readVealues = False

def exportChartData():
    st.write("To be implemented");

def drawChart(args):
        import numpy as np
        import time
        
        my_st = args[0]
        last_rows = [[0.0]] #np.random.randn(1, 1)
        chart = my_st.line_chart(last_rows)

        for i in range(1, 101):
            #new_rows = last_rows[-1, :] + np.random.randn(2, 1)#.cumsum(axis=0)        
#            new_rows = np.random.randn(2, 1)
            #new_rows = ([[1.0,  1.0, 0.0,  1.0],   # random
                         #[ 0.0,  1.0,  0.0,  1.0]])
            new_rows = [[float(np.random.randint(2))]]
            chart.add_rows(new_rows)
            last_rows = new_rows
            time.sleep(0.01)   

def executar_analisador_digital():
    import streamlit as st

    st.markdown(f'# {list(page_names_to_funcs.keys())[0]}')
    st.write(
        """
        Verifique em tempo real o nível lógico das sondas em sua protoboard.
"""
    )
    col1, col2, col3 = st.columns([3,2,1])

    availableUSBPorts = ["COM1", "COM2", "COM3", "COM4", "COM5"]# TODO make a get
    col1.selectbox("Porta USB:", availableUSBPorts)
    col2.button("Atualizar lista")
    bitsPerSecond = col1.select_slider( 'Selecione uma taxa de transmissão', options=[300, 600, 1200, 2400, 4800, 9600, 14400, 19200, 28800, 31250, 38400, 57600, 115200], value=9600)
        
    col1, col2, col3 = st.columns([1,1,1])
    col1.button(":green[ :arrow_forward: Iniciar]", "startButton", "Iniciar leitura de dados", startValuesReadings)
    col2.button(":red[ :large_red_square: Parar]", "stopButton","Parar leitura de dados", stopValuesReadings)
    col3.download_button(":card_file_box: Exportar", "data.txt")

    if st.session_state.showChart:
        drawChart([st])

def configurar():
    import streamlit as st
    import time
    import numpy as np

    st.markdown(f'# {list(page_names_to_funcs.keys())[0]}')
    st.write(
        """
        This demo illustrates a combination of plotting and animation with
Streamlit. We're generating a bunch of random numbers in a loop for around
5 seconds. Enjoy!
"""
    )

    progress_bar = st.sidebar.progress(0)
    status_text = st.sidebar.empty()
    last_rows = np.random.randn(1, 1)
    chart = st.line_chart(last_rows)

    while(True):
        #new_rows = last_rows[-1, :] + np.random.randn(5, 1).cumsum(axis=0)
        
        #status_text.text("%i%% Complete" % i)
        chart.add_rows(new_rows)
        #progress_bar.progress(i)
        last_rows = new_rows
        time.sleep(0.01)

    progress_bar.empty()

    # Streamlit widgets automatically run the script from top to bottom. Since
    # this button is not connected to any other logic, it just causes a plain
    # rerun.
    st.button("Re-run")        

page_names_to_funcs = {
    "Analisador Digital": executar_analisador_digital,
    "Analisador Analógico": executar_analisador_digital
}

demo_name = st.sidebar.selectbox("Funcionalidades", page_names_to_funcs.keys())
page_names_to_funcs[demo_name]()
