import sqlite3
import csv
import argparse

parser = argparse.ArgumentParser(description='Scripts that dumps and save on csv file a recon.db')
parser.add_argument('db', help='the recon.db sqlite3 to get the data from')
parser.add_argument('outfile', help='the output file path.')
args = parser.parse_args()


con = sqlite3.connect(args.db)
cur = con.cursor()

nets = list(cur.execute('select ssid,bssid,encryption,hidden from aps'))

con.close()

conversion_table = {
    '0': 'open',
    '4': 'wep',
    '8950883': 'WPA Mixed Enterprise (CCMP TKIP)',
    '17845315': 'WPA Mixed PSK (CCMP)',
    '1050689': 'WPA PSK (CCMP)',
    '16778242': 'WPA2 (CCMP)',
    '16777218': 'wpa2',
    '8422914': 'WPA2 Enterprise (CCMP TKIP)',
    '16843778': 'WPA2 Enterprise FT (CCMP)',
    '8406530': 'WPA2 PSK (CCMP TKIP)',
    '16794626': 'WPA2 PSK (CCMP)',
    '8405506': 'WPA2 PSK (TKIP)',
}

with open(args.outfile, 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=' ',quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for net in nets:
        spamwriter.writerow([net[0],net[1],conversion_table.get(str(net[2]), ''),net[3]])
