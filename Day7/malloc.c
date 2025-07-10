//
// >>>> malloc challenge! <<<<
//
// Your task is to improve utilization and speed of the following malloc
// implementation.
// Initial implementation is the same as the one implemented in simple_malloc.c.
// For the detailed explanation, please refer to simple_malloc.c.

#include <assert.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define BIN_COUNT 10
//
// Interfaces to get memory pages from OS
//

void *mmap_from_system(size_t size);
void munmap_to_system(void *ptr, size_t size);

//
// Struct definitions
//

typedef struct my_metadata_t {
  size_t size;
  struct my_metadata_t *next;
} my_metadata_t;

typedef struct my_heap_t {
  my_metadata_t *bins[BIN_COUNT]; // ビンごとの空きリスト
} my_heap_t;

my_heap_t my_heap;

//
// Helper functions (feel free to add/remove/edit!)
//

// サイズに応じてビンのインデックスを返す
int get_bin_index(size_t size) {
  int index = 0;
  size_t bin_size = 8;
  while (index < BIN_COUNT - 1 && size > bin_size) {
    bin_size <<= 1; // bin_size *= 2
    index++;
  }
  return index;
}

void my_add_to_bin(my_metadata_t *metadata) {
  assert(metadata->next == NULL);
  int index = get_bin_index(metadata->size);
  metadata->next = my_heap.bins[index];
  my_heap.bins[index] = metadata;
}

void my_remove_from_bin(my_metadata_t *metadata, my_metadata_t *prev, int index) {
  if (prev) {
    prev->next = metadata->next;
  } else {
    my_heap.bins[index] = metadata->next;
  }
  metadata->next = NULL;
}

//
// Interfaces of malloc (DO NOT RENAME FOLLOWING FUNCTIONS!)
//

// This is called at the beginning of each challenge.
void my_initialize() {
  for (int i = 0; i < BIN_COUNT; i++) {
    my_heap.bins[i] = NULL;
  }
}

// my_malloc() is called every time an object is allocated.
// |size| is guaranteed to be a multiple of 8 bytes and meets 8 <= |size| <=
// 4000. You are not allowed to use any library functions other than
// mmap_from_system() / munmap_to_system().
void *my_malloc(size_t size) {
  int start_bin = get_bin_index(size);
  my_metadata_t *best_fit = NULL;
  my_metadata_t *best_prev = NULL;
  int best_index = -1;
  size_t min_diff = SIZE_MAX;

  for (int i = start_bin; i < BIN_COUNT; i++) {
    my_metadata_t *curr = my_heap.bins[i];
    my_metadata_t *prev = NULL;
    while (curr) {
      if (curr->size >= size) {
        size_t diff = curr->size - size;
        if (diff < min_diff) {
          best_fit = curr;
          best_prev = prev;
          best_index = i;
          min_diff = diff;
          if (diff == 0) break; // ぴったりなら決定
        }
      }
      prev = curr;
      curr = curr->next;
    }
    if (best_fit) break;
  }

  if (!best_fit) {
    size_t buffer_size = 4096;
    my_metadata_t *metadata = (my_metadata_t *)mmap_from_system(buffer_size);
    metadata->size = buffer_size - sizeof(my_metadata_t);
    metadata->next = NULL;
    my_add_to_bin(metadata);
    return my_malloc(size);
  }

  void *ptr = best_fit + 1;
  size_t remaining_size = best_fit->size - size;

  my_remove_from_bin(best_fit, best_prev, best_index);

  if (remaining_size > sizeof(my_metadata_t)) {
    best_fit->size = size;
    my_metadata_t *new_metadata = (my_metadata_t *)((char *)ptr + size);
    new_metadata->size = remaining_size - sizeof(my_metadata_t);
    new_metadata->next = NULL;
    my_add_to_bin(new_metadata);
  }

  return ptr;
}

// This is called every time an object is freed.  You are not allowed to
// use any library functions other than mmap_from_system / munmap_to_system.
void my_free(void *ptr) {
  my_metadata_t *metadata = (my_metadata_t *)ptr - 1;
  my_add_to_bin(metadata);
}

// This is called at the end of each challenge.
void my_finalize() {
  // Nothing is here for now.
  // feel free to add something if you want!
}

void test() {
  // Implement here!
  assert(1 == 1); /* 1 is 1. That's always true! (You can remove this.) */
}
