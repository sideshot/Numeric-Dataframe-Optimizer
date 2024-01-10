
import pandas as pd
import numpy as np

def numeric_df_optimizer(df):
    print('Starting DataFrame Optimization')
    
    def determine_numeric_type(column):
        non_na_values = column.dropna()
    
        # If column has only integers (no fractional part), return 'int'
        # Use np.floor and direct comparison for efficiency
        if non_na_values.size == 0:
            return 'empty'
        if np.all(non_na_values == np.floor(non_na_values)):
            return 'int'
        else:
            return 'float'
    
    def best_fit_int_type(column):
        # Check if NaNs are present
        has_nan = column.isnull().any()
        
        # Find the minimum and maximum values, ignoring NaNs
        min_val = column.min(skipna=True)
        max_val = column.max(skipna=True)
        # Determine the best fit type
        if column.dropna().size == 0:
            return 'empty'
        elif has_nan:
            # Use Pandas nullable integer types if NaNs are present
            if min_val >= 0:
                if max_val <= np.iinfo(np.uint8).max:
                    return 'UInt8'
                elif max_val <= np.iinfo(np.uint16).max:
                    return 'UInt16'
                elif max_val <= np.iinfo(np.uint32).max:
                    return 'UInt32'
                else:
                    return 'UInt64'
            else:
                if min_val >= np.iinfo(np.int8).min and max_val <= np.iinfo(np.int8).max:
                    return 'Int8'
                elif min_val >= np.iinfo(np.int16).min and max_val <= np.iinfo(np.int16).max:
                    return 'Int16'
                elif min_val >= np.iinfo(np.int32).min and max_val <= np.iinfo(np.int32).max:
                    return 'Int32'
                else:
                    return 'Int64'
        else:
            # Use NumPy integer types if no NaNs are present
            if min_val >= 0:
                if max_val <= np.iinfo(np.uint8).max:
                    return 'uint8'
                elif max_val <= np.iinfo(np.uint16).max:
                    return 'uint16'
                elif max_val <= np.iinfo(np.uint32).max:
                    return 'uint32'
                else:
                    return 'uint64'
            else:
                if min_val >= np.iinfo(np.int8).min and max_val <= np.iinfo(np.int8).max:
                    return 'int8'
                elif min_val >= np.iinfo(np.int16).min and max_val <= np.iinfo(np.int16).max:
                    return 'int16'
                elif min_val >= np.iinfo(np.int32).min and max_val <= np.iinfo(np.int32).max:
                    return 'int32'
                else:
                    return 'int64'
    
    def best_fit_float_type(column):
        # Find the absolute maximum value (ignoring NaNs)
        max_val = column.abs().max(skipna=True)
    
        # Determine the best fit type based on the maximum value
        if np.isnan(max_val) or max_val <= np.finfo(np.float16).max:
            return 'float16'
        elif max_val <= np.finfo(np.float32).max:
            return 'float32'
        else:
            return 'float64'
    
    def memory_usage_of_dataframe(prefix, df):
        # Calculate the memory usage of each column and sum it up
        total_memory_bytes = df.memory_usage(deep=True).sum()
        
        # Convert bytes to gigabytes for a large dataset
        total_memory_gb = total_memory_bytes / 1024**3
    
        # Format the output similar to DataFrame.info()
        if total_memory_gb > 1:
            memory_usage_str = f"{total_memory_gb:.1f}+ GB"
        else:
            memory_usage_str = f"{total_memory_bytes / 1024**2:.1f} MB"
    
        print(prefix, f"Memory usage: {memory_usage_str}",f"Total Columns: {len(df.columns)}")

    memory_usage_of_dataframe('Before Optimization: ', df)

    # queue up the datatypes to change all at once.
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

    for col in numeric_cols:
        numeric_type = determine_numeric_type(df[col])
    
        if numeric_type == 'int':
            best_type = best_fit_int_type(df[col])
            df[col] = df[col].astype(best_type)
        elif numeric_type == 'float':
            best_type = best_fit_float_type(df[col])
            df[col] = df[col].astype(best_type)
        elif numeric_type == 'empty':
            df = df.drop(columns=[col])
            continue
        else:
            continue

    print('DataFrame optimization Completed')
    
    memory_usage_of_dataframe('After Optimization:', df)

    return df


def generate_mysql_dtype_script(df: pd.DataFrame, table_name: str) -> str:
    """
    Generates a MySQL ALTER TABLE script to match the data types in a given Pandas DataFrame.

    Args:
    df (pd.DataFrame): The DataFrame whose schema is to be translated into MySQL.
    table_name (str): The name of the MySQL table to be altered.

    Returns:
    str: A string containing the MySQL ALTER TABLE script.
    """

    # Mapping of Pandas/Numpy data types to MySQL data types
    type_mapping = {
        'int64': 'BIGINT',
        'int32': 'INT',
        'int16': 'SMALLINT',
        'int8': 'TINYINT',
        'float64': 'DOUBLE',
        'float32': 'FLOAT',
        'float16': 'FLOAT',  # MySQL does not have an exact equivalent for float16
        'uint8': 'TINYINT UNSIGNED',
        'uint16': 'SMALLINT UNSIGNED',
        'uint32': 'INT UNSIGNED',
        'uint64': 'BIGINT UNSIGNED',  # Included for completeness
        'object': 'VARCHAR(255)',  # Default VARCHAR size, adjust as needed
        'bool': 'BOOLEAN',
        'datetime64[ns]': 'DATETIME'
    }

    # Generate the ALTER TABLE script
    alter_statements = []
    for column, dtype in df.dtypes.items():
        mysql_type = type_mapping.get(dtype.name.lower(), 'VARCHAR(255)')
        alter_statements.append(f"MODIFY COLUMN `{column}` {mysql_type}")

    # Combine all statements into a single ALTER TABLE command
    alter_script = f"ALTER TABLE `{table_name}` " + ",\n".join(alter_statements) + ";"
    return alter_script

# Example Usage:
# df = pd.DataFrame({
#     'a': pd.Series([1], dtype='uint8'),
#     'b': pd.Series([1], dtype='float16'),
#     'c': ['text'],
#     'd': pd.to_datetime(['2021-01-01']),
#     'e': pd.Series([1], dtype='uint16'),
#     'f': pd.Series([1], dtype='uint32'),
#     # Add other columns as needed
# })
# script = generate_mysql_dtype_script(df, 'your_table_name')
# print(script)
