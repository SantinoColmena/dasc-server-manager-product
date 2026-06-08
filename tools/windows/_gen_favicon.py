"""Script temporal: genera web/favicon.ico a partir del logo Vigex (sin deps externas)."""
import struct, zlib, math, pathlib

def lerp_i(a, b, t): return int(a + (b - a) * t)

def hex2rgb(h):
    h = h.lstrip('#')
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)

def dist_pt_seg(px, py, ax, ay, bx, by):
    dx, dy = bx - ax, by - ay
    l2 = dx * dx + dy * dy
    if l2 < 1e-10:
        return math.hypot(px - ax, py - ay)
    t = max(0.0, min(1.0, ((px - ax) * dx + (py - ay) * dy) / l2))
    return math.hypot(px - (ax + t * dx), py - (ay + t * dy))

def render(size):
    s = size / 64.0
    rx   = 14.0 * s
    sw   = 3.5  * s
    dotr = 4.5  * s
    c1  = hex2rgb('#6366f1');  c2  = hex2rgb('#3730a3')
    dc1 = hex2rgb('#c7d2fe');  dc2 = hex2rgb('#818cf8')
    vx = [15 * s, 32 * s, 49 * s]
    vy = [16 * s, 46 * s, 16 * s]
    out = []
    for y in range(size):
        for x in range(size):
            fx, fy = x + 0.5, y + 0.5
            masked = False
            if   fx < rx        and fy < rx        and math.hypot(fx - rx,          fy - rx)          > rx: masked = True
            elif fx > size - rx and fy < rx        and math.hypot(fx - (size - rx), fy - rx)          > rx: masked = True
            elif fx < rx        and fy > size - rx and math.hypot(fx - rx,          fy - (size - rx)) > rx: masked = True
            elif fx > size - rx and fy > size - rx and math.hypot(fx - (size - rx), fy - (size - rx)) > rx: masked = True
            if masked:
                out.append((0, 0, 0, 0))
                continue
            t  = (fx + fy) / (2.0 * size)
            r  = lerp_i(c1[0], c2[0], t)
            g  = lerp_i(c1[1], c2[1], t)
            b  = lerp_i(c1[2], c2[2], t)
            dd = math.hypot(fx - vx[1], fy - vy[1])
            if dd < dotr:
                dt = dd / dotr
                out.append((lerp_i(dc1[0], dc2[0], dt), lerp_i(dc1[1], dc2[1], dt), lerp_i(dc1[2], dc2[2], dt), 255))
                continue
            d1 = dist_pt_seg(fx, fy, vx[0], vy[0], vx[1], vy[1])
            d2 = dist_pt_seg(fx, fy, vx[1], vy[1], vx[2], vy[2])
            if min(d1, d2) < sw:
                out.append((255, 255, 255, 255))
                continue
            out.append((r, g, b, 255))
    return out

def make_png(size, pix):
    def chunk(tag, data):
        c = zlib.crc32(tag + data) & 0xffffffff
        return struct.pack('>I', len(data)) + tag + data + struct.pack('>I', c)
    raw = b''
    for y in range(size):
        raw += b'\x00'
        for x in range(size):
            rr, gg, bb, aa = pix[y * size + x]
            raw += bytes([rr, gg, bb, aa])
    ihdr = struct.pack('>IIBBBBB', size, size, 8, 6, 0, 0, 0)
    return (b'\x89PNG\r\n\x1a\n'
            + chunk(b'IHDR', ihdr)
            + chunk(b'IDAT', zlib.compress(raw, 9))
            + chunk(b'IEND', b''))

sizes = [48, 32, 16]
pngs  = [make_png(s, render(s)) for s in sizes]

ico  = struct.pack('<HHH', 0, 1, len(sizes))
off  = 6 + 16 * len(sizes)
for sz, p in zip(sizes, pngs):
    ico += struct.pack('<BBBBHHII', sz, sz, 0, 0, 1, 32, len(p), off)
    off += len(p)
for p in pngs:
    ico += p

dest = pathlib.Path(__file__).parent.parent.parent / 'web' / 'favicon.ico'
dest.write_bytes(ico)
print(f'Generado: {dest}  ({len(ico):,} bytes, tamaños={sizes})')
