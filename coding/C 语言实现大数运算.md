最终效果:

![image-20251030110759108](https://cdn.xnnehang.top/MrXnneHang/blog_img/refs/heads/main/BlogHosting/img/25/11/202510301108748.png)

**上面只是验算，实际支持位数多长都可以**，只需要调高char[SIZE]的SIZE，SIZE>十进制位数，并且保证不爆内存就行。

最终测试时我们用的是2048bit(十进制约630位)，单片机用时十秒以内，windows visual studio用时一秒以内。

![image-20251030110849971](https://cdn.xnnehang.top/MrXnneHang/blog_img/refs/heads/main/BlogHosting/img/25/11/202510301108485.png)

### 源代码：

经过调试，这些大数运算时可以直接被keil编译的。

可以直接在**实验34 FLASH模拟EEPROM实验**的项目中内编译烧录（需要注释掉原来的主函数。），烧录后开启单片机并且复位就会得到上面的返回。

```C
#pragma once
#pragma warning(disable:4996)
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define SIZE 100

// ????
int a[SIZE], b[SIZE], c[SIZE];
char result1[SIZE + 1], result2[SIZE + 1], result3[SIZE + 1];
char tempNum[SIZE + 1], dividedNum[SIZE + 1];
int temp2[SIZE + 1];
char binaryString[SIZE + 1];
char modBaseResult[SIZE + 1], modResult[SIZE + 1], newResult[SIZE + 1], newBase[SIZE + 1];
char tempBase[SIZE + 1];

char localResult1[SIZE + 1];
char localModResult[SIZE + 1];
char localNewResult[SIZE + 1];
char localTempBase[SIZE + 1];
char localModBaseResult[SIZE + 1];
char localNewBase[SIZE + 1];


//E
char binaryExp[SIZE + 1]; char D[SIZE + 1]; char result[SIZE + 1]; char m[SIZE + 1];


// ???????
int max(int a, int b) {
    return (a > b) ? a : b;
}

// ??????0
void setZero(int* num, int len) {
    int i;
    for (i = 0; i < len; i++)
        num[i] = 0;
}

// ????????????
int Compare(int* num1, int* num2) {
    int i, j;
    for (i = SIZE - 1; num1[i] == 0; i--);
    for (j = SIZE - 1; num2[j] == 0; j--);
    if (i < j) return -1;
    else if (i > j) return 1;
    else {
        for (; i >= 0; i--) {
            if (num1[i] > num2[i])
                return 1;
            else if (num1[i] < num2[i])
                return -1;
        }
        return 0;
    }
}

// ????????????
int copy(int* num1, int* num2) {
    int i, j;
    for (i = 0; i < SIZE; i++)
        num1[i] = 0;
    for (i = SIZE - 1; num2[i] == 0; i--);
    for (j = 0; j <= i; j++)
        num1[j] = num2[j];
    return i + 1;
}

char* add(char* str1, char* str2) {
    int carry, len1, len2, len;
    int i;

    setZero(a, SIZE);
    setZero(b, SIZE);
    setZero(c, SIZE);

    carry = 0;
    len1 = strlen(str1);
    len2 = strlen(str2);
    len = (len1 > len2) ? len1 : len2;

    for (i = 0; i < len1; i++) {
        a[i] = str1[len1 - 1 - i] - '0';
    }
    for (i = 0; i < len2; i++) {
        b[i] = str2[len2 - 1 - i] - '0';
    }
    for (i = 0; i < len; i++) {
        c[i] = (a[i] + b[i] + carry) % 10;
        carry = (a[i] + b[i] + carry) / 10;
    }
    if (carry != 0) {
        c[len++] = 1;
    }

    for (i = len - 1; i >= 0; i--) {
        result1[len - 1 - i] = c[i] + '0';
    }
    result1[len] = '\0';

    return result1;
}

char* subtract(char* str1, char* str2) {
    int borrow, len1, len2, len;
    int i;

    setZero(a, SIZE);
    setZero(b, SIZE);
    setZero(c, SIZE);

    borrow = 0;
    len1 = strlen(str1);
    len2 = strlen(str2);
    len = (len1 > len2) ? len1 : len2;

    for (i = 0; i < len1; i++) {
        a[i] = str1[len1 - 1 - i] - '0';
    }
    for (i = 0; i < len2; i++) {
        b[i] = str2[len2 - 1 - i] - '0';
    }

    for (i = 0; i < len; i++) {
        c[i] = a[i] - b[i] - borrow;
        if (c[i] < 0) {
            borrow = 1;
            c[i] += 10;
        }
        else {
            borrow = 0;
        }
    }

    while (c[len - 1] == 0 && len > 1) {
        len--;
    }

    for (i = len - 1; i >= 0; i--) {
        result2[len - 1 - i] = c[i] + '0';
    }
    result2[len] = '\0';

    return result2;
}

char* multiply(char* str1, char* str2) {
    int carry, tmp, len1, len2;
    int i, j, k;

    setZero(a, SIZE);
    setZero(b, SIZE);
    setZero(c, SIZE);

    len1 = strlen(str1);
    len2 = strlen(str2);

    for (i = 0; i < len1; i++)
        a[i] = str1[len1 - 1 - i] - '0';
    for (i = 0; i < len2; i++)
        b[i] = str2[len2 - 1 - i] - '0';

    for (i = 0; i < len1; i++) {
        for (k = i, j = 0; j < len2; j++, k++) {
            c[k] += a[i] * b[j];
        }
    }

    carry = 0;
    for (i = 0; i < SIZE; i++) {
        c[i] += carry;
        tmp = c[i];
        c[i] = tmp % 10;
        carry = tmp / 10;
    }

    for (i = SIZE - 1; i >= 0 && c[i] == 0; i--);
    if (i == -1) {
        result3[0] = '0';
        result3[1] = '\0';
    }
    else {
        for (j = 0; j <= i; j++)
            result3[j] = c[i - j] + '0';
        result3[i + 1] = '\0';
    }

    return result3;
}

char* divide(char* str1, char* str2) {
    static char result[SIZE + 1];
    int i, j, tmp, tmp2 = 0, borrow = 0, temp[SIZE] = { 0 }, temp2[SIZE] = { 0 };
    int len1, len2;

    setZero(a, SIZE);
    setZero(b, SIZE);
    setZero(c, SIZE);

    len1 = strlen(str1);
    len2 = strlen(str2);

    for (i = 0; i < len1; i++)
        a[i] = str1[len1 - 1 - i] - '0';
    for (i = 0; i < len2; i++)
        b[i] = str2[len2 - 1 - i] - '0';

    if (Compare(a, b) < 0) {
        result[0] = '0';
        result[1] = '\0';
        return result;
    }

    while (Compare(a, b) >= 0) {
        tmp = len1 - len2;
        if (tmp == tmp2 && tmp > 0)
            tmp--;
        tmp2 = tmp;

        setZero(temp2, SIZE);
        for (i = len1 - 1; i >= tmp; i--)
            temp2[i] = b[i - tmp];
        copy(temp, a);

        if (Compare(temp, temp2) < 0)
            continue;
        for (j = 1;; j++) {
            borrow = 0;
            for (i = tmp; i < len1; i++) {
                temp[i] = a[i] - temp2[i] - borrow;
                if (temp[i] < 0) {
                    borrow = 1;
                    temp[i] += 10;
                }
                else
                    borrow = 0;
            }

            len1 = copy(a, temp);
            c[tmp] = j;
            if (Compare(temp, temp2) < 0)
                break;
        }
    }

    for (i = SIZE - 1; c[i] == 0 && i >= 0; i--);
    for (j = 0; i >= 0; i--, j++)
        result[j] = c[i] + '0';
    result[j] = '\0';

    return result;
}

char* mod(char* str1, char* str2, char* result) {
    int i, j, tmp, tmp2 = 0, borrow = 0, len1, len2;
    int nonZeroFound;

    setZero(a, SIZE);
    setZero(b, SIZE);
    setZero(c, SIZE);

    len1 = strlen(str1);
    len2 = strlen(str2);

    for (i = 0; i < len1; i++)
        a[i] = str1[len1 - 1 - i] - '0';
    for (i = 0; i < len2; i++)
        b[i] = str2[len2 - 1 - i] - '0';

    if (Compare(a, b) < 0) {
        for (i = len1 - 1; i >= 0; i--)
            result[len1 - 1 - i] = a[i] + '0';
        result[len1] = '\0';
        return result;
    }

    while (Compare(a, b) >= 0) {
        tmp = len1 - len2;
        if (tmp == tmp2 && tmp > 0)
            tmp--;
        tmp2 = tmp;

        setZero(temp2, SIZE);
        for (i = len1 - 1; i >= tmp; i--)
            temp2[i] = b[i - tmp];
        copy(c, a);

        if (Compare(c, temp2) < 0)
            continue;
        for (j = 1;; j++) {
            borrow = 0;
            for (i = tmp; i < len1; i++) {
                c[i] = a[i] - temp2[i] - borrow;
                if (c[i] < 0) {
                    borrow = 1;
                    c[i] += 10;
                }
                else
                    borrow = 0;
            }

            len1 = copy(a, c);
            if (Compare(c, temp2) < 0)
                break;
        }
    }

    nonZeroFound = 0;
    for (i = len1 - 1; i >= 0; i--) {
        result[len1 - 1 - i] = a[i] + '0';
        if (a[i] != 0) {
            nonZeroFound = 1;
        }
    }
    result[len1] = '\0';

    if (!nonZeroFound) {
        result[0] = '0';
        result[1] = '\0';
    }

    return result;
}

char* processed_mod(char* base, char* m, char* result) {
    return mod(base, m, result);
}


void divideByTwo(const char* num, char* result) {
    int len;
    int carry;
    int i;
    int start;
    carry = 0;
    len = strlen(num);
    start = 0;
    for (i = 0; i < len; i++) {
        int currentDigit = num[i] - '0' + carry * 10;
        result[i] = (currentDigit / 2) + '0';
        carry = currentDigit % 2;
    }

    result[len] = '\0';

    while (result[start] == '0' && result[start + 1] != '\0') {
        start++;
    }
    memmove(result, result + start, len - start + 1);
}

int isZero(const char* num) {
    while (*num) {
        if (*num != '0') {
            return 0;
        }
        num++;
    }
    return 1;
}

char* decimalToBinary(const char* num, int bits) {
    int i;
    strcpy(tempNum, num);

    for (i = bits - 1; i >= 0; i--) {
        if (isZero(tempNum)) {
            binaryString[i] = '0';
        }
        else {
            int lastDigit = (tempNum[strlen(tempNum) - 1] - '0') % 2;
            binaryString[i] = lastDigit ? '1' : '0';

            divideByTwo(tempNum, dividedNum);
            strcpy(tempNum, dividedNum);
        }
    }

    return binaryString;
}
void my_strcpy(char* dest, const char* src) {
    while (*src) {
        *dest++ = *src++;
    }
    *dest = '\0'; // ???????????
}

char* fastpowermod(const char* base, const char* binaryexp, const char* m) {
    int i; int len;
    my_strcpy(localResult1, "1");
    my_strcpy(localTempBase, base);

    len = strlen(binaryexp);

    for ( i = 0; i < len; i++) {
        if (binaryexp[len - 1 - i] == '1') {

            my_strcpy(localNewResult, multiply(localResult1, localTempBase));

            my_strcpy(localModResult, processed_mod(localNewResult, (char*)m, localModResult));

            my_strcpy(localResult1, localModResult);

        }

        my_strcpy(localNewBase, multiply(localTempBase, localTempBase));
        my_strcpy(localModBaseResult, processed_mod(localNewBase, (char*)m, localModBaseResult));
        my_strcpy(localTempBase, localModBaseResult);
    }

    my_strcpy(result1, localResult1);
    return result1;
}

char* removeLeadingZeros(const char* str) {
    while (*str == '0') {
        str++;
    }
    return (char*)str;
}



int main() {
    // ????
    int bits;
    char num1[SIZE], num2[SIZE]; 

    // ????
    strcpy(num1, "123456789123456789");
    strcpy(num2, "987654321987654321");
    strcpy(result, add(num1, num2));
    printf("Addition: %s + %s = %s\n", num1, num2, result);

    // ????
    strcpy(num1, "987654321987654321");
    strcpy(num2, "123456789123456789");
    strcpy(result, subtract(num1, num2));
    printf("Subtraction: %s - %s = %s\n", num1, num2, result);

    // ????
    strcpy(num1, "260");
    strcpy(num2, "20000000");
    strcpy(result, multiply(num1, num2));
    printf("Multiplication: %s * %s = %s\n", num1, num2, result);

    // ????
    strcpy(num1, "6000");
    strcpy(num2, "5");
    strcpy(result, divide(num1, num2));
    printf("Division: %s / %s = %s\n", num1, num2, result);

    // ????
    strcpy(num1, "1661");
    strcpy(num2, "1000");
    strcpy(result, mod(num1, num2, result));
    printf("Modulo: %s %% %s = %s\n", num1, num2, result);

    // ??????
    strcpy(num1, "2210613142");
    strcpy(num2, "45654");
    strcpy(m, "1000");
    bits = strlen(num2) * 4;
    strcpy(binaryExp,decimalToBinary(num2, bits));
    strcpy(binaryExp,removeLeadingZeros(binaryExp));
    printf("Binary:%s\n", binaryExp);
    strcpy(result, fastpowermod(num1, binaryExp, m));
    printf("Fast Power Modulo: %s^%s %% %s = %s\n", num1, num2, m, removeLeadingZeros(result));

    return 0;
}

```



### **速度：**

同样算法，2048bit的授权码，65537的公钥，**单片机上运行时间十秒以内**出解密结果,windows上一秒以内（同样用公钥进行测试）。



### 底层实现：

我们最开始统一使用char*，并且动态内存分配。这样会更加安全。但是是用的stm32fxx库不支持标准库的malloc函数，或者说使用的开发板是支持动态内存释放。编译方面只要写一句：

```
char* a;
a = (char*)malloc(a,sizeof(char)*2);
```

就会报错

![malloc报错](https://image.baidu.com/search/down?url=https://img1.doubanio.com/view/photo/l/public/p2910285748.webp)

但是依然不信邪，我用底层API库实现了一个mymalloc.h，一个个函数调试最终编译成功，乘法也运行成功，以为要成功的时候碰到快速幂取模就卡住了。

区别在于申请内存的次数。快速幂取模多次调用乘法，单次乘法可以释放内存，但几百几千次乘法申请内存，内存块就碎片化了，free会卡住。

通常会在连续运行十次乘法左右就无法free。

后来使用char[SIZE]来直接全局声明变量，调试通过。

同样保存了另一个完全使用malloc实现动态管理内存的算法，上传到了github上。

## Windows串口程序的两种实现方法。



### **第一种解法：pyserial库**

这很适合我调串口的过程。

用python写串口，应该很容易，但是，pyserial库无法规定发送和接收的数据的格式，似乎都是以二进制传输的。简单来说它写得太烂了。而它写得

也确实不好，第一是没有自带decode输出，需要手动decode。也不能Encode输入。第二是，read函数碰到输出很长的时候（单片机是流式输出）。它不会检测终止点和起始点会截断输出。

以上部分该库都写得相当得烂。

于是我规定了和组员（单片机的部分的）说，每次**\n前面必须加上[complete]**，我会根据是否接收来[complete]来决定是否拼接数据为完整数据进行解码。

并且**一个线程只专注Listen，每隔半秒read一次信息**，并且执行上述检查操作。

一个线程监控user的输入和发送。当发送按钮开始的时候，暂停Listen线程，然后send_message。

并且把它的UI处理成对话式。

![Snipaste_2024-07-04_15-26-29](https://image.baidu.com/search/down?url=https://img3.doubanio.com/view/photo/l/public/p2910285747.webp)

碰到长度几百上千的，它会读取几次，然后把它拼凑起来。



### **另一种解法：用C++ Windows API来掏空正点原子串口调试助手**

C++的windowsAPI支持之间读取窗口句柄，并且子窗口也是有句柄的，比如输入框，输出框，发送按钮，打开串口按钮，关闭串口按钮。

这些框都可以根据APISendMessage+WM_GETTEXT来触发，读取输出框，写入输入框，发送。打开串口。

优点：读取到的直接的UTF-8的格式。不需要更多编码解码。

缺点：实际上和手动操作串口调试助手没什么区别。



我用的是这种，取巧了一点，但是有捷径为什么不走。这个也是个很好的示例，多会几门编程语言，至少解法思路上就广一些。所以nodejs还是要学的。javascript也是要看的，就得看能不能找到个适合的项目直接入门。入门也就够用了，有个思路其他全靠gpt。