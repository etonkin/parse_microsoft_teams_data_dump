# parse_microsoft_teams_data_dump
Interactively select conversation logs from Microsoft Teams, and build them into a csv file

This is just a small piece of code to interactively select conversation logs from Microsoft Teams, and build them into a csv file.
Download your GDPR datadump from Microsoft Teams:

https://support.microsoft.com/en-gb/office/export-or-delete-your-data-in-microsoft-teams-free-1ed6ac68-5fb4-41be-9861-1a4127fecf68
or possibly 
https://go.microsoft.com/fwlink/?linkid=2128346
(Disclaimer: I only have a business account myself, and this data dump seems to be unaccessible for business users, presumably on 
the decision of the account administrators: I built this for someone who uses Microsoft services for personal use)

Put this script into the same directory. Run it with 
python readfile.py

Select a conversation by typing in the relevant number

Once run, you should find a csv file containing the relevant information.
