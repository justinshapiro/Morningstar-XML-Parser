# Morningstar XML Parser
This program parses XML data relating to the financial holdings of mutual funds. Morningstar provides this data in a series of `.7z` compressed folders. Each compressed folder has around 10 XML files in it. This Python script runs a batch job on these compressed folders by extracting the `.xml` files from them and parsing the format to CSV. If there are 10 XML files in a `.7z` or `.zip` folder, a single CSV will contain the parsed information for each one of those files.

Because of the hierarchical structure of the XML data, there is quite a bit of repeated information throughout several rows in order for the data to "flatten" into a CSV format. This is the trade off that needs to be made when parsing complicated XML structures to a more manageable CSV format.

### How to run
- Needs Python 3.3 or greater
- `setup.py` has been included to use cx_Freeze to package this program into a Windows executable for distrubution
- Run with `python xml_to_csv.py`
- No command line arguments are supported at this time
