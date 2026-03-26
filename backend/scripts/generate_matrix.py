import csv

DISTRICTS = ["AG","SF-E","SF-10","SF-7","SF-5","SFA","2F","MF","NO","CO","NS","CR","LC","HC","IN","UR","UB"]

matrix = [
    # AGRICULTURAL
    ("Agricultural","Farm, Ranch, Orchard",["P","","","","","","","","","","","","","","","",""]),
    ("Agricultural","Feed Store",["S","","","","","","","","","","","","","","","",""]),
    ("Agricultural","Stable, Commercial",["P","","","","","","","","","","","","","","","",""]),
    ("Agricultural","Stable, Private",["P","S","","","","","","","","","","","","","","",""]),

    # RESIDENTIAL
    ("Residential","Dwelling, Single-Family Detached",["P","P","P","P","P","P","P","P","","","","","","","","",""]),
    ("Residential","Dwelling, Two-Family (duplex)",["","","","","","","P","P","","","","","","","","",""]),
    ("Residential","Dwelling, Multifamily",["","","","","","","","P","*","*","*","*","*","*","","P","P"]),
    ("Residential","Dwelling, Single-Family Attached (Townhouse)",["","","","","","P","P","*","*","*","*","*","*","","","P","P"]),
    ("Residential","Dwelling, Apartment",["","","","","","","","","*","*","*","*","*","*","","P","P"]),
    ("Residential","Dwelling, Live/Work",["","","","","","","","","","","","","","","","P","P"]),
    ("Residential","Dwelling, Zero-Lot-Line Home",["","","","P","P","","","","","","","","","","","",""]),
    ("Residential","Dwelling, Industrialized Housing Unit",["P","P","P","P","P","P","P","","","","","","","","","",""]),
    ("Residential","Dwelling, Manufactured/HUD-Code Home",["S","","","","","","","","","","","","","","","",""]),
    ("Residential","Dwelling, Mobile Home",["S","","","","","","","","","","","","","","","",""]),
    ("Residential","Accessory Dwelling - Guest House",["S","S","S","S","","","","","","","","","","","","",""]),
    ("Residential","Accessory Dwelling - Rental Unit",["S","S","","","","","","","","","","","","","","",""]),
    ("Residential","Assisted Living",["P","","","","","","","","","","","","","","","","S"]),
    ("Residential","Independent Living",["P","P","P","","","","","","","","","","","","","",""]),
    ("Residential","Nursing/Convalescent Care",["P","","","","","","","","","","","","","","","","S"]),
    ("Residential","Rehabilitation Facility, In Home/Residential",["S","S","S","S","S","S","","","","","","","","","","",""]),

    # INSTITUTIONAL & EDUCATIONAL
    ("Institutional & Educational","Church or Place of Worship",["P","P","P","P","P","P","P","P","P","P","P","P","P","P","P","P","P"]),
    ("Institutional & Educational","School, Public",["P","P","P","P","P","P","P","P","P","P","P","P","P","P","P","P","P"]),
    ("Institutional & Educational","School, Private/Religious/Charter",["S","S","S","S","S","S","S","S","S","S","S","S","S","S","S","S","S"]),
    ("Institutional & Educational","School, Trade",["","","","","","","","","","S","","","P","P","","",""]),
    ("Institutional & Educational","School, Business",["","","","","","","","","S","P","S","","P","P","P","P",""]),
    ("Institutional & Educational","School, Retail/Personal Services Training",["","","","","","","","","S","S","S","P","P","P","P","","S"]),
    ("Institutional & Educational","College or University",["","S","","","","","","","P","P","P","P","S","","P","",""]),
    ("Institutional & Educational","Convention Facility",["","","","","","","","","S","S","P","P","P","P","","",""]),
    ("Institutional & Educational","Day Care Center, Adult",["","","","","","","","","S","S","S","S","S","S","S","P","P"]),
    ("Institutional & Educational","Day Care, Youth - Licensed Child-Care Center",["S","S","S","S","S","S","S","S","P","P","P","P","P","S","S","S",""]),
    ("Institutional & Educational","Learning Center, Specialized",["","S","","P","","","","","P","P","P","S","S","S","","",""]),
    ("Institutional & Educational","Makerspace/Hackerspace",["","","","","","","","","","","","","","","P","",""]),

    # GOVERNMENT & HUMAN SERVICES
    ("Government & Human Services","Post Office",["","","","","","","","","","","","P","P","P","P","P","P"]),
    ("Government & Human Services","Social Service Facility/Agency",["","","","","","","","","","","S","S","P","P","P","",""]),
    ("Government & Human Services","Garden, Civic",["P","P","P","P","P","P","P","P","P","P","","","","","","",""]),

    # MEDICAL & HEALTH
    ("Medical & Health","Medical and Dental Office/Clinic",["","","","","","","","","P","P","P","P","P","P","P","P","P"]),
    ("Medical & Health","Hospital",["P","","","","","","","","","","","S","","P","P","S",""]),
    ("Medical & Health","Mortuary/Funeral Home",["","","","","","","","","","","S","S","S","P","S","",""]),

    # RECREATIONAL
    ("Recreational","Athletic Events Facility, Indoor",["","","","","","","","","S","","P","P","P","P","S","",""]),
    ("Recreational","Civic Club/Fraternal Lodge",["","","","","","","","","","","P","P","P","P","P","",""]),
    ("Recreational","Commercial Amusement, Indoor",["","","","","","","","","","","P","P","P","P","S","P",""]),
    ("Recreational","Commercial Amusement, Outdoor",["","","","","","","","","","","S","P","P","S","S","",""]),
    ("Recreational","Cultural Facility",["","","","","","","","","P","S","P","P","P","S","P","",""]),
    ("Recreational","Health & Fitness Gym (indoor)",["","","","","","","","","S","","P","P","P","P","S","P","P"]),
    ("Recreational","Reception Facility, Large Scale",["","","","","","","","","","","S","S","S","S","","",""]),
    ("Recreational","Reception Facility, Small Scale",["","","","","","","","","","","","P","P","P","P","",""]),
    ("Recreational","Theater, Large Scale",["","","","","","","","","","","S","","P","P","","",""]),
    ("Recreational","Theater, Small Scale",["","","","","","","","","","","P","P","P","S","","",""]),

    # OFFICE, RETAIL & SERVICE
    ("Office, Retail & Service","Office, General",["","","","","","","","","P","P","P","P","P","P","P","P","P"]),
    ("Office, Retail & Service","Restaurant",["","","","","","","","","","","P","P","P","P","P","P","P"]),
    ("Office, Retail & Service","Restaurant, Drive-Through",["","","","","","","","","","","S","S","S","S","","",""]),
    ("Office, Retail & Service","Retail Store",["","","","","","","","","","","","P","P","P","P","P","P"]),
    ("Office, Retail & Service","Bakery, Retail",["","","","","","","","","S","","P","P","P","P","P","P","P"]),
    ("Office, Retail & Service","Bed and Breakfast",["P","S","S","S","S","","","","","","","","","","","",""]),
    ("Office, Retail & Service","Business & Media Service",["","","","","","","","","P","P","P","P","P","P","P","P","P"]),
    ("Office, Retail & Service","Call Center",["","","","","","","","","","","P","P","P","P","P","S",""]),
    ("Office, Retail & Service","Convenience Store (1,000-5,000sf)",["","","","","","","","","S","S","P","P","P","P","S","",""]),
    ("Office, Retail & Service","Financial Institution",["","","","","","","","","P","P","P","P","P","P","P","P","P"]),
    ("Office, Retail & Service","Grocery/Supermarket (>5,000sf)",["","","","","","","","","","","P","P","P","S","S","",""]),
    ("Office, Retail & Service","Hotel/Motel, Full Service",["","","","","","","","","","","S","S","P","P","S","S",""]),
    ("Office, Retail & Service","Hotel/Motel, Limited Service",["","","","","","","","","","","S","S","S","S","","",""]),
    ("Office, Retail & Service","Hotel/Motel, Extended Stay",["","","","","","","","","","","S","S","S","S","","",""]),
    ("Office, Retail & Service","Personal Services",["","","","","","","","","S","S","P","P","P","P","S","P","P"]),
    ("Office, Retail & Service","Pet Store (indoors only)",["","","","","","","","","S","","P","P","P","P","P","",""]),
    ("Office, Retail & Service","Pharmacy (with drive-through)",["","","","","","","","","P","S","P","P","P","S","S","",""]),
    ("Office, Retail & Service","Pharmacy (without drive-through)",["","","","","","","","","P","S","P","P","P","P","P","",""]),
    ("Office, Retail & Service","Home Improvement Center (>50,000sf)",["","","","","","","","","","","","","P","P","P","",""]),
    ("Office, Retail & Service","Furniture/Appliance Sales/Rental",["","","","","","","","","","","","","P","P","P","",""]),
    ("Office, Retail & Service","Laundry, Self-Serve (Laundromat)",["","","","","","","","","","","S","S","P","P","S","",""]),
    ("Office, Retail & Service","Laundry, Drop-Off (with drive-through)",["","","","","","","","","","","P","P","P","P","S","S",""]),
    ("Office, Retail & Service","Laundry, Drop-Off (without drive-through)",["","","","","","","","","","","P","P","P","P","S","S",""]),
    ("Office, Retail & Service","Antique Shop (indoors only)",["","","","","","","","","","","","P","P","P","S","",""]),
    ("Office, Retail & Service","Studio, Arts/Crafts",["","","","","","","","","","","","P","P","P","P","P","P"]),
    ("Office, Retail & Service","Studio, Fitness or Performing Arts",["","","","","","","","","","","","P","P","P","P","P","P"]),
    ("Office, Retail & Service","Used Goods, Retail Sales (Indoors)",["","","","","","","","","","","S","","P","P","","",""]),
    ("Office, Retail & Service","Pawn Shop",["","","","","","","","","","","","","","P","","",""]),
    ("Office, Retail & Service","Smoke Shop",["","","","","","","","","","","","","","","S","",""]),
    ("Office, Retail & Service","Sexually Oriented Business",["","","","","","","","","","","","","","P","","",""]),
    ("Office, Retail & Service","Alternative Financial Establishment",["","","","","","","","","","","","","","S","","",""]),
    ("Office, Retail & Service","Tattooing/Body Piercing Establishment",["","","","","","","","","","","S","S","S","","","",""]),

    # COMMERCIAL
    ("Commercial","Contractor's Office/Warehouse (indoors only)",["","","","","","","","","","","","","P","P","P","",""]),
    ("Commercial","Contractor's Office/Storage Yard (outside storage)",["","","","","","","","","","","","","S","S","P","",""]),
    ("Commercial","Bakery, Commercial",["","","","","","","","","","","S","","P","P","","",""]),
    ("Commercial","Custom Products Manufacturing",["","","","","","","","","","","S","","P","P","","",""]),
    ("Commercial","Equipment Leasing/Rental, Indoor",["","","","","","","","","","","","","P","P","P","P",""]),
    ("Commercial","Pet Care/Play Facility (indoor)",["","","","","","","","","","","S","","P","P","P","S","S"]),
    ("Commercial","Pet Care/Play Facility (outdoor)",["","","","","","","","","","","S","S","P","P","","",""]),
    ("Commercial","Recording Studio/Media Production",["","","","","","","","","","","S","","P","P","P","P","S"]),
    ("Commercial","Self-Storage Facility (mini-warehouse)",["","","","","","","","","","","","","S","S","P","P",""]),
    ("Commercial","Veterinary Clinic, Small Animal (indoors only)",["","","","","","","","","S","","P","S","P","P","P","P","P"]),
    ("Commercial","Veterinary Clinic, Small Animal (outdoor kennels)",["","","","","","","","","","","S","S","P","P","","",""]),
    ("Commercial","Commercial Drone Delivery Hub (small)",["","","","","","","","","","","S","S","S","S","","",""]),
    ("Commercial","Commercial Drone Delivery Hub (large)",["","","","","","","","","","","","","","S","","",""]),

    # MOTOR VEHICLE
    ("Motor Vehicle","Automobile Leasing/Rental",["","","","","","","","","","","S","P","P","P","P","P",""]),
    ("Motor Vehicle","Automobile Repair, Major",["","","","","","","","","","","S","","P","P","","",""]),
    ("Motor Vehicle","Automobile Repair, Minor",["","","","","","","","","","","S","S","P","P","P","",""]),
    ("Motor Vehicle","Automobile Sales, New or Used",["","","","","","","","","","","S","","P","S","","",""]),
    ("Motor Vehicle","Car Wash, Automated/Rollover",["","","","","","","","","","","S","S","P","P","P","",""]),
    ("Motor Vehicle","Car Wash, Full-Service/Detail",["","","","","","","","","","","S","P","P","P","","",""]),
    ("Motor Vehicle","Car Wash, Self-Service/Wand",["","","","","","","","","","","S","","P","P","","",""]),
    ("Motor Vehicle","Parking Lot or Garage, Commercial",["","","","","","","","","P","P","P","P","P","P","P","",""]),
    ("Motor Vehicle","Wrecker/Towing Service",["","","","","","","","","","","","","P","P","","",""]),

    # TRANSPORTATION
    ("Transportation","Bus Stop",["P","P","P","P","P","P","P","P","P","P","P","P","P","P","P","P","P"]),
    ("Transportation","Transit Station, Public",["","","","","","","","","P","P","P","P","P","P","P","",""]),

    # INDUSTRIAL
    ("Industrial","Data Center",["","","","","","","","","","","","","S","","P","P","S"]),
    ("Industrial","Distribution Center, Large (indoors only)",["","","","","","","","","","","","","S","","P","",""]),
    ("Industrial","Distribution Center, Small (indoors only)",["","","","","","","","","","","","","S","","P","P",""]),
    ("Industrial","Industrial or Manufacturing, Heavy",["","","","","","","","","","","","","","","S","",""]),
    ("Industrial","Industrial or Manufacturing, Light",["","","","","","","","","","","","","","","P","",""]),
    ("Industrial","Warehouse, Office/Showroom (indoors only)",["","","","","","","","","","","","","S","","P","P","P"]),
    ("Industrial","Breweries/Wineries/Distilleries",["","","","","","","","","","","","","S","S","P","S","S"]),
    ("Industrial","Laboratory, Analytical or Research (indoor)",["","","","","","","","","","","","","S","S","P","P","P"]),

    # UTILITY
    ("Utility","Electric Substation",["S","S","S","S","S","S","S","S","S","S","S","S","S","S","S","",""]),
    ("Utility","Telecommunications Switching Station",["","","","","","","","","","","","","","","P","",""]),
    ("Utility","Antenna, Commercial",["*","S","S","S","S","S","S","S","S","S","S","S","P","P","S","S","S"]),
]

with open('data/garland_land_use_matrix.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['category', 'use_name'] + DISTRICTS)
    for row in matrix:
        category, use_name, statuses = row
        padded = (statuses + [''] * 17)[:17]
        writer.writerow([category, use_name] + padded)

print(f"Done — wrote {len(matrix)} land uses to data/garland_land_use_matrix.csv")