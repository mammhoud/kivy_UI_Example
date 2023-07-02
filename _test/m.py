
import pandas as pd
    
r1=['b','c','d','c','d']
    
df=pd.DataFrame(r1,columns=['c'])
    
print(df)
print(df.c.apply(lambda x: pd.value_counts(x.split( ))).sum(axis = 0))
