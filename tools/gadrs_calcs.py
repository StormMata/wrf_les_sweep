#!/usr/bin/env python3
import numpy as np

D  = 178
dx = 4

width  = 0.5
length = 1.0

nElements = 36

nRings = min(np.round(0.5 * D / (width * dx)), nElements)

sections = 0
for m in range(int(nRings)):
    sections = sections + max(8, np.ceil(width * np.pi * (2 * (m + 1) - 1)/ length))

print(f'nRings : {nRings}')
print(f'nSections: {sections}')