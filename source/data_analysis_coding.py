""" data_aadsasdafas.py                                           Harrison Cross
---|----1----|----2----|----3----|----4----|----5----|----6----|----7----|----8

"""

#------------------------------------------------------------------------------
#--- (0) Imports and directory locations
#------------------------------------------------------------------------------
ROOT = "/home/hcross27/BEE2041/Emperical_Project/Harrison-Cross---BEE2041-Emperical-Project-Repo/"

DATA_RAW = ROOT+'data/raw_data/'
DATA = ROOT+'data/clean_data/'
FIG  = ROOT+'results/figures/'
TAB  = ROOT+'results/tables/'

import pandas as pd
import numpy as np
import os

from econml.dml import CausalForestDML

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import GradientBoostingRegressor, GradientBoostingClassifier

import matplotlib.pyplot as plt
from pystout import pystout

from statsmodels.stats.outliers_influence import variance_inflation_factor
from statsmodels.iolib.table import SimpleTable
from statsmodels.stats.diagnostic import het_breuschpagan
from statsmodels.regression.linear_model import OLS
from statsmodels.tools import add_constant


os.makedirs(FIG, exist_ok=True)
os.makedirs(TAB, exist_ok=True)

#------------------------------------------------------------------------------
#--- (1) Load data and confirm contents
#------------------------------------------------------------------------------
filename = "Oreopoulos2011skilled.dta"  
df = pd.read_stata(DAT + filename)

y_var = 'callback'
D_var = 'canadian_name'
X_var = ['female', 'ba_quality', 'extracurricular_skills', 'language_skills',
         'ma', 'same_exp', 'exp_highquality', 'reference', 'accreditation',
         'legal']

# Ensure specified columns exist and have data
assert y_var in df.columns, "'callback' is not found in the data"
assert D_var in df.columns, "'canadian_name' not found in the data"

for column in X_var:
    assert column in df.columns, f"'{column}' is not found in the data"

Y = df[y_var]
D = df[D_var]
X = df[X_var]
Y=Y*100

#------------------------------------------------------------------------------
#--- (2) Examine heterogeneity in basic way
#------------------------------------------------------------------------------
# Linear Regression to evaluate treatment effect heterogeneity
X_with_D = pd.concat([pd.DataFrame(X), D], axis=1)
model_ols = OLS(Y, add_constant(X_with_D)).fit()
print(model_ols.summary())


# To add interaction terms and perform Breusch-Pagan test or similar, we are 
# going to do it manually. In this example, we are adding an interaction 
# between 'canadian_name' and 'female', and similar for BA quality.
X_with_D['canadian_name_female'] = X_with_D['female'] * X_with_D['canadian_name']
X_with_D['canadian_name_BA']     = X_with_D['ba_quality'] * X_with_D['canadian_name']
model_ols_interaction = OLS(Y, add_constant(X_with_D)).fit()
print(model_ols_interaction.summary())

#Now just define model specifications
spec1 = ['const']+[D_var]
spec2 = ['const']+X_var+[D_var]
spec3 = ['const']+[D_var] + ['female','canadian_name_female']
spec4 = ['const']+X_var + [D_var] + ['canadian_name_female']
spec5 = ['const']+[D_var] + ['ba_quality','canadian_name_BA']
spec6 = ['const']+X_var + [D_var] + ['canadian_name_BA']


#Estimate OLS
m1 =  OLS(Y, add_constant(D)).fit()
m2 =  OLS(Y, add_constant(X_with_D)[spec2]).fit()
m3 =  OLS(Y, add_constant(X_with_D)[spec3]).fit()
m4 =  OLS(Y, add_constant(X_with_D)[spec4]).fit()
m5 =  OLS(Y, add_constant(X_with_D)[spec5]).fit()
m6 =  OLS(Y, add_constant(X_with_D)[spec6]).fit()
m7 =  OLS(Y, add_constant(X_with_D)).fit()

#Export in tex format
yt = 'Callback' 
pystout(models=[m1, m2, m3, m4, m5, m6],
        file=TAB+'regressionTable.tex',
        addnotes=['All dependent variables are call back rates in percent.',
                  'Standard errors are presented in parentheses. *: p<0.10; **:p<0.05; ***:p<0.01.'],
        digits=2,
        endog_names=[yt,yt,yt,yt,yt,yt],
        varlabels={'const':'Constant',
                   'canadian_name':'Canadian Name',
                   'female':'Female',
                   'ba_quality':'BA Quality',
                   'extracurricular_skills':'Extracurriculars',
                   'language_skills':'Language Skills',
                   'ma':'Masters', 
                   'same_exp':'Same experience', 
                   'exp_highquality':'High quality experience', 
                   'reference': 'References', 
                   'accreditation': 'Accreditation',
                   'legal':'Legal Right',
                   'canadian_name_female':'Canadian Name $\\times$ Female',
                   'canadian_name_BA':'Canadian Name $\\times$ BA Quality'
                   },
        mgroups={'Baseline':[1,2],'Gender interaction':[3,4],'BA interaction':[5,6]},
        modstat={'nobs':'Obs','rsquared_adj':'Adj. R\sym{2}','fvalue':'F-stat'},
        stars =  {.1:'*',.05:'**',.01:'***'}
        )

# Breusch-Pagan test for heteroscedasticity
bp_test = het_breuschpagan(model_ols.resid, model_ols.model.exog)
print('Breusch-Pagan test:', bp_test)


#------------------------------------------------------------------------------
#--- (3) Estimate causal forest
#------------------------------------------------------------------------------
# Updating cf to use GradientBoostingClassifier for the treatment model
cf = CausalForestDML(
    model_y=GradientBoostingRegressor(),
    model_t=GradientBoostingClassifier(),  # Now using a classifier for the treatment
    discrete_treatment=True,
    random_state=121316
)

# Fitting the model
cf.fit(Y, D, X=X)
tau_hat    = cf.effect(X.values)
tau_hat_se = cf.effect_interval(X.values)



#------------------------------------------------------------------------------
#--- (4) Visualise causal forest results
#------------------------------------------------------------------------------
# Average Tregatment Effect (ATE)
cf.summary()

ate = np.mean(tau_hat)
print("ATE:", ate)

# Histogram of treatment effects
plt.hist(tau_hat, bins=30, color='lightblue', edgecolor='grey')
plt.axvline(x=ate, color='red', linestyle='--', label='ATE')
plt.xlabel('Treatment Effects')
plt.ylabel('Count')
plt.grid(True, linestyle='--', linewidth=0.5, alpha=0.5)
plt.legend()
plt.savefig(FIG+'treatmentCATEs.pdf')
plt.clf()

#Ordered effects along with 95% CI
effects = cf.effect(X.values).flatten()
CIs     = cf.effect_interval(X.values)[1]-effects
indices = np.argsort(effects)
effects_sorted = effects[indices]
ci_sorted = CIs[indices]

color_palette = ['#3380FF', '#FFC300']
plt.figure(figsize=(10, 6))
plt.errorbar(np.arange(len(effects)), effects_sorted, yerr=ci_sorted, 
             fmt='o', markersize=5, capsize=3, color=color_palette[0], 
             ecolor=color_palette[1], 
             alpha=0.3, elinewidth=0.01, capthick=0.01)
plt.xlabel('Data Point Index (Ordered by Effect Size)', fontsize=12)
plt.ylabel(r'$\Delta$ Callback Rate', fontsize=12)
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)
plt.grid(True, linestyle='--', linewidth=0.5, alpha=0.5)
plt.tight_layout()
plt.savefig(FIG+'orderedCATEs.pdf')
plt.clf()

#Let's just quickly see what these groups look like...
cf.cate_output_names(X.values)[indices]
cf.cate_output_names(X.values)[indices][0]


#------------------------------------------------------------------------------
#--- (5) Visualise heterogeneity by subgroups
#            Suppose we want to explore heterogeneity in the treatment effect, 
#            based on the level of education ('ba_quality' in this case).
#------------------------------------------------------------------------------

# Divide the dataset into subgroups based on 'ba_quality'.
high_ba_quality = X['ba_quality'] == 1
low_ba_quality = X['ba_quality'] == 0

# Calculate treatment effects for each group
effect_high_ba_quality = cf.effect(X[high_ba_quality].values)
effect_low_ba_quality = cf.effect(X[low_ba_quality].values)

# Compare average treatment effects
ate_high_ba_quality = np.mean(effect_high_ba_quality)
ate_low_ba_quality = np.mean(effect_low_ba_quality)

print(f"ATE for high BA quality: {ate_high_ba_quality}")
print(f"ATE for low BA quality: {ate_low_ba_quality}")

# Visualise the distribution of treatment effects in both groups
plt.figure(figsize=(6, 5))
plt.hist(effect_high_ba_quality, bins=30, alpha=0.5, label='High BA Quality')
plt.hist(effect_low_ba_quality, bins=30, alpha=0.5, label='Low BA Quality')
plt.legend()
plt.grid(True, linestyle='--', linewidth=0.5, alpha=0.5)
plt.xlabel('Treatment Effect')
plt.ylabel('Density')
plt.savefig(FIG+'CATEbyGroup.pdf')
plt.clf()

""""
#------------------------------------------------------------------------------
#--- (6) Which features are important in generating causal forest?
#        Commented out as a bit slow
#------------------------------------------------------------------------------
shap_values = cf.shap_values(X.values)
shap.summary_plot(shap_values['callback']['canadian_name_1.0'].values, 
                  features=X.values, 
                  feature_names=['Female', 'BA Quality', 'Extracurriculars', 
                                 'Language Skills', 'Masters', 
                                 'Same Experience', 'High Quality Exp', 
                                 'References', 'Accreditation','Legal'],
                 plot_type="bar", 
                  show=False)
plt.grid(True, linestyle='--', linewidth=0.5, alpha=0.5)
plt.savefig(FIG+'SHAPvalues.pdf')
plt.clf()
"""