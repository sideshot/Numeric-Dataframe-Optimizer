# Correctly Optimize Numeric Columns in a DataFrame.

## Overview
This script is designed to optimize memory usage in large Pandas DataFrames. It intelligently selects the most appropriate data types for numeric columns, balancing memory efficiency with the need to represent the data accurately. This is particularly useful for large datasets, where memory management is crucial.

## Features
- **Automatic Data Type Selection**: Determines the best data type for each numeric column based on the range of values and presence of NaNs.
- **Memory Usage Reduction**: Significantly reduces the memory footprint of the DataFrame.
- **Column Removal**: Drops completely empty columns, further optimizing memory usage.

## Results
Using this script on a DataFrame with 12 million rows showed substantial improvements:
- **Runtime**: 54 seconds
- **Before Optimization**: 
  - Memory Usage: 10.5+ GB
  - Total Columns: 107
- **After Optimization**: 
  - Memory Usage: 2.9+ GB
  - Total Columns: 85

## Usage
1. Import the required libraries: `pandas` and `numpy`.
2. Define the `optimize_df` function in your script.
3. Pass your DataFrame to the `optimize_df` function.

Example:
```python
import pandas as pd
import numpy as np

# Your DataFrame
original_df = ...

optimized_df = numeric_df_optimizer(original_df)
```

## Implementation Details
- The script includes functions to determine the best-fit data type for integer and floating-point columns.
- It uses a combination of NumPy and Pandas data types, choosing between standard and nullable types based on the presence of NaN values.
- The script begins by reporting the initial memory usage and ends with the optimized memory usage for easy comparison.

## Requirements
- Python 3.x
- Pandas 2.x
- NumPy

## Disclaimer
- The script assumes that the input DataFrame is well-formed and contains numeric columns that can benefit from data type optimization.
- The performance may vary based on the DataFrame's structure and content.

------------------

# NEW! MySQL Table Schema Generator

This section introduces a Python function `generate_mysql_dtype_script` designed to create a MySQL ALTER TABLE script based on the schema of a Pandas DataFrame. It is particularly useful in scenarios where the DataFrame's schema has been optimized for memory efficiency, and the same optimizations are desired in the corresponding MySQL database schema.

### Functionality

- Maps Pandas/Numpy data types to the closest MySQL data types.
- Generates ALTER TABLE scripts to modify existing MySQL tables to align with DataFrame schemas.
- Useful for ensuring data type consistency between in-memory (Pandas) and database (MySQL) representations.

### Usage

1. Ensure you have Pandas installed in your environment.
2. Import the function using `from your_script_name import generate_mysql_dtype_script`.
3. Pass your DataFrame and the target MySQL table name to the function.
4. Execute the returned script in your MySQL database environment.

### Example

```python
import pandas as pd
from your_script_name import generate_mysql_script

# Example DataFrame
df = pd.DataFrame({
    # Your DataFrame columns and data here
})

# Generate the ALTER TABLE script
script = generate_mysql_dtype_script(df, 'your_mysql_table_name')
print(script)
