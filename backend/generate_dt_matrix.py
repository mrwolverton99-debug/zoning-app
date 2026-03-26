import csv

# Column order from GDC Table 7-1: DH, DS, U, IR, SC
DT_DISTRICTS = ["DH", "DS", "U", "IR", "SC"]

# (category, use_name, [DH, DS, U, IR, SC])
dt_matrix = [
    # RESIDENTIAL - ACCESSORY DWELLINGS
    ("Residential", "Dwelling, Accessory - Guest House", ["P","","P","P","P"]),
    ("Residential", "Dwelling, Accessory - Rental Unit", ["P","","P","P","P"]),
    ("Residential", "Dwelling, Accessory - Guard/Manager/Caretaker", ["P","","P","P","P"]),

    # ELDER CARE — confirmed from PDF: DH DS U IR SC
    ("Residential", "Elder Care - Independent Living", ["","","P","","P"]),
    ("Residential", "Elder Care - Assisted Living", ["","","","","P"]),
    ("Residential", "Elder Care - Nursing/Convalescent Care", ["","","","","P"]),
    ("Residential", "Elder Care - Continuing Care", ["","","","","P"]),

    # HOUSEHOLD LIVING
    ("Residential", "Dwelling, Two-Family (duplex)", ["","","P","P",""]),
    ("Residential", "Dwelling, Multi-Family", ["P","S","P","","P"]),
    ("Residential", "Dwelling, Live-Work unit", ["P","P","P","P","P"]),
    ("Residential", "Dwelling, Single-Family Detached", ["","","P","P",""]),
    ("Residential", "Dwelling, Single-Family Attached (Townhouse)", ["","","P","P",""]),
    ("Residential", "Dwelling, Apartment", ["P","S","P","P","P"]),

    # ACCESSORY & TEMPORARY
    ("Accessory & Temporary", "Accessory Structure, Residential", ["P","P","P","P",""]),
    ("Accessory & Temporary", "Drive-In Service", ["","","","","S"]),
    ("Accessory & Temporary", "Drive-Through Service", ["","S","","","S"]),
    ("Accessory & Temporary", "Walk-Up Service", ["P","P","P","P",""]),
    ("Accessory & Temporary", "Fuel Pumps, Retail", ["","","","","S"]),
    ("Accessory & Temporary", "ATM, Drive-Up", ["","S","","","S"]),
    ("Accessory & Temporary", "ATM, Walk-Up", ["P","P","P","P",""]),
    ("Accessory & Temporary", "Outside Display, New Materials", ["P","P","P","P",""]),
    ("Accessory & Temporary", "Outside Display, Used Materials", ["S","S","S","S",""]),
    ("Accessory & Temporary", "Outside Storage, New Materials", ["","P","","","P"]),
    ("Accessory & Temporary", "Outside Storage, Used Materials", ["","S","","","S"]),
    ("Accessory & Temporary", "Seasonal Sales", ["","","","","S"]),

    # INSTITUTIONAL & EDUCATIONAL
    ("Institutional & Educational", "College or University", ["P","P","P","",""]),
    ("Institutional & Educational", "Convention Facility", ["","P","","","P"]),
    ("Institutional & Educational", "Day Care Center, Adult", ["P","P","S","P",""]),
    ("Institutional & Educational", "Day Care, Youth - Licensed Child-Care Center", ["P","P","S","P",""]),
    ("Institutional & Educational", "Day Care, Youth - Registered Child-Care Home", ["P","P","S","P",""]),
    ("Institutional & Educational", "Church or Place of Worship", ["P","P","P","P","P"]),
    ("Institutional & Educational", "Learning Center, Specialized", ["P","P","P","",""]),
    ("Institutional & Educational", "School, Business", ["P","P","P","",""]),
    ("Institutional & Educational", "School, Retail/Personal Services Training", ["P","P","P","",""]),
    ("Institutional & Educational", "School, Trade", ["","","S","",""]),
    ("Institutional & Educational", "School, Public", ["P","P","P","P",""]),
    ("Institutional & Educational", "School, Private, Religious or Charter", ["S","S","S","S",""]),

    # GOVERNMENT & HUMAN SERVICES
    ("Government & Human Services", "Charitable Boarding", ["S","S","S","S",""]),
    ("Government & Human Services", "Garden, Charitable", ["S","S","S","S",""]),
    ("Government & Human Services", "Garden, Civic", ["P","P","P","P",""]),
    ("Government & Human Services", "Post Office", ["","P","","","P"]),
    ("Government & Human Services", "Social Service Facility/Agency", ["P","P","P","",""]),

    # MEDICAL & HEALTH
    ("Medical & Health", "Hospital", ["","","","","P"]),
    ("Medical & Health", "Medical and Dental Office/Clinic", ["P","P","P","",""]),
    ("Medical & Health", "Mortuary/Funeral Home", ["P","P","P","",""]),

    # RECREATIONAL
    ("Recreational", "Athletic Events Facility, Indoor", ["","","S","",""]),
    ("Recreational", "Civic Club/Fraternal Lodge", ["P","P","P","",""]),
    ("Recreational", "Commercial Amusement, Indoor", ["P","P","P","P",""]),
    ("Recreational", "Commercial Amusement, Outdoor", ["","S","","","S"]),
    ("Recreational", "Public Amusement, Temporary", ["S","S","S","",""]),
    ("Recreational", "Cultural Facility", ["P","P","P","P",""]),
    ("Recreational", "Health & Fitness Gym (indoor)", ["P","S","P","P",""]),
    ("Recreational", "Reception Facility, Large Scale", ["S","S","S","",""]),
    ("Recreational", "Reception Facility, Small Scale", ["P","P","P","",""]),
    ("Recreational", "Theater, Small Scale", ["P","P","P","",""]),
    ("Recreational", "Theater, Large Scale", ["","P","","",""]),

    # OFFICE, RETAIL & SERVICE
    ("Office, Retail & Service", "Antique Shop (indoors only)", ["P","P","P","P","P"]),
    ("Office, Retail & Service", "Bakery, Retail", ["P","P","P","P",""]),
    ("Office, Retail & Service", "Bed and Breakfast", ["S","S","P","S",""]),
    ("Office, Retail & Service", "Business & Media Service", ["P","P","P","",""]),
    ("Office, Retail & Service", "Call Center", ["","S","","","P"]),
    ("Office, Retail & Service", "Convenience Store (1,000-5,000sf)", ["P","S","P","P",""]),
    ("Office, Retail & Service", "Financial Institution", ["P","P","P","P",""]),
    ("Office, Retail & Service", "Flea Market, Indoor", ["S","S","S","",""]),
    ("Office, Retail & Service", "Flea Market, Outdoor", ["S","S","S","",""]),
    ("Office, Retail & Service", "Furniture, Household Furnishings and Appliance Sales/Rental", ["P","S","P","P",""]),
    ("Office, Retail & Service", "Grocery/Supermarket (>5,000sf)", ["P","P","P","",""]),
    ("Office, Retail & Service", "Home Improvement Center (>50,000sf)", ["","S","","","P"]),
    ("Office, Retail & Service", "Hotel/Motel, Extended Stay", ["P","P","P","",""]),
    ("Office, Retail & Service", "Hotel/Motel, Full Service", ["P","S","P","P",""]),
    ("Office, Retail & Service", "Hotel/Motel, Limited Service", ["P","S","P","P",""]),
    ("Office, Retail & Service", "Indoor Shopping Mall", ["S","S","S","",""]),
    ("Office, Retail & Service", "Landscape Nursery (retail)", ["","","","","P"]),
    ("Office, Retail & Service", "Laundry, Self-Serve (Laundromat)", ["P","P","P","",""]),
    ("Office, Retail & Service", "Laundry, Drop-Off (with drive-through)", ["","S","","","P"]),
    ("Office, Retail & Service", "Laundry, Drop-Off (without drive-through)", ["P","P","P","",""]),
    ("Office, Retail & Service", "Mobile Food Truck Park", ["S","S","S","S",""]),
    ("Office, Retail & Service", "Office, General", ["P","S","P","P","P"]),
    ("Office, Retail & Service", "Personal Services", ["P","S","P","P","P"]),
    ("Office, Retail & Service", "Pet Store (indoors only)", ["","S","P","P",""]),
    ("Office, Retail & Service", "Pharmacy (with drive-through)", ["","S","","","P"]),
    ("Office, Retail & Service", "Pharmacy (without drive-through)", ["P","S","P","P",""]),
    ("Office, Retail & Service", "Produce Stand/Outdoor Farmers Market", ["S","S","S","S",""]),
    ("Office, Retail & Service", "Restaurant", ["P","P","P","P","P"]),
    ("Office, Retail & Service", "Restaurant, Drive-Through", ["","","","","S"]),
    ("Office, Retail & Service", "Retail Store", ["P","P","P","P","P"]),
    ("Office, Retail & Service", "Retail/Service", ["","S","P","","P"]),
    ("Office, Retail & Service", "Studio, Arts/Crafts", ["P","P","P","P","P"]),
    ("Office, Retail & Service", "Studio, Fitness or Performing Arts", ["P","S","P","P","P"]),
    ("Office, Retail & Service", "Used Goods, Retail Sales (Indoors)", ["P","P","P","P",""]),
    ("Office, Retail & Service", "Tattooing/Body Piercing Establishment", ["S","S","S","S",""]),

    # COMMERCIAL
    ("Commercial", "Bakery, Commercial", ["P","","","","P"]),
    ("Commercial", "Building/Garden Materials Sales & Storage (wholesale)", ["","","","","S"]),
    ("Commercial", "Bulk Material Sales & Storage", ["","","","","S"]),
    ("Commercial", "Contractor's Office/Warehouse (indoors only)", ["","","","","S"]),
    ("Commercial", "Equipment Leasing/Rental, Indoor", ["","","","","P"]),
    ("Commercial", "Furniture and Appliance Cleaning/Repair", ["","","","","S"]),
    ("Commercial", "Pet Care/Play Facility (indoor)", ["S","","","","S"]),
    ("Commercial", "Printing/Publishing House", ["S","","","","P"]),
    ("Commercial", "Recording Studio/Media Production", ["P","","","","P"]),
    ("Commercial", "Small Engine/Lawn Equipment Rental & Repair (indoors)", ["P","","","","P"]),
    ("Commercial", "Veterinary Clinic, Small Animal (indoors only)", ["P","","","","P"]),

    # MOTOR VEHICLES
    ("Motor Vehicle", "Parking Lot or Garage, Commercial", ["P","P","P","",""]),

    # TRANSPORTATION
    ("Transportation", "Bus Stop", ["P","P","P","P","P"]),
    ("Transportation", "Helipad", ["","","S","",""]),
    ("Transportation", "Transit Station, Public", ["P","S","P","P",""]),
    ("Transportation", "Transportation Depot, Passenger", ["","S","","","S"]),

    # INDUSTRIAL
    ("Industrial", "Batching Plant, Temporary", ["P","P","P","P",""]),
    ("Industrial", "Breweries/Wineries/Distilleries", ["S","S","S","S",""]),
    ("Industrial", "Laboratory, Analytical or Research (indoor)", ["","","","","S"]),
    ("Industrial", "Warehouse, Office/Showroom (indoors only)", ["","","","","S"]),

    # UTILITY
    ("Utility", "Antenna, Commercial", ["*","*","*","*",""]),
    ("Utility", "Antenna, Private", ["P","P","P","P",""]),
    ("Utility", "Electric Substation", ["","S","","","S"]),
    ("Utility", "Gas Regulating Station", ["S","S","S","S",""]),
    ("Utility", "Telecommunication Switching Station", ["S","S","S","S",""]),
]

with open('data/garland_dt_land_use_matrix.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['category', 'use_name'] + DT_DISTRICTS)
    for row in dt_matrix:
        category, use_name, statuses = row
        padded = (statuses + [''] * 5)[:5]
        writer.writerow([category, use_name] + padded)

print(f"Done — wrote {len(dt_matrix)} downtown uses to data/garland_dt_land_use_matrix.csv")