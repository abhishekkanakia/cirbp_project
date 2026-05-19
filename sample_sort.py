import pandas as pd

df = pd.read_excel('data_sources_original/CIRBP complete expression.xlsx')

df_normal = df[df['REGULATION'] == 'normal']
df_under = df[df['REGULATION'] == 'under']
df_over = df[df['REGULATION'] == 'over']

df_normal.to_excel('CIRBP_normal.xlsx', index=False)
df_under.to_excel('CIRBP_under.xlsx', index=False)
df_over.to_excel('CIRBP_over.xlsx', index=False)
