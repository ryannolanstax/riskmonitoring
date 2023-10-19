import streamlit as st
import pandas as pd
import numpy as np
import io
import datetime
import xlsxwriter
from datetime import date, timedelta

uploaded_files = st.file_uploader("Upload CSV", type="csv", accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        file.seek(0)
    uploaded_data_read = [pd.read_csv(file) for file in uploaded_files]
    dfpreclean = pd.concat(uploaded_data_read)

    buffer = io.BytesIO()

    dfpreclean2 = dfpreclean.loc[:,['Return Date', 'Original Date', 'Attempted Funds Transfer Date',
       'Sub Merchant Business Name', 'Funding Sub Merchant ID', 'Funds Transfer Request ID', 
       'Funds Transfer Amount', 'Reason Code', 'Reason Message',
       ]]
    
    dda = dfpreclean.loc[:,['Routing Number', 'Account Number', 'Account Name']]

    dfpreclean2['Funds Transfer Amount'] = dfpreclean2['Funds Transfer Amount'] / 100.00

    dfpreclean2['Funding Sub Merchant ID'] = dfpreclean2['Funding Sub Merchant ID'].apply(str)
    dfpreclean2['Funding Sub Merchant ID'] = dfpreclean2['Funding Sub Merchant ID'].apply(lambda x: '0' + x  if len(x) == 8 else x)


    ##funding sub merchant ID NEEDS TO BE CLEANED UP


 

  #  dfcalc.to_csv('test.csv', index=False)




    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        # Write each dataframe to a different worksheet.
        dfpreclean2.to_excel(writer, sheet_name='Clean_Data', index=False)
        dda.to_excel(writer, sheet_name='dda', index=False)

        # Close the Pandas Excel writer and output the Excel file to the buffer
        writer.close()

        st.download_button(
            label="Download Excel worksheets",
            data=buffer,
            file_name="achrejects.xlsx",
            mime="application/vnd.ms-excel"
        )

else:
   st.warning("you need to upload a csv file.")