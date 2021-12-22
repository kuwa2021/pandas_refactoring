from main3_2 import *

def test_read_data():
    assert climate_precip.shape == (151110, 29), f'エラー１'
    assert climate_temp.shape == (127020, 21), f'エラー２'

def test_filter_and_join():
    assert precip_one_station.shape == (365, 29), f'エラー３'

def test_clean_nan1():
    assert inner_join["DLY-SNOW-PCTALL-GE030TI"].isnull().sum() == 25, f'エラー４'

def test_extract_month_from_date():
    assert inner_join.shape == (365, 48), f'エラー５'

def test_compute_monthly_rain_snow_ratio():
    assert monthly_precip_snow.shape == (12, 3), f'エラー６'

def test_clean_nan2():
    assert avg_clouds.shape == (12,), f'エラー７'

def test_merge_precipitations_and_cloud_data():    
    assert df_merged.shape == (12, 4), f'エラー８'

def test_print_correlations():
    assert len(corrs) == 6 , f'エラー９'