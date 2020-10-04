from crossref.restful import Works
import json

works = Works()

record = works.doi("10.16995/dm.75")

with open("crossref-api.json", "w") as fd:
    json.dump(record, fd) 