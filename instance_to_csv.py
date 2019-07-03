
import csv

instanceName = 'pr02.txt'
textFile = open('./data/c-mdvrptw/txt/%s' % instanceName, 'r')



with open(instanceName.split(".")[0] + '.csv', 'w', newline='') as writeFile:
    writer = csv.writer(writeFile)
    firstRow = ['x', 'y']
    writer.writerow(firstRow)
    for lineCount, line in enumerate(textFile, start=1):
        if lineCount >= 6:
            values = line.strip().split()
            # newLine = values[0] + ',' + values[1] + ',' + values[2]
            newRow = [values[1], values[2]]
            writer.writerow(newRow)

textFile.close()
writeFile.close()