import pandas as pd
import streamlit as st

st.set_page_config(layout="wide")

st.title("Interactive Sankey diagrams of iron and steel flows", anchor=None)
st.markdown("**Author**: Takuma Watari (National Institute of Environmental Studies, Japan)")
st.markdown(
    "**Aim**: This web application presents interactive Sankey diagrams of iron and steel flows for the world's top 30 crude steel producing countries.")
st.markdown(
    "**Data sources**: The primary data used in this analysis comes from the World Steel Association and the US Geological Survey.")
st.markdown(
    "**Software**: The Sankey diagram is designed using floWeaver software: https://github.com/ricklupton/floweaver.")
st.markdown("**Interact with Sankey diagrams:**")
st.markdown("**-** Select a country: Use the pull-down menu to select the country you're interested in.")
st.markdown("**-** Select a year: Drag the slider to select the year you want to explore.")
st.markdown(
    "**-** View the graph: Once you've made your selection, the Sankey diagram for the selected country and year will instantly appear.")

available_years = [2000, 2005, 2010, 2015, 2019]
year = st.slider('Year', min_value=min(available_years), max_value=max(available_years), step=5)
file_path = f'data_{available_years[0]}.xlsx'
country_names_df = pd.read_excel(file_path, sheet_name='list')
country = st.selectbox('Country', country_names_df)

with open("sankey/" + f'{country}_{year}.svg', encoding="utf8") as file:
    svg_content = file.read()
# Display the SVG using markdown with raw HTML
st.markdown(f'<div style="justify-content: center;">{svg_content}</div>', unsafe_allow_html=True)
