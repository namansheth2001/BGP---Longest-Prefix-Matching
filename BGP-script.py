# the required files are uploaded to GitHub repo

from google.colab import files
uploaded = files.upload()
DB = next(iter(uploaded))
print(DB, "uploaded")

uploaded = files.upload()
IP_LIST = next(iter(uploaded))
print(IP_LIST, "uploaded")

import ipaddress

def parseBGPTable(filename):
    dictToStoreIP = {}
    dbFile = open("DB_091803_v1.txt") 
    for line in dbFile:
      fileContents = line.strip().split(' ')
      subnet = fileContents[0]
      mask = fileContents[1]
      asn = fileContents[2]
      try:
        network = ipaddress.IPv4Network(subnet + '/' + mask)
        dictToStoreIP[network] = asn
      except ValueError as formatError:
        print(formatError)
    return dictToStoreIP
    dbFile.close()

def asnForIP(ipAddr, dictToStoreIP):  
    maxPrefLen = 0
    asn = None
    for prefix in dictToStoreIP:
      if (ipAddr in prefix):
        if (prefix.prefixlen > maxPrefLen):
          maxPrefLen = prefix.prefixlen
          asn = dictToStoreIP[prefix]
    return maxPrefLen, asn

dictToStoreIP = parseBGPTable('DB_091803_v1.txt')
ipFile = open('IPlist.txt')
for line in ipFile:
  ipAddr = ipaddress.IPv4Address(line.strip())
  prefix_len, asn = asnForIP(ipAddr, dictToStoreIP)
  print("\n")
  print('IP = %s' % ipAddr)
  print('Prefix Len = %d' % prefix_len)
  print('ASN = %s' % asn)
ipFile.close()