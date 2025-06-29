#!/usr/bin/env python3
import json
import os
import time
from pathlib import Path
from datetime import datetime

def estimate_compression_ratio(file_path, file_type):
    """Estimate compression potential based on file type and content patterns"""
    # Typical compression ratios for different file types
    compression_estimates = {
        'text': 0.3,  # Text files typically compress to 30% of original
        'csv': 0.25,  # CSV files with repetitive data compress well
        'json': 0.35, # JSON has structure but also repetition
        'log': 0.2,   # Log files often have very repetitive patterns
    }
    return compression_estimates.get(file_type, 0.5)

def analyze_files():
    start_time = time.time()
    
    # Read manifest
    with open('test-data/manifest.json', 'r') as f:
        manifest = json.load(f)
    
    # Initialize statistics
    stats = {
        'total_files': 0,
        'total_bytes': 0,
        'size_distribution': {
            '1kb': {'count': 0, 'total_bytes': 0, 'files': []},
            '10kb': {'count': 0, 'total_bytes': 0, 'files': []},
            '100kb': {'count': 0, 'total_bytes': 0, 'files': []}
        },
        'file_types': {},
        'compression_potential': {
            'total_original_bytes': 0,
            'total_compressed_estimate': 0,
            'potential_savings_bytes': 0,
            'potential_savings_percent': 0
        },
        'files_analyzed': [],
        'largest_file': {'name': '', 'size': 0},
        'smallest_file': {'name': '', 'size': float('inf')}
    }
    
    # Process each file
    for file_info in manifest:
        file_path = file_info['path']
        declared_size_kb = file_info['size_kb']
        file_type = file_info['type']
        
        try:
            # Get actual file size
            actual_size = os.path.getsize(file_path)
            
            # Update statistics
            stats['total_files'] += 1
            stats['total_bytes'] += actual_size
            
            # Categorize by size
            size_category = f"{declared_size_kb}kb"
            if size_category in stats['size_distribution']:
                stats['size_distribution'][size_category]['count'] += 1
                stats['size_distribution'][size_category]['total_bytes'] += actual_size
                stats['size_distribution'][size_category]['files'].append({
                    'name': file_info['filename'],
                    'actual_size': actual_size,
                    'declared_size_kb': declared_size_kb
                })
            
            # Track by file type
            if file_type not in stats['file_types']:
                stats['file_types'][file_type] = {
                    'count': 0,
                    'total_bytes': 0,
                    'average_size': 0
                }
            stats['file_types'][file_type]['count'] += 1
            stats['file_types'][file_type]['total_bytes'] += actual_size
            
            # Estimate compression
            compression_ratio = estimate_compression_ratio(file_path, file_type)
            compressed_estimate = int(actual_size * compression_ratio)
            stats['compression_potential']['total_original_bytes'] += actual_size
            stats['compression_potential']['total_compressed_estimate'] += compressed_estimate
            
            # Track largest and smallest
            if actual_size > stats['largest_file']['size']:
                stats['largest_file'] = {
                    'name': file_info['filename'],
                    'size': actual_size,
                    'size_kb': round(actual_size / 1024, 2)
                }
            if actual_size < stats['smallest_file']['size']:
                stats['smallest_file'] = {
                    'name': file_info['filename'],
                    'size': actual_size,
                    'size_kb': round(actual_size / 1024, 2)
                }
            
            # Add to analyzed files list
            stats['files_analyzed'].append({
                'filename': file_info['filename'],
                'type': file_type,
                'declared_size_kb': declared_size_kb,
                'actual_size_bytes': actual_size,
                'actual_size_kb': round(actual_size / 1024, 2),
                'size_difference_bytes': actual_size - (declared_size_kb * 1024),
                'compression_ratio': compression_ratio,
                'compressed_estimate_bytes': compressed_estimate
            })
            
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
    
    # Calculate averages and final stats
    if stats['total_files'] > 0:
        stats['average_file_size'] = {
            'bytes': round(stats['total_bytes'] / stats['total_files'], 2),
            'kb': round((stats['total_bytes'] / stats['total_files']) / 1024, 2)
        }
    
    # Calculate file type averages
    for file_type in stats['file_types']:
        type_stats = stats['file_types'][file_type]
        if type_stats['count'] > 0:
            type_stats['average_size'] = round(type_stats['total_bytes'] / type_stats['count'], 2)
    
    # Calculate compression savings
    total_original = stats['compression_potential']['total_original_bytes']
    total_compressed = stats['compression_potential']['total_compressed_estimate']
    if total_original > 0:
        stats['compression_potential']['potential_savings_bytes'] = total_original - total_compressed
        stats['compression_potential']['potential_savings_percent'] = round(
            ((total_original - total_compressed) / total_original) * 100, 2
        )
    
    # Convert total bytes to human readable
    stats['total_size_human_readable'] = {
        'bytes': stats['total_bytes'],
        'kb': round(stats['total_bytes'] / 1024, 2),
        'mb': round(stats['total_bytes'] / (1024 * 1024), 2)
    }
    
    # Execution time
    execution_time = time.time() - start_time
    stats['execution_time_seconds'] = round(execution_time, 4)
    stats['timestamp'] = datetime.now().isoformat()
    
    # Sort files for cleaner output
    stats['files_analyzed'].sort(key=lambda x: x['actual_size_bytes'], reverse=True)
    
    return stats

if __name__ == "__main__":
    # Ensure results directory exists
    os.makedirs('results', exist_ok=True)
    
    # Run analysis
    results = analyze_files()
    
    # Save results
    with open('results/agent5-size-analysis.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    # Print summary
    print(f"Analysis complete!")
    print(f"Total files analyzed: {results['total_files']}")
    print(f"Total size: {results['total_size_human_readable']['mb']:.2f} MB")
    print(f"Average file size: {results['average_file_size']['kb']:.2f} KB")
    print(f"Execution time: {results['execution_time_seconds']:.4f} seconds")