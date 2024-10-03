import sys
from collections import OrderedDict


class MapReduce:
    def __init__(self):
        self.intermediate = OrderedDict()
        self.result = []

    def emitIntermediate(self, key, value):
        self.intermediate.setdefault(key, [])
        self.intermediate[key].append(value)

    def emit(self, value):
        self.result.append(value)

    def execute(self, data, mapper, reducer):
        for record in data:
            mapper(record)

        for key in self.intermediate:
            reducer(key, self.intermediate[key])

        self.result.sort()
        for item in self.result:
            print(item)


mapReducer = MapReduce()


def mapper(record):
    record = record.split(",")
    # Removing '\n' for the last word in the line
    record[-1] = record[-1][:-1]
    if record[0] == "Department":
        ssn = record.pop(1)
    else:
        ssn = record.pop(2)
    mapReducer.emitIntermediate(key=ssn, value=record)


def reducer(key, list_of_values):
    for i, l in enumerate(list_of_values):
        if l[0] == "Employee":
            employee_name = l[1]
            break
    employee_name = list_of_values.pop(i)[1]
    for l in list_of_values:
        mapReducer.emit((key, employee_name, l[1]))


if __name__ == "__main__":
    inputData = []
    for line in sys.stdin:
        inputData.append(line)
        mapReducer.execute(inputData, mapper, reducer)
