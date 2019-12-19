from scipy.stats import beta, ttest_ind
import numpy as np
import constants as c

#%%

def create_beta_priors(df):
    """
    calculates and returns dataframe with beta priors for each location
    df (pandas dataframe): dataframe with location_id, channel, variance, and expected columns
    """
    df['alpha'] = np.maximum((1 - df.expected) * np.power(df.expected, 2) / df.variance - df.expected, 0.1)
    df['beta'] = df.alpha / df.expected - df.alpha
    return df


def create_beta_posteriors(df):
    """
    creates posteriors from fpd stats and priors
    df (pandas dataframe): dataframe with alpha, beta, fpd, and num_matured columns
    """
    goods = df.num_matured - df.fpd
    df['alpha_p'] = df.alpha + df.fpd
    df['beta_p'] = df.beta + goods
    return df


def vectorize(func, excluded=None):
    return np.vectorize(func, excluded=excluded)


def beta_sf_wrapper(q, a, b):
    """
    wrapper function for beta.sf to not consider low fpd locations
    beta.sf is equivalent to "1 - beta.cdf"
    """
    if a / (a + b) < c.low_score:
        return c.low_score
    return beta.sf(q, a, b)


beta_sf = vectorize(beta_sf_wrapper)

beta_ppf = vectorize(beta.ppf, [0])


def beta_quantiles(df, p=c.alpha):
    """
    df (pandas dataframe): containing alpha, beta (priors) and alpha_p, beta_p (posteriors)
    p (float): float between 0 and 1 indicating significance level (prob of Type I error)
    """
    q_beta = beta_ppf(1 - p, df.alpha, df.beta)
    df['fpd_score'] = beta_sf(q_beta, df.alpha_p, df.beta_p)
    return df

#%%

def ttest(array1, array2):
    """
    returns 1 - Student's T-test (unequal variances)
    array1 (numpy array or pandas series): 1 dimensional array of treatment data
    array2 (numpy array or pandas series): 1 dimensional array of control data
    """
    diff = np.mean(array1) - np.mean(array2)
    if diff < c.cart_p60:
        return c.low_score
    if array1.size <= 1 or array2.size <= 1:
        return min(diff, c.single_item_cart_max)
    return 1 - ttest_ind(array1, array2, equal_var=False).pvalue
    # return diff

#%%
def round_scores(df, score_col):
    df[score_col] = np.round(df[score_col] * 100).astype(np.int16)
    return df