TAB_1 = "\t"
TAB_2 = "\t\t"
TAB_3 = "\t\t\t"
TAB_4 = "\t\t\t\t"
import struct
import socket
class Sniffer:

    def __init__(self):
        self.newest= str()
        self.suggestion=str()
        self.IP_ADDR = "10.0.0.1"

        self.conn = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)

        self.conn.bind((self.IP_ADDR, 0))

        # Include IP headers
        self.conn.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

        # receive all packages
        self.conn.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)


    def get_ipv4_addr(self, bytes_addr):
        """
       Returns a readble ipv4 from bytes (X.X.X.X)
       :param bytes_addr: IP address in bytes
       :return: readble ipv4 (string)
       """
        return socket.inet_ntoa(bytes_addr)

    def IPv4_packet(self, data):
        """
       Extracts IPV4 packet
       :param data: A packet (Bytes)
       :return: version, ttl, protocol, src, target and the rest of the data
       """
        version_header_length, ttl, proto, src, target = struct.unpack('! B 7x B B 2x 4s 4s', data[:20])

        version = version_header_length >> 4
        header_length = (version_header_length & 15) * 4

        return version, ttl, proto, self.get_ipv4_addr(src), self.get_ipv4_addr(target), data[header_length:]

    def ICMP_packet(self, data):
        """
       Extracts ICMP packet
       :param data: A packet (Bytes)
       :return: icmp_type, code and checksum
       """
        icmp_type, code, checksum = struct.unpack('! B B H', data[:4])
        return icmp_type, code, checksum, data[4:]

    def TCP_segment(self, data):
        """
       Extracts TCP segment
       :param data: A segment (Bytes)
       :return: source port, destenation port, sequence number, acknowledgment number and all flags
       """
        (src_port, dest_port, sequence, ack, offset_reserved_flags) = struct.unpack('! H H L L H', data[:14])
        offset = (offset_reserved_flags >> 12) * 4

        flag_urg = (offset_reserved_flags & 32) >> 5
        flag_ack = (offset_reserved_flags & 16) >> 4
        flag_psh = (offset_reserved_flags & 8) >> 3
        flag_rst = (offset_reserved_flags & 4) >> 2
        flag_syn = (offset_reserved_flags & 2) >> 1
        flag_fin = (offset_reserved_flags & 1)

        return src_port, dest_port, sequence, ack, flag_urg, flag_ack, flag_psh, flag_rst, flag_syn, flag_fin, data[
                                                                                                               offset:]

    def UDP_segment(self, data):
        """
       Extracts UDP segment
       :param data: A segment (Bytes)
       :return: source port, destenation port, checksum and the rest data
       """
        (src_port, dest_port, checksum) = struct.unpack('! H H 2x H', data[:8])
        return src_port, dest_port, checksum, data[8:]

    def DNS_packet(self, data):
        ans = struct.unpack("!H H H H H H", data[:12])
        return data[13:]

    def fix_url(self, url):
        pass

    def check_url(self,url):
        all_urls=open("C:\Users\Amit\PycharmProjects\P1\Last_registers.txt",'r') # TODO: change the path so that workingin the usb
        all_urls_array=all_urls.read().split()
        if url in all_urls_array:
            self.newest=url
            all_urls.close()

    def run(self):
        """
       Runs Network class
       :return:
       """
        # TODO: Gets computer's ip through the config file

        while True:
            raw_data, addr = self.conn.recvfrom(65535)

            version, ttl, proto, src, dest, data = self.IPv4_packet(raw_data)
            # # region Print
            #print('\nIP Packet:')
            #print('Version: {}, Destination: {}, Source: {}, Next Protocol: {}'.format(version, dest, src, proto))
            # # endregion

            # ICMP pakcet
            if proto == 1:
                (icmp_type, code, checksum, data) = self.ICMP_packet(data)
                # # region Print
                #print TAB_1 + "ICMP Packet:"
                #print (TAB_2 + 'icmp_type: {}, code: {}, checksum: {}'.format(icmp_type, code, checksum, data))
                # # endregion

            # TCP segment
            elif proto == 6:

                (src_port, dest_port, sequence, ack,
                 flag_urg,
                 flag_ack,
                 flag_psh,
                 flag_rst,
                 flag_syn,
                 flag_fin,
                 data) = self.TCP_segment(data)

                flags = {"urg": flag_urg,
                         "ack": flag_ack,
                         "psh": flag_psh,
                         "rst": flag_rst,
                         "syn": flag_syn,
                         "fin": flag_fin}


            # UDP segment
            elif proto == 17 :

                (src_port, dest_port, length, data) = self.UDP_segment(data)
                if dest_port is 53:
                    print "_____________________UDP_____________________"
                    # print ('Source Port: {}, Destination Port: {}, Length: {}'.format(src_port, dest_port, length))
                    URL = self.DNS_packet(data)
                    URL = ''.join([i if 122 > ord(i) > 95 else ' ' for i in URL])
                    URL = URL.replace(' ', '.')
                    URL = URL[:len(URL)-5]
                    self.check_url(URL)

                    print self.newest

            else:
                print(TAB_1 + 'Other IPv4 Data...')


n = Sniffer()
n.run()