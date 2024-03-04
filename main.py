# %%
from reading_file import load_data
import pickle
from merging_file import (merging_data, assign_fuel_costs, fill_missing_fuel_costs, assign_em_rates, long_wide, transmission_func,
                          ffill_ren_cost, ffill_ren_cap, cluster_and_aggregate, long_wide_load, load_dic, wind_cap_dic, wind_cost_dic, solar_cap_dic,
                          solar_cost_dic, storage_object, gen_object, load_object,trans_object, transmission_dic1, transmission_dic2, cp_dic, plant_dic, plant_capacity, trans_index, renewable_transmission_cost)

# %% Loading Input Data
(Plant, Transmission, Parsed, Input, NEEDS, Wind_generation_profile, Load, Wind_onshore_capacity,
 Wind_capital_cost, Solar_regional_capacity, Solar_generation_profile, Solar_capital_cost_photov, Solar_capacity_factor, Regional_Cost, Unit_Cost) = load_data()


Plant_short = merging_data(Plant, Parsed)

# Assigning fuel cost
Plant_short = assign_fuel_costs(Plant_short)
# Replacing missing fuel cost
Plant_short = fill_missing_fuel_costs(Plant_short, Transmission)
# Replacing missing fuel cost
Plant_short = assign_em_rates(Plant_short)
# Aggregating the power plants
Plants_ungroup,  Plants_group = cluster_and_aggregate(Plant_short, num_bins=20)
# Converting to data dictionary
Plants_Dic = plant_dic(Plants_group)


Wind_generation_profile_wide = long_wide(Wind_generation_profile)
Solar_generation_profile_wide = long_wide(Solar_generation_profile)

Transmission_Capacity, Transmission_Energy, Transmission_Cost = transmission_func(Transmission)

Wind_onshore_capacity, Solar_regional_capacity = ffill_ren_cap(Wind_onshore_capacity, Solar_regional_capacity)
Wind_capital_cost, Solar_capital_cost_photov = ffill_ren_cost(Wind_capital_cost, Solar_capital_cost_photov)

Load_wide = long_wide_load(Load)

load_final = load_dic(Load_wide)

Wind_onshore_capacity_final = wind_cap_dic(Wind_onshore_capacity)
Wind_capital_cost_final = wind_cost_dic(Wind_capital_cost)

Solar_regional_capacity_final = solar_cap_dic(Solar_regional_capacity)
Solar_capital_cost_photov_final = solar_cost_dic(Solar_capital_cost_photov)

Transmission_Capacity_final = transmission_dic1(Transmission_Capacity)
Transmission_Energy_final = transmission_dic1(Transmission_Energy)

Solar_capacity_factor_final = cp_dic(Solar_generation_profile_wide)
Wind_capacity_factor_final = cp_dic(Wind_generation_profile_wide)


Transmission_Capacity_dic = transmission_dic1(Transmission_Capacity)
Transmission_Energy_dic = transmission_dic1(Transmission_Energy)

Transmission_Cost_dic = transmission_dic2(Transmission_Cost)

Transmission_index = trans_index(Transmission_Capacity)

Plant_capacity_dic = plant_capacity(Plant_short)

Wind_trans_capital_cost_final, Solar_trans_capital_cost_photov_final, Wind_capital_cost_copy, Solar_capital_cost_photov_copy = renewable_transmission_cost(Unit_Cost, Regional_Cost, Wind_capital_cost, Solar_capital_cost_photov)

dicts_with_names = {'Plants_Dic': Plants_Dic,
                    'load_final': load_final,
                    'Wind_onshore_capacity_final': Wind_onshore_capacity_final,
                    'Wind_capital_cost_final': Wind_capital_cost_final,
                    'Solar_regional_capacity_final': Solar_regional_capacity_final,
                    'Solar_capital_cost_photov_final': Solar_capital_cost_photov_final,
                    'Transmission_Capacity_final': Transmission_Capacity_final,
                    'Transmission_Energy_final': Transmission_Energy_final,
                    'Solar_capacity_factor_final': Solar_capacity_factor_final,
                    'Wind_capacity_factor_final': Wind_capacity_factor_final,
                    'Transmission_Capacity_dic': Transmission_Capacity_dic,
                    'Transmission_Energy_dic': Transmission_Energy_dic,
                    'Transmission_Cost_dic': Transmission_Cost_dic,
                    'Transmission_index': Transmission_index,
                    'Plant_capacity_dic': Plant_capacity_dic,
                    'Wind_trans_capital_cost_final': Wind_trans_capital_cost_final,
                    'Solar_trans_capital_cost_photov_final': Solar_trans_capital_cost_photov_final
                    }


trasnmission_oo = trans_object(Transmission_Capacity, Transmission_Cost)
load_oo = load_object(Load_wide)
generator_oo = gen_object(Plants_group)
storage_oo = storage_object(Plants_group)

#
# Pickle the dictionary with names
with open('dicts_with_names.pkl', 'wb') as pickle_file:
    pickle.dump(dicts_with_names, pickle_file)

# Load the pickled file
with open('dicts_with_names.pkl', 'rb') as pickle_file:
    loaded_dicts_with_names = pickle.load(pickle_file)

