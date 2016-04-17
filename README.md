
#### sailfish sms and recent calls exporter.

Convert sailfish sms and call history to xml to be imported to android phones

Reads a sailfish commhistory.db (which can be found in `/home/nemo/.local/share/commhistory`)
and creates a xml-file of all contained sms that is understood by the Android Application
"SMS Backup and Restore" (which can be obtained here:
https://play.google.com/store/apps/details?id=com.riteshsahu.SMSBackupRestore)

Usage:
* `cd` to the folder this script resides in
* `scp nemo@192.168.0.10:~/.local/share/commhistory/commhistory.* .` (replace IP with your sailfish-phone-IP)
* `./converter.py`
* This generates two files: `sms.xml` and `calls.xml`. Copy them to your android-phone, and point the "SMS Backup and Restore" App to the target-folder.

Requirements:
* Python3