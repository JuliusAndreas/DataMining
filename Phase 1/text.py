import csv

output=open('dataset.txt','w')

with open('PreprocessedDataset.csv',"rt") as f:
    for row in f:
        output.write(row)


output.close()