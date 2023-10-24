

def row_col_config(root,rows=[],cols=[]):

    if isinstance(rows,dict):
        for row,row_weight in rows.items():
            root.rowconfigure(row,weight=row_weight)
    elif isinstance(rows,list):
        for row in rows:
            root.rowconfigure(row,weight=1)

    if isinstance(cols,dict):
        for col,col_weight in cols.items():
            root.columnconfigure(col,weight=col_weight)
    elif isinstance(cols,list):
        for col in cols:
            root.columnconfigure(col,weight=1)
