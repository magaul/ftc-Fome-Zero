import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="Home",
    page_icon="📈"
)

image_path = r"C:\Users\lucca\OneDrive\Documentos\Curso ds\Python_zero_ao_ds\logo.png"
image = Image.open(image_path )
st.sidebar.image(image, width=120)


st.header ('Fome Zero')
st.header ('The best place to find your newest favorite restaurant!')

st.sidebar.markdown ("<h3 style='text-align: center; color: red;'> World Gastronomic Best Experiences</h3>", unsafe_allow_html=True)
st.sidebar.markdown ('''___''')

st.write(" Fome Zero Company Growth Dashboard" )

st.markdown(
    """
    Groth Dashboard was built to track the metrics of Restaurant reviews around the World.
    ### How to use this Growth Dashboard?
    - The data was made available on the Dashboard and the customer can search from simple to advanced to get the best ratings.
    - There is a geographic view, which shows the exact points of each location.
    - Filters are available to better serve the customer.
    - it is separated by category, Country vision, City Vision, and gastronomic Vision
    - The indicators are always updated to have better evaluations.
    ### Ask for Help
    - Data Science team
""")