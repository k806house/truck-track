import pandas as pd
import pickle

from utils import get_coords_by_address, dest


class Model:
    def __init__(self,
                 weather_file="datasets/last_weather.csv",
                 traffic_file="datasets/traffic2021.csv",
                 model_file="model/model.pkl"):
        self.weather_data = pd.read_csv(weather_file)
        self.traffic_data = pd.read_csv(traffic_file)

        with open(model_file, "rb") as f:
            self.model = pickle.load(f)

        self.mean_washtime = 9.64
        self.payload_event_pouring = 5.21
        self.from_cis_to_door = 14.12
        self.payload_event_batch = 1.57

        self.plant_lat = 43.730833
        self.plant_lon = -79.472778

    def get_time(self, date, address, volume):
        after_road = self.payload_event_pouring * volume + self.mean_washtime

        predict = self.predict(date, address)

        before_road = self.payload_event_batch * volume + self.from_cis_to_door

        date_ts = pd.to_datetime(date)
        date4 = date_ts - pd.Timedelta(after_road, 'minutes')
        date3 = date4 - pd.Timedelta(predict[0], 'minutes')
        date2 = date3 - pd.Timedelta(before_road, 'minutes')
        date1 = date_ts

        return [date2.strftime("%Y/%m/%d %H:%M"), date3.strftime("%Y/%m/%d %H:%M"), date4.strftime("%Y/%m/%d %H:%M"), date1.strftime("%Y/%m/%d %H:%M")]

    def predict(self, date, address):
        date_str = str(date)[:10]

        X = pd.DataFrame()

        weather_params1 = ["Temperature", "Precipitation", "Visibility"]
        X = pd.concat([X, self.weather_data[self.weather_data["date"] == date_str][weather_params1]], axis=1)

        date_ts = pd.to_datetime(date)
        day_num = date_ts.dayofweek
        day_hour = date_ts.hour
        X["traffic"] = self.traffic_data.iloc[day_hour][day_num]

        goal_lat, goal_lon = get_coords_by_address(address)

        X["distance"] = dest(self.plant_lat, self.plant_lon, goal_lat, goal_lon)

        weather_params2 = ["Cond_Clear", "Cond_Rain", "Cond_Snow"]
        X = pd.concat([X, self.weather_data[self.weather_data["date"] == date_str][weather_params2]], axis=1)

        pred = self.model.predict(X)

        return pred
