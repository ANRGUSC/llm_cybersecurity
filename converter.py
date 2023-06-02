import sys
import pandas as pd

def converter(row, colnames):
    a = ""
    for i in range(len(row)):
        a += str(colnames[i]) + ":" + str(row[i])
        if i != len(row)-1:
            a += " - "
    
    return a
    
fname = sys.argv[1]

df = pd.read_csv(fname)
colnames = df.columns.values.tolist() 
print("Converting to strings...")
df2 = df.apply((lambda x: converter(x,colnames)), axis=1)
print(df2)
print("Writing results to result.csv")
df2.to_csv("result.csv")