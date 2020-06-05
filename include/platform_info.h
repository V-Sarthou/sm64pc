#ifndef PLATFORM_INFO_H
#define PLATFORM_INFO_H

#include <stdint.h>
#define IS_64_BIT (UINTPTR_MAX == 0xFFFFFFFFFFFFFFFFU)
#ifdef WIN32
#define IS_BIG_ENDIAN (0)
#else
#define IS_BIG_ENDIAN (__BYTE_ORDER__ == __ORDER_BIG_ENDIAN__)
#endif

#define DOUBLE_SIZE_ON_64_BIT(size) ((size) * (sizeof(void *) / 4))

#endif
