# Parallel Test Execution

Execute 5 different file processing tests in parallel using the Task tool to demonstrate Claude Code's parallelization capabilities.

## Steps:

1. First, verify test data exists in `test-data/` directory. If not, run the file generator.

2. Launch 5 parallel agents using the Task tool, each performing a different analysis:
   - **Agent 1**: Count total words and calculate word frequency across all text files
   - **Agent 2**: Analyze all CSV files - count rows, columns, and extract unique values
   - **Agent 3**: Validate all JSON lines files and extract statistics
   - **Agent 4**: Parse all log files and generate log level summary report
   - **Agent 5**: Calculate file size statistics and compression ratios

3. Each agent should:
   - Read files from the manifest at `test-data/manifest.json`
   - Filter for their specific file type
   - Process files and measure execution time
   - Write results to a unique output file in `results/`
   - Return a summary of their findings

4. After all agents complete:
   - Collect all agent results
   - Calculate total execution time
   - Compare with sequential baseline (0.50 seconds for 50 files)
   - Generate a consolidated report showing:
     - Individual agent completion times
     - Total parallel execution time
     - Speedup factor vs sequential
     - Any errors or issues encountered

5. Save the final comparison report to `results/parallel-test-report.md`

## Expected Output:
- 5 individual result files from each agent
- 1 consolidated comparison report
- Performance metrics showing parallelization benefits