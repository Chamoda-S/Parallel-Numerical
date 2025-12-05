# Comprehensive Performance Testing Script
# This script runs all implementations with consistent parameters and saves results

# Test parameters
$a = 0
$b = 10
$func = 0  # sin(x)
$n_values = @(1000000, 10000000, 50000000)  # Different problem sizes
$repeats = 3

# Create outputs directory if it doesn't exist
$outputDir = "outputs"
if (-not (Test-Path $outputDir)) {
    New-Item -ItemType Directory -Path $outputDir | Out-Null
}

# Results file
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$resultsFile = "$outputDir\comprehensive_results_$timestamp.csv"

# Initialize CSV
"Implementation,Workers,N,Run,Time_s,Result" | Out-File -FilePath $resultsFile -Encoding UTF8

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Comprehensive Performance Testing" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Test Parameters:"
Write-Host "  Interval: [$a, $b]"
Write-Host "  Function: $func (sin(x))"
Write-Host "  N values: $($n_values -join ', ')"
Write-Host "  Repeats per config: $repeats"
Write-Host ""

foreach ($n in $n_values) {
    Write-Host "----------------------------------------" -ForegroundColor Yellow
    Write-Host "Testing with N = $n" -ForegroundColor Yellow
    Write-Host "----------------------------------------" -ForegroundColor Yellow
    
    # SERIAL
    Write-Host "`n[SERIAL]" -ForegroundColor Green
    for ($i = 1; $i -le $repeats; $i++) {
        Write-Host "  Run $i/$repeats..." -NoNewline
        $output = & ".\bin\serial" $a $b $n $func 2>&1 | Out-String
        Write-Host " Done"
        
        # Parse output
        if ($output -match "result=([\d.]+)\s+time=([\d.]+)") {
            $result = $matches[1]
            $time = $matches[2]
            "Serial,1,$n,$i,$time,$result" | Out-File -FilePath $resultsFile -Append -Encoding UTF8
            Write-Host "    Result: $result, Time: ${time}s" -ForegroundColor Gray
        }
    }
    
    # OPENMP with different thread counts
    $thread_counts = @(1, 2, 4, 8)
    foreach ($threads in $thread_counts) {
        Write-Host "`n[OPENMP - $threads threads]" -ForegroundColor Green
        for ($i = 1; $i -le $repeats; $i++) {
            Write-Host "  Run $i/$repeats..." -NoNewline
            $output = & ".\bin\openmp" $a $b $n $func $threads 2>&1 | Out-String
            Write-Host " Done"
            
            if ($output -match "result=([\d.]+)\s+time=([\d.]+)") {
                $result = $matches[1]
                $time = $matches[2]
                "OpenMP,$threads,$n,$i,$time,$result" | Out-File -FilePath $resultsFile -Append -Encoding UTF8
                Write-Host "    Result: $result, Time: ${time}s" -ForegroundColor Gray
            }
        }
    }
    
    # MPI with different process counts
    $process_counts = @(2, 4, 8)
    foreach ($procs in $process_counts) {
        Write-Host "`n[MPI - $procs processes]" -ForegroundColor Green
        for ($i = 1; $i -le $repeats; $i++) {
            Write-Host "  Run $i/$repeats..." -NoNewline
            $output = mpiexec -n $procs ".\bin\mpi" $a $b $n $func 2>&1 | Out-String
            Write-Host " Done"
            
            if ($output -match "result=([\d.]+)\s+time=([\d.]+)") {
                $result = $matches[1]
                $time = $matches[2]
                "MPI,$procs,$n,$i,$time,$result" | Out-File -FilePath $resultsFile -Append -Encoding UTF8
                Write-Host "    Result: $result, Time: ${time}s" -ForegroundColor Gray
            }
        }
    }
}

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "Testing Complete!" -ForegroundColor Cyan
Write-Host "Results saved to: $resultsFile" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

# Generate summary
Write-Host "`nGenerating summary..." -ForegroundColor Yellow
python scripts\analyze_results.py $resultsFile
