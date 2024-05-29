#include <stdio.h>

// to compile in cmd terminal:
// gcc testCcode.c -fPIC -shared -o testccode.so

typedef struct {
    int num1;
    int num2;
    int num3;
} testStruct;

//typedef void (*pyFunc)(int* a, int b);
typedef void (*pyFunc)(testStruct* attributes, unsigned char* bytePtr);

void callbackCaller(int num, pyFunc func) {
    printf("input int is %d\n", num);
    testStruct nums;
    nums.num1 = 31;
    nums.num2 = 41;
    nums.num3 = 59;
    unsigned char ret_arr[4] = {1,2,3,4};
    func(&nums, ret_arr);
}