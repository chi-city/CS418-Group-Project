import pandas as pd
import matplotlib.pyplot as plt
import math as m
from datetime import datetime


# Returns the distance in miles between two coordinates
# Distance function source: https://stackoverflow.com/a/41337005
def distance(lat1, lon1, lat2, lon2):
    p = 0.017453292519943295
    a = (0.5 - m.cos((lat2 - lat1) * p) / 2 + m.cos(lat1 * p) * m.cos(lat2 * p) * (1 - m.cos((lon2 - lon1) * p)) / 2)
    return (12742 * m.asin(m.sqrt(a)))


# Using the provided latitude, longitude, Chicago crime data, and distance
# This function gets all nearby crime, seperating it by month
def get_crime_nearby_chicago(latitude, longitude, data, dist):
    counter = 0
    all_results = {}

    for i in range(0, len(data)):
        # First check if the current crime is within the radius
        if distance(latitude, longitude, data.iloc[i]["Latitude"], data.iloc[i]["Longitude"]) <= dist:
            try:
                crime_month = datetime.strptime(data.iloc[i]["Date"], "%m/%d/%y %H:%M")
            except ValueError:
                crime_month = datetime.strptime(data.iloc[i]["Date"], "%m/%d/%Y %H:%M")
            crime_month = crime_month.month
            crime_type = data.iloc[i]["Primary Type"]

            if crime_type not in all_results:
                all_results[crime_type] = {}
            
            if crime_month not in all_results[crime_type]:
                all_results[crime_type][crime_month] = 0
            
            all_results[crime_type][crime_month] += 1
            counter+=1

    print("Total crime found in specified radius: " + str(counter))

    all_results_data = {}
    all_crime_types = list(set(all_results.keys()))

    # Iterates over each crime type and month, and adds the count to a dictionary
    for crime_type in all_crime_types:
        for month in all_results[crime_type]:
            if month not in all_results_data:
                all_results_data[month] = {}
            all_results_data[month][crime_type] = all_results[crime_type][month]


    all_results_df = pd.DataFrame.from_dict(all_results_data, orient='index') 

    # Set all blank spaces to 0
    all_results_df.fillna(value=0, inplace=True)

    return all_results_df

# Using the provided latitude, longitude, Los Angeles crime data, and distance
# This function gets all nearby crime, seperating it by month
def get_crime_nearby_la(latitude, longitude, data, dist):
    counter = 0
    all_results = {}

    for i in range(0, len(data)):
        # First check if the current crime is within the radius
        if distance(latitude, longitude, data.iloc[i]["LAT"], data.iloc[i]["LON"]) <= dist:
            try:
                crime_month = datetime.strptime(data.iloc[i]["Date Rptd"], "%m/%d/%y %H:%M")
            except ValueError:
                crime_month = datetime.strptime(data.iloc[i]["Date Rptd"], "%m/%d/%Y %H:%M")
            crime_month = crime_month.month
            crime_type = data.iloc[i]["Crm Cd Desc"]

            if crime_type not in all_results:
                all_results[crime_type] = {}
            
            if crime_month not in all_results[crime_type]:
                all_results[crime_type][crime_month] = 0
            
            all_results[crime_type][crime_month] += 1
            counter+=1

    print("Total crime found in specified radius: " + str(counter))

    all_results_data = {}
    all_crime_types = list(set(all_results.keys()))

    # Iterates over each crime type and month, and adds the count to a dictionary
    for crime_type in all_crime_types:
        for month in all_results[crime_type]:
            if month not in all_results_data:
                all_results_data[month] = {}
            all_results_data[month][crime_type] = all_results[crime_type][month]


    all_results_df = pd.DataFrame.from_dict(all_results_data, orient='index') 

    # Set all blank spaces to 0
    all_results_df.fillna(value=0, inplace=True)

    return all_results_df


def main():
    chicago_crime_file = "Chicago_2022_Crime_Data.csv"
    chicago_crime_data = pd.read_csv(chicago_crime_file, usecols=["Date", "Latitude", "Longitude", "Arrest", "Primary Type"])
    chicago_crime_data = chicago_crime_data.dropna(subset=["Latitude", "Longitude"])

    chicago_cta_ridership_file = "Chicago_CTA_Ridership.csv"
    chicago_cta_ridership_data = pd.read_csv(chicago_cta_ridership_file)
    chicago_cta_ridership_data['station_id'] = chicago_cta_ridership_data['station_id'].astype(int)
    chicago_cta_l_stops_file = "CTA_L-Stops_Chicago.csv"
    chicago_cta_l_stops_data = pd.read_csv(chicago_cta_l_stops_file, usecols=['MAP_ID', 'Location'])
    chicago_cta_l_stops_data['MAP_ID'] = chicago_cta_l_stops_data['MAP_ID'].astype(int)
    # chicago_cta_ridership_and_coordinates_data = pd.merge(chicago_cta_ridership_data, chicago_cta_l_stops_data, left_on="station_id", right_on="MAP_ID", how="inner")

    # chicago_cta_ridership_and_coordinates_data['month_beginning'] = pd.to_datetime(chicago_cta_ridership_and_coordinates_data["month_beginning"], format='%m/%d/%y')
    # chicago_cta_ridership_and_coordinates_data_2022 = chicago_cta_ridership_and_coordinates_data[chicago_cta_ridership_and_coordinates_data['month_beginning'].dt.year == 2022]
    # highest_ridership_station = chicago_cta_ridership_and_coordinates_data_2022[chicago_cta_ridership_and_coordinates_data_2022['monthtotal'] == chicago_cta_ridership_and_coordinates_data_2022['monthtotal'].max()]
    # highest_ridership_station_name = highest_ridership_station['stationame'].head(1).values[0]
    # highest_ridership_station_id = highest_ridership_station['station_id'].head(1).values[0]
    # highest_ridership_location = highest_ridership_station['Location'].head(1).values[0]
    # highest_ridership_location_string = highest_ridership_location.strip('()')
    # latitude_string, longitude_string = highest_ridership_location_string.split(',')
    # all_results_data = get_crime_nearby(float(latitude_string), float(longitude_string), chicago_crime_data, 0.5)
    # all_crime_sums = all_results_data.sum(axis=0)
    # all_crime_sums = all_crime_sums.sort_values(ascending=False)
    # all_crime_sums.columns = ["Crime", "Count"]

    la_crime_file = "Los_Angeles_Crime_2022.csv"
    la_crime_data = pd.read_csv(la_crime_file, usecols=["Date Rptd", "Crm Cd", "Crm Cd Desc", "LAT", "LON"])
    la_crime_data = la_crime_data.dropna(subset=["LAT", "LON"])

    # First visulization: comparing the top five OVERALL most popular types of crime in Chicago and LA (Alex Castillo)
    most_frequent_chicago_crimes = chicago_crime_data['Primary Type'].value_counts().head(5)
    most_frequest_la_crimes = la_crime_data["Crm Cd Desc"].value_counts().head(5)

    fig, (ax1, ax2) = plt.subplots(1,2, figsize=(12,6))
    most_frequent_chicago_crimes.plot(kind="bar", ax=ax1)
    ax1.set_title("Chicago")
    ax1.set_xlabel("Crime Description")
    ax1.set_ylabel("Number of occurences")
    ax1.set_xticklabels(ax1.get_xticklabels(), rotation=45)
    most_frequest_la_crimes.plot(kind="bar", ax=ax2)
    ax2.set_title("Los Angeles")
    ax2.set_xlabel("Crime Description")
    ax2.set_ylabel("Number of occurences")
    ax2.set_xticklabels(ax2.get_xticklabels(), rotation=45)

    plt.suptitle("Top 5 Most Common Crimes Per City in 2022")
    plt.tight_layout()
    plt.show()

    # Second visulization: comparing the five most popular types of crime near the terminus stations on the MOST popular lines for Chicago and LA (Alex Castillo)
    chicago_red_line_howard = get_crime_nearby_chicago(42.019063, -87.672892, chicago_crime_data, 0.5).sum(axis=0).sort_values(ascending=False).head(5)
    chicago_red_line_95th_dan_ryan = get_crime_nearby_chicago(41.722377, -87.624342, chicago_crime_data, 0.5).sum(axis=0).sort_values(ascending=False).head(5)
    la_union_station = get_crime_nearby_la(34.056061, -118.234759, la_crime_data, 0.5).sum(axis=0).sort_values(ascending=False).head(5)
    la_north_hollywood_station = get_crime_nearby_la(34.168504, -118.376808, la_crime_data, 0.5).sum(axis=0).sort_values(ascending=False).head(5)

    fig, axes = plt.subplots(2,2, figsize=(18,12))
    chicago_red_line_howard.plot(kind="bar", ax=axes[0, 1])
    axes[0, 1].set_title("Chicago Red Line - Howard Terminal")
    axes[0, 1].set_xlabel("Crime Description")
    axes[0, 1].set_ylabel("Number of occurences")
    axes[0, 1].set_xticklabels(axes[0, 1].get_xticklabels(), rotation=45)
    chicago_red_line_95th_dan_ryan.plot(kind="bar", ax=axes[1, 1])
    axes[1, 1].set_title("Chicago Red Line - 95th Dan Ryan Terminal")
    axes[1, 1].set_xlabel("Crime Description")
    axes[1, 1].set_ylabel("Number of occurences")
    axes[1, 1].set_xticklabels(axes[1, 1].get_xticklabels(), rotation=45)

    la_union_station.plot(kind="bar", ax=axes[1, 0])
    axes[1, 0].set_title("LA Metro D Line - Union Station Terminal")
    axes[1, 0].set_xlabel("Crime Description")
    axes[1, 0].set_ylabel("Number of occurences")
    axes[1, 0].set_xticklabels(axes[1, 0].get_xticklabels(), rotation=45)
    la_north_hollywood_station.plot(kind="bar", ax=axes[0, 0])
    axes[0, 0].set_title("LA Metro D Line - North Hollywood Terminal")
    axes[0, 0].set_xlabel("Crime Description")
    axes[0, 0].set_ylabel("Number of occurences")
    axes[0, 0].set_xticklabels(axes[0,0].get_xticklabels(), rotation=45)

    plt.suptitle("Top 5 Most Common Crimes At Terminal Stations on Highest Ridership Lines (2022)")
    plt.tight_layout()
    plt.show()

    # Third visualization: comparing crime counts by season per city (Alex Castillo)
    winter_months = [12, 1, 2]
    spring_months = [3, 4, 5]
    summer_months = [6, 7, 8]
    fall_months = [9, 10, 11]

    chicago_crime_data['Date'] = pd.to_datetime(chicago_crime_data['Date'], format='%m/%d/%Y %H:%M')
    chicago_number_of_winter_crimes = chicago_crime_data['Date'].dt.month.isin(winter_months).sum()
    chicago_number_of_spring_crimes = chicago_crime_data['Date'].dt.month.isin(spring_months).sum()
    chicago_number_of_summer_crimes = chicago_crime_data['Date'].dt.month.isin(summer_months).sum()
    chicago_number_of_fall_crimes = chicago_crime_data['Date'].dt.month.isin(fall_months).sum()
    chicago_seasonal_crime_values = {
        "Winter": chicago_number_of_winter_crimes,
        "Spring": chicago_number_of_spring_crimes,
        "Summer": chicago_number_of_summer_crimes,
        "Fall": chicago_number_of_fall_crimes
    }

    la_crime_data['Date Rptd'] = pd.to_datetime(la_crime_data['Date Rptd'], format='%m/%d/%y %H:%M')
    la_number_of_winter_crimes = la_crime_data['Date Rptd'].dt.month.isin(winter_months).sum()
    la_number_of_spring_crimes = la_crime_data['Date Rptd'].dt.month.isin(spring_months).sum()
    la_number_of_summer_crimes = la_crime_data['Date Rptd'].dt.month.isin(summer_months).sum()
    la_number_of_fall_crimes = la_crime_data['Date Rptd'].dt.month.isin(fall_months).sum()
    la_seasonal_crime_values = {
        "Winter": la_number_of_winter_crimes,
        "Spring": la_number_of_spring_crimes,
        "Summer": la_number_of_summer_crimes,
        "Fall": la_number_of_fall_crimes
    }

    plt.plot(list(chicago_seasonal_crime_values.keys()), list(chicago_seasonal_crime_values.values()), marker='o', label="Chicago")
    plt.plot(list(la_seasonal_crime_values.keys()), list(la_seasonal_crime_values.values()), marker='o', label="Los Angeles")
    plt.xlabel("Season")
    plt.ylabel("Number Of Recorded Crimes")
    plt.legend()
    plt.title("Total Crime Counts Per Season")
    plt.ylim(40000, 70000)
    plt.tight_layout()
    plt.show()

    # Fourth visualization: comparing crime counts by season near the terminus stations on the MOST popular lines for Chicago and LA (Alex Castillo)
    chicago_crime_data = pd.read_csv(chicago_crime_file, usecols=["Date", "Latitude", "Longitude", "Arrest", "Primary Type"])
    chicago_crime_data = chicago_crime_data.dropna(subset=["Latitude", "Longitude"])
    la_crime_data = pd.read_csv(la_crime_file, usecols=["Date Rptd", "Crm Cd", "Crm Cd Desc", "LAT", "LON"])
    la_crime_data = la_crime_data.dropna(subset=["LAT", "LON"])

    chicago_red_line_howard = get_crime_nearby_chicago(42.019063, -87.672892, chicago_crime_data, 0.5)
    chicago_red_line_howard = chicago_red_line_howard.sort_index()
    chicago_red_line_howard_winter_crime_count = chicago_red_line_howard.loc[12].sum() +  chicago_red_line_howard.loc[1].sum() +  chicago_red_line_howard.loc[2].sum()
    chicago_red_line_howard_spring_crime_count = chicago_red_line_howard.loc[3].sum() +  chicago_red_line_howard.loc[4].sum() +  chicago_red_line_howard.loc[5].sum()
    chicago_red_line_howard_summer_crime_count = chicago_red_line_howard.loc[6].sum() +  chicago_red_line_howard.loc[7].sum() +  chicago_red_line_howard.loc[8].sum()
    chicago_red_line_howard_fall_crime_count = chicago_red_line_howard.loc[9].sum() +  chicago_red_line_howard.loc[10].sum() +  chicago_red_line_howard.loc[11].sum()
    chicago_red_line_howard_seasonal_crime_values = {
        "Winter": chicago_red_line_howard_winter_crime_count,
        "Spring": chicago_red_line_howard_spring_crime_count,
        "Summer": chicago_red_line_howard_summer_crime_count,
        "Fall": chicago_red_line_howard_fall_crime_count
    }

    chicago_red_line_95th_dan_ryan = get_crime_nearby_chicago(41.722377, -87.624342, chicago_crime_data, 0.5)
    chicago_red_line_95th_dan_ryan = chicago_red_line_95th_dan_ryan.sort_index()
    chicago_red_line_95th_dan_ryan_winter_crime_count = chicago_red_line_95th_dan_ryan.loc[12].sum() +  chicago_red_line_95th_dan_ryan.loc[1].sum() +  chicago_red_line_95th_dan_ryan.loc[2].sum()
    chicago_red_line_95th_dan_ryan_spring_crime_count = chicago_red_line_95th_dan_ryan.loc[3].sum() +  chicago_red_line_95th_dan_ryan.loc[4].sum() +  chicago_red_line_95th_dan_ryan.loc[5].sum()
    chicago_red_line_95th_dan_ryan_summer_crime_count = chicago_red_line_95th_dan_ryan.loc[6].sum() +  chicago_red_line_95th_dan_ryan.loc[7].sum() +  chicago_red_line_95th_dan_ryan.loc[8].sum()
    chicago_red_line_95th_dan_ryan_fall_crime_count = chicago_red_line_95th_dan_ryan.loc[9].sum() +  chicago_red_line_95th_dan_ryan.loc[10].sum() +  chicago_red_line_95th_dan_ryan.loc[11].sum()
    chicago_red_line_95th_dan_ryan_seasonal_crime_values = {
        "Winter": chicago_red_line_95th_dan_ryan_winter_crime_count,
        "Spring": chicago_red_line_95th_dan_ryan_spring_crime_count,
        "Summer": chicago_red_line_95th_dan_ryan_summer_crime_count,
        "Fall": chicago_red_line_95th_dan_ryan_fall_crime_count
    }

    la_union_station = get_crime_nearby_la(34.056061, -118.234759, la_crime_data, 0.5)
    la_union_station = la_union_station.sort_index()
    la_union_station_winter_crime_count = la_union_station.loc[12].sum() +  la_union_station.loc[1].sum() +  la_union_station.loc[2].sum()
    la_union_station_spring_crime_count = la_union_station.loc[3].sum() +  la_union_station.loc[4].sum() +  la_union_station.loc[5].sum()
    la_union_station_summer_crime_count = la_union_station.loc[6].sum() +  la_union_station.loc[7].sum() +  la_union_station.loc[8].sum()
    la_union_station_fall_crime_count = la_union_station.loc[9].sum() +  la_union_station.loc[10].sum() +  la_union_station.loc[11].sum()
    la_line_d_union_station_seasonal_crime_values = {
        "Winter": la_union_station_winter_crime_count,
        "Spring": la_union_station_spring_crime_count,
        "Summer": la_union_station_summer_crime_count,
        "Fall": la_union_station_fall_crime_count
    }

    la_north_hollywood_station = get_crime_nearby_la(34.168504, -118.376808, la_crime_data, 0.5)
    la_north_hollywood_station = la_north_hollywood_station.sort_index()
    la_north_hollywood_station_winter_crime_count = la_north_hollywood_station.loc[12].sum() +  la_north_hollywood_station.loc[1].sum() +  la_north_hollywood_station.loc[2].sum()
    la_north_hollywood_station_spring_crime_count = la_north_hollywood_station.loc[3].sum() +  la_north_hollywood_station.loc[4].sum() +  la_north_hollywood_station.loc[5].sum()
    la_north_hollywood_station_summer_crime_count = la_north_hollywood_station.loc[6].sum() +  la_north_hollywood_station.loc[7].sum() +  la_north_hollywood_station.loc[8].sum()
    la_north_hollywood_station_fall_crime_count = la_north_hollywood_station.loc[9].sum() +  la_north_hollywood_station.loc[10].sum() +  la_north_hollywood_station.loc[11].sum()
    la_line_d_north_hollywood_station_seasonal_crime_values = {
        "Winter": la_north_hollywood_station_winter_crime_count,
        "Spring": la_north_hollywood_station_spring_crime_count,
        "Summer": la_north_hollywood_station_summer_crime_count,
        "Fall": la_north_hollywood_station_fall_crime_count
    }

    plt.plot(list(chicago_red_line_howard_seasonal_crime_values.keys()), list(chicago_red_line_howard_seasonal_crime_values.values()), marker='o', label="Chicago - Red Line - Howard Station")
    plt.plot(list(chicago_red_line_95th_dan_ryan_seasonal_crime_values.keys()), list(chicago_red_line_95th_dan_ryan_seasonal_crime_values.values()), marker='o', label="Chicago - Red Line - 95th Dan Ryan Station")
    plt.plot(list(la_line_d_union_station_seasonal_crime_values.keys()), list(la_line_d_union_station_seasonal_crime_values.values()), marker='o', label="Los Angeles - Line B - Union Station")
    plt.plot(list(la_line_d_north_hollywood_station_seasonal_crime_values.keys()), list(la_line_d_north_hollywood_station_seasonal_crime_values.values()), marker='o', label="Los Angeles - Line B - North Hollywood Station")
    plt.xlabel("Season")
    plt.ylabel("Number Of Recorded Crimes")
    plt.legend()
    plt.title("Total Crime Counts Per Season Per Line (within 0.5 mile radius of station, 2022)")
    plt.tight_layout()
    plt.show()
    
    # Fifth Visulization: busiest vs least busiest station top 5 crimes on Chicago CTA (Alex Castillo)
    chicago_crime_data = pd.read_csv(chicago_crime_file, usecols=["Date", "Latitude", "Longitude", "Arrest", "Primary Type"])
    chicago_crime_data = chicago_crime_data.dropna(subset=["Latitude", "Longitude"])
    chicago_cta_busiest_station_crimes = get_crime_nearby_chicago(41.884809, -87.627813, chicago_crime_data, 0.5).sum(axis=0).sort_values(ascending=False).head(5)
    chicago_cta_least_busiest_station_crimes = get_crime_nearby_chicago(41.78013, -87.615546, chicago_crime_data, 0.5).sum(axis=0).sort_values(ascending=False).head(5)
    fig, axes = plt.subplots(1,2, figsize=(12,6))
    chicago_cta_busiest_station_crimes.plot(kind="bar", ax=axes[0])
    axes[0].set_title("CTA Red Line - Lake/State (Busiest Station)")
    axes[0].set_xlabel("Crime Description")
    axes[0].set_ylabel("Number of occurences")
    axes[0].set_xticklabels(axes[0].get_xticklabels(), rotation=45)
    chicago_cta_least_busiest_station_crimes.plot(kind="bar", ax=axes[1])
    axes[1].set_title("CTA Green Line - King Drive (Least Busiest Station)")
    axes[1].set_xlabel("Crime Description")
    axes[1].set_ylabel("Number of occurences")
    axes[1].set_xticklabels(axes[1].get_xticklabels(), rotation=45)
    plt.suptitle("Top 5 Most Common Crimes Near the Busiest and Least Busiest Station on the CTA (0.5 mile radius, 2022)")
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()



