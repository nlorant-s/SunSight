from select import selection, full_data, rankings_df

def filter(selection_df, full_data, rankings_df):
    # Get the indices from the first column of selection
    indices = selection_df.iloc[:, 0].tolist()
    # Get corresponding zip codes from rankings_df using these indices
    zip_codes = rankings_df.loc[indices, 'zip_code'].tolist()
    
    # Debug
    print("First 5 zip codes selected:")
    print(zip_codes[:5])
    
    # Filter main DataFrame based on zip codes
    filtered_df = full_data[full_data['zip_code'].isin(zip_codes)]
    
    return filtered_df

# need to fix repeat selections (unless desired)
selected_data = filter(selection, full_data, rankings_df)