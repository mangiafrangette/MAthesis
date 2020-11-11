import re

item = "French National Center for Academic Research (CNRS - Centre National de la Recherche Scientifique)."
aaa = []

print(re.split(r'[,|;|:|(|)]', item.lower()))

