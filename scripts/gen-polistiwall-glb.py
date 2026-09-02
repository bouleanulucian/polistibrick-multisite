#!/usr/bin/env python3
"""Polistiwall Wall 200 — PSE grafit 120×340×20 cm + beton 20 cm."""
from __future__ import annotations

import json
import struct
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "shared" / "images" / "polistiwall"

C_PSE = (0.043, 0.043, 0.047)      # polistiren grafitat
C_BETON = (0.196, 0.193, 0.185)
C_CAVITY = (0.11, 0.10, 0.09)      # cavitate înainte de turnare

# Dimensiuni reale Wall 200 (metri)
W = 1.20    # 120 cm lățime
H = 3.40    # 340 cm înălțime
T_PSE = 0.20
T_BETON = 0.20


def tri(a, b, c):
    return [a, b, c]


def box(x0, y0, z0, x1, y1, z1):
    verts, tris = [], []
    faces = [
        ([(x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)], (0, 0, 1)),
        ([(x1, y0, z0), (x0, y0, z0), (x0, y1, z0), (x1, y1, z0)], (0, 0, -1)),
        ([(x0, y1, z0), (x1, y1, z0), (x1, y1, z1), (x0, y1, z1)], (0, 1, 0)),
        ([(x0, y0, z0), (x0, y0, z1), (x0, y1, z1), (x0, y1, z0)], (-1, 0, 0)),
        ([(x1, y0, z1), (x1, y0, z0), (x1, y1, z0), (x1, y1, z1)], (1, 0, 0)),
        ([(x0, y0, z0), (x1, y0, z0), (x1, y0, z1), (x0, y0, z1)], (0, -1, 0)),
    ]
    for quad, n in faces:
        base = len(verts) // 6
        for vx, vy, vz in quad:
            verts.extend([vx, vy, vz, n[0], n[1], n[2]])
        tris.extend(tri(base, base + 1, base + 2))
        tris.extend(tri(base, base + 2, base + 3))
    return verts, tris


def pse_panel(z0, z1):
    """Placă PSE grafit 120×340 cm (în picioare), 20 cm grosime."""
    verts, tris, idx = [], [], 0
    rows, gap = 17, 0.006
    dy = H / rows
    for r in range(rows):
        off = dy * 0.22 if r % 2 else 0
        y0 = -H / 2 + r * dy + gap
        y1 = y0 + dy - gap * 2
        x0 = -W / 2 + off + gap
        x1 = W / 2 - gap
        v, t = box(x0, y0, z0, x1, y1, z1)
        tris.extend([i + idx for i in t])
        verts.extend(v)
        idx += len(v) // 6
    return {"verts": verts, "tris": tris, "color": C_PSE, "name": "Polistiren grafitat"}


def build_cofraj():
    """Înainte de turnare: PSE 20 cm + cavitate beton 20 cm."""
    z_pse0 = -T_PSE - T_BETON / 2
    z_pse1 = -T_BETON / 2
    parts = [pse_panel(z_pse0, z_pse1)]
    v, t = box(-W / 2, -H / 2, -T_BETON / 2, W / 2, H / 2, T_BETON / 2)
    parts.append({"verts": v, "tris": t, "color": C_CAVITY, "name": "Cavitate beton"})
    return parts


def build_perete():
    """După turnare: PSE 20 cm + beton armat 20 cm."""
    z_pse0 = -T_PSE - T_BETON / 2
    z_pse1 = -T_BETON / 2
    parts = [pse_panel(z_pse0, z_pse1)]
    v, t = box(-W / 2, -H / 2, -T_BETON / 2, W / 2, H / 2, T_BETON / 2)
    parts.append({"verts": v, "tris": t, "color": C_BETON, "name": "Beton armat"})
    return parts


def export_glb(parts: list, path: Path, label: str):
    pos, nrm, indices = [], [], []
    materials = []
    idx_chunks = []

    for p in parts:
        base = len(pos) // 3
        for i in range(0, len(p["verts"]), 6):
            pos.extend(p["verts"][i : i + 3])
            nrm.extend(p["verts"][i + 3 : i + 6])
        chunk = [base + i for i in p["tris"]]
        idx_chunks.append(chunk)
        indices.extend(chunk)
        r, g, b = p["color"]
        materials.append({
            "name": p["name"],
            "pbrMetallicRoughness": {
                "baseColorFactor": [r, g, b, 1.0],
                "metallicFactor": 0.03,
                "roughnessFactor": 0.80,
            },
            "doubleSided": True,
        })

    pos_bytes = struct.pack(f"<{len(pos)}f", *pos)
    nrm_bytes = struct.pack(f"<{len(nrm)}f", *nrm)
    idx_parts = b"".join(struct.pack(f"<{len(c)}H", *c) for c in idx_chunks)
    buf = pos_bytes + nrm_bytes + idx_parts
    while len(buf) % 4:
        buf += b"\x00"

    accessors = [
        {"bufferView": 0, "componentType": 5126, "count": len(pos) // 3, "type": "VEC3",
         "max": [max(pos[0::3]), max(pos[1::3]), max(pos[2::3])],
         "min": [min(pos[0::3]), min(pos[1::3]), min(pos[2::3])]},
        {"bufferView": 1, "componentType": 5126, "count": len(nrm) // 3, "type": "VEC3"},
    ]
    buffer_views = [
        {"buffer": 0, "byteOffset": 0, "byteLength": len(pos_bytes), "target": 34962},
        {"buffer": 0, "byteOffset": len(pos_bytes), "byteLength": len(nrm_bytes), "target": 34962},
    ]
    off = len(pos_bytes) + len(nrm_bytes)
    prims = []
    for i, chunk in enumerate(idx_chunks):
        accessors.append({"bufferView": 2 + i, "componentType": 5123, "count": len(chunk), "type": "SCALAR"})
        buffer_views.append({"buffer": 0, "byteOffset": off, "byteLength": len(chunk) * 2, "target": 3493})
        prims.append({"attributes": {"POSITION": 0, "NORMAL": 1}, "indices": 2 + i, "material": i, "mode": 4})
        off += len(chunk) * 2

    gltf = {
        "asset": {"version": "2.0", "generator": "gen-polistiwall-glb.py"},
        "scene": 0,
        "scenes": [{"nodes": [0]}],
        "nodes": [{"mesh": 0, "name": label}],
        "meshes": [{"name": label, "primitives": prims}],
        "materials": materials,
        "accessors": accessors,
        "bufferViews": buffer_views,
        "buffers": [{"byteLength": len(buf)}],
    }

    json_bytes = json.dumps(gltf, separators=(",", ":")).encode("utf-8")
    json_bytes += b" " * ((4 - len(json_bytes) % 4) % 4)
    header = struct.pack("<III", 0x46546C67, 2, 12 + 8 + len(json_bytes) + 8 + len(buf))
    path.write_bytes(header + struct.pack("<II", len(json_bytes), 0x4E4F534A) + json_bytes
                     + struct.pack("<II", len(buf), 0x004E4942) + buf)
    print(f"✓ {path.name} — {W*100:.0f}×{H*100:.0f} cm, PSE {T_PSE*100:.0f} + beton {T_BETON*100:.0f} cm")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    export_glb(build_cofraj(), OUT / "polistiwall-cofraj-v2.glb", "PolistiWall-cofraj")
    export_glb(build_perete(), OUT / "polistiwall-perete-v2.glb", "PolistiWall-perete")


if __name__ == "__main__":
    main()
