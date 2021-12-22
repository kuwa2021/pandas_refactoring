import numpy as np
import pandas as pd
import itertools

def read_data(x1, y1):
    climate_precip = pd.read_csv(x1)
    climate_temp = pd.read_csv(y1)
    return climate_precip, climate_temp
climate_precip, climate_temp = read_data("../data/climate_precip.csv", "../data/climate_temp.csv")

def filter_and_join(x2, y2):
    climate_precip_col, station_code = x2, y2
    precip_one_station = climate_precip[climate_precip[climate_precip_col] == station_code]
    inner_join = pd.merge(precip_one_station, climate_temp)
    return inner_join, precip_one_station
inner_join, precip_one_station = filter_and_join("STATION", "GHCND:USW00024215")

def clean_nan1(x3, y3):
    inner_join_col = [x3, y3]
    for column in inner_join_col:
        inner_join.loc[inner_join[column] < 0, column] = np.nan
    return inner_join, inner_join_col
inner_join, inner_join_col = clean_nan1("DLY-PRCP-PCTALL-GE001HI", "DLY-SNOW-PCTALL-GE030TI")

def extract_month_from_date(x4, y4):
    inner_join[y4] = inner_join[x4].apply(lambda x: int(str(x)[4:6]),)
    inner_join[inner_join.month == 1][inner_join_col[1]].unique()
    return inner_join
inner_join = extract_month_from_date("DATE", "month")

def compute_monthly_rain_snow_ratio(x5, y5):
    monthly_precip_snow = inner_join.groupby([x5])[inner_join_col].agg(sum)
    rain_snow_ratio = []
    for i, row in monthly_precip_snow.iterrows():
        try:
            rain_snow_ratio.append(row[inner_join_col[0]] / row[inner_join_col[1]])
        except:
            rain_snow_ratio.append(np.nan)
    monthly_precip_snow[y5] = rain_snow_ratio
    return monthly_precip_snow
monthly_precip_snow = compute_monthly_rain_snow_ratio("month", "rain_snow_ratio")

def clean_nan2(x6, y6):
    inner_join[inner_join[x6] == -7777] = np.nan
    avg_clouds = inner_join.groupby(y6)[x6].agg(np.mean)
    return avg_clouds
avg_clouds = clean_nan2("DLY-HTDD-NORMAL", "month")

def merge_precipitations_and_cloud_data(x7, y7):
    df_merged = pd.concat([x7, y7], axis=1)
    return df_merged
df_merged = merge_precipitations_and_cloud_data(monthly_precip_snow, avg_clouds)

def print_correlations(x8, y8, z8, a8):
    corrs = []
    for pair in itertools.combinations([x8, y8, z8, a8], 2):
        corr = df_merged[[pair[0], pair[1]]].corr().values[0, 1]
        print(f"Monthly {pair[0]}, {pair[1]} correlation is {corr:.4f}")
        corrs.append(corr)
    return corrs
corrs = print_correlations("rain_snow_ratio", "DLY-HTDD-NORMAL", "DLY-SNOW-PCTALL-GE030TI", "DLY-PRCP-PCTALL-GE001HI")

df_merged.to_csv("output.csv")