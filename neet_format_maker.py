import streamlit as st
import pandas as pd

# Hardcoded student data from CSV

student_record =pd.read_csv('name_roll.csv')
# Streamlit App
st.title("NEET Format Maker")

# File upload section
uploaded_file = st.file_uploader("Upload your test data file (CSV or Excel)", type=["csv", "xlsx"])

file_name=st.text_input('enter file name code , date ')

if uploaded_file:
    # Determine file type and read the file
    if uploaded_file.name.endswith(".csv"):
        data = pd.read_csv(uploaded_file)
    elif uploaded_file.name.endswith(".xlsx"):
        data = pd.read_excel(uploaded_file)
    else:
        st.error("Unsupported file format!")

    # Display raw data
    st.subheader("Uploaded Data")
    st.dataframe(data.head())

    # Process the data
    col_name = data.columns
    flag = 0
    for i in range(len(col_name)):
        if col_name[i] == "Test Rank":
            flag = i + 1
            break

    data2 = data.iloc[:, :flag]

    # Drop unnecessary columns
    data2 = data2.drop(columns=['FATHER', 'GROUP', 'PASSWORD', 'Test No', 'Test'], axis=1)

    # Add calculated columns
    data2['PHY_'] = data2['PHY'] + data2['PHY(S)']
    data2['CHEM_'] = data2['CHEM'] + data2['CHEM(S)']
    data2['BOTANY_'] = data2['BOTANY'] + data2['BIOLOGY']
    data2['ZOOLOGY_'] = data2['ZOOLOGY'] + data2['IQ']

    # Drop original columns after calculations
    data2 = data2.drop(columns=['PHY', 'CHEM', 'BOTANY', 'ZOOLOGY', 'BIOLOGY', 'IQ', 'PHY(S)', 'CHEM(S)'], axis=1)

    # Reorganize columns
    data2 = data2[['CANDIDATE ID', 'PHY_', 'CHEM_', 'BOTANY_', 'ZOOLOGY_', 'Total', 'Test Rank']]

    # Ensure both columns have the same data type
    data2['CANDIDATE ID'] = data2['CANDIDATE ID'].astype(str)
    student_record['roll_no'] = student_record['roll_no'].astype(str)

    # Merge with student data
    merged_data = pd.merge(data2, student_record, left_on='CANDIDATE ID', right_on='roll_no', how='left')

    # Display processed data
    st.subheader("Processed Data")
    st.dataframe(merged_data)


    merged_data = merged_data[['CANDIDATE ID','name', 'PHY_', 'CHEM_', 'BOTANY_', 'ZOOLOGY_', 'Total', 'Test Rank']]
    merged_data=merged_data.sort_values(by=['Test Rank'])
    # Download link for processed file
    output_file = "merged_data.xlsx"
    merged_data.to_excel(output_file, index=False)

    with open(output_file, "rb") as file:
        btn = st.download_button(
            label="Download Processed Data",
            data=file,
            file_name=f"{file_name}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
