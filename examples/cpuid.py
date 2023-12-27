# Print processor information
from pyzutil import maps

cvt = maps.ptr32(0x10)
cvtsname = maps.string(cvt + 0x154, 8, rtrim=True)
ecvt = maps.ptr32(cvt + 0x8c)
ipa = maps.ptr32(ecvt + 0x188)
ipasxnam = maps.string(ipa + 0x160, 8, rtrim=True)

print(f"SYSNAME={cvtsname} SYSPLEX={ipasxnam}")

iosdshid = maps.ptr32(cvt + 0x42C)
type = maps.string(iosdshid + 0x1A, 6, rtrim=True)
model = maps.string(iosdshid + 0x20, 3, rtrim=True)
man = maps.string(iosdshid + 0x23, 3, rtrim=True)
plant = maps.string(iosdshid + 0x26, 2, rtrim=True)
seqno = maps.string(iosdshid + 0x28, 12, rtrim=True)

print(f"CPC={type}.{model}.{man}.{plant}.{seqno}\n")

cvtmaxmp = maps.uint16(cvt + 0x1DC)
cvtpccat = maps.ptr32(cvt + 0x2FC)

PCCAZIIP = 0x04   # CP is a zIIP
PCCAZAAP = 0x01   # CP is a zAAP

print(""" ID VER CPUID  MODEL
         --- --- ------ -----""")
for id in range(cvtmaxmp):
    pcaa = maps.ptr32(cvtpccat + id * 4)
    if pcaa == 0:
        continue
    pccapcca = maps.string(pcaa, 4)
    if pccapcca != "PCCA":
        continue
    pccavc = maps.string(pcaa + 4, 2)
    pccacpid = maps.string(pcaa + 6, 6)
    pccamdl = maps.string(pcaa + 12, 4)
    pccaattr = maps.uint8(pcaa + 0x178)
    sp = ''
    if pccaattr & PCCAZIIP:
        sp += ' zIIP'
    if pccaattr & PCCAZAAP:
        sp += ' zAAP'
    print(f"{id:03} {pccavc}  {pccacpid} {pccamdl} {sp}")
