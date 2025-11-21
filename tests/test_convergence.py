#!/usr/bin/env python3
"""Convergence test: verify error decreases as n increases for a smooth function.

This is a lightweight check that the trapezoidal implementation converges.
"""
import os
import math
import subprocess

ROOT = os.path.dirname(os.path.dirname(__file__))
BIN = os.path.join(ROOT, 'bin', 'serial')
if os.name == 'nt':
    BIN = BIN + '.exe'

def run_serial(a,b,n,func):
    proc = subprocess.run([BIN,str(a),str(b),str(n),str(func)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out = proc.stdout.decode()
    for line in out.splitlines():
        if 'result=' in line:
            try:
                val = float(line.split('result=')[1].split()[0])
                return val
            except Exception:
                pass
    return None

def test_convergence_sin():
    if not os.path.exists(BIN):
        raise RuntimeError('serial binary not found; build first')
    a, b = 0.0, math.pi
    exact = 2.0
    ns = [1000, 2000, 4000]
    errors = []
    for n in ns:
        val = run_serial(a,b,n,0)
        assert val is not None
        errors.append(abs(val - exact))
    # error should decrease when n increases
    assert errors[1] < errors[0]
    assert errors[2] < errors[1]
