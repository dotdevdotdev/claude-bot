#!/usr/bin/env python3
import json
import csv
import time
from datetime import datetime
from pathlib import Path

def analyze_csv_files():
    start_time = time.time()
    
    # Read manifest
    with open('test-data/manifest.json', 'r') as f:
        manifest = json.load(f)
    
    # Filter CSV files
    csv_files = [item for item in manifest if item['type'] == 'csv']
    
    # Initialize counters
    total_rows = 0
    all_departments = set()
    age_values = []
    column_counts = []
    files_processed = 0
    
    file_results = []
    
    for csv_file in csv_files:
        file_path = csv_file['path']
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                headers = reader.fieldnames
                
                if headers:
                    column_counts.append(len(headers))
                
                row_count = 0
                file_departments = set()
                file_ages = []
                
                for row in reader:
                    row_count += 1
                    
                    # Check for department column
                    if 'department' in row:
                        if row['department']:
                            file_departments.add(row['department'])
                            all_departments.add(row['department'])
                    
                    # Check for age column
                    if 'age' in row:
                        try:
                            age = int(row['age'])
                            file_ages.append(age)
                            age_values.append(age)
                        except (ValueError, TypeError):
                            pass
                
                total_rows += row_count
                files_processed += 1
                
                file_result = {
                    'filename': csv_file['filename'],
                    'rows': row_count,
                    'columns': len(headers) if headers else 0,
                    'departments_found': list(file_departments),
                    'average_age': sum(file_ages) / len(file_ages) if file_ages else None
                }
                file_results.append(file_result)
                
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
    
    execution_time = time.time() - start_time
    
    # Calculate overall statistics
    results = {
        'total_files_processed': files_processed,
        'total_rows': total_rows,
        'column_statistics': {
            'min_columns': min(column_counts) if column_counts else 0,
            'max_columns': max(column_counts) if column_counts else 0,
            'avg_columns': sum(column_counts) / len(column_counts) if column_counts else 0
        },
        'unique_departments': sorted(list(all_departments)),
        'total_unique_departments': len(all_departments),
        'overall_average_age': sum(age_values) / len(age_values) if age_values else None,
        'execution_time_seconds': execution_time,
        'timestamp': datetime.now().isoformat(),
        'file_details': file_results
    }
    
    # Create results directory if it doesn't exist
    Path('results').mkdir(exist_ok=True)
    
    # Write results
    with open('results/agent2-csv-analysis.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    return results

if __name__ == '__main__':
    results = analyze_csv_files()
    print(f"Analysis complete!")
    print(f"Files processed: {results['total_files_processed']}")
    print(f"Total rows: {results['total_rows']}")
    print(f"Unique departments: {results['total_unique_departments']}")
    print(f"Execution time: {results['execution_time_seconds']:.3f} seconds")