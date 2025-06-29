#!/usr/bin/env python3
"""
Generate random text files for parallel processing tests
"""
import os
import random
import string
import json
import csv
from datetime import datetime, timedelta

class TestFileGenerator:
    def __init__(self, output_dir="test-data"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
    def generate_random_text(self, size_kb):
        """Generate random Lorem Ipsum style text"""
        words = ['lorem', 'ipsum', 'dolor', 'sit', 'amet', 'consectetur', 
                 'adipiscing', 'elit', 'sed', 'do', 'eiusmod', 'tempor',
                 'incididunt', 'ut', 'labore', 'et', 'dolore', 'magna']
        
        target_size = size_kb * 1024
        content = []
        current_size = 0
        
        while current_size < target_size:
            sentence_length = random.randint(5, 15)
            sentence = ' '.join(random.choices(words, k=sentence_length))
            sentence = sentence.capitalize() + '.\n'
            content.append(sentence)
            current_size += len(sentence.encode('utf-8'))
            
        return ''.join(content)
    
    def generate_json_data(self, size_kb):
        """Generate random JSON data"""
        target_size = size_kb * 1024
        data = []
        current_size = 0
        
        while current_size < target_size:
            record = {
                'id': random.randint(1000, 9999),
                'name': ''.join(random.choices(string.ascii_letters, k=10)),
                'value': round(random.uniform(0, 1000), 2),
                'timestamp': (datetime.now() - timedelta(days=random.randint(0, 365))).isoformat(),
                'active': random.choice([True, False])
            }
            record_str = json.dumps(record) + '\n'
            data.append(record_str)
            current_size += len(record_str.encode('utf-8'))
            
        return ''.join(data)
    
    def generate_csv_data(self, size_kb):
        """Generate random CSV data"""
        target_size = size_kb * 1024
        rows = []
        headers = ['id', 'name', 'age', 'email', 'score', 'department']
        rows.append(','.join(headers) + '\n')
        current_size = len(rows[0].encode('utf-8'))
        
        departments = ['Sales', 'Engineering', 'Marketing', 'HR', 'Finance']
        
        while current_size < target_size:
            row = [
                str(random.randint(1000, 9999)),
                ''.join(random.choices(string.ascii_letters, k=8)),
                str(random.randint(20, 65)),
                f"{''.join(random.choices(string.ascii_lowercase, k=8))}@example.com",
                str(round(random.uniform(0, 100), 2)),
                random.choice(departments)
            ]
            row_str = ','.join(row) + '\n'
            rows.append(row_str)
            current_size += len(row_str.encode('utf-8'))
            
        return ''.join(rows)
    
    def generate_log_data(self, size_kb):
        """Generate random log entries"""
        target_size = size_kb * 1024
        logs = []
        current_size = 0
        
        log_levels = ['INFO', 'WARNING', 'ERROR', 'DEBUG']
        components = ['auth', 'database', 'api', 'cache', 'worker']
        
        base_time = datetime.now() - timedelta(days=1)
        
        while current_size < target_size:
            timestamp = base_time + timedelta(seconds=random.randint(0, 86400))
            level = random.choice(log_levels)
            component = random.choice(components)
            message = f"Operation {''.join(random.choices(string.ascii_lowercase, k=10))} completed"
            
            log_entry = f"[{timestamp.isoformat()}] [{level}] [{component}] {message}\n"
            logs.append(log_entry)
            current_size += len(log_entry.encode('utf-8'))
            
        return ''.join(logs)
    
    def generate_files(self, count=50, sizes=[1, 10, 100]):
        """Generate test files with various types and sizes"""
        file_types = ['text', 'json', 'csv', 'log']
        generated_files = []
        
        for i in range(count):
            file_type = random.choice(file_types)
            size = random.choice(sizes)
            
            if file_type == 'text':
                content = self.generate_random_text(size)
                ext = 'txt'
            elif file_type == 'json':
                content = self.generate_json_data(size)
                ext = 'jsonl'
            elif file_type == 'csv':
                content = self.generate_csv_data(size)
                ext = 'csv'
            else:  # log
                content = self.generate_log_data(size)
                ext = 'log'
            
            filename = f"test_{i:03d}_{size}kb.{ext}"
            filepath = os.path.join(self.output_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            generated_files.append({
                'filename': filename,
                'type': file_type,
                'size_kb': size,
                'path': filepath
            })
            
        return generated_files

if __name__ == "__main__":
    generator = TestFileGenerator()
    print("Generating test files...")
    files = generator.generate_files(count=50)
    print(f"Generated {len(files)} files in 'test-data' directory")
    
    # Save file manifest
    with open('test-data/manifest.json', 'w') as f:
        json.dump(files, f, indent=2)
    print("File manifest saved to test-data/manifest.json")