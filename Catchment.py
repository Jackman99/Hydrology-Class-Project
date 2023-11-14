import csv
import matplotlib.pyplot as plt
import datetime
import matplotlib

class WaterData:
    """
    A class to represent water data for a given date.

    Attributes
    ----------
    date : str
        The date of the water data in YYYY-MM-DD format.
    precipitation : float
        The amount of precipitation in millimeters.
    potential_evaporation : float
        The potential evaporation in millimeters.
    total_streamflow : float
        The total streamflow in cubic meters per second.
    fast_flow : float
        The fast flow component of streamflow in cubic meters per second.
    slow_flow : float
        The slow flow component of streamflow in cubic meters per second.
    """

    def __init__(self, date, precipitation, potential_evaporation, total_streamflow, fast_flow, slow_flow):
        self.date = date
        self.precipitation = precipitation
        self.potential_evaporation = potential_evaporation
        self.total_streamflow = total_streamflow
        self.fast_flow = fast_flow
        self.slow_flow = slow_flow

class Catchment:
    """
    A class representing a catchment.

    Attributes:
    -----------
    mopex_site_id : str
        The Mopex site ID of the catchment.
    state : str
        The state where the catchment is located.
    location : str
        The location of the catchment.
    drainage_area : float
        The drainage area of the catchment.
    usgs_gage_id : str
        The USGS gage ID of the catchment.
    outlet_gage_longitude : float
        The longitude of the outlet gage of the catchment.
    outlet_gage_latitude : float
        The latitude of the outlet gage of the catchment.
    water_data : list
        A list of WaterData objects representing the water data of the catchment.

    Methods:
    --------
    add_water_data(year, month, day, precipitation, potential_evaporation, total_streamflow, fast_flow, slow_flow)
        Adds water data to the catchment.
    process_csv_file(file_path)
        Processes a CSV file containing water data and adds it to the catchment.
    plot_yearly_data(year, data_type='precipitation', average_over_month=False)
        Plots the yearly data of the catchment for a given year and data type.
    """
    def __init__(self, mopex_site_id, state, location, drainage_area, usgs_gage_id, outlet_gage_longitude, outlet_gage_latitude):
        self.location = location
        self.state = state
        self.drainage_area = drainage_area
        self.usgs_gage_id = usgs_gage_id
        self.mopex_site_id = mopex_site_id
        self.outlet_gage_latitude = outlet_gage_latitude
        self.outlet_gage_longitude = outlet_gage_longitude
        self.water_data = []
    
    # Reader Methods
    def add_water_data(self, year, month, day, precipitation, potential_evaporation, total_streamflow, fast_flow, slow_flow):
        date = datetime.date(int(year), int(month), int(day))
        new_water_data = WaterData(date, precipitation, potential_evaporation, total_streamflow, fast_flow, slow_flow)
        self.water_data.append(new_water_data)

    def process_csv_file(self, file_path):
        with open(file_path, newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                year, month, day, precip, pot_evap, total_flow, fast_flow, slow_flow = map(float, row)
                # Convert the date parts to integers
                year, month, day = int(year), int(month), int(day)
                new_water_data = WaterData(datetime.date(year, month, day), precip, pot_evap, total_flow, fast_flow, slow_flow)
                self.water_data.append(new_water_data)

    # Plotting Methods
    def plot_yearly_data(self, year = 1990, data_type='precipitation', average_over_all_years=False):
        
        
        data_to_plot = {
            'precipitation': 'precipitation',
            'potential_evaporation': 'potential_evaporation',
            'total_streamflow': 'total_streamflow',
            'fast_flow': 'fast_flow',
            'slow_flow': 'slow_flow'
        }



        if data_type == 'combination':
            data_columns = ['precipitation', 'total_streamflow', 'potential_evaporation', 'fast_flow', 'slow_flow']
            data_to_plot = 'combination'
        else:
            data_column = data_to_plot.get(data_type)

        if average_over_all_years:
            all_years_data = {year: [] for year in range(min(self.water_data, key=lambda x: x.date.year).date.year, max(self.water_data, key=lambda x: x.date.year).date.year + 1)}

            for water_day in self.water_data:
                all_years_data[water_day.date.year].append(getattr(water_day, data_column))

            averages = [sum(values) / len(values) if values else 0 for values in all_years_data.values()]
            overall_mean = sum(averages) / len(averages)

            # Plotting
            plt.figure(figsize=(10, 6))
            fontsize = 22
            matplotlib.rc('xtick', labelsize=16) 
            matplotlib.rc('ytick', labelsize=16)
            # Set the fontsize for x-axis and y-axis tick labels
            plt.xticks(fontsize=16)  # Adjust the fontsize as needed
            plt.yticks(fontsize=16)  # Adjust the fontsize as needed
            plt.plot(range(min(all_years_data), max(all_years_data) + 1), averages, linewidth = 4, marker='o', linestyle='-', color='blue')
            plt.axhline(y=overall_mean, linestyle='--', color='red', linewidth = 4, label='Overall Mean')  # Add dashed line for overall mean
            plt.title(f'{self.location} - Average {data_type.replace("_", " ").title()} per Year', fontsize=fontsize)
            plt.xlabel('Year', fontsize=fontsize)
            plt.ylabel(f'Average {data_type.replace("_", " ").title()} [mm]', fontsize=fontsize)
            plt.ylim(bottom=0, top = 12.5)
            plt.legend(fontsize=fontsize)
        else:
            # Plotting for a specific year
            data_values = []

            for water_day in self.water_data:
                if water_day.date.year == year:
                    if data_to_plot == 'combination':
                        values = [getattr(water_day, column) for column in data_columns]
                        data_values.append(values)
                    else:
                        data_values.append(getattr(water_day, data_column))

            # Plotting
            if data_to_plot == 'combination':
                data_values = list(zip(*data_values))
                labels = ['Precipitation', 'Total Streamflow', 'Potential Evaporation', 'Fast Flow', 'Slow Flow']
                colors = ['blue', 'green', 'orange', 'red', 'purple']
                for values, label, color in zip(data_values, labels, colors):
                    plt.plot(range(1, len(values) + 1), values, label=label, color=color)
                plt.title(f'Flow Year {year}', fontsize=fontsize)
                plt.xlabel('Day of the Year', fontsize=fontsize)
                plt.ylabel(data_type.replace("_", " ").title(), fontsize=fontsize)
                plt.legend(fontsize=fontsize)
            else:
                plt.plot(range(1, len(data_values) + 1), data_values, color='blue')
                plt.title(f'{data_type.replace("_", " ").title()} for Year {year}', fontsize=fontsize)
                plt.xlabel('Day of the Year', fontsize=fontsize)
                plt.ylabel(data_type.replace("_", " ").title(), fontsize=fontsize)
        plt.savefig(f'1 {self.location}_{data_type}_allyears.png', dpi=300, bbox_inches='tight')
        plt.show()

    # Chapter 6
    # Parent Distribution and Extreme Value Distribution
    def get_max_values_each_year(self, attribute='total_streamflow'):
        max_values = []
        max_dates = []

        years = {}
        for data in self.water_data:
            year = data.date.year
            if year not in years:
                years[year] = []

            years[year].append(data)

        for year, data_list in years.items():
            max_value = -float('inf')
            max_date = None

            for data in data_list:
                value = getattr(data, attribute)
                if value > max_value:
                    max_value = value
                    max_date = data.date

            max_values.append(max_value)
            max_dates.append(max_date)

        return max_values, max_dates

    def plot_max_values_each_year(self, attribute='total_streamflow'):
        max_values, max_dates = self.get_max_values_each_year(attribute)
        fontsize = 22
        plt.figure(figsize=(15, 6))
        matplotlib.rc('xtick', labelsize=16) 
        matplotlib.rc('ytick', labelsize=16)
        # Set the fontsize for x-axis and y-axis tick labels
        plt.xticks(fontsize=16)  # Adjust the fontsize as needed
        plt.yticks(fontsize=16)  # Adjust the fontsize as needed

        # Plot Time Series
        all_dates = [data.date for data in self.water_data]
        all_values = [getattr(data, attribute) for data in self.water_data]
        plt.subplot(1, 2, 1)
        plt.plot(all_dates, all_values, label='Time Series')
        plt.scatter(max_dates, max_values, color='red', s=50, label='Max Values')
        plt.xlabel('Date', fontsize=fontsize)  # Increase x-axis label font size
        plt.ylabel(attribute.replace('_', ' ').title() + ' [mm]', fontsize=fontsize)  # Increase y-axis label font size
        plt.title(f'{self.location} - {attribute.replace("_", " ").title()}', fontsize=fontsize)  # Increase title font size
        plt.legend(fontsize=fontsize)

        # Plot Histogram
        plt.subplot(1, 2, 2)
        plt.hist(max_values, bins=15, color='red', alpha=0.5, label='Max Values', orientation='horizontal', density=True)
        plt.hist(all_values, bins=15, color='blue', alpha=0.5, label='All Values', orientation='horizontal', density=True)
        plt.ylabel(attribute.replace('_', ' ').title() + ' [mm]', fontsize=fontsize)  # Increase y-axis label font size
        plt.xlabel('Frequency', fontsize=fontsize)  # Increase x-axis label font size
        plt.title('Frequency Distribution', fontsize=fontsize)  # Increase title font size
        plt.legend(fontsize=fontsize)

        plt.tight_layout()
        plt.show()