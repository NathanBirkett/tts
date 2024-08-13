from collections import defaultdict
import re


f_in = open("vocab/in.txt", "r", encoding="utf8")

dict_map = dict()
for i, line in enumerate(f_in):
    term = line.split("` ")[0]
    definition = " (".join(line.split("` ")[1].split(" (")[:-1])
    tags = list(filter(str.isnumeric, line.split("` ")[1].split(" (")[-1][:-2].replace(";", ",").split(", ")))
    if (term not in dict_map):
        dict_map[term] = (definition, tags)
    else:
        dict_map[term] = (dict_map[term][0] + "; " + definition, dict_map[term][1] + tags)

f_out = open("vocab/out.txt", "w", encoding="utf8")
for term, tup in dict_map.items():
    f_out.write('"{}";"{}";{}\n'.format(term, tup[0], " ".join(set(tup[1]))))