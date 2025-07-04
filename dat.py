import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta

# Tehsil names
tehsils = ["Kannad", "Soyagaon", "Sillod", "Phulambri", "Aurangabad",
           "Khuldabad", "Vaijapur", "Gangapur", "Paithan"]

# Monthly averages (rough reference for Aurangabad)
monthly_stats = {
    1:  {"t_min": 17, "t_max": 29, "rain": 3,   "hum": 55, "wind": 9.9, "press": 1014},
    2:  {"t_min": 20, "t_max": 32, "rain": 3.5, "hum": 45, "wind": 10.6, "press": 1013},
    3:  {"t_min": 23, "t_max": 36, "rain": 5.6, "hum": 37, "wind": 11.3, "press": 1011},
    4:  {"t_min": 26, "t_max": 39, "rain": 4.7, "hum": 32, "wind": 13.2, "press": 1008},
    5:  {"t_min": 27, "t_max": 39, "rain": 25.3,"hum": 36, "wind": 17.9, "press": 1005},
    6:  {"t_min": 25, "t_max": 34, "rain": 106, "hum": 66, "wind": 20.0, "press": 1004},
    7:  {"t_min": 23, "t_max": 29, "rain": 129, "hum": 78, "wind": 21.1, "press": 1004},
    8:  {"t_min": 22, "t_max": 28, "rain": 125, "hum": 79, "wind": 18.4, "press": 1005},
    9:  {"t_min": 22, "t_max": 30, "rain": 126, "hum": 77, "wind": 12.6, "press": 1007},
    10: {"t_min": 25, "t_max": 31, "rain": 52.2,"hum": 64, "wind": 10.0, "press": 1011},
    11: {"t_min": 23, "t_max": 30, "rain": 16.4,"hum": 58, "wind": 9.8,  "press": 1013},
    12: {"t_min": 21, "t_max": 28, "rain": 5.2, "hum": 56, "wind": 9.8,  "press": 1014},
}

years = [2020, 2021, 2022, 2023, 2024]

# Output folder
os.makedirs("BhoomiVardhan", exist_ok=True)

def inject_noise(value, noise=1.5):
    """Add small normal noise to the value."""
    return round(np.random.normal(loc=value, scale=noise), 2)

def inject_outlier(value, chance=0.01):
    """Introduce an outlier randomly."""
    if np.random.rand() < chance:
        return round(value * np.random.uniform(2, 4), 2)
    return value

def maybe_missing(value, chance=0.01):
    """Randomly replace value with NaN."""
    return np.nan if np.random.rand() < chance else value

# Generate data per tehsil
for tehsil in tehsils:
    writer = pd.ExcelWriter(f"BhoomiVardhan/{tehsil}_weather.xlsx", engine="openpyxl")
    
    for year in years:
        records = []
        start_date = datetime(year, 1, 1)
        
        for day_offset in range(365):
            date = start_date + timedelta(days=day_offset)
            month = date.month
            m = monthly_stats[month]
            
            min_temp = inject_noise(m["t_min"])
            max_temp = inject_noise(m["t_max"])
            rain = np.random.poisson(m["rain"] / 30)
            humidity = inject_noise(m["hum"], 5)
            wind = inject_noise(m["wind"], 2)
            pressure = inject_noise(m["press"], 1)

            # Inject outliers
            min_temp = inject_outlier(min_temp)
            max_temp = inject_outlier(max_temp)
            rain = inject_outlier(rain, chance=0.02)
            humidity = inject_outlier(humidity)
            wind = inject_outlier(wind)
            pressure = inject_outlier(pressure)

            # Inject missing values
            rain = maybe_missing(rain)
            min_temp = maybe_missing(min_temp)
            max_temp = maybe_missing(max_temp)
            humidity = maybe_missing(humidity)
            wind = maybe_missing(wind)
            pressure = maybe_missing(pressure)

            records.append({
                "Date": date.strftime("%Y-%m-%d"),
                "Rainfall_mm": rain,
                "MinTemp_C": min_temp,
                "MaxTemp_C": max_temp,
                "Humidity_pct": humidity,
                "Wind_kmph": wind,
                "Pressure_hPa": pressure
            })
        
        df = pd.DataFrame(records)
        df.to_excel(writer, sheet_name=str(year), index=False)

    writer._save()
    print(f" File created: {tehsil}_weather.xlsx")

print(" All synthetic weather files generated with realistic seasonal data, outliers, and missing values.")
