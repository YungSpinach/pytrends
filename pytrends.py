import pandas as pd # type: ignore
import pytrends
from pytrends.request import TrendReq # type: ignore

# Initialize pytrends
pytrends = TrendReq(hl='en-GB', tz=0)

# Load the input CSV file
input_file = "pytrends_inputs.csv"
input_data = pd.read_csv(input_file)

# Prepare an empty DataFrame to store the results
result_df = pd.DataFrame()

# Iterate over each row in the input CSV
for index, row in input_data.iterrows():
    # Extract search terms from the row
    search_terms = row.values.tolist()
    
    # Build the payload for pytrends
    pytrends.build_payload(search_terms, timeframe='today 12-m', geo='GB')
    
    # Fetch interest over time
    trends_data = pytrends.interest_over_time()
    
    # Drop the 'isPartial' column if it exists
    if 'isPartial' in trends_data.columns:
        trends_data = trends_data.drop(columns=['isPartial'])
    
    # Add the search terms as columns to the DataFrame
    trends_data = trends_data.reset_index()
    for i, term in enumerate(search_terms):
        trends_data[f"Search Term {i+1}"] = term
    
    # Append the trends data to the result DataFrame
    result_df = pd.concat([result_df, trends_data], ignore_index=True)

# Save the result DataFrame to a CSV file
output_file = "pytrends_results.csv"
result_df.to_csv(output_file, index=False)

print(f"Search trend data has been saved to {output_file}")