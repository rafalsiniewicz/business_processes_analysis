def read(filename):
    log = []
    with open(filename, 'r') as f:
        for line in f.readlines():
            assert isinstance(line, str)
            log.append(tuple(line.split()))
    return log


print(read("logs.txt"))