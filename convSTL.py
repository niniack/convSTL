#!/usr/bin/env python3
# convSTL.py v1 - Python script to convert from binary to ascii .stl
# by Nishant Aswani @niniack

import argparse
import os
import numpy as np


HEADER_COUNT = 80

class convert:

    @classmethod
    def readType(cls, filename):
        print ("Determining STL File Type...")
        df = open(filename,'rb')
        header = df.read(80)
        df.close()

        if (header[0:5] == "solid"):
        	return("ascii")

        else:
        	return("binary")

    @classmethod
    def conv2ascii(cls, filename, **kwargs):

        # ASCII STL format (from Wikipedia):
        # solid name(optional)
            # [foreach triangle]
            # facet normal ni nj nk
            # outer loop
            # vertex v1x v1y v1z
            # vertex v2x v2y v2z
            # vertex v3x v3y v3z
            # endloop
            # endfacet
        # endsolid name(optional)

        print ("Converting to ASCII format...")

        dtObj = np.dtype([
        		('normals', np.float32, (3,)),
        		('vectors', np.float32, (3, 3)),
        		('attrs', np.uint16, (1,))
				])

        rf = open(filename,'rb')
        header = np.fromfile(rf, dtype=np.uint8, count=HEADER_COUNT)
        cls.numTriangles = np. fromfile(rf, dtype=np.uint32, count=1)
        cls.mesh = np.fromfile(rf, dtype=dtObj, count=-1)
        rf.close()

        if (kwargs.get('outfile',"default value")):
            outfile = str(kwargs.get('outfile',"default value")+".stl")
        else:
            outfile = "out.stl"

        wf = open(outfile,'w+')
        wf.write("solid\n")

        for i in range(int(cls.numTriangles)):

            wf.write(" face normal {} {} {}\n".format(str(cls.mesh['normals'][i][0]),
                                            str(cls.mesh['normals'][i][1]),
                                            str(cls.mesh['normals'][i][2])))
            wf.write("  outer loop\n")

            for j in range(3):
                wf.write("  vertex {} {} {}\n".format(str(cls.mesh['vectors'][i][j][0]),
                                                str(cls.mesh['vectors'][i][j][1]),
                                                str(cls.mesh['vectors'][i][j][2])))
            wf.write("  endloop\n")

            wf.write(" endfacet\n\n")

        wf.write("endsolid")


        wf.close()


def main():
    parser = argparse.ArgumentParser(description="QR Code Extractor")
    parser.add_argument("infile", help="The filename of the STL. e.g.: 'gimbal.stl' ")
    parser.add_argument("outfile", nargs='?',help="The name of the output file e.g.: 'profile'. It is unnecessary to add the .stl extension")
    args = parser.parse_args()

    if (not os.path.exists(args.infile)):
        print ("File", args.infile, "does not exist.")
        sys.exit(1)

    file = convert()
    type = file.readType(args.infile)

    if (type == "binary"):
        file.conv2ascii(args.infile, outfile=args.outfile)

    elif (type == "ascii"):
        print("ASCII to binary not yet implemented...")
        sys.exit(0)

    else:
        print("Error!")
        sys.exit(0)

    # origins = findCircumcenter(mesh.vectors, int(mesh.numTriangles))
    # plotNormals(origins, normals, int(mesh.numTriangles))

if __name__ == '__main__':
    main()
