from os import listdir
def read(filename):
    log = []
    with open("../logs/" + filename, 'r') as f:
        for line in f.readlines():
            assert isinstance(line, str)
            log.append(tuple(line.split()))
    return log
