# -*- coding: utf-8 -*-
"""
Created on Wed Nov 23 20:51:18 2016

@author: rek
"""

import pandas as pd
import numpy as np

filename = 'Medicare_Physician_and_Other_Supplier_NPI_Aggregate_CY2014.txt'
data = pd.read_csv(filename,sep='\t')
dataI = data[data.nppes_entity_code=='I']


# 1.1) Find provider with highest total_medicare_payment_amount
    # Note: Since all rows have unique npi, we know that each provider is listed just once
maxTMPA = dataI[dataI.total_medicare_payment_amt==max(dataI.total_medicare_payment_amt)]
maxTMPA.transpose()     # display relevant data about this provider

# 1.2) 
providertypeCounts = dataI.groupby('provider_type').size()
provtypes100 = providertypeCounts[providertypeCounts>=100]
# len(provtypes100.index)  # 74
dataI_PT = dataI[dataI['provider_type'].isin(provtypes100.index)] # retain only PT>=100
TMPA_gPT = dataI_PT.groupby('provider_type')['total_medicare_payment_amt']
median_TMPA = TMPA_gPT.median().sort_values(ascending=False)
    # this gives the full list of median payments by specialty, sorted from high to low

# 1.3)
def median_PT_top10(inData,subsetField,inString,valueField):
    # function computes median of top ten valueField entries for given subset
    data_PT = inData[inData[subsetField]==inString][valueField].sort_values(ascending=False)
    return (0.5*sum(data_PT.iloc[4:6]))
uniq_PT = pd.Series(provtypes100.index,index=provtypes100.index)
medoftop10_PT = uniq_PT.apply(lambda x: 
                median_PT_top10(dataI_PT,'provider_type',x,'total_medicare_payment_amt'))
medoftop10_PT = medoftop10_PT.sort_values(ascending=False)
