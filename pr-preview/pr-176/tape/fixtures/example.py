from idfkit import load_idf

doc = load_idf("model.idf")
hw = doc["DistrictHeating"]["Main Heating Plant"]
print(hw.nominal_capacity)
