"""Convert the original Z-up scene to glTF Y-up, preserving skin/animation data."""
from pathlib import Path
import json, math, struct
source = Path('imported_publish_v02/tsurekun_dance_rig_v02.glb')
b = source.read_bytes()
length, kind = struct.unpack_from('<II', b, 12)
d = json.loads(b[20:20 + length])
assert d['scenes'][0]['nodes'] == [0]
assert not any(k in d['nodes'][0] for k in ('rotation', 'matrix', 'translation', 'scale'))
d['nodes'][0]['rotation'] = [-math.sqrt(0.5), 0, 0, math.sqrt(0.5)]
payload = json.dumps(d, separators=(',', ':')).encode()
payload += b' ' * (-len(payload) % 4)
rest = b[20 + length:]
out = struct.pack('<4sII', b'glTF', 2, 20 + len(payload) + len(rest)) + struct.pack('<II', len(payload), kind) + payload + rest
Path('docs/model.glb').write_bytes(out)
assert out[20 + len(payload):] == rest
print('Converted Z-up to Y-up; binary geometry, skin and animation buffers unchanged.')
