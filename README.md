# app-reading-script
A script that assigns apps to members for app reading

#### 1. Add data to input folder
**apps.txt**: Once you have all the apps in the airtable, copy the App ID column and paste into apps.txt

**leadership.txt & general.txt** can be found in master roster airtable base. Make sure not to leave out the names of anyone who's missing app reading.
      
#### 2. Run `assign.py`
#### 3. `output.csv` appears in output folder
Currently formatted to be easily copied + pasted into Airtable. Uncomment line 86 in `assign.py` to switch back to Google Sheets.