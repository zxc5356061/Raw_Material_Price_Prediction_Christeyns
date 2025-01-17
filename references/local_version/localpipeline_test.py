
from references.local_version import (extract_and_clean as ec,
                 transform as ts,
                 feature_engineer as fe)

from src import format_handle



# import data
gad_dict = ec.get_fred_data('PNGASEUUSDM', 2014, 2024)
gas_df = format_handle.json_to_dataframe(gad_dict,'Time')

wheat_dict = ec.get_fred_data('PWHEAMTUSDM', 2014, 2024)
wheat_df = format_handle.json_to_dataframe(wheat_dict,'Time')

ammonia_dict = ec.get_fred_data('WPU0652013A', 2014, 2024)
ammonia_df = format_handle.json_to_dataframe(ammonia_dict,'Time')


elec_dict = ec.clean_elec_csv('/Users/barryhuang/Projects/Raw_Material_Price_Prediction/data/raw/ELECTRICITY_03_2024.csv',2014,2024)
elec_df = format_handle.json_to_dataframe(elec_dict,'Time')

df_dict = ec.clean_pred_price_evo_csv("/Users/barryhuang/Projects/Raw_Material_Price_Prediction/data/raw/Dataset_Future_Predicting_Price_Evolutions_202403.csv",2014,2023)
df = format_handle.json_to_dataframe(df_dict,'Time')

# other variables
target = 'acid'.lower()

RM_codes = ['RM01/0001','RM01/0004','RM01/0006','RM01/0007']

external_drivers = {
    "PNGASEUUSDM": gas_df,
    "PWHEAMTUSDM": wheat_df,
    "WPU0652013A": ammonia_df,
    "Electricity": elec_df
}

# Impute raw data of target variables
imputed_df, missing = ts.impute_pred_price_evo_csv(df)
dummy_df = ts.get_dummies_and_average_price(imputed_df,target,*RM_codes)

# Feature engineering
feature_df = fe.generate_features(1,12,dummy_df,missing,*RM_codes, **external_drivers)

# feature_df.to_csv("local_test_result.csv", index=False)