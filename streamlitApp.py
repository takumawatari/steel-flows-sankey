import pandas as pd
import streamlit as st

st.set_page_config(layout="wide")

tabs = st.tabs(["Overview", "Interact"])

with tabs[0]:
    st.markdown("**Author**: Takuma Watari (National Institute of Environmental Studies, Japan)")
    st.markdown("**Aim**: This notebook presents interactive Sankey diagrams of iron and steel flows for the world's top 30 crude steel producing countries.")
    st.markdown("**Data sources**: The primary data used in this analysis comes from the World Steel Association and the US Geological Survey.")
    st.markdown("**Software**: The Sankey diagram is designed using floWeaver software: https://github.com/ricklupton/floweaver.")

with tabs[1]:
    st.markdown("**Interact with Sankey diagrams:**")
    available_years = [2000, 2005, 2010, 2015, 2019]
    year = st.selectbox('Year', available_years)
    file_path = f'data_{available_years[0]}.xlsx'
    country_names_df = pd.read_excel(file_path, sheet_name='list')
    country = st.selectbox('Country', country_names_df)
    with open("sankey/" + f'{country}_{year}.svg', encoding="utf8") as file:
        svg_content = file.read()
    st.markdown(f'<div style="justify-content: center;">{svg_content}</div>', unsafe_allow_html=True)


with open("sankey/" + f'{country}_{year}.svg', encoding="utf8") as file:
    svg_content = file.read()
# Display the SVG using markdown with raw HTML
st.markdown(f'<div style="justify-content: center;">{svg_content}</div>', unsafe_allow_html=True)
