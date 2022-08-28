import pandas as pd

list_of_dfs = pd.read_html('https://dse.com.bd/latest_PE.php')
#print(list_of_dfs)
size = len(list_of_dfs)
print("DFS Size:",size)
position = size - 2
print("Position of the table in DFS:",position)
table = list_of_dfs[position]
table = table.fillna('')
print(table)
table.to_excel("latest_PE3.xlsx", index=False)