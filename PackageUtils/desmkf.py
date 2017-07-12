#!/usr/bin/env python
# -*- coding: utf-8 -*-  
import argparse
import struct
import os

def deMKF(f,postfix):
    mkf_name=os.path.basename(f.name)
    prefix=os.path.splitext(mkf_name)[0]
    f.seek(0,os.SEEK_END)
    total_length=f.tell()
    f.seek(0,os.SEEK_SET)
    first_index, = struct.unpack("<h",f.read(2))
    subfiles = first_index-1
    for i in range(0,subfiles):
        with open(prefix+str(i)+"."+postfix, 'wb') as subfile:
            f.seek(i*2,os.SEEK_SET)
            begin,end = struct.unpack("<hh",f.read(4))
            if end==0:
                end=total_length/2
            f.seek(begin*2,os.SEEK_SET)
            subfile.write(f.read(end*2-begin*2))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='sMKF unpack util')
    parser.add_argument('sMKF', type=argparse.FileType('rb'), action="store",
                       help='sMKF file to unpack')
    parser.add_argument('-p','--postfix', required=True,
                       help='postfix for unpacked files')

    args = parser.parse_args()
    deMKF(args.sMKF,args.postfix)