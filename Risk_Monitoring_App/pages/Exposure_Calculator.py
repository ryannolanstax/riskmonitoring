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


st.title("Risk Exposure Calculator")

buffer = io.BytesIO()

filename = st.text_input("Filename (must include merchant name + deal id)", key="filename")


delayed = pd.read_csv('Risk_Monitoring_App/MCC & Business Models - MCC Ratings_Sales.csv')


MCC = st.number_input("MCC", key='MCC', value=1711)

testing = delayed.loc[delayed['MCC'] == MCC, ['CNP Delayed Delivery']].iloc[0, 0]

CNP_DD = delayed.loc[delayed['MCC'] == MCC, ['CNP Delayed Delivery']].iloc[0, 0]
CP_ACH_DD = delayed.loc[delayed['MCC'] == MCC, ['CP/ACH Delayed Delivery']].iloc[0, 0]

Annual_CNP_Volume = st.number_input("Annual CNP Volume ($)", key="Annual_CNP_Volume")
Annual_CP_ACH_Volume = st.number_input("Annual CP/ACH Volume ($)", key="Annual_CP_ACH_Volume")

Refund_Rate = st.number_input("Refund Rate (%)", value=3.0, key="Refund_Rate", step=0.1, format="%0.1f")
Refund_Days = st.number_input("Refund Days (#) #Default 30 ie. If official 90 day return policy for online sales, Use 90", value=30, key="Refund_Days")

Chargeback_Rate = st.number_input("'Chargeback Rate (%)", value=0.5, key="Chargeback_Rate", step=0.1, format="%0.1f")
Chargeback_Days = 180

my_expander = st.expander(label='Delayed Delivery Calcs')

with my_expander:
    data = {
        'Terms': ['Annual', 'Monthly', 'One-time', 'Arrears payment', 'Other', 'Other'],
        'DD': [15, 1, 0, 0, 0, 0],
        'Vol': [20, 80, 0, 0, 0, 0],
    }

    df_original = pd.DataFrame(data)
    edited_df = st.data_editor(df_original)

    def calculate_results(df):
        weighted_avg_DD = (df['DD'] * df['Vol']).sum() / df['Vol'].sum()
        volume = df['Vol'].sum()
        return weighted_avg_DD, volume

    if st.button("Calculate"):
        weighted_avg_DD, volume = calculate_results(edited_df)
        st.write('Calculated Results:')
        st.write(f'Weighted Average DD: {weighted_avg_DD}')
        st.write(f'Total Volume: {volume}')

#st.write(f'MCC Delayed_Delivery_Days: {CNP_DD}')
Delayed_Delivery = st.number_input("Delayed Delivery (DD)", key='Delayed_Delivery', value=CNP_DD)

#st.write(f'MCC ACH_Delayed_Delivery_Days: {CP_ACH_DD}')
ACH_Delayed_Delivery_Days = st.number_input("ACH_Delayed_Delivery_Days", key='ACH_Delayed_Delivery_Days', value=CP_ACH_DD)

ACH_Reject_Rate = st.number_input('ACH Reject (%)',min_value=0.0, max_value=100.0, key='ACH_Reject_Rate')
ACH_Reject_Days = st.number_input("ACH Reject Days (#)", key='ACH_Reject_Days', value=5)

Rolling_Reserve_Percent = st.number_input('Rolling Reserve Percent',min_value=0.0, max_value=100.0, key='Rolling_Reserve_Percent')
Rolling_Reserve_Days = st.number_input("Rolling Reserve Days", key='Rolling_Reserve_Days', min_value=0)

Minimium_Reserve = st.number_input("Minimium Reserve", key='Minimium_Reserve')
Capture_Rate = st.number_input('Capture Rate',min_value=0.0, max_value=100.0, key='Capture_Rate')

Flat_Reserve = st.number_input("Flat_Reserve", key='Flat_Reserve')

#Calculations Section Exposure
Refund_Risk = (Annual_CNP_Volume/365) * Refund_Rate * Refund_Days
Chargeback_Risk = (Annual_CNP_Volume/365) * Chargeback_Rate * Chargeback_Days
DD_Risk = (Annual_CNP_Volume/365) * Delayed_Delivery 

ACH_Reject_Exposure = ((Annual_CP_ACH_Volume/365)*ACH_Delayed_Delivery_Days) + ((Annual_CP_ACH_Volume/365)*ACH_Reject_Rate*ACH_Reject_Days)
Total_Exposure = Refund_Risk + Chargeback_Risk + DD_Risk + ACH_Reject_Exposure

Total_Volume = Annual_CNP_Volume + Annual_CP_ACH_Volume

Rolling_Reserve = ((Annual_CP_ACH_Volume + Annual_CP_ACH_Volume)/365) * Rolling_Reserve_Percent * Rolling_Reserve_Days

if (Annual_CP_ACH_Volume or Annual_CNP_Volume) and Total_Exposure:
    Full_Capture_Days = (Minimium_Reserve / ((Annual_CP_ACH_Volume + Annual_CNP_Volume)/365)) / Capture_Rate
    Full_Capture_Month = Full_Capture_Days / 30

    Total_Collateral = Rolling_Reserve + Minimium_Reserve + Flat_Reserve

    Exposure_Coverage = Total_Collateral / Total_Exposure
    Collateral_Coverage = Exposure_Coverage
 
    Exposure = pd.DataFrame({'Annual_CNP_Volume':[Annual_CNP_Volume],
                            'Annual_CP_ACH_Volume':[Annual_CP_ACH_Volume],
                            'Refund_Rate':[Refund_Rate],
                            'Refund_Days':[Refund_Days],
                            'Chargeback_Rate':[Chargeback_Rate],
                            'Chargeback_Days':[Chargeback_Days],
                            'Delayed_Delivery':[Delayed_Delivery], 
                            'ACH_Delayed_Delivery_Days':[ACH_Delayed_Delivery_Days],
                            'ACH_Reject_Rate':[ACH_Reject_Rate],
                            'ACH_Reject_Days':[ACH_Reject_Days],     
                            'Rolling_Reserve_Percent':[Rolling_Reserve_Percent],
                            'Rolling_Reserve_Days':[Rolling_Reserve_Days],
                            'Minimium_Reserve':[Minimium_Reserve],
                            'Capture_Rate':[Capture_Rate],
                            'Flat_Reserve':[Flat_Reserve],
                            'MCC':[MCC],
                            'CNP_DD':[CNP_DD],
                            'CP_ACH_DD':[CP_ACH_DD],
                            'Refund_Risk':[Refund_Risk],
                            'Chargeback_Risk':[Chargeback_Risk],
                            'DD_Risk':[DD_Risk],
                            'ACH_Reject_Exposure':[ACH_Reject_Exposure],
                            'Total_Exposure':[Total_Exposure],
                            'Total_Volume':[Total_Volume],
                            'Rolling_Reserve':[Rolling_Reserve],
                            'Full_Capture_Days':[Full_Capture_Days],
                            'Full_Capture_Month':[Full_Capture_Month],
                            'Total_Collateral':[Total_Collateral],
                            'Exposure_Coverage':[Exposure_Coverage],
                            'Collateral_Coverage':[Collateral_Coverage],
                                })

    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        Exposure.to_excel(writer, sheet_name='Exposure_Data')

        # Close the Pandas Excel writer and output the Excel file to the buffer
        writer.close()

        st.download_button(
            label="Download Excel worksheets",
            data=buffer,
            file_name=f"{st.session_state.filename}.xlsx",
            mime="application/vnd.ms-excel"
        )
