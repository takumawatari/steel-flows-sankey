import pandas as pd
import streamlit as st

st.set_page_config(layout="wide")
st.title("Sankey Diagrams of Iron and Steel Flows", anchor=None)

st.markdown("**Author**: [Takuma Watari](https://takuma-watari.com/en/) (National Institute of Environmental Studies, Japan)")

st.markdown(
    """
    **Aim**: This web application presents Sankey diagrams of iron and steel flows for the world's top 30 crude steel producing countries.
    
    **Software**: The Sankey diagrams are designed using [floWeaver software](https://github.com/ricklupton/floweaver).
    
    **Interact with Sankey diagrams:**
    - **Select a country**: Use the pull-down menu to select the country you're interested in.
    - **Select a year**: Drag the slider to select the year you want to explore.
    - **View the diagram**: Once you've made your selection, the Sankey diagram for the selected country and year will instantly appear.
    """
)

available_years = [2000, 2005, 2010, 2015, 2019]
year = st.select_slider('Year', options=available_years)
file_path = f'data_{year}.xlsx'
country_names_df = pd.read_excel(file_path, sheet_name='list')
country = st.selectbox('Country', country_names_df['Country'])

with open("sankey/" + f'{country}_{year}.svg', encoding="utf8") as file:
    svg_content = file.read()
st.markdown(f'<div style="justify-content: center;">{svg_content}</div>', unsafe_allow_html=True)