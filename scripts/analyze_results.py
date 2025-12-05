#!/usr/bin/env python3
"""
Analyze comprehensive test results and generate summary statistics
"""
import sys
import pandas as pd
import os

def analyze_results(csv_file):
    """Analyze the test results and generate summary"""
    if not os.path.exists(csv_file):
        print(f"Error: Results file {csv_file} not found")
        return
    
    # Read results
    df = pd.read_csv(csv_file)
    
    print("\n" + "="*80)
    print("PERFORMANCE ANALYSIS SUMMARY")
    print("="*80)
    
    # Group by implementation, workers, and N
    grouped = df.groupby(['Implementation', 'Workers', 'N'])
    
    # Calculate statistics
    summary = grouped['Time_s'].agg(['mean', 'std', 'min', 'max']).reset_index()
    summary['Result'] = grouped['Result'].first().values
    
    # Calculate speedup relative to serial for each N
    for n in df['N'].unique():
        print(f"\n{'─'*80}")
        print(f"Problem Size: N = {n:,}")
        print(f"{'─'*80}")
        
        n_data = summary[summary['N'] == n].copy()
        
        # Get serial baseline
        serial_time = n_data[n_data['Implementation'] == 'Serial']['mean'].values[0]
        
        # Calculate speedup and efficiency
        n_data['Speedup'] = serial_time / n_data['mean']
        n_data['Efficiency'] = (n_data['Speedup'] / n_data['Workers']) * 100
        
        # Print table
        print(f"\n{'Implementation':<12} {'Workers':<8} {'Time(s)':<12} {'Speedup':<10} {'Efficiency':<12} {'Result':<15}")
        print("─" * 80)
        
        for _, row in n_data.iterrows():
            impl = row['Implementation']
            workers = int(row['Workers'])
            time_mean = row['mean']
            time_std = row['std']
            speedup = row['Speedup']
            efficiency = row['Efficiency']
            result = row['Result']
            
            print(f"{impl:<12} {workers:<8} {time_mean:>8.6f}±{time_std:.6f}  {speedup:>6.2f}x    {efficiency:>8.2f}%    {result:.10f}")
        
        # Best performers
        print(f"\n{'Best Configuration:':<20} ", end="")
        best = n_data.loc[n_data['Speedup'].idxmax()]
        print(f"{best['Implementation']} with {int(best['Workers'])} workers - {best['Speedup']:.2f}x speedup")
    
    # Generate output CSV for plotting
    output_file = csv_file.replace('.csv', '_summary.csv')
    summary.to_csv(output_file, index=False)
    print(f"\n{'='*80}")
    print(f"Summary saved to: {output_file}")
    print(f"{'='*80}\n")
    
    # Check for consistency
    print("\nCORRECTNESS VALIDATION:")
    print("─" * 40)
    for n in df['N'].unique():
        n_results = summary[summary['N'] == n]['Result'].values
        if len(set(n_results.round(8))) == 1:
            print(f"✓ N={n:>10,}: All implementations agree")
        else:
            print(f"✗ N={n:>10,}: Results differ!")
            for _, row in summary[summary['N'] == n].iterrows():
                print(f"  {row['Implementation']}-{int(row['Workers'])}: {row['Result']:.12f}")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python analyze_results.py <results_csv_file>")
        sys.exit(1)
    
    analyze_results(sys.argv[1])
