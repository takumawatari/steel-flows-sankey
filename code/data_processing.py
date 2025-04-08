import pandas as pd

# Process data pipeline
def process_data_pipeline(file_path, sheet_name):
    original_data = read_original_data(file_path, sheet_name)
    transposed_data = transpose_data(original_data)
    transformed_data = add_transformed_data_columns(transposed_data)
    transformed_data = add_balancing_flows(transformed_data)
    transformed_data = swap_source_target(transformed_data)
    transformed_data = rename_target_source_based_on_type(transformed_data)
    transformed_data = rename_scrap(transformed_data)
    transformed_data = rename_exports_imports(transformed_data)
    transformed_data = add_iron_ore_production(transformed_data)
    transformed_data = convert_values_to_positive(transformed_data)

    reference_flow = pd.DataFrame({'source': ['Reference flow start'],
                                   'target': ['Reference flow end'],
                                   'value': [30000],
                                   'type': ['Reference']})
    transformed_data = pd.concat([transformed_data, reference_flow], ignore_index=True)
    
    return transformed_data

# Read the original data
def read_original_data(file_path, sheet_name):
    try:
        original_data = pd.read_excel(file_path, sheet_name=sheet_name, usecols='A:K,M:P', nrows=12, index_col=0)
        original_data.fillna(0, inplace=True)
        return original_data
    except FileNotFoundError:
        print("File not found.")
        return None

# Transpose the original data
def transpose_data(original_data):
    return original_data.T

# Add source, target, and type columns
def add_transformed_data_columns(transposed_data):
    transformed_data = pd.DataFrame()
    transformed_data['source'] = transposed_data.columns.tolist() * len(transposed_data.index)
    transformed_data['target'] = transposed_data.index.repeat(len(transposed_data.columns))
    transformed_data['type'] = transposed_data.columns.tolist() * len(transposed_data.index)
    transformed_data['value'] = transposed_data.values.flatten()
    return transformed_data

# Add rows for balancing flows
def add_balancing_flows(transformed_data):
    new_rows = []
    for index, row in transformed_data.iterrows():
        if row['target'] == 'Balancing flows':
            if row['value'] > 0:
                transformed_data.at[index, 'target'] = 'Exports'
                transformed_data.at[index, 'type'] = 'Balancing flows'
                new_rows.append({'source': row['source'], 'target': 'Imports', 'type': 'Balancing flows', 'value': 0})
            elif row['value'] < 0:
                transformed_data.at[index, 'target'] = 'Imports'
                transformed_data.at[index, 'type'] = 'Balancing flows'
                new_rows.append({'source': row['source'], 'target': 'Exports', 'type': 'Balancing flows', 'value': 0})

        if row['target'] == 'Balancing flows' and row['value'] == 0:
            new_rows.append({'source': row['source'], 'target': 'Exports', 'type': 'Balancing flows', 'value': 0})
            new_rows.append({'source': row['source'], 'target': 'Imports', 'type': 'Balancing flows', 'value': 0})

    return pd.concat([transformed_data, pd.DataFrame(new_rows)], ignore_index=True)

# Swap source and target columns
def swap_source_target(transformed_data):
    transformed_data.loc[transformed_data['source'] == 'Loss', ['source', 'target']] = transformed_data.loc[transformed_data['source'] == 'Loss', ['target', 'source']].values
    transformed_data.loc[transformed_data['source'] == 'In-use goods', ['source', 'target']] = transformed_data.loc[transformed_data['source'] == 'In-use goods', ['target', 'source']].values
    transformed_data.loc[transformed_data['source'] == 'Generated scrap', ['source', 'target']] = transformed_data.loc[transformed_data['source'] == 'Generated scrap', ['target', 'source']].values
    transformed_data.loc[transformed_data['target'] == 'Imports', ['source', 'target']] = transformed_data.loc[transformed_data['target'] == 'Imports', ['target', 'source']].values
    return transformed_data

# Rename source and target
def rename_target_source_based_on_type(transformed_data):
    for index, row in transformed_data.iterrows():
        if row['target'] == 'Exports' or row['source'] == 'Imports' or row['source'] == 'Production':
            if row['type'] != 'Balancing flows':
                if row['target'] == 'Exports':
                    transformed_data.at[index, 'target'] = f'Exports of {row["type"].lower()}'
                elif row['source'] == 'Imports':
                    transformed_data.at[index, 'source'] = f'Imports of {row["type"].lower()}'
                elif row['source'] == 'Production':
                    transformed_data.at[index, 'source'] = f'Production of {row["type"].lower()}'
    return transformed_data

# Rename 'Generated scrap'
def rename_scrap(transformed_data):
    transformed_data.loc[transformed_data['target'] == 'Generated scrap', 'target'] = 'Scrap steel'
    return transformed_data

# Rename 'Exports' and 'Imports'
def rename_exports_imports(transformed_data):
    for index, row in transformed_data.iterrows():
        if row['target'] == 'Exports' and row['type'] == 'Balancing flows':
            transformed_data.at[index, 'target'] = f'Exports of {row["source"].lower()}'
        elif row['source'] == 'Imports' and row['type'] == 'Balancing flows':
            transformed_data.at[index, 'source'] = f'Imports of {row["target"].lower()}'
    return transformed_data

# Add data for iron ore production
def add_iron_ore_production(transformed_data):
    iron_ore_data = transformed_data[
        (transformed_data['source'] == 'Iron ore') | 
        (transformed_data['target'] == 'Iron ore')
    ]
    value_iron_ore_production = iron_ore_data['value'].sum()
    
    new_row = pd.DataFrame({'source': ['Production of iron ore'],
                            'target': ['Iron ore'],
                            'type': ['Iron ore'],
                            'value': [value_iron_ore_production]})
    
    transformed_data = pd.concat([transformed_data, new_row], ignore_index=True)
    return transformed_data

# Convert all values to positive
def convert_values_to_positive(transformed_data):
    transformed_data['value'] = transformed_data['value'].abs()
    return transformed_data