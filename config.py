import json
import os

def byteify(input):
    if isinstance(input, dict):
        return {byteify(key): byteify(value)
                for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [byteify(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input

class Config:
    def __init__(self, json_path):
        self.load(json_path)

    def load(self, json_path):
        with open(json_path, 'r') as f:
            self.__json = byteify(json.load(f))
             	
            for k,v in self.__json.items():
                if k == "CLASS_TO_IDX":
                    setattr(self, k, v)
                    self.IDX_TO_CLASS = {}
                    for k1, v1 in v.items():
                        self.IDX_TO_CLASS[k1] = {v2:k2 for k2, v2 in v1.items()}
                elif k == "MIN_AREA":
                    d = {}
                    for k1, v1 in v.items():
                        d_temp = {}
                        for k2,v2 in v1.items():
                            d_temp[int(k2)] = v2
                        d[k1] = d_temp
                    self.MIN_AREA = d
                elif k == "IMG_SIZE_TRAIN":
                    self.IMG_SIZE_TRAIN = (v["width"], v["height"])
                else:
                    setattr(self, k, v)
        print(self.CLASS_TO_IDX)

    def dump(self, path):
        with open(os.path.join(path, "config.json"), 'w') as f:
            json.dump(self.__json, f, sort_keys = True, indent = 4, ensure_ascii = False)