"""
decodeTNC.py is a module for a HAM Radio tracking program for the HARBOR High Altitude Balloon Project.
    This module contains functions for the manual decoding of APRS and D710 packets.
    
Ian Sohl
"""
import re
done = False
def delimit(rawdata):
    """Delimit APRS and D710 packets into constituent parts"""
    # For PKWDPOS D710 Packets
    if "PKWDPOS" in rawdata:
        # Split along commas and asterisks
        splitonce = rawdata.split(',')
        splittwice = rawdata[10].split('*')
        # This only works for the North Western Quadrant
        if 'N' in splitonce[4] and 'W' in splitonce[6]:
            returnable = [splitonce[3] + "N", splitonce[5] + "W", "A=" + splittwice[0]]
            return returnable
    # For $GPRMC D710 Packets
    if "GPRMC" in rawdata:
        # Split on commas
        splitonce = rawdata.split(',')
        # If the data matches, return
        if 'N' in splitonce[4] and 'W' in splitonce[6]:
            returnable = [splitonce[3] + splitonce[4], splitonce[5] + splitonce[6]]
            return returnable
    if "GPGGA" in rawdata:
        # Accepts sentence format: $GPGGA,hhmmss.ss,ddmm.mmmmm,N,dddmm.mmmmm,E,2,12,0.91,69.8,M,16.3,M,,*65
        # Split on commas
        splitonce = rawdata.split(',')
        if 'N' in splitonce[3] and 'W' in splitonce[5]:# We may be able to remove this line if we do a checksum
            returnable = [splitonce[2] + splitonce[3], splitonce[4] + splitonce[5]]
            return returnable
    # For APRS packets (deprecated, use FAP when possible)
    else:
        # Split along the regular expression of /, h and O
        splitonce = re.split('/|h|O', rawdata)
        # Only return if it has the right number of fields
        if len(splitonce) >= 7:
            if 'A=' in splitonce[6]:
                returnable = [splitonce[2], splitonce[3], splitonce[6]]
                return returnable


def latlong(newdata):
    global latsign, longsign
    """Return the latitude and longitude of a given packet"""
    # Delimit the data to determine correct chunks
    output = delimit(newdata)
    if "W" in output[1]:
        longsign = '-'
    else:
        longsign = ''
    if "S" in output[0]:
        latsign = '-'
    else:
        latsign = ''
    # Convert latitude and longitude from Degrees:minutes to decimal degrees
    latitude = latsign + str(float(output[0][:2]) + (float(output[0][2:7]) / 60))
    longitude = longsign + str(float(output[1][:3]) + (float(output[1][3:8]) / 60))
    # I know, it's terrible...
    return longitude, latitude


def determineCompatability(APRSstring, listenfor):
    """Determine whether the APRS packet is being tracked and compatible with the parser"""
    if not done:
        for listento in listenfor:
            # Iterate through callsigns and check
            if APRSstring.startswith(listento):
                returnable = True, listento
                ##                print returnable
                return returnable
    else:
        return False

##print latlong()
