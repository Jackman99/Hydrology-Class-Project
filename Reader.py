import pandas as pd
import Objects as obj
import pickle
import glob

'''Create a List of Catchment objects and populate them with the data'''
catchments = []

# Read the Catchment Data first
XLS_file_path = 'CEE450_Fall2014_ ProjectCatchments.xls'  # Replace 'data.xlsx' with your file path
excel_data = pd.read_excel(XLS_file_path, sheet_name='Sheet1')

directory_path = r'C:\Users\jdrimer2\OneDrive - University of Illinois - Urbana\Classes\Hydrology\Project'

# Process CSV files based on the first two numbers in their names
csv_file_names = []
for file_path in glob.glob(f"{directory_path}/*_30years.csv"):
    csv_file_names.append(file_path)

# Iterate through the Excel data and create Catchment objects
for index, row in excel_data.iterrows():
    
    catchment = obj.Catchment(
        row['MOPEX SITE ID'],
        row['STATE'],
        row['Location'],
        row['Drainage Area_km2'],
        row['USGS Gage ID'],
        row['Outlet gage LONGITUDE'],
        row['Outlet gage LATITUDE'],
    )

    path_to_read = ''
    #add the water data
    for csv_file_name in csv_file_names:
        if int(csv_file_name.split('\\')[-1].split('_')[0]) == row['MOPEX SITE ID']:
            path_to_read = csv_file_name

    catchment.process_csv_file(path_to_read)

    catchments.append(catchment)

# Function to save Catchment objects to a file
def save_catchments(filename, catchments_list):
    with open(filename, 'wb') as file:
        pickle.dump(catchments_list, file)

# Function to load Catchment objects from a file
def load_catchments(filename):
    with open(filename, 'rb') as file:
        return pickle.load(file)

# Save Catchment objects to a file
save_catchments('catchments_data.pkl', catchments)

# Load Catchment objects from the file
loaded_catchments = load_catchments('catchments_data.pkl')