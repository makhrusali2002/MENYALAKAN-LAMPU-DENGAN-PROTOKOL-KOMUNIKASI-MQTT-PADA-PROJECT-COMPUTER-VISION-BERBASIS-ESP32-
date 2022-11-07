import json

#str(fingerVal[0]) + str(fingerVal[1]) + str(fingerVal[2]) + str(fingerVal[3]) + str(fingerVal[4])

# a Python object (dict):
x = {
    "jempol": fingerVal[0],
    "telunjuk": fingerVal[1],
    "tengah": fingerVal[2],
    "manis": fingerVal[3],
    "kelingking": fingerVal[4]
}

# convert into JSON:
y = json.dumps(x)

# the result is a JSON string:
print(y)