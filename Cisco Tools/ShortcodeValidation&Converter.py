import phonenumbers
import csv
print("""
=======================================================================================
//This script is designed to take parse a csv containing both short codes            // 
//and the long dial's in various formats. It then checks if the long dials are in a  //
//recognisable format and changes them to the E.164 format for calling from the      //
//chosen region. Any numbers within the input file that are not in a recognisable    //
//format will be marked as invalid in the output file for manual intervention.       //
=======================================================================================""")
inputcsv = input("Please enter the location/name of the source file:[Default:input.csv] \n >") or "input.csv"
print("//The output of this program will be output.csv within the dirctory you are running this script//")
Longdial = input("Please enter the name of the column containing the long format of the number:[Default:Longdial] \n >") or "Longdial"
Shortdial = input("Please enter the name of the column containing the short format of the number:[Default:Shortdial] \n >") or "Shortdial"
routepartition = input("Please input the route partition where these Translation Patterns are to exist:[Default:Internal-PT] \n >") or "Internal-PT"
css = input("Please enter the destination CSS for this Translation Pattern \n >")
region = input("""Please enter the region for these numbers to be called from, for example
for calling from the UK enter GB , or for the US enter US:[Default:GB] \n >""") or "GB"
#Open Output File in Write Mode
correctednumbers = open("output.csv","w", newline='')
fieldnames = [Longdial, Shortdial,"<-RemoveBeforeImport","TRANSLATION PATTERN","ROUTE PARTITION","DESCRIPTION","NUMBERING PLAN","ROUTE FILTER","MLPP PRECEDENCE","CALLING SEARCH SPACE","ROUTE OPTION","OUTSIDE DIAL TONE","URGENT PRIORITY","CALLING PARTY TRANSFORMATION MASK","CALLING PARTY PREFIX DIGITS (OUTGOING CALLS)","CALLING LINE ID PRESENTATION","CALLING NAME PRESENTATION","CONNECTED LINE ID PRESENTATION","CONNECTED NAME PRESENTATION","DISCARD DIGITS","CALLED PARTY TRANSFORM MASK","CALLED PARTY PREFIX DIGITS (OUTGOING CALLS)","BLOCK THIS PATTERN OPTION","CALLING PARTY IE NUMBER TYPE","CALLING PARTY NUMBERING PLAN","CALLED PARTY IE NUMBER TYPE","CALLED PARTY NUMBERING PLAN","USE CALLING PARTYS EXTERNAL PHONE NUMBER MASK","RESOURCE PRIORITY NAMESPACE NETWORK DOMAIN","ROUTE CLASS","ROUTE NEXT HOP BY CALLING PARTY NUMBER","EXTERNAL CALL CONTROL PROFILE","USE ORIGINATOR'S CALLING SEARCH SPACE","IS AN EMERGENCY SERVICES NUMBER","DO NOT WAIT FOR INTERDIGIT TIMEOUT ON SUBSEQUENT HOPS"]
writer = csv.DictWriter(correctednumbers, fieldnames=fieldnames)
writer.writeheader()

#Open Source file 
with open(inputcsv) as inputfile:
    csv_reader = csv.DictReader(inputfile)
    line_count = 0
    error_count = 0
    #Test numbers within selected column against valid & possible formats in the selected region, then mutating these into e.164
    for row in csv_reader:
        try:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                x = phonenumbers.parse(f'\t{row[Longdial]}', region)
                test = 'True'
                test = phonenumbers.is_possible_number(x)
                if test is False:
                    e164number = 'Invaild Longdial Format'
                test = phonenumbers.is_valid_number(x)
                if test is False:
                    e164number = 'Invaild Longdial Format'
                if test is True:
                    e164number = phonenumbers.format_number(x, phonenumbers.PhoneNumberFormat.E164)
                if test is False:
                    error_count += 1
                row.update({ 'CALLED PARTY TRANSFORM MASK' : e164number })
                row.update({ 'ROUTE PARTITION' : routepartition })
                row.update({ 'CALLING SEARCH SPACE' : css })
                row.update({ 'ROUTE OPTION' : 'f'})
                row.update({ 'OUTSIDE DIAL TONE' : 't'})
                row.update({ 'URGENT PRIORITY' : 't'})
                row.update({ 'CALLING LINE ID PRESENTATION' : 'Default'})
                row.update({ 'CALLING NAME PRESENTATION' : 'Default'})
                row.update({ 'CONNECTED LINE ID PRESENTATION' : 'Default'})
                row.update({ 'CONNECTED NAME PRESENTATION' : 'Default'})
                row.update({ 'BLOCK THIS PATTERN OPTION' : 'No Error'})
                row.update({ 'CALLING PARTY IE NUMBER TYPE' : 'Cisco CallManager'})
                row.update({ 'CALLING PARTY NUMBERING PLAN' : 'Cisco CallManager'})
                row.update({ 'CALLED PARTY IE NUMBER TYPE' : 'Cisco CallManager'})
                row.update({ 'CALLED PARTY NUMBERING PLAN' : 'Cisco CallManager'})
                row.update({ 'USE CALLING PARTYS EXTERNAL PHONE NUMBER MASK' : 'On' })
                row.update({ 'ROUTE NEXT HOP BY CALLING PARTY NUMBER' : 'f' })
                row.update({ "USE ORIGINATOR'S CALLING SEARCH SPACE" : 'f' })
                row.update({ 'IS AN EMERGENCY SERVICES NUMBER' : 'f' })
                row.update({ 'DO NOT WAIT FOR INTERDIGIT TIMEOUT ON SUBSEQUENT HOPS' : 'f' })
                row.update({ '<-RemoveBeforeImport' : '<-RemoveBeforeImport' })
                row.update({ 'TRANSLATION PATTERN' : f'\t{row[Shortdial]}' })
                print(f'Short Dial: \t{row[Shortdial]} Orginal Long Dial: {row[Longdial]} E.164 Long Dial: {row["CALLED PARTY TRANSFORM MASK"]}')
                writer.writerow(row)
                line_count += 1
        except:
            e164number = 'ERROR!'
            error_count += 1
            row.update({ 'CALLED PARTY TRANSFORM MASK' : e164number })
            row.update({ 'ROUTE PARTITION' : routepartition })
            row.update({ 'CALLING SEARCH SPACE' : css })
            row.update({ 'ROUTE OPTION' : 'f'})
            row.update({ 'OUTSIDE DIAL TONE' : 't'})
            row.update({ 'URGENT PRIORITY' : 't'})
            row.update({ 'CALLING LINE ID PRESENTATION' : 'Default'})
            row.update({ 'CALLING NAME PRESENTATION' : 'Default'})
            row.update({ 'CONNECTED LINE ID PRESENTATION' : 'Default'})
            row.update({ 'CONNECTED NAME PRESENTATION' : 'Default'})
            row.update({ 'BLOCK THIS PATTERN OPTION' : 'No Error'})
            row.update({ 'CALLING PARTY IE NUMBER TYPE' : 'Cisco CallManager'})
            row.update({ 'CALLING PARTY NUMBERING PLAN' : 'Cisco CallManager'})
            row.update({ 'CALLED PARTY IE NUMBER TYPE' : 'Cisco CallManager'})
            row.update({ 'CALLED PARTY NUMBERING PLAN' : 'Cisco CallManager'})
            row.update({ 'USE CALLING PARTYS EXTERNAL PHONE NUMBER MASK' : 'On' })
            row.update({ 'ROUTE NEXT HOP BY CALLING PARTY NUMBER' : 'f' })
            row.update({ "USE ORIGINATOR'S CALLING SEARCH SPACE" : 'f' })
            row.update({ 'IS AN EMERGENCY SERVICES NUMBER' : 'f' })
            row.update({ 'DO NOT WAIT FOR INTERDIGIT TIMEOUT ON SUBSEQUENT HOPS' : 'f' })
            row.update({ '<-RemoveBeforeImport' : '<-RemoveBeforeImport' })
            row.update({ 'TRANSLATION PATTERN' : f'\t{row[Shortdial]}' })
            print(f'Short Dial: \t{row[Shortdial]} Orginal Long Dial: {row[Longdial]}','CALLED PARTY TRANSFORM MASK:',e164number)
            writer.writerow(row)
            line_count += 1
    print(f'Processed {line_count} lines with {error_count} rows containing errors requiring manual intervention.')
correctednumbers.close()