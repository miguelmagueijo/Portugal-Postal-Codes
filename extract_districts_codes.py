import csv
from time import time as time_now

FILE_ENCODING = "UTF-8"

# Might be useful https://pt.wikipedia.org/wiki/C%C3%B3digo_postal#Portugal

if __name__ == "__main__":
    start = time_now()

    districts_map = dict()

    print("[INFO] Creating districts code dictionary map")
    with open("./ThirdPartyData/distritos.csv", "r", encoding=FILE_ENCODING) as f:
        for row in f.readlines()[1:]:  # skip CSV header
            code, name = row.strip().split(",")

            if int(code) > 18:  # skip Madeira & Açores
                continue

            districts_map[code] = name

    # Manual mapping
    districts_map["31"] = districts_map["32"] = "Região autónoma da Madeira"
    for n in range(41, 50):
        districts_map[str(n)] = "Região autónoma dos Açores"
    print("[INFO] Districts code dictionary map created successfully")

    print("[INFO] Writing districts possible postal codes into CSV")
    written_codes = set()
    with (open("./ThirdPartyData/codigos_postais.csv", "r", encoding=FILE_ENCODING) as pc_file,
          open("./OutputData/districts_postal_codes.csv", "w", encoding=FILE_ENCODING) as dpc_file,
          open("./InputData/missing_district_postal_codes.csv", "r", encoding=FILE_ENCODING) as mdpc_file):
        pc_header_row = pc_file.readline().split(",")
        district_code_idx = pc_header_row.index("cod_distrito")
        postal_code_idx = pc_header_row.index("num_cod_postal")

        dpc_file.write("code,name\n")  # Write output file header

        # Manual file, idx 0 = district code, idx 1 = four digits postal code
        for row in mdpc_file.readlines()[1:]:
            district_code, postal_code = row.split(",")
            dpc_file.write(f"{postal_code},{districts_map[district_code]}\n")

        for row_list in csv.reader(pc_file, delimiter=",", quotechar="\""):
            district_code = row_list[district_code_idx]
            postal_code = row_list[postal_code_idx]

            if postal_code in written_codes:
                continue

            name = ""
            try:
                name = districts_map[district_code]
            except KeyError:
                print(f"[ERROR] No district name found for code \"{district_code}\" (postal code \"{postal_code}\").")
                print("[ASK] Do you wish to input manually a district name? (y/n)")
                answer = input("Answer: ")
                if answer == "y":
                    name = input("District name: ")
                    print(f"[INFO] Postal code \"{postal_code}\" will have \"{name}\" value")
                else:
                    print(f"[INFO] Ignoring code \"{district_code}\" (postal code \"{postal_code}\").")
                    continue

            dpc_file.write(f"{postal_code},{name}\n")
            written_codes.add(postal_code)

        print(f"[INFO] Finished writing districts postal code CSV, took {time_now() - start:.2}s")