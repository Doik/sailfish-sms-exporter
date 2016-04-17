#!/usr/bin/env python3

"""
Convert sailfish sms to xml to be imported to android phones.

Reads a sailfish commhistory.db (which can be found in `/home/nemo/.local/share/commhistory`)
and creates a xml-file of all contained sms that is understood by the Android Application
"SMS Backup and Restore" (which can be obtained here:
https://play.google.com/store/apps/details?id=com.riteshsahu.SMSBackupRestore)
"""

import sqlite3
from datetime import datetime

jolla_db_filename = 'commhistory.db'
target_filename = 'out.xml'


def encode_xml(text):
    """Escape the text for xml."""
    text = text.replace("&", "&amp;")
    text = text.replace("\"", "&quot;")
    text = text.replace("'", "&apos;")
    text = text.replace("<", "&lt;")
    text = text.replace(">", "&gt;")
    return text

cols = ["id", "type", "startTime", "endTime", "direction", "isDraft", "isRead", "isMissedCall", "isEmergencyCall", "status", "bytesReceived", "localUid", "remoteUid", "parentId", "subject", "freeText", "groupId", "messageToken", "lastModified", "vCardFileName", "vCardLabel", "isDeleted", "reportDelivery", "validityPeriod", "contentLocation", "messageParts", "headers", "readStatus", "reportRead", "reportedReadRequested", "mmsId", "isAction", "hasExtraProperties", "hasMessageParts"]


connection = sqlite3.connect(jolla_db_filename)
cursor = connection.cursor()
cursor.execute("SELECT * FROM Events WHERE type=2")
entries = cursor.fetchall()

date = datetime.now()

out = """<?xml version='1.0' encoding='UTF-8' standalone='yes' ?>
<!--File Created on {date}-->
<?xml-stylesheet type="text/xsl" href="sms.xsl"?>
<smses count="{count}">""".format(count=len(entries), date=date.strftime("%d/%m/%y %H:%M:%S"))

# type: Android             Sailfish
# 1 = msg rcvd              1
# 2 = msg sent              2
# 3 = msg draft

for entry in entries:
    direction = entry[cols.index('direction')]
    # if direction == 2 and not entry[cols.index('remoteUid')]:
    #     continue
    date = datetime.fromtimestamp(entry[cols.index('startTime')])
    out += """<sms
    protocol="{protocol}"
    address="{address}"
    date="{date}"
    type="{type}"
    subject="{subject}"
    body="{body}"
    toa="{toa}"
    sc_toa="{sc_toa}"
    service_center="{service_center}"
    read="{read}"
    status="{status}"
    locked="{locked}"
    date_sent="{date_sent}"
    readable_date="{readable_date}"
    contact_name="{contact_name}" />\n""".format(
        protocol=0,
        address=entry[cols.index('remoteUid')],
        date=entry[cols.index('startTime')] * 1000,
        type=direction,
        subject=entry[cols.index('subject')] or "null",
        body=encode_xml(entry[cols.index('freeText')]),
        toa="null",
        sc_toa="null",
        service_center="null",
        read=1,
        status=-1,
        locked=0,
        date_sent=(0 if direction == 2 else entry[cols.index('startTime')] * 1000),
        readable_date=date.strftime("%d.%m.%Y %H:%M:%S"),
        contact_name=""
    )

out += "\n</smses>"

with open(target_filename, 'w') as fp:
    fp.write(out)

print("Done")
