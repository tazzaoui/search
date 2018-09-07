#!/usr/bin/env python

import os
import base64

input_files = os.path.abspath("docs")
output_dir = os.path.abspath("raw")
os.system("rm -rf raw; mkdir raw")

for input_file in os.listdir(input_files):
    with open(os.path.join(input_files, input_file), "rb") as f:
        lines = f.readlines()
        for i in range(len(lines)):
            line = lines[i].decode("latin-1")
            if line[0] == "<" and line[1] != "/":
                title_index = line.find("title=\"") + 7
                end_of_title_index = line.find("\"", title_index)
                title = lines[i][title_index:end_of_title_index]
                if title == b"":
                    continue
                i += 1
                line = lines[i].decode("latin-1")
                try:
                    output = open(
                        os.path.join(
                            output_dir,
                            base64.b16encode(title).decode()),
                        "w")
                except OSError:
                    print("TOO LONG!!!")
                    continue
                output.write("Title: {}\n".format(title.decode("latin-1")))
                while line.strip() != "ENDOFARTICLE.":
                    output.write(line)
                    i += 1
                    if i >= len(lines) - 1:
                        break
                    line = lines[i].decode("latin-1")
                output.close()
