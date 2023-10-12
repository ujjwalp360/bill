from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import io
import pandas as pd
import streamlit as st
# Authenticate using the JSON credentials file you downloaded
gauth = GoogleAuth()
gauth.LocalWebserverAuth()
drive = GoogleDrive(gauth)

# Name of the folder you want to create
folder_name = "data"

# Locate the "data" folder in Google Drive
folder_query = f"title = '{folder_name}' and mimeType = 'application/vnd.google-apps.folder'"
folder_list = drive.ListFile({'q': folder_query}).GetList()

if not folder_list:
    # If the "data" folder doesn't exist, create it
    data_folder = drive.CreateFile({'title': folder_name, 'mimeType': 'application/vnd.google-apps.folder'})
    data_folder.Upload()
    data_folder_id = data_folder['id']
else:
    # Use the existing "data" folder
    data_folder = folder_list[0]
    data_folder_id = data_folder['id']

# Name of the CSV file you want to create or update
file_name = "bills.csv"

# Check if the CSV file exists in the "data" folder
file_query = f"'{data_folder_id}' in parents and title = '{file_name}'"
file_list = drive.ListFile({'q': file_query}).GetList()

if not file_list:
    # If the CSV file doesn't exist, create it
    csv_file = drive.CreateFile({'title': file_name, 'parents': [{'id': data_folder_id}]})
    csv_file.Upload()
else:
    # Use the existing CSV file
    csv_file = file_list[0]

# Prompt the user for data and add it to the CSV file
name = st.text+input("Enter Name: ")
user_id = st.number_input("Enter ID: ")
dob = st.text_input("Enter Date of Birth (MM/DD/YYYY): ")

# Prepare the new data to append
new_data = f"{name}, {user_id}, {dob}"

# Download the CSV file
csv_file.GetContentFile(file_name)

# Read the existing content from the downloaded file
with open(file_name, 'r') as file:
    existing_data = file.read()

# Concatenate the existing data and the new data
updated_content = existing_data + "\n" + new_data

# Write the updated content back to the downloaded file
with open(file_name, 'w') as file:
    file.write(updated_content)

# Upload the updated CSV file
csv_file.SetContentFile(file_name)
csv_file.Upload()
st.success(f"Added data to {file_name} in the '{folder_name}' folder in Google Drive.")
# Name of the folder where the CSV file is located
folder_name = "data"

# Name of the CSV file you want to read
file_name = "bills.csv"

# Locate the "data" folder in Google Drive
folder_query = f"title = '{folder_name}' and mimeType = 'application/vnd.google-apps.folder'"
folder_list = drive.ListFile({'q': folder_query}).GetList()

if folder_list:
    data_folder = folder_list[0]  # Assuming there's only one folder with that name
    data_folder_id = data_folder['id']

    # Check if the CSV file exists in the "data" folder
    file_query = f"'{data_folder_id}' in parents and title = '{file_name}'"
    file_list = drive.ListFile({'q': file_query}).GetList()

    if file_list:
        # Use the existing CSV file
        csv_file = file_list[0]

        # Download the CSV file
        csv_file.GetContentFile(file_name)

        # Read the CSV data using Pandas
        df = pd.read_csv(file_name)

        # Print the DataFrame (the contents of the CSV file)
        st.table(df)

    else:
        st.write(f"'{file_name}' CSV file not found in the '{folder_name}' folder.")
else:
    st.write(f"'{folder_name}' folder not found in Google Drive.")

