import socket
import sys, getopt
import argparse

def PrintLogo():
  print '      _                 _         _            '
  print '     | |               | |       | |           '
  print '   __| |_   _ _ __ ___ | |__   __| |_ __  ___  '
  print '  / _| | | | | |_ \ _ \| |_ \ / _| | |_ \/ __| '
  print ' | (_| | |_| | | | | | | |_) | (_| | | | \__ \\'
  print '  \__,_|\__,_|_| |_| |_|_.__/ \__,_|_| |_|___/ '
  print
  print



class DNSQuery:
  def __init__(self, data):
    self.data = data

  def makeResponse(self, ip):
    packet=''

    packet+=self.data[:2] + "\x81\x80"
    packet+=self.data[4:6] + self.data[4:6] + '\x00\x00\x00\x00'   # Questions and Answers Counts
    packet+=self.data[12:]                                         # Original Domain Name Question
    packet+='\xc0\x0c'                                             # Pointer to domain name
    packet+='\x00\x01\x00\x01\x00\x00\x00\x3c\x00\x04'             # Response type, ttl and resource data length -> 4 bytes
    packet+=str.join('',map(lambda x: chr(int(x)), ip.split('.'))) # 4bytes of IP
    return packet

if __name__ == '__main__':
  PrintLogo()
  
  parser = argparse.ArgumentParser()
  parser.add_argument("-a", "--addr", type=str, help="Selected IPv4 address")
  args = parser.parse_args()

  ip = args.addr
  print '[*] Starting nameserver'
  print '[*] Destination ip is', ip

  sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  sock.bind(('',53))
  print '[*] Server is started'

  try:
    while 1:
      data, addr = sock.recvfrom(1024)
      dnsquery = DNSQuery(data)
      sock.sendto(dnsquery.makeResponse(ip), addr)
      print '[*] DNS query was sent'

  except KeyboardInterrupt:
    print '[*] Closing nameserver'
    sock.close()
