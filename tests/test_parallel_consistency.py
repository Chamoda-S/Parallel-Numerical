#!/usr/bin/env python3
"""Consistency tests: compare OpenMP and MPI outputs to serial (within tolerance).

These tests only run if the relevant binaries are present; they are minimal
sanity checks required by the assignment to show parallel versions match serial.
"""
import os
import subprocess
import math

ROOT = os.path.dirname(os.path.dirname(__file__))
BIN_SERIAL = os.path.join(ROOT, 'bin', 'serial')
BIN_OPENMP = os.path.join(ROOT, 'bin', 'openmp')
BIN_MPI = os.path.join(ROOT, 'bin', 'mpi')
if os.name == 'nt':
    BIN_SERIAL += '.exe'
    BIN_OPENMP += '.exe'
    BIN_MPI += '.exe'

def run(cmd):
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return proc.stdout.decode()

def parse_result(out):
    for line in out.splitlines():
        if 'result=' in line:
            try:
                return float(line.split('result=')[1].split()[0])
            except Exception:
                pass
    return None

def test_openmp_matches_serial():
    if not os.path.exists(BIN_OPENMP):
        return
    if not os.path.exists(BIN_SERIAL):
        raise RuntimeError('serial binary not found; build first')
    a, b, n, func = 0.0, 1.0, 200000, 0
    out_s = run([BIN_SERIAL, str(a), str(b), str(n), str(func)])
    out_o = run([BIN_OPENMP, str(a), str(b), str(n), str(func), '4'])
    v_s = parse_result(out_s)
    v_o = parse_result(out_o)
    assert v_s is not None and v_o is not None
    assert abs(v_s - v_o) < 1e-8

def test_mpi_matches_serial():
    if not os.path.exists(BIN_MPI):
        return
    if not os.path.exists(BIN_SERIAL):
        raise RuntimeError('serial binary not found; build first')
    a, b, n, func = 0.0, 1.0, 200000, 0
    out_s = run([BIN_SERIAL, str(a), str(b), str(n), str(func)])
    out_m = run(['mpirun','-np','2',BIN_MPI,str(a),str(b),str(n),str(func)])
    v_s = parse_result(out_s)
    v_m = parse_result(out_m)
    assert v_s is not None and v_m is not None
    assert abs(v_s - v_m) < 1e-8
