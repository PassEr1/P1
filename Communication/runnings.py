import pprint
import socket
import struct
import ctypes
import win32gui
import sys
import  time
import os
import traceback
import ctypes
from ctypes import wintypes
from subprocess import Popen, PIPE
import re
import win32con
import win32api
import win32gui
import win32process

def decode_labels(message, offset):
    labels = []

    while True:
        length, = struct.unpack_from("!B", message, offset)

        if (length & 0xC0) == 0xC0:
            pointer, = struct.unpack_from("!H", message, offset)
            offset += 2

            return labels + decode_labels(message, pointer & 0x3FFF), offset

        if (length & 0xC0) != 0x00:
            raise StandardError("unknown label encoding")

        offset += 1

        if length == 0:
            return labels, offset

        labels.append(*struct.unpack_from("!%ds" % length, message, offset))
        offset += length


DNS_QUERY_SECTION_FORMAT = struct.Struct("!2H")

def decode_question_section(message, offset, qdcount):
    questions = []

    for _ in range(qdcount):
        qname, offset = decode_labels(message, offset)

        qtype, qclass = DNS_QUERY_SECTION_FORMAT.unpack_from(message, offset)
        offset += DNS_QUERY_SECTION_FORMAT.size

        question = {"domain_name": qname,
                    "query_type": qtype,
                    "query_class": qclass}

        questions.append(question)

    return questions, offset


DNS_QUERY_MESSAGE_HEADER = struct.Struct("!6H")

def decode_dns_message(message):

    id, misc, qdcount, ancount, nscount, arcount = DNS_QUERY_MESSAGE_HEADER.unpack_from(message)

    qr = (misc & 0x8000) != 0
    opcode = (misc & 0x7800) >> 11
    aa = (misc & 0x0400) != 0
    tc = (misc & 0x200) != 0
    rd = (misc & 0x100) != 0
    ra = (misc & 0x80) != 0
    z = (misc & 0x70) >> 4
    rcode = misc & 0xF

    offset = DNS_QUERY_MESSAGE_HEADER.size
    questions, offset = decode_question_section(message, offset, qdcount)

    result = {"id": id,
              "is_response": qr,
              "opcode": opcode,
              "is_authoritative": aa,
              "is_truncated": tc,
              "recursion_desired": rd,
              "recursion_available": ra,
              "reserved": z,
              "response_code": rcode,
              "question_count": qdcount,
              "answer_count": ancount,
              "authority_count": nscount,
              "additional_count": arcount,
              "questions": questions}

    print result
    return result

def enumWindowsProc(hwnd, lParam):
    if (lParam is None) or ((lParam is not None) and (win32process.GetWindowThreadProcessId(hwnd)[1] == lParam)):
        text = win32gui.GetWindowText(hwnd)
        if text:
            wStyle = win32api.GetWindowLong(hwnd, win32con.GWL_STYLE)
            if wStyle & win32con.WS_VISIBLE:
                print("%08X - %s" % (hwnd, text))

def enumProcWnds(pid=None):
    win32gui.EnumWindows(enumWindowsProc, pid)

def enumProcs(procName=None):
    pids = win32process.EnumProcesses()
    if procName is not None:
        bufLen = 0x100
        bytes = wintypes.DWORD(bufLen)
        _OpenProcess = ctypes.cdll.kernel32.OpenProcess
        _GetProcessImageFileName = ctypes.cdll.psapi.GetProcessImageFileNameA
        _CloseHandle = ctypes.cdll.kernel32.CloseHandle
        filteredPids = ()
        for pid in pids:
            try:
                hProc = _OpenProcess(wintypes.DWORD(win32con.PROCESS_ALL_ACCESS), ctypes.c_int(0), wintypes.DWORD(pid))
            except:
                print("Process [%d] couldn't be opened: %s" % (pid, traceback.format_exc()))
                continue
            try:
                buf = ctypes.create_string_buffer(bufLen)
                _GetProcessImageFileName(hProc, ctypes.pointer(buf), ctypes.pointer(bytes))
                if buf.value:
                    name = buf.value.decode().split(os.path.sep)[-1]
                    #print name
                else:
                    _CloseHandle(hProc)
                    continue
            except:
                print("Error getting process name: %s" % traceback.format_exc())
                _CloseHandle(hProc)
                continue
            if name.lower() == procName.lower():
                filteredPids += (pid,)
        return filteredPids
    else:
        return pids

def main(args):
    if args:
        procName = args
    else:
        procName = None
    pids = enumProcs(procName)
    print(pids)
    for pid in pids:
        enumProcWnds(pid)




"""
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
host = '127.0.0.1'
port = 53
size = 512
s.bind((host, port))
while True:
    data, addr = s.recvfrom(size)

    pprint.pprint(decode_dns_message(data))
"""
#win32gui.EnumWindows(enumHandler, None)
def get_active_window_title(self):
    root_check = ''
    root = Popen(['xprop', '-root'],  stdout=PIPE)

    if root.stdout != root_check:
        root_check = root.stdout

        for i in root.stdout:
            if '_NET_ACTIVE_WINDOW(WINDOW):' in i:
                id_ = i.split()[4]
                id_w = Popen(['xprop', '-id', id_], stdout=PIPE)
        id_w.wait()
        buff = []
        for j in id_w.stdout:
            buff.append(j)

        for line in buff:
            match = re.match("WM_NAME\((?P<type>.+)\) = (?P<name>.+)", line)
            if match != None:
                type = match.group("type")
                if type == "STRING" or type == "COMPOUND_TEXT":
                    return match.group("name")
        return "Active window not found"
if __name__ == "__main__":

    time.sleep(5)
    main("chrome.exe")
