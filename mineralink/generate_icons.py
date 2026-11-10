#!/usr/bin/env python3
"""Generate small PNG PWA icons for the public deployment, no additional dependencies."""
import struct
import sys
import zlib
from pathlib import Path

def distance(px,py,ax,ay,bx,by):
    dx,dy=bx-ax,by-ay
    t=max(0.,min(1.,((px-ax)*dx+(py-ay)*dy)/(dx*dx+dy*dy)))
    return ((px-ax-t*dx)**2+(py-ay-t*dy)**2)**.5

def build(size,path):
    points=[(107,316),(211,155),(257,231),(305,160),(407,316)]
    rows=[]
    for y in range(size):
        row=bytearray([0])
        for x in range(size):
            px,py=(x+.5)*512/size,(y+.5)*512/size
            rgb=(18,53,60)
            if min(distance(px,py,*points[i],*points[i+1]) for i in range(4)) < 17:
                rgb=(240,191,106)
            if distance(px,py,112,372,400,372) < 11:
                rgb=(255,255,255)
            if (px-256)**2+(py-311)**2<29**2:
                rgb=(240,191,106)
            row.extend(rgb)
        rows.append(bytes(row))
    raw=b''.join(rows)
    def chunk(tag,data):return struct.pack('>I',len(data))+tag+data+struct.pack('>I',zlib.crc32(tag+data)&0xffffffff)
    png=b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',struct.pack('>2I5B',size,size,8,2,0,0,0))+chunk(b'IDAT',zlib.compress(raw,9))+chunk(b'IEND',b'')
    Path(path).write_bytes(png)

if __name__=='__main__':
    root=Path(sys.argv[1]) if len(sys.argv)>1 else Path('assets')
    root.mkdir(parents=True,exist_ok=True)
    for size in [192,512]:
        build(size,root/f'icon-{size}.png')
