import pandas as pd
from data_processing import process_data_pipeline
from sankey_drawing import generate_sankey_diagram
from ipywidgets import interact, widgets
from IPython.display import display
import os

# Read the Excel file and extract the country names
def read_country_names(file_path):
    country_names_df = pd.read_excel(file_path, sheet_name='list')
    return country_names_df['Country'].tolist()
    
# Generate Sankey widgets
def generate_sankey_widgets(year):
    file_path = os.path.join('..', 'data', f'data_{year}.xlsx')
    country_names = read_country_names(file_path)
    
    transformed_data_path = os.path.join('..', 'data', f'transformed_data_{year}.xlsx')
    excel_writer = pd.ExcelWriter(transformed_data_path)
    
    sankey_widgets = {} 
    with pd.ExcelWriter(transformed_data_path) as excel_writer:
        for country_name in country_names:
            transformed_data = process_data_pipeline(file_path, country_name)
            transformed_data.to_excel(excel_writer, sheet_name=country_name, index=False)
            file_name = f'{country_name}_{year}.svg'
            sankey_widget = generate_sankey_diagram(transformed_data, country_name, year, file_name=file_name)[0]
            sankey_widgets[country_name] = sankey_widget
    
    return sankey_widgets

# Display the Sankey widget
def display_sankey(country, year, sankey_widgets):
    display(sankey_widgets[year][country])

# Run an interactive Sankey diagram
def run_sankey_interactive(available_years):
    sankey_widgets = {}
    for year in available_years:
        sankey_widgets[year] = generate_sankey_widgets(year)

    initial_file_path = os.path.join('..', 'data', f'data_{available_years[0]}.xlsx')
    country_names = read_country_names(initial_file_path)
    
    interact(display_sankey, 
             country=widgets.Dropdown(options=country_names, description='Country:'), 
             year=widgets.SelectionSlider(options=available_years, description='Year:', continuous_update=False),
             sankey_widgets=widgets.fixed(sankey_widgets))