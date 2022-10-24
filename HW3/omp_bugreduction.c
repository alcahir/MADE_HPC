#include <omp.h>
#include <stdio.h>
#include <stdlib.h>



float dotprod(float * a, float * b, size_t N)
{
    int i, tid;
    tid = omp_get_thread_num();
    float sum;
#pragma omp parallel for reduction(+:sum)
    for (i = 0; i < N; ++i)
    {
        sum += a[i] * b[i];
        printf("tid = %d i = %d sum=%f\n", tid, i, sum);
    }

    return sum;
}

int main (int argc, char *argv[])
{
    const size_t N = 100;
    int i;
    float a[N], b[N];
    float sum;
    for (i = 0; i < N; ++i)
    {
        a[i] = b[i] = (double)i;
    }
    sum = 0.0;
    sum = dotprod(a, b, N);

    printf("Sum = %f\n",sum);
    return 0;
}
