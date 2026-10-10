#!/usr/bin/env python3
"""Copies OX212's public seal registry into this repository. Manifests are written once and never overwritten
(their sha256 is checked against the registry first); proofs are refreshed until they reach Bitcoin."""
import hashlib, json, os, sys, urllib.request

REGISTRY = os.environ.get('REGISTRY', 'https://app-beta--ox212-ctrader-demo-20260820.netlify.app/api/public/seal')

def get(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'ox212-seal-mirror'}), timeout=30) as r:
        return r.read()

reg = json.loads(get(REGISTRY))
for s in sorted(reg['seals'], key=lambda x: x['id']):
    folder = os.path.join('seals', s['sealed_at'][:10].replace('-', '/'))
    os.makedirs(folder, exist_ok=True)
    base = os.path.join(folder, f"ox212-seal-{s['id']}.json")
    if not os.path.exists(base):
        manifest = get(s['manifest'])
        if hashlib.sha256(manifest).hexdigest() != s['manifest_sha256']:
            sys.exit(f"Seal {s['id']}: the manifest does not match its published sha256. Not mirrored.")
        open(base, 'wb').write(manifest)
    elif hashlib.sha256(open(base, 'rb').read()).hexdigest() != s['manifest_sha256']:
        sys.exit(f"Seal {s['id']}: the registry now shows a different manifest than the one mirrored here.")
    for i, p in enumerate(s['proofs']):
        path = base + ('.ots' if i == 0 else f".{chr(97 + i)}.ots")
        if p['status'] == 'bitcoin' and os.path.exists(path + '.final'):
            continue
        open(path, 'wb').write(get(p['ots']))
        if p['status'] == 'bitcoin':
            open(path + '.final', 'w').write(f"bitcoin block {p['bitcoin_block']}\n")
json.dump(reg, open('registry.json', 'w'), indent=2)
print(f"{len(reg['seals'])} seals mirrored")
