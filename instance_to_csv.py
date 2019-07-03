
import csv
textFile = open('./data/c-mdvrptw/pr01', 'r')

with open('pr01_2.csv', 'w', newline='') as writeFile:
    writer = csv.writer(writeFile)
    for lineCount, line in enumerate(textFile, start=1):
        if lineCount >= 6:
            values = line.strip().split()
            # newLine = values[0] + ',' + values[1] + ',' + values[2]
            newRow = [values[1], values[2]]
            writer.writerow(newRow)

textFile.close()
writeFile.close()