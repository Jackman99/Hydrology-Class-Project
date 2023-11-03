import csv
import matplotlib.pyplot as plt
import datetime

class WaterData:
    def __init__(self, date, precipitation, potential_evaporation, total_streamflow, fast_flow, slow_flow):
        self.date = date
        self.precipitation = precipitation
        self.potential_evaporation = potential_evaporation
        self.total_streamflow = total_streamflow
        self.fast_flow = fast_flow
        self.slow_flow = slow_flow

class Catchment:
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

    def plot_yearly_data(self, year, data_type='precipitation', average_over_month=False):
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

        data_values = []

        for water_day in self.water_data:
            if water_day.date.year == year:
                if data_to_plot == 'combination':
                    values = [getattr(water_day, column) for column in data_columns]
                    data_values.append(values)
                else:
                    data_values.append(getattr(water_day, data_column))

        # Plotting
        plt.figure(figsize=(10, 6))

        if average_over_month:
            monthly_values = {month: [] for month in range(1, 13)}
            for day, value in enumerate(data_values, start=1):
                month = (datetime.date(year, 1, 1) + datetime.timedelta(day - 1)).month
                monthly_values[month].append(value)
            monthly_averages = [sum(values) / len(values) if values else 0 for values in monthly_values.values()]
            plt.plot(range(1, 13), monthly_averages, marker='o', linestyle='-', color='blue')
            plt.title(f'Average {data_type.replace("_", " ").title()} per Month for Year {year}')
            plt.xlabel('Month')
            plt.ylabel(f'Average {data_type.replace("_", " ").title()}')
        else:
            if data_to_plot == 'combination':
                data_values = list(zip(*data_values))
                labels = ['Precipitation', 'Total Streamflow', 'Potential Evaporation', 'Fast Flow', 'Slow Flow']
                colors = ['blue', 'green', 'orange', 'red', 'purple']
                for values, label, color in zip(data_values, labels, colors):
                    plt.plot(range(1, len(values) + 1), values, label=label, color=color)
                plt.legend()
            else:
                plt.plot(range(1, len(data_values) + 1), data_values, color='blue')
                plt.title(f'{data_type.replace("_", " ").title()} for Year {year}')
                plt.xlabel('Day of the Year')
                plt.ylabel(data_type.replace("_", " ").title())

        plt.tight_layout()
        plt.show()
