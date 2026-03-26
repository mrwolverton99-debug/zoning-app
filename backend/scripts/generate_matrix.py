import csv

DISTRICTS = ["AG","SF-E","SF-10","SF-7","SF-5","SFA","2F","MF","NO","CO","NS","CR","LC","HC","IN","UR","UB"]

matrix = [
    # AGRICULTURAL
    ("Agricultural","Farm, Ranch, Orchard",["P","","","","","","","","","","","","","","","",""],"2/dwelling unit"),
    ("Agricultural","Feed Store",["S","","","","","","","","","","","","","","","",""],"1/250 gfa"),
    ("Agricultural","Stable, Commercial",["P","","","","","","","","","","","","","","","",""],".5/stall"),
    ("Agricultural","Stable, Private",["P","S","","","","","","","","","","","","","","",""],"N/A"),

    # RESIDENTIAL
    ("Residential","Dwelling, Single-Family Detached",["P","P","P","P","P","P","P","P","","","","","","","","",""],"2 enclosed/dwelling unit"),
    ("Residential","Dwelling, Two-Family (duplex)",["","","","","","","P","P","","","","","","","","",""],"2 enclosed/dwelling unit"),
    ("Residential","Dwelling, Multifamily",["","","","","","","","P","*","*","*","*","*","*","","P","P"],"1 space/dwelling unit"),
    ("Residential","Dwelling, Single-Family Attached (Townhouse)",["","","","","","P","P","*","*","*","*","*","*","","","P","P"],"2.25 enclosed/dwelling unit"),
    ("Residential","Dwelling, Apartment",["","","","","","","","","*","*","*","*","*","*","","P","P"],"1 space/dwelling unit"),
    ("Residential","Dwelling, Live/Work",["","","","","","","","","","","","","","","","P","P"],"2 spaces plus nonresidential requirement"),
    ("Residential","Dwelling, Zero-Lot-Line Home",["","","","P","P","","","","","","","","","","","",""],"2 enclosed/dwelling unit"),
    ("Residential","Dwelling, Industrialized Housing Unit",["P","P","P","P","P","P","P","","","","","","","","","",""],"2 enclosed/dwelling unit"),
    ("Residential","Dwelling, Manufactured/HUD-Code Home",["S","","","","","","","","","","","","","","","",""],"2 enclosed/dwelling unit"),
    ("Residential","Dwelling, Mobile Home",["S","","","","","","","","","","","","","","","",""],"2 enclosed/dwelling unit"),
    ("Residential","Accessory Dwelling - Guest House",["S","S","S","S","","","","","","","","","","","","",""],"1/dwelling unit"),
    ("Residential","Accessory Dwelling - Rental Unit",["S","S","","","","","","","","","","","","","","",""],"Efficiency/1BR: 1 space; 2+BR: 2 spaces"),
    ("Residential","Assisted Living",["P","","","","","","","","","","","","","","","","S"],"1/3 dwelling units"),
    ("Residential","Independent Living",["P","P","P","","","","","","","","","","","","","",""],"1/dwelling unit"),
    ("Residential","Nursing/Convalescent Care",["P","","","","","","","","","","","","","","","","S"],".5/bed"),
    ("Residential","Rehabilitation Facility, In Home/Residential",["S","S","S","S","S","S","","","","","","","","","","",""],".2/resident"),

    # INSTITUTIONAL & EDUCATIONAL
    ("Institutional & Educational","Church or Place of Worship",["P","P","P","P","P","P","P","P","P","P","P","P","P","P","P","P","P"],"1/4 seats"),
    ("Institutional & Educational","School, Public",["P","P","P","P","P","P","P","P","P","P","P","P","P","P","P","P","P"],"Elementary/Middle: 1/17 students; High: 1/3 students"),
    ("Institutional & Educational","School, Private/Religious/Charter",["S","S","S","S","S","S","S","S","S","S","S","S","S","S","S","S","S"],"Elementary/Middle: 1/17 students; High: 1/3 students"),
    ("Institutional & Educational","School, Trade",["","","","","","","","","","S","","","P","P","","",""],"1/3 students"),
    ("Institutional & Educational","School, Business",["","","","","","","","","S","P","S","","P","P","P","P",""],"1/3 students"),
    ("Institutional & Educational","School, Retail/Personal Services Training",["","","","","","","","","S","S","S","P","P","P","P","","S"],"1/3 students"),
    ("Institutional & Educational","College or University",["","S","","","","","","","P","P","P","P","S","","P","",""],".5/student (site-specific study required)"),
    ("Institutional & Educational","Convention Facility",["","","","","","","","","S","S","P","P","P","P","","",""],"1/100 gfa"),
    ("Institutional & Educational","Day Care Center, Adult",["","","","","","","","","S","S","S","S","S","S","S","P","P"],"1/3 clients + 1/employee at maximum shift"),
    ("Institutional & Educational","Day Care, Youth - Licensed Child-Care Center",["S","S","S","S","S","S","S","S","P","P","P","P","P","S","S","S",""],"1/10 children + 1/employee at maximum shift"),
    ("Institutional & Educational","Learning Center, Specialized",["","S","","P","","","","","P","P","P","S","S","S","","",""],"1/10 students"),
    ("Institutional & Educational","Makerspace/Hackerspace",["","","","","","","","","","","","","","","P","",""],"1/3 students + 1/500 sf workshop + 1/1000 sf warehouse"),

    # GOVERNMENT & HUMAN SERVICES
    ("Government & Human Services","Post Office",["","","","","","","","","","","","P","P","P","P","P","P"],"1/300 gfa"),
    ("Government & Human Services","Social Service Facility/Agency",["","","","","","","","","","","S","S","P","P","P","",""],"1/300 gfa"),
    ("Government & Human Services","Garden, Civic",["P","P","P","P","P","P","P","P","P","P","","","","","","",""],"2 spaces"),

    # MEDICAL & HEALTH
    ("Medical & Health","Medical and Dental Office/Clinic",["","","","","","","","","P","P","P","P","P","P","P","P","P"],"1/250 gfa"),
    ("Medical & Health","Hospital",["P","","","","","","","","","","","S","","P","P","S",""],"1.5/bed"),
    ("Medical & Health","Mortuary/Funeral Home",["","","","","","","","","","","S","S","S","P","S","",""],"1/200 gfa or 1/4 seats (whichever greater)"),

    # RECREATIONAL
    ("Recreational","Athletic Events Facility, Indoor",["","","","","","","","","S","","P","P","P","P","S","",""],"1/125 gfa or 1/3 bleacher seats (whichever greater)"),
    ("Recreational","Civic Club/Fraternal Lodge",["","","","","","","","","","","P","P","P","P","P","",""],"1/200 gfa"),
    ("Recreational","Commercial Amusement, Indoor",["","","","","","","","","","","P","P","P","P","S","P",""],"1/150 gfa"),
    ("Recreational","Commercial Amusement, Outdoor",["","","","","","","","","","","S","P","P","S","S","",""],"1/1,000 sf of amusement area"),
    ("Recreational","Cultural Facility",["","","","","","","","","P","S","P","P","P","S","P","",""],"1/300 gfa"),
    ("Recreational","Health & Fitness Gym (indoor)",["","","","","","","","","S","","P","P","P","P","S","P","P"],"1/150 gfa"),
    ("Recreational","Reception Facility, Large Scale",["","","","","","","","","","","S","S","S","S","","",""],"1/100 gfa or 1/3 occupants (whichever greater)"),
    ("Recreational","Reception Facility, Small Scale",["","","","","","","","","","","","P","P","P","P","",""],"1/100 gfa or 1/3 occupants (whichever greater)"),
    ("Recreational","Theater, Large Scale",["","","","","","","","","","","S","","P","P","","",""],"1/3 seats"),
    ("Recreational","Theater, Small Scale",["","","","","","","","","","","P","P","P","S","","",""],"1/3 seats"),

    # OFFICE, RETAIL & SERVICE
    ("Office, Retail & Service","Office, General",["","","","","","","","","P","P","P","P","P","P","P","P","P"],"1/300 gfa"),
    ("Office, Retail & Service","Restaurant",["","","","","","","","","","","P","P","P","P","P","P","P"],"1/100 gfa"),
    ("Office, Retail & Service","Restaurant, Drive-Through",["","","","","","","","","","","S","S","S","S","","",""],"1/100 gfa"),
    ("Office, Retail & Service","Retail Store",["","","","","","","","","","","","P","P","P","P","P","P"],"1/333 gfa"),
    ("Office, Retail & Service","Bakery, Retail",["","","","","","","","","S","","P","P","P","P","P","P","P"],"1/250 gfa"),
    ("Office, Retail & Service","Bed and Breakfast",["P","S","S","S","S","","","","","","","","","","","",""],"1/guest room + residential use requirement"),
    ("Office, Retail & Service","Business & Media Service",["","","","","","","","","P","P","P","P","P","P","P","P","P"],"1/300 gfa"),
    ("Office, Retail & Service","Call Center",["","","","","","","","","","","P","P","P","P","P","S",""],"1/150 gfa"),
    ("Office, Retail & Service","Convenience Store (1,000-5,000sf)",["","","","","","","","","S","S","P","P","P","P","S","",""],"1/250 gfa"),
    ("Office, Retail & Service","Financial Institution",["","","","","","","","","P","P","P","P","P","P","P","P","P"],"1/300 gfa"),
    ("Office, Retail & Service","Grocery/Supermarket (>5,000sf)",["","","","","","","","","","","P","P","P","S","S","",""],"1/250 gfa"),
    ("Office, Retail & Service","Hotel/Motel, Full Service",["","","","","","","","","","","S","S","P","P","S","S",""],"1/room + 1/200 sf restaurant/retail/conference"),
    ("Office, Retail & Service","Hotel/Motel, Limited Service",["","","","","","","","","","","S","S","S","S","","",""],"1/room + 1/200 sf restaurant/retail/conference"),
    ("Office, Retail & Service","Hotel/Motel, Extended Stay",["","","","","","","","","","","S","S","S","S","","",""],"1.25/room + 1/200 sf restaurant/retail/conference"),
    ("Office, Retail & Service","Personal Services",["","","","","","","","","S","S","P","P","P","P","S","P","P"],"1/250 gfa"),
    ("Office, Retail & Service","Pet Store (indoors only)",["","","","","","","","","S","","P","P","P","P","P","",""],"1/250 gfa"),
    ("Office, Retail & Service","Pharmacy (with drive-through)",["","","","","","","","","P","S","P","P","P","S","S","",""],"1/250 gfa"),
    ("Office, Retail & Service","Pharmacy (without drive-through)",["","","","","","","","","P","S","P","P","P","P","P","",""],"1/250 gfa"),
    ("Office, Retail & Service","Home Improvement Center (>50,000sf)",["","","","","","","","","","","","","P","P","P","",""],"1/250 gfa"),
    ("Office, Retail & Service","Furniture/Appliance Sales/Rental",["","","","","","","","","","","","","P","P","P","",""],"1/400 gfa"),
    ("Office, Retail & Service","Laundry, Self-Serve (Laundromat)",["","","","","","","","","","","S","S","P","P","S","",""],"1/250 gfa"),
    ("Office, Retail & Service","Laundry, Drop-Off (with drive-through)",["","","","","","","","","","","P","P","P","P","S","S",""],"1/250 gfa"),
    ("Office, Retail & Service","Laundry, Drop-Off (without drive-through)",["","","","","","","","","","","P","P","P","P","S","S",""],"1/250 gfa"),
    ("Office, Retail & Service","Antique Shop (indoors only)",["","","","","","","","","","","","P","P","P","S","",""],"1/250 gfa"),
    ("Office, Retail & Service","Studio, Arts/Crafts",["","","","","","","","","","","","P","P","P","P","P","P"],"1/250 gfa"),
    ("Office, Retail & Service","Studio, Fitness or Performing Arts",["","","","","","","","","","","","P","P","P","P","P","P"],"1/150 gfa"),
    ("Office, Retail & Service","Used Goods, Retail Sales (Indoors)",["","","","","","","","","","","S","","P","P","","",""],"1/250 gfa"),
    ("Office, Retail & Service","Pawn Shop",["","","","","","","","","","","","","","P","","",""],"1/250 gfa"),
    ("Office, Retail & Service","Smoke Shop",["","","","","","","","","","","","","","","S","",""],"1/250 gfa"),
    ("Office, Retail & Service","Sexually Oriented Business",["","","","","","","","","","","","","","P","","",""],"1/250 gfa"),
    ("Office, Retail & Service","Alternative Financial Establishment",["","","","","","","","","","","","","","S","","",""],"1/250 gfa"),
    ("Office, Retail & Service","Tattooing/Body Piercing Establishment",["","","","","","","","","","","S","S","S","","","",""],"1/250 gfa"),

    # COMMERCIAL
    ("Commercial","Contractor's Office/Warehouse (indoors only)",["","","","","","","","","","","","","P","P","P","",""],"1/500 gfa office + 1/1,000 sf warehouse"),
    ("Commercial","Contractor's Office/Storage Yard (outside storage)",["","","","","","","","","","","","","S","S","P","",""],"1/500 gfa office + 1/1,000 sf warehouse"),
    ("Commercial","Bakery, Commercial",["","","","","","","","","","","S","","P","P","","",""],"1/1,000 gfa"),
    ("Commercial","Custom Products Manufacturing",["","","","","","","","","","","S","","P","P","","",""],"1/1,000 gfa"),
    ("Commercial","Equipment Leasing/Rental, Indoor",["","","","","","","","","","","","","P","P","P","P",""],"1/250 gfa"),
    ("Commercial","Pet Care/Play Facility (indoor)",["","","","","","","","","","","S","","P","P","P","S","S"],"1/300 gfa"),
    ("Commercial","Pet Care/Play Facility (outdoor)",["","","","","","","","","","","S","S","P","P","","",""],"1/300 gfa"),
    ("Commercial","Recording Studio/Media Production",["","","","","","","","","","","S","","P","P","P","P","S"],"1/300 gfa"),
    ("Commercial","Self-Storage Facility (mini-warehouse)",["","","","","","","","","","","","","S","S","P","P",""],"1/20 units (1/25 if over 100 units) + 1/300 office gfa"),
    ("Commercial","Veterinary Clinic, Small Animal (indoors only)",["","","","","","","","","S","","P","S","P","P","P","P","P"],"1/300 gfa"),
    ("Commercial","Veterinary Clinic, Small Animal (outdoor kennels)",["","","","","","","","","","","S","S","P","P","","",""],"1/300 gfa"),
    ("Commercial","Commercial Drone Delivery Hub (small)",["","","","","","","","","","","S","S","S","S","","",""],"Determined by SUP"),
    ("Commercial","Commercial Drone Delivery Hub (large)",["","","","","","","","","","","","","","S","","",""],"Determined by SUP"),

    # MOTOR VEHICLE
    ("Motor Vehicle","Automobile Leasing/Rental",["","","","","","","","","","","S","P","P","P","P","P",""],"1/400 gfa"),
    ("Motor Vehicle","Automobile Repair, Major",["","","","","","","","","","","S","","P","P","","",""],"1/400 gfa + 2/repair bay"),
    ("Motor Vehicle","Automobile Repair, Minor",["","","","","","","","","","","S","S","P","P","P","",""],"1/400 gfa + 2/repair bay"),
    ("Motor Vehicle","Automobile Sales, New or Used",["","","","","","","","","","","S","","P","S","","",""],"1/400 gfa (min 2 spaces) + 1/employee on site"),
    ("Motor Vehicle","Car Wash, Automated/Rollover",["","","","","","","","","","","S","S","P","P","P","",""],"1/200 gfa"),
    ("Motor Vehicle","Car Wash, Full-Service/Detail",["","","","","","","","","","","S","P","P","P","","",""],"1/200 gfa"),
    ("Motor Vehicle","Car Wash, Self-Service/Wand",["","","","","","","","","","","S","","P","P","","",""],"1/bay"),
    ("Motor Vehicle","Parking Lot or Garage, Commercial",["","","","","","","","","P","P","P","P","P","P","P","",""],"1/300 office gfa"),
    ("Motor Vehicle","Wrecker/Towing Service",["","","","","","","","","","","","","P","P","","",""],"1/300 office gfa + 1/wrecker"),

    # TRANSPORTATION
    ("Transportation","Bus Stop",["P","P","P","P","P","P","P","P","P","P","P","P","P","P","P","P","P"],"N/A"),
    ("Transportation","Transit Station, Public",["","","","","","","","","P","P","P","P","P","P","P","",""],"Determined by operating agency"),

    # INDUSTRIAL
    ("Industrial","Data Center",["","","","","","","","","","","","","S","","P","P","S"],"1/5,000 gfa"),
    ("Industrial","Distribution Center, Large (indoors only)",["","","","","","","","","","","","","S","","P","",""],"1/300 office gfa + 1/1,000 remainder gfa"),
    ("Industrial","Distribution Center, Small (indoors only)",["","","","","","","","","","","","","S","","P","P",""],"1/300 office gfa + 1/1,000 remainder gfa"),
    ("Industrial","Industrial or Manufacturing, Heavy",["","","","","","","","","","","","","","","S","",""],"1/1,000 gfa or 5 visitors + 1/employee at max shift"),
    ("Industrial","Industrial or Manufacturing, Light",["","","","","","","","","","","","","","","P","",""],"1/1,000 gfa or 5 visitors + 1/employee at max shift"),
    ("Industrial","Warehouse, Office/Showroom (indoors only)",["","","","","","","","","","","","","S","","P","P","P"],"1/300 office gfa + 1/1,000 remainder gfa"),
    ("Industrial","Breweries/Wineries/Distilleries",["","","","","","","","","","","","","S","S","P","S","S"],"1/1,000 gfa or 5 visitors + 1/employee at max shift; 1/100 gfa for dining/tasting areas"),
    ("Industrial","Laboratory, Analytical or Research (indoor)",["","","","","","","","","","","","","S","S","P","P","P"],"1/1,000 gfa or 5 visitors + 1/employee at max shift"),

    # UTILITY
    ("Utility","Electric Substation",["S","S","S","S","S","S","S","S","S","S","S","S","S","S","S","",""],"1/employee at maximum shift"),
    ("Utility","Telecommunications Switching Station",["","","","","","","","","","","","","","","P","",""],"1/employee at maximum shift"),
    ("Utility","Antenna, Commercial",["*","S","S","S","S","S","S","S","S","S","S","S","P","P","S","S","S"],"N/A"),
]

with open('data/garland_land_use_matrix.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['category', 'use_name'] + DISTRICTS + ['parking'])
    for row in matrix:
        category, use_name, statuses, parking = row
        padded = (statuses + [''] * 17)[:17]
        writer.writerow([category, use_name] + padded + [parking])

print(f"Done — wrote {len(matrix)} land uses to data/garland_land_use_matrix.csv")