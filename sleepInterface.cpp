#include <iostream>
// Interestingly, timeapi.h does not work:
// #include <timeapi.h>
#include <Windows.h>
//#include <winmm.lib>

int sleepPeriodChanger(unsigned int uPeriod)
{
    std::cout << "Hello!" << std::endl;
    timeBeginPeriod(uPeriod);
    timeEndPeriod(uPeriod);
    //MSG msg = {};
    return 0;
}