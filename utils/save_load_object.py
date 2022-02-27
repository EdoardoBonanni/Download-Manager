import pickle

def saveObject(obj, name):
    # save pickle object
    with open(name + ".pkl", "wb") as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def loadObject(name):
    # load pickle object
    with open(name + ".pkl", "rb") as f:
        obj = pickle.load(f)
        return obj