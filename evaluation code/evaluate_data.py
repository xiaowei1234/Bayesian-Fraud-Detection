import sys
import pandas as pd
import eval_constants as c
sys.path.append('../code/')


from cart_analysis import main_cart_pipes
from fpd_analysis import main_fpd_pipes


def merge_carts(cart_raw):
    cart_df = main_cart_pipes(cart_raw)
    return cart_raw[['location_id', 'mp60', 'pull', 'cnt', 'approval_amount']].drop_duplicates('location_id').merge(cart_df, on='location_id', how='inner')


def make_each_set_metrics(csv_path, func):
    df = pd.read_csv(csv_path)
    pulls = df.pull.unique()
    lst = []
    for pull in pulls:
        lst.append(func(df.loc[df.pull==pull, :]))
    return pd.concat(lst, ignore_index=True)


#%%
if __name__ == '__main__':
    fpd_df = make_each_set_metrics(c.fpd_sql_data, main_fpd_pipes)
    fpd_df.to_csv(c.eval_fpd_output, index=False)
    cart_df = make_each_set_metrics(c.cart_sql_data, merge_carts)
    cart_df.to_csv(c.eval_cart_output, index=False)
