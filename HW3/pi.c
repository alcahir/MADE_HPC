#include <omp.h>

#include <stdio.h>

#include <stdlib.h>

#include <time.h>

int main(int argc, char ** argv) {
  float sum;
  int i;
  int num_threads = atoi(argv[2]);
  int N = atoi(argv[1]);
  sum = 0.0;
  omp_set_num_threads(num_threads);

  double begin_time = omp_get_wtime();
  #pragma omp parallel\
  shared(N)\
  private(i) {
    unsigned int seed = time(NULL) + omp_get_thread_num() + 42;
    #pragma omp
    for reduction(+: sum)
    for (i = 0; i < N; ++i) {
      double x = (double) rand_r( & seed) / (double) RAND_MAX;
      double y = (double) rand_r( & seed) / (double) RAND_MAX;
      /*printf("X=%f, Y=%f, num_t=%d, thread=%d\n", x, y, seed, omp_get_thread_num());*/
      if (x * x + y * y < 1.0) {
        sum += 1;
      }
    }
  }
  double end_time = omp_get_wtime();
  printf("%fs\n", end_time - begin_time);
  printf("PI = %f\n", 4 * sum / N);
  return 0;
}