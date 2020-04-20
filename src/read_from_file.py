from os import listdir
def read(filename):
    log = []
    with open(filename, 'r') as f:
        for line in f.readlines():
            assert isinstance(line, str)
            log.append(line.split())
    return log
