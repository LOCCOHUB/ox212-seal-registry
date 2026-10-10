#!/usr/bin/env python3
"""Checks that every mirrored seal continues the one before: chain = sha256(prev_chain || root)."""
import glob, hashlib, json, sys

seals = sorted((json.load(open(f)) | {'file': f} for f in glob.glob('seals/**/ox212-seal-*.json', recursive=True)), key=lambda m: m['first_leaf'])
prev = None
for m in seals:
    chain = hashlib.sha256(bytes.fromhex(m['prev_chain']) + bytes.fromhex(m['root'])).hexdigest()
    if chain != m['chain']:
        sys.exit(f"{m['file']}: chain does not match its root")
    if prev and m['prev_chain'] != prev:
        sys.exit(f"{m['file']}: does not continue the previous seal")
    prev = m['chain']
print(f"{len(seals)} seals, one unbroken chain")
