from pyunpack import Archive
import xmltodict
import platform
import shutil
import json
import os


# if the passed in key does not exist, return an empty string for the value
def get_key_if_exists(key, _dict):
    if type(_dict) != dict:
        return ""

    if key in _dict.keys():
        return _dict[key]
    else:
        return ""


sep = '\\'
system_type = platform.platform()
if system_type.find('mac') != -1 or system_type.find('linux') != -1:
    sep = '/'

target_path = os.path.dirname(os.path.realpath('__file__'))

csv_header = [
    "MasterPortfolioId",
    "CurrencyId",
    "Date",
    "PreviousPortfolioDate",
    "SalePosition",
    "NumberOfHolding",
    "NumberOfStockHolding",
    "NumberOfBondHolding",
    "TotalMarketValue",
    "HoldingId",
    "HoldingTypeId",
    "ExternalName",
    "StorageId",
    "CountryId",
    "Country",
    "CUSIP",
    "CurrencyId",
    "Currency",
    "SecurityName",
    "Weighting",
    "NumberOfShare",
    "MarketValue",
    "CostBasis",
    "ShareChange",
    "SectorId",
    "Sector",
    "IndustryId",
    "GlobalIndustryId",
    "GlobalSector",
    "GICSIndustryId"
]

target_zip_files = []

print("Creating ~temp directory...")
temp_directory = target_path + sep + "~temp"
if not os.path.exists(temp_directory):
    os.makedirs(temp_directory)

print("Getting list of .zip or .7z files...")
for file in os.listdir(target_path):
    if file.endswith(".7z") or file.endswith(".zip"):
        print("     -> " + file)
        target_zip_files.append(os.path.join(target_path, file))

for zip_file in target_zip_files:
    file_name = list(reversed(str(zip_file).split(sep)))[0]
    zip_dir = temp_directory + sep + file_name
    zip_ext = '.7z'
    if zip_dir.find('.zip') != -1:
        zip_ext = '.zip'
        zip_dir = zip_dir.replace('.zip', '')
    elif zip_file.find('.7z') != -1:
        zip_dir = zip_dir.replace('.7z', '')

    if not os.path.exists(zip_dir):
        os.makedirs(zip_dir)

    print("Extracting " + zip_file + " to ~temp directory...")
    Archive(zip_file).extractall(zip_dir)

    csv_file = file_name.replace(zip_ext, '.csv')

    try:
        os.remove(csv_file)
    except OSError:
        pass

    xml_csv = open(csv_file, 'w')
    xml_csv.write(",".join(csv_header) + "\n")

    print("Parsing XML files in " + zip_file)
    for i, file in enumerate(os.listdir(zip_dir)):
        if file.endswith('.xml'):
            print("     -> " + file)

            json_dict = json.loads(json.dumps(xmltodict.parse(open(os.path.join(zip_dir, file), 'r', encoding='utf-8-sig').read())))
            portfolio = json_dict['Portfolio']
            master_portfolio_id = get_key_if_exists('@_MasterPortfolioId', portfolio)
            currency_id = get_key_if_exists('@_CurrencyId', portfolio)

            summary = portfolio['PortfolioSummary']
            date = get_key_if_exists('Date', summary)
            previous_portfolio_date = get_key_if_exists('PreviousPortfolioDate', summary)

            holding_aggregate = summary['HoldingAggregate']
            sale_position = get_key_if_exists('@_SalePosition', holding_aggregate)
            number_of_holding = get_key_if_exists('NumberOfHolding', holding_aggregate)
            number_of_stock_holding = get_key_if_exists('NumberOfStockHolding', holding_aggregate)
            number_of_bond_holding = get_key_if_exists('NumberOfBondHolding', holding_aggregate)
            total_market_value = get_key_if_exists('TotalMarketValue', holding_aggregate)

            level_1_str = ",".join([
                master_portfolio_id,
                currency_id,
                date,
                previous_portfolio_date,
                sale_position,
                number_of_holding,
                number_of_stock_holding,
                number_of_bond_holding,
                total_market_value
            ])

            level_2_strs = []
            for detail in portfolio['Holding']['HoldingDetail']:
                holding_id = get_key_if_exists('@_Id', detail)
                holding_type_id = get_key_if_exists('@_DetailHoldingTypeId', detail)
                external_name = get_key_if_exists('@ExternalName', detail)
                storage_id = get_key_if_exists('@_StorageId', detail)
                country_id = get_key_if_exists('@_Id', get_key_if_exists('Country', detail))
                country = get_key_if_exists('#text', get_key_if_exists('Country', detail))
                cusip = get_key_if_exists('CUSIP', detail)
                currency_id = get_key_if_exists('@_Id', get_key_if_exists('Currency', detail))
                currency = get_key_if_exists('#text', get_key_if_exists('Currency', detail))
                security_name = get_key_if_exists('SecurityName', detail)
                weighting = get_key_if_exists('Weighting', detail)
                number_of_share = get_key_if_exists('NumberOfShare', detail)
                market_value = get_key_if_exists('MarketValue', detail)
                cost_basis = get_key_if_exists('CostBasis', detail)
                share_change = get_key_if_exists('ShareChange', detail)
                sector_id = get_key_if_exists('@_Id', get_key_if_exists('Sector', detail))
                sector = get_key_if_exists('#text', get_key_if_exists('Sector', detail))
                industry_id = get_key_if_exists('IndustryId', detail)
                global_industry_id = get_key_if_exists('GlobalIndustryId', detail)
                global_sector = get_key_if_exists('GlobalSector', detail)
                gics_industry_id = get_key_if_exists('GICSIndustryId', detail)

                level_2_strs.append(",".join([
                    holding_id,
                    holding_type_id,
                    external_name,
                    storage_id,
                    country_id,
                    country,
                    cusip,
                    currency_id,
                    currency,
                    security_name,
                    weighting,
                    number_of_share,
                    market_value,
                    cost_basis,
                    share_change,
                    sector_id,
                    sector,
                    industry_id,
                    global_industry_id,
                    global_sector,
                    gics_industry_id
                ]))

            for level_2_row_str in level_2_strs:
                xml_csv.write(level_1_str + "," + level_2_row_str + "\n")
    xml_csv.close()

print("Removing ~temp directory")
shutil.rmtree(temp_directory)

print("\n\nJob complete.")