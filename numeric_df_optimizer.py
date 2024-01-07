
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
