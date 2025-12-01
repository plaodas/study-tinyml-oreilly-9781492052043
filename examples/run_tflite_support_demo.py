"""Runnable demo that mirrors the notebook cells for quick verification.
This script prints Python and tensorflow_lite_support info, lists package layout,
and performs a small synthetic demo (no model file required).
"""
import sys
import os
import pkgutil

print('Python:', sys.version.splitlines()[0])

# Try importing tensorflow_lite_support
try:
    import tensorflow_lite_support as tls
    print('Imported tensorflow_lite_support ->', getattr(tls, '__name__', 'tensorflow_lite_support'))
    tls_path = tls.__path__[0]
    print('package path:', tls_path)
    print('\nTop-level entries:')
    for name in sorted(os.listdir(tls_path)):
        print('-', name)
    print('\nAvailable subpackages (first 40):')
    count = 0
    for mod in pkgutil.walk_packages([tls_path]):
        print('-', mod.name)
        count += 1
        if count >= 40:
            break
except Exception as e:
    print('Failed to import tensorflow_lite_support:', type(e).__name__, e)

# Basic numeric demo (safe)
try:
    import numpy as np
    X = np.linspace(0, 1, 10)
    y = (X * 2.0 + 0.1).astype(float)
    def normalize(arr):
        a = np.asarray(arr, dtype=float)
        mn, mx = a.min(), a.max()
        return a - mn if mx == mn else (a - mn) / (mx - mn)
    print('\nSample shapes:', X.shape, y.shape)
    print('normalized sample:', normalize(X)[:3])
    def predict_linear(x, slope=2.0, intercept=0.1):
        return x * slope + intercept
    pred = predict_linear(X)
    mse = float(((pred - y) ** 2).mean())
    print('MSE demo:', mse)
except Exception as e:
    print('Numeric demo failed:', type(e).__name__, e)

# Guarded metadata example
MODEL_PATH = './model.tflite'
print('\nMODEL_PATH:', MODEL_PATH)
if os.path.exists(MODEL_PATH):
    try:
        from tensorflow_lite_support.metadata import metadata as _metadata
        print('metadata module imported; you can use MetadataDisplayer APIs here.')
    except Exception as e:
        print('metadata import failed:', type(e).__name__, e)
else:
    print('No model found at', MODEL_PATH, '(skipping metadata demo)')

print('\nDemo finished')
