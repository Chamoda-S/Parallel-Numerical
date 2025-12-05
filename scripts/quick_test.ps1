# Quick Test Script - Verify all binaries work
# Run this first before the comprehensive test

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Quick Binary Verification Test" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

$a = 0
$b = 10
$n = 1000000
$func = 0

Write-Host "`nTesting Serial..." -ForegroundColor Yellow
if (Test-Path ".\bin\serial") {
    .\bin\serial $a $b $n $func
} else {
    Write-Host "  ✗ Serial binary not found!" -ForegroundColor Red
}

Write-Host "`nTesting OpenMP (4 threads)..." -ForegroundColor Yellow
if (Test-Path ".\bin\openmp") {
    .\bin\openmp $a $b $n $func 4
} else {
    Write-Host "  ✗ OpenMP binary not found!" -ForegroundColor Red
}

Write-Host "`nTesting MPI (2 processes)..." -ForegroundColor Yellow
if (Test-Path ".\bin\mpi") {
    mpiexec -n 2 .\bin\mpi $a $b $n $func
} else {
    Write-Host "  ✗ MPI binary not found!" -ForegroundColor Red
}

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "If all tests passed, run:" -ForegroundColor Green
Write-Host "  .\scripts\run_comprehensive_tests.ps1" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
