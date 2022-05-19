#!/usr/bin/python
# -*- coding: utf-8 -*-

import optparse, re

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

start_line = "2022年收益"

parser = optparse.OptionParser()
parser.add_option("-i", "--input", action="store",
                  type="string")
parser.add_option("-o", "--out", action="store",
                  type="string", default="./out.csv")
args = parser.parse_args()[0]

if args.input == None:
    print "input file is not set"

data_start = False
count = 0
out = open(args.out, "w")

lines = []

for line in open(args.input):
    line = line.strip()
    line = line.replace("％", "%")
    line = line.replace("－", "-")
    lines.append(line)

i = 0
while i < len(lines):
    line = lines[i]
    i += 1
    if line == None:
        continue
    if line.endswith(start_line):
        data_start = True
        out.write("管理人,产品名称,策略,近一周收益,2022年收益\n")
    elif data_start:
        if count == 0:
            if line == "沪深300" or line == "中证500" or line == "中证1000":
                out.write(","+line+",,"+lines[i]+","+lines[i+1]+"\n")
                i += 2
                continue
        if count == 3 or count == 4:
            if not line.endswith(r'%'):
                not_got = True
                for j in range(i, len(lines)):
                    if lines[j].endswith(r'%'):
                        out.write(lines[j] + ",")
                        lines[j] = None
                        i -= 1
                        not_got = False
                        break
                if not_got:
                    print line, "cannot be fixed"
                    break
            else:
                out.write(line+",")
        elif line.endswith(r'%'):
            print "line "+str(i), line, "is not right"
            break
        else:
            out.write(line+",")
        count += 1
        if count >= 5:
            out.write("\n")
            count = 0

out.close()
