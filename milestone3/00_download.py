from pathlib import Path
import urllib.request, hashlib, json
ROOT=Path(__file__).resolve().parent
RAW=ROOT/'raw';RAW.mkdir(exist_ok=True)
expected=json.loads((ROOT/'source_manifest.json').read_text())
for name,meta in expected.items():
 target=RAW/name
 if not target.exists(): urllib.request.urlretrieve(meta['url'],target)
 actual=hashlib.sha256(target.read_bytes()).hexdigest()
 if actual!=meta['sha256']: raise RuntimeError(f'{name}: source changed since 2026-11-13; keep supplied cleaned sample for exact published figures or review/rebuild explicitly.')
 print(name,'verified')
