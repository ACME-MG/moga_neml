from modules.api import API
api = API("", 0)
api.define_model("evpwd")

# api.read_file("cyclic/AirBase316_time_strain.csv", True)

# api.read_file("inl_1/AirBase_800_80_G25.csv", True)
# api.read_file("inl_1/AirBase_800_70_G44.csv", True)
# api.read_file("inl_1/AirBase_800_65_G33.csv", True)
# api.read_file("inl_1/AirBase_800_60_G32.csv", True)
# api.read_file("tensile/AirBase_800_D7.csv", True)

# api.read_file("inl_1/AirBase_900_36_G22.csv", True)
# api.read_file("inl_1/AirBase_900_31_G50.csv", True)
# api.read_file("inl_1/AirBase_900_28_G45.csv", True)
# api.read_file("inl_1/AirBase_900_26_G59.csv", True)
# api.__remove_oxidised_creep__()
# api.read_file("tensile/AirBase_900_D10.csv", False)

# api.read_file("inl_1/AirBase_1000_11_G39.csv", True)
# api.read_file("inl_1/AirBase_1000_12_G52.csv", True)
# api.read_file("inl_1/AirBase_1000_13_G30.csv", True)
# api.read_file("inl_1/AirBase_1000_16_G18.csv", True)
# api.__remove_oxidised_creep__()
# api.read_file("tensile/AirBase_1000_D12.csv", False)

# api.read_file("inl_2/AirBase_750_118_b.csv", True)
# api.read_file("inl_2/AirBase_750_137_a.csv", True)
# api.read_file("inl_2/AirBase_750_95_a.csv", True)

# api.read_file("inl_2/AirBase_850_43_a.csv", True)
# api.read_file("inl_2/AirBase_850_54_a.csv", True)
# api.read_file("inl_2/AirBase_850_63_b.csv", True)

# api.read_file("kaeri_1/AirBase_900_25_a.csv", True)
# api.read_file("kaeri_1/AirBase_900_28_a.csv", True)
# api.read_file("kaeri_1/AirBase_900_30_a.csv", True)
# api.read_file("kaeri_1/AirBase_900_40_a.csv", True)

# api.read_file("kaeri_2/AirBase_900_30_a.csv", True)
# api.read_file("kaeri_2/AirBase_900_35_a.csv", False)
# api.read_file("kaeri_2/AirBase_900_40_a.csv", True)
# api.read_file("kaeri_2/AirBase_900_45_a.csv", False)
# api.read_file("kaeri_2/AirBase_900_50_a.csv", True)

# api.read_file("kaeri_2/AirBase_950_18_a.csv", True)
# api.read_file("kaeri_2/AirBase_950_20_a.csv", True)
# api.read_file("kaeri_2/AirBase_950_22_a.csv", True)
# api.read_file("kaeri_2/AirBase_950_30_a.csv", False)
# api.read_file("kaeri_2/AirBase_950_35_a.csv", True)

api.read_file("kaeri_3/AirBase_900_25_a.csv", False)
api.read_file("kaeri_3/AirBase_900_28_a.csv", False)
api.read_file("kaeri_3/AirBase_900_35_a.csv", True)
api.read_file("kaeri_3/AirBase_900_40_a.csv", True)
api.read_file("kaeri_3/AirBase_900_45_a.csv", False)
api.read_file("kaeri_3/AirBase_900_50_a.csv", True)

api.visualise()
# api.__plot_results__([6.548501602,44.04643902,50.93493579,2.05416603,68466.00514,0.33925536,3.356367201,6.625275181])