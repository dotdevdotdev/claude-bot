#!/usr/bin/env python3
"""
Sequential file processor - baseline for performance comparison
"""
import json
import time
import os
import re
from collections import Counter
from datetime import datetime

class SequentialProcessor:
    def __init__(self):
        self.results = []
        self.start_time = None
        self.end_time = None
    
    def process_file(self, filepath):
        """Process a single file and return statistics"""
        start = time.time()
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Basic statistics
            stats = {
                'filename': os.path.basename(filepath),
                'size_bytes': len(content.encode('utf-8')),
                'line_count': len(content.splitlines()),
                'char_count': len(content),
                'word_count': len(content.split()),
            }
            
            # Character type analysis
            stats['letter_count'] = sum(1 for c in content if c.isalpha())
            stats['digit_count'] = sum(1 for c in content if c.isdigit())
            stats['special_count'] = sum(1 for c in content if not c.isalnum() and not c.isspace())
            
            # Word frequency (top 10)
            words = re.findall(r'\b\w+\b', content.lower())
            word_freq = Counter(words)
            stats['top_words'] = dict(word_freq.most_common(10))
            
            # File type specific processing
            if filepath.endswith('.csv'):
                lines = content.splitlines()
                stats['csv_rows'] = len(lines) - 1 if lines else 0
                stats['csv_columns'] = len(lines[0].split(',')) if lines else 0
            
            elif filepath.endswith('.jsonl'):
                valid_json_lines = 0
                for line in content.splitlines():
                    try:
                        json.loads(line)
                        valid_json_lines += 1
                    except:
                        pass
                stats['valid_json_lines'] = valid_json_lines
            
            elif filepath.endswith('.log'):
                log_levels = {'INFO': 0, 'WARNING': 0, 'ERROR': 0, 'DEBUG': 0}
                for level in log_levels:
                    log_levels[level] = len(re.findall(f'\\[{level}\\]', content))
                stats['log_levels'] = log_levels
            
            stats['process_time'] = time.time() - start
            stats['status'] = 'success'
            
        except Exception as e:
            stats = {
                'filename': os.path.basename(filepath),
                'status': 'error',
                'error': str(e),
                'process_time': time.time() - start
            }
        
        return stats
    
    def run(self, manifest_path='test-data/manifest.json'):
        """Process all files sequentially"""
        print("Starting sequential processing...")
        
        # Load manifest
        with open(manifest_path, 'r') as f:
            files = json.load(f)
        
        self.start_time = time.time()
        
        # Process each file
        for i, file_info in enumerate(files):
            print(f"Processing {i+1}/{len(files)}: {file_info['filename']}", end='\r')
            result = self.process_file(file_info['path'])
            result['file_type'] = file_info['type']
            result['declared_size_kb'] = file_info['size_kb']
            self.results.append(result)
        
        self.end_time = time.time()
        print(f"\nCompleted processing {len(files)} files")
        
        return self.generate_report()
    
    def generate_report(self):
        """Generate performance report"""
        total_time = self.end_time - self.start_time
        successful = sum(1 for r in self.results if r['status'] == 'success')
        failed = len(self.results) - successful
        
        report = {
            'method': 'sequential',
            'timestamp': datetime.now().isoformat(),
            'summary': {
                'total_files': len(self.results),
                'successful': successful,
                'failed': failed,
                'total_time': total_time,
                'avg_time_per_file': total_time / len(self.results) if self.results else 0,
                'files_per_second': len(self.results) / total_time if total_time > 0 else 0
            },
            'performance': {
                'start_time': self.start_time,
                'end_time': self.end_time,
                'duration': total_time
            },
            'file_results': self.results
        }
        
        # Calculate aggregate statistics
        if successful > 0:
            success_results = [r for r in self.results if r['status'] == 'success']
            report['aggregate_stats'] = {
                'total_bytes_processed': sum(r['size_bytes'] for r in success_results),
                'total_words_processed': sum(r['word_count'] for r in success_results),
                'total_lines_processed': sum(r['line_count'] for r in success_results),
                'avg_process_time': sum(r['process_time'] for r in success_results) / len(success_results)
            }
        
        return report

if __name__ == "__main__":
    processor = SequentialProcessor()
    report = processor.run()
    
    # Save detailed report
    with open('results/sequential-report.json', 'w') as f:
        json.dump(report, f, indent=2)
    
    # Print summary
    print("\n=== Sequential Processing Summary ===")
    print(f"Total Time: {report['summary']['total_time']:.2f} seconds")
    print(f"Files Processed: {report['summary']['total_files']}")
    print(f"Success Rate: {report['summary']['successful']}/{report['summary']['total_files']}")
    print(f"Average Time per File: {report['summary']['avg_time_per_file']:.4f} seconds")
    print(f"Files per Second: {report['summary']['files_per_second']:.2f}")
    
    if 'aggregate_stats' in report:
        print(f"\nTotal Bytes Processed: {report['aggregate_stats']['total_bytes_processed']:,}")
        print(f"Total Words Processed: {report['aggregate_stats']['total_words_processed']:,}")