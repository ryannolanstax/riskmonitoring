import altair as alt
import pandas as pd
import seaborn as sns
import streamlit as st
import streamlit.components.v1 as components
import base64
import json
import numpy as np
import datetime
from datetime import date, timedelta
import io
import matplotlib.pyplot as plt  

st.set_page_config(page_title="Underwriting Calculator", page_icon="💾", layout="wide")

st.title("Risk Tiering Calculator")

filename = st.text_input("Filename (must include merchant name + deal id)", key="filename")

buffer = io.BytesIO()

#Tiering Calc Fields

BankHistory = st.selectbox(
    'What is the customers business processing and banking history?',
    (['Merchant refuses to provide current bank statements OR merchants current bank statements show negative balances and recent NSFs',\
      'Merchant provided current bank statements that show no negative balances or NSFs; however, the average balances would not cover the high ticket and/or volumes would not support 50% or more of the exposure amount',\
        'Merchant provided current bank statements that cover approved high ticket and at least 50% of exposure amount OR bank statements were not requested as part of this review',\
            'Merchant provided current bank statements that cover 2x approved high ticket and at least 60% of exposure amount',\
                'Merchant provided current bank statements that cover at least 3x approved high ticket and entirety of exposure amount']))

MCCRisk = st.radio('What is the risk level associated with the MCC??', options=['5', '4', '3', '2', '1'], 
          horizontal=True)

SignerCreditScore = st.radio('How old is the business?', options=['<550','551-579 or Unknown', '580-650', '651-750', '751-850'], 
          horizontal=True)

AvgReview = st.radio('What is the business average review score across all review platforms? ', options=['< 4.0 Stars', '> 4.0 Stars – 4.3 Stars', '> 4.3 Stars to 4.5 Stars OR less than 20 reviews across all review sites', \
      '> 4.5 Stars to 4.8 Stars', '> 4.8 Stars'], 
          horizontal=True)

ChargeRefundACH = st.selectbox(
    'What is the merchants chargeback, refund, or ACH reversal rates?',
    (['Merchants chargeback rate over the last 180 days is 2% or higher OR merchants refund rate in the last 90 days is 10% or higher OR merchants ACH reversal rate in the last 30 days is 0.5% or higher where the majority of codes are R05, R07, R08, R10, R29, R51 or 15% or higher where the majority of codes are not previously listed.',\
      'Merchants chargeback rate over the last 180 days is at least 1%, but lower than 2% OR merchants refund rate in the last 90 days is at least 7.5%, but lower than 10% OR merchants ACH reversal rate in the last 30 days is 0.4% where the majority of codes are R05, R07, R08, R10, R29, R51 or at least 10%, but lower than 15% where the majority of codes are not previously listed.',\
      'Merchants chargeback rate over the last 180 days is at least 0.75%, but lower than 1% OR merchants refund rate in the last 90 days is at least 5%, but lower than 7.5% OR merchants ACH reversal rate in the last 30 days is 0.3% where the majority of codes are R05, R07, R08, R10, R29, R51 or at least 7.5%, but lower than 10% where the majority of codes are not previously listed.',\
      'Merchants chargeback rate over the last 180 days is at least 0.05%, but lower than 0.75% OR merchants refund rate in the last 90 days is at least 3%, but lower than 5% OR merchants ACH reversal rate in the last 30 days is 0.2% where the majority of codes are R05, R07, R08, R10, R29, R51 or at least 5%, but lower than 7.5% where the majority of codes are not previously listed.',\
      'Merchants chargeback rate over the last 180 days is less than 0.05% OR merchants refund rate in the last 90 days is less than 3% OR merchants ACH reversal rate in the last 30 days is less than 0.2% where the majority of codes are R05, R07, R08, R10, R29, R51 or less than 5% where the majority of codes are not previously listed.' ]))


if BankHistory == 'Merchant refuses to provide current bank statements OR merchants current bank statements show negative balances and recent NSFs' or MCCRisk == '5' or SignerCreditScore == '<550' or AvgReview == '< 4.0 Stars' or ChargeRefundACH == 'Merchants chargeback rate over the last 180 days is 2% or higher OR merchants refund rate in the last 90 days is 10% or higher OR merchants ACH reversal rate in the last 30 days is 0.5% or higher where the majority of codes are R05, R07, R08, R10, R29, R51 or 15% or higher where the majority of codes are not previously listed.':
    final_score = 5
elif BankHistory == 'Merchant provided current bank statements that show no negative balances or NSFs; however, the average balances would not cover the high ticket and/or volumes would not support 50% or more of the exposure amount' or MCCRisk == '4' or SignerCreditScore == '551-579 or Unknown' or AvgReview == '> 4.0 Stars – 4.3 Stars' or ChargeRefundACH == 'Merchants chargeback rate over the last 180 days is at least 1%, but lower than 2% OR merchants refund rate in the last 90 days is at least 7.5%, but lower than 10% OR merchants ACH reversal rate in the last 30 days is 0.4% where the majority of codes are R05, R07, R08, R10, R29, R51 or at least 10%, but lower than 15% where the majority of codes are not previously listed.':
    final_score = 4
elif BankHistory == 'Merchant provided current bank statements that cover approved high ticket and at least 50% of exposure amount OR bank statements were not requested as part of this review' or MCCRisk == '3' or SignerCreditScore == '580-650' or AvgReview == '> 4.3 Stars to 4.5 Stars OR less than 20 reviews across all review sites' or ChargeRefundACH == 'Merchants chargeback rate over the last 180 days is at least 0.75%, but lower than 1% OR merchants refund rate in the last 90 days is at least 5%, but lower than 7.5% OR merchants ACH reversal rate in the last 30 days is 0.3% where the majority of codes are R05, R07, R08, R10, R29, R51 or at least 7.5%, but lower than 10% where the majority of codes are not previously listed.':
    final_score = 3
elif BankHistory == 'Merchant provided current bank statements that cover 2x approved high ticket and at least 60% of exposure amount' or MCCRisk == '2' or SignerCreditScore == '651-750' or AvgReview == '> 4.5 Stars to 4.8 Stars' or ChargeRefundACH == 'Merchants chargeback rate over the last 180 days is at least 0.05%, but lower than 0.75% OR merchants refund rate in the last 90 days is at least 3%, but lower than 5% OR merchants ACH reversal rate in the last 30 days is 0.2% where the majority of codes are R05, R07, R08, R10, R29, R51 or at least 5%, but lower than 7.5% where the majority of codes are not previously listed.':
    final_score = 2
elif BankHistory == 'Merchant provided current bank statements that cover at least 3x approved high ticket and entirety of exposure amount' or MCCRisk == '1' or SignerCreditScore == '751-850' or AvgReview == '> 4.8 Stars' or ChargeRefundACH == 'Merchants chargeback rate over the last 180 days is less than 0.05% OR merchants refund rate in the last 90 days is less than 3% OR merchants ACH reversal rate in the last 30 days is less than 0.2% where the majority of codes are R05, R07, R08, R10, R29, R51 or less than 5% where the majority of codes are not previously listed.':
    final_score = 1


Tiering = pd.DataFrame({'FinalTier': [final_score],
                        'BankHistory':[BankHistory],
                        'MCCRisk':[MCCRisk],
                        'SignerCreditScore':[SignerCreditScore], 
                        'AvgReview':[AvgReview],
                        'ChargeRefundACH':[ChargeRefundACH],
                            })

st.write('The Final Tier of the Customer is: ', final_score)

#Exposure Calc Fields
#flow of this app sucks







with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
    Tiering.to_excel(writer, sheet_name='Tier_Data')

        # Close the Pandas Excel writer and output the Excel file to the buffer
    writer.close()

    st.download_button(
        label="Download Excel worksheets",
        data=buffer,
        file_name=f"{st.session_state.filename}.xlsx",
        mime="application/vnd.ms-excel"
    )

#ACH Reject (%) / Rolling Reserve Percent needs to go down level
#Capture Rate need to go up 1 decimal places