#include "binary_vector.h"
#include <stdlib.h>
#include <math.h>
#define T BINARY_VECTOR_P

T VEC_add(T a, T b)
{
    float x = a->x + b->x;
    float y = a->y + b->y;
    T result;
    result = VEC_new();
    result->x = x;
    result->y = y;
    return result;
}

float VEC_mul(T a, T b)
{
    float result = a->x * b->x + a->y * b->y;
    return result;
}

T VEC_new(void)
{
    T ptr;
    ptr = (T)malloc(((long)sizeof *(ptr)));
    ptr->x = 0.0;
    ptr->y = 0.0;
    return ptr;
}

T VEC_init(float x, float y)
{
    T ptr;
    ptr = (T)malloc(((long)sizeof *(ptr)));
    ptr->x = x;
    ptr->y = y;
    return ptr;
}

void VEC_del(T ptr)
{
    if (ptr)
        free(ptr);
}
float VEC_mod(T a)
{
    float result = sqrt(a->x * a->x + a->y * a->y);
    return result;
}
#undef T