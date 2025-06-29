# Bulk File Generation & Transformation Test Case

## Test Case Overview
Generate multiple random text files with varying sizes and content, then transform them (e.g., count words, extract statistics, convert formats) to measure parallelization benefits.

## Test Parameters
- **File Count**: 50-100 files
- **File Sizes**: Small (1KB), Medium (10KB), Large (100KB)
- **Content Types**: 
  - Random sentences with Lorem Ipsum style text
  - JSON data with random values
  - CSV data with random rows
  - Log-style entries with timestamps

## Transformation Tasks
1. Word count and frequency analysis
2. Character statistics (letters, numbers, special chars)
3. Line count and average line length
4. Format conversion (e.g., text to JSON summary)
5. Pattern matching (find specific words/phrases)

## Metrics to Measure
- Total execution time
- Time per file
- CPU utilization
- Memory usage
- Success/failure rate
- Files processed per second

## Test Variations
1. **Sequential**: Process files one by one
2. **Batch Parallel**: Process in batches of N files
3. **Full Parallel**: Process all files simultaneously
4. **Smart Parallel**: Distribute based on file size

## Expected Outcomes
- Identify optimal parallelization strategies
- Understand Claude Code's concurrency limits
- Document performance improvements
- Find bottlenecks and failure points