/**
 * Single property test for debugging
 */

#include <check.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>
#include "../include/position.h"

#define PROPERTY_TEST_ITERATIONS 10

static int rand_range(int min, int max) {
    return min + rand() % (max - min + 1);
}

START_TEST(test_manhattan_distance_calculation) {
    for (int i = 0; i < PROPERTY_TEST_ITERATIONS; i++) {
        int row1 = rand_range(0, 100);
        int col1 = rand_range(0, 100);
        int row2 = rand_range(0, 100);
        int col2 = rand_range(0, 100);
        
        Position pos1 = position_create(row1, col1);
        Position pos2 = position_create(row2, col2);
        
        int distance = position_manhattan_distance(pos1, pos2);
        int expected_distance = abs(row1 - row2) + abs(col1 - col2);
        
        ck_assert_int_eq(distance, expected_distance);
        ck_assert_int_ge(distance, 0);
        
        if (row1 == row2 && col1 == col2) {
            ck_assert_int_eq(distance, 0);
        }
        
        ck_assert_int_eq(position_manhattan_distance(pos1, pos2), 
                        position_manhattan_distance(pos2, pos1));
    }
}
END_TEST

Suite* test_suite(void) {
    Suite* s = suite_create("One Property");
    TCase* tc = tcase_create("Manhattan Distance");
    tcase_add_test(tc, test_manhattan_distance_calculation);
    suite_add_tcase(s, tc);
    return s;
}

int main(void) {
    srand(time(NULL));
    
    int number_failed;
    Suite* s = test_suite();
    SRunner* sr = srunner_create(s);
    
    srunner_run_all(sr, CK_VERBOSE);
    number_failed = srunner_ntests_failed(sr);
    srunner_free(sr);
    
    return (number_failed == 0) ? 0 : 1;
}
