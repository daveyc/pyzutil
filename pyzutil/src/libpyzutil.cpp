#include <cstring>
#include <cstdint>
#include <ctime>
#include <csignal>
#include <csetjmp>
#include <cstdlib>
#include <iostream>

extern "C" {

static odp::mvs_module *callable_service;
static void *save_area;

double pyzutil_clock() {
    return ((double) clock()) / CLOCKS_PER_SEC;
}

int pyzutil_stck(char *outbuf, size_t size) {
    if (size < 8) return -1;
    __asm(" STCK %0"
            : "=m"(*outbuf)
            :
            :
            );
    return 0;
}

int pyzutil_stcke(char *outbuf, size_t size) {
    if (size < 16) return -1;
    __asm(" STCKE %0"
            : "=m"(*outbuf)
            :
            :
            );
    return 0;
}

uint64_t pyzutil_time_used()
{
    uint64_t mics = 0;
    __asm(" L     14,16(0,0)         CVT address                    \n"
          " L     14,772(14,0)       SFT address                    \n"
          " L     14,244(14,0)       LX/EX for service routine      \n"
          " LA    0,1                Set timing flag to CPU/MIC     \n"
          " PC    0(14)              PC to TIMEUSED service routine \n"
          " STM   0,1,%0                                              "
            : "=m"(mics)  // output  definition
            :              // no input
            : "r0", "r1", "r14", "r15");  // clobber list
    return mics >> 12;
}

int pyzutil_time()
{
    int mics = 0;
    return mics;
}

static jmp_buf jmpbuf;
static void segv_handler(int sig) {
    if (sig == SIGSEGV) longjmp(jmpbuf, 1);  // return control to where setjump() is called
}

bool pzutil_storage(uint64_t address, char *outbuf, size_t length) {
    const char *ptr = reinterpret_cast<const char *>(address);
    if (length == 0) return false;
    // set a signal handler to recover from segmentation faults.
    signal(SIGSEGV, segv_handler);
    // Save the stack environment context. If the signal handler is called due to a SIGSEGV (OC4)
    // then control will be restored to this point.
    int rc = setjmp(jmpbuf);
    if (rc == 0) {  // sta
        memcpy(outbuf, ptr, length); // copy the data (may 0C4 if the address is bad)
    } // else longjmp() was called from the signal handler
    signal(SIGSEGV, SIG_DFL);  // always unregister the signal handler
    return rc == 0;
}

} // extern "C"