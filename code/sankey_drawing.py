import pandas as pd
import os
from floweaver import *
from data_processing import process_data_pipeline
from ipywidgets import interact
from IPython.display import display

def create_nodes():
    """
    Define the nodes.
    """
    nodes = {
        'Production of iron ore': ProcessGroup(['Production of iron ore'], title='Mine'),
        'Iron ore': ProcessGroup(['Iron ore'], title='Iron ore'),
        'Scrap steel': ProcessGroup(['Scrap steel'], title='Scrap steel'),
        'Imports of ore and scrap': ProcessGroup(['Imports of iron ore', 'Imports of scrap steel'], title='Imports'),
        'Exports of ore and scrap': ProcessGroup(['Exports of iron ore', 'Exports of scrap steel'], title='Exports'),
        'Pig iron': ProcessGroup(['Pig iron'], title='Pig iron'),
        'DRI': ProcessGroup(['DRI'], title='Direct reduced iron'),
        'Imports of pig and DRI': ProcessGroup(['Imports of pig iron', 'Imports of dri'], title='Imports'),
        'Exports of pig and DRI': ProcessGroup(['Exports of pig iron', 'Exports of dri'], title='Exports'),
        'BOF steel': ProcessGroup(['BOF steel'], title='BOF steel'),
        'EAF steel': ProcessGroup(['EAF steel'], title='EAF steel'),
        'Ingots and semis': ProcessGroup(['Ingots and semis'], title='Ingots and semis'),
        'Imports of ingots and semis': ProcessGroup(['Imports of ingots and semis'], title='Imports'),
        'Exports of ingots and semis': ProcessGroup(['Exports of ingots and semis'], title='Exports'),
        'Long products': ProcessGroup(['Long products'], title='Long products'),
        'Flat products': ProcessGroup(['Flat products'], title='Flat products'),
        'Imports of long and flat': ProcessGroup(['Imports of long products', 'Imports of flat products'], title='Imports'),
        'Exports of long and flat': ProcessGroup(['Exports of long products', 'Exports of flat products'], title='Exports'),
        'End-use goods': ProcessGroup(['End-use goods'], title='End-use goods'),
        'Imports of goods': ProcessGroup(['Imports of end-use goods'], title='Imports'),
        'Exports of goods': ProcessGroup(['Exports of end-use goods'], title='Exports'),
        'Stock': ProcessGroup(['Stock'], Partition.Simple('type', []), title='Stock'),
        'Loss': ProcessGroup(['Loss'], title='Loss'),
        'Loss_way1': Waypoint(title='', direction='R'),
        'Loss_way2': Waypoint(title='', direction='R'),
        'Scrap_way1': Waypoint(title='', direction='L'),
        'Scrap_way2': Waypoint(title='', direction='L'),
        'Scrap_way3': Waypoint(title='', direction='L'),
        'Reference flow start': ProcessGroup(['Reference flow start'], title='30 Mt'),
        'Reference flow end': ProcessGroup(['Reference flow end'], title=' ')
    }
    return nodes

def create_bundles():
    """
    Define the bundles.
    """
    bundles = [
        Bundle('Production of iron ore', 'Iron ore'),
        Bundle('Imports of ore and scrap', 'Iron ore'),
        Bundle('Iron ore', 'Pig iron'),
        Bundle('Iron ore', 'DRI'),
        Bundle('Iron ore', 'Exports of ore and scrap'),
        Bundle('Imports of ore and scrap', 'Scrap steel'),
        Bundle('Scrap steel', 'Exports of ore and scrap'),
        Bundle('Scrap steel', 'BOF steel'),
        Bundle('Scrap steel', 'EAF steel'),
        Bundle('Imports of pig and DRI', 'Pig iron'),
        Bundle('Pig iron', 'Exports of pig and DRI'),
        Bundle('Pig iron', 'BOF steel'),
        Bundle('Pig iron', 'EAF steel'),
        Bundle('Imports of pig and DRI', 'DRI'),
        Bundle('DRI', 'Exports of pig and DRI'),
        Bundle('DRI', 'EAF steel'),
        Bundle('BOF steel', 'Ingots and semis'),
        Bundle('EAF steel', 'Ingots and semis'),
        Bundle('Imports of ingots and semis', 'Ingots and semis'),
        Bundle('Ingots and semis', 'Exports of ingots and semis'),
        Bundle('Ingots and semis', 'Long products'),
        Bundle('Ingots and semis', 'Flat products'),
        Bundle('Imports of long and flat', 'Long products'),
        Bundle('Long products', 'Exports of long and flat'),
        Bundle('Imports of long and flat', 'Flat products'),
        Bundle('Flat products', 'Exports of long and flat'),
        Bundle('Long products', 'End-use goods'),
        Bundle('Flat products', 'End-use goods'),
        Bundle('Imports of goods', 'End-use goods'),
        Bundle('End-use goods', 'Exports of goods'),
        Bundle('End-use goods', 'Stock'),
        Bundle('Scrap steel', 'Loss', waypoints=['Loss_way1', 'Loss_way2']),
        Bundle('Pig iron', 'Loss', waypoints=['Loss_way2']),
        Bundle('DRI', 'Loss', waypoints=['Loss_way2']),
        Bundle('BOF steel', 'Loss'),
        Bundle('EAF steel', 'Loss'),
        Bundle('Long products', 'Scrap steel', waypoints=['Scrap_way1']),
        Bundle('Flat products', 'Scrap steel', waypoints=['Scrap_way1']),
        Bundle('End-use goods', 'Scrap steel', waypoints=['Scrap_way2', 'Scrap_way1']),
        Bundle('Stock', 'Scrap steel', waypoints=['Scrap_way3', 'Scrap_way2', 'Scrap_way1']),
        Bundle('Reference flow start', 'Reference flow end'),
    ]
    return bundles

def create_ordering():
    """
    Define the ordering.
    """
    ordering = [
    [['Imports of ore and scrap'],['Production of iron ore'], [],[],['Reference flow start']],
    [['Imports of pig and DRI'],['Iron ore', 'Scrap steel'],[],[],['Reference flow end']],
    [[],['Pig iron','DRI'],['Loss_way1'],[],['Exports of ore and scrap']],
    [['Imports of ingots and semis'],['BOF steel','EAF steel'],['Loss_way2'],[],['Exports of pig and DRI']],
    [['Imports of long and flat'],['Ingots and semis'],['Loss'],[],[]],
    [['Imports of goods'],['Long products','Flat products'],[],['Scrap_way1'],['Exports of ingots and semis']],
    [[],['End-use goods'],[],['Scrap_way2'],[ 'Exports of long and flat']],
    [[],['Stock'],[],['Scrap_way3'],['Exports of goods']],
    ]
    return ordering

def create_palette():
    """
    Define the color palette.
    """
    palette = {
        'Iron ore': '#525252',
        'Pig iron': '#0868ac',
        'DRI': '#4eb3d3',
        'BOF steel': '#2b8cbe',
        'EAF steel': '#7bccc4',
        'Ingots and semis': '#a8ddb5',
        'Long products': '#ccebc5',
        'Flat products': '#e0f3db',
        'End-use goods': '#dfc27d',
        'Loss': '#f0f0f0',
        'Generated scrap': '#d9d9d9',
        'Scrap steel': '#d9d9d9',
        'Balancing flows': '#fb6a4a',
        'Reference': '#d9d9d9',
    }
    return palette

def generate_sankey_diagram(transformed_data, country, year, file_name=None):
    """
    Generate the Sankey diagram.
    """
    dataset = Dataset(transformed_data)
    nodes = create_nodes()
    bundles = create_bundles()
    ordering = create_ordering()
    palette = create_palette()
    
    sdd = SankeyDefinition(nodes, bundles, ordering, flow_partition=dataset.partition('type'))
    sankey_widget = weave(sdd, dataset, palette=palette).to_widget(width=1100, height=400)
    
    directory = os.path.join('..', 'sankey')
    os.makedirs(directory, exist_ok=True)
    file_name = f'{country}_{year}.svg'
    file_path = os.path.join(directory, file_name)
    sankey_widget.auto_save_svg(file_path)

    return sankey_widget, transformed_data