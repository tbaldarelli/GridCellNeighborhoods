/**
 * Simple test to verify Check framework is working
 */

#include <check.h>
#include <stdlib.h>
#include "../include/position.h"
#include "../include/grid.h"

START_TEST(test_simple_position) {
    Position pos = position_create(5, 10);
    ck_assert_int_eq(pos.row, 5);
    ck_assert_int_eq(pos.column, 10);
}
END_TEST

START_TEST(test_simple_grid) {
    Grid* grid = grid_create(10, 10, NULL, 0);
    ck_assert_ptr_nonnull(grid);
    ck_assert_int_eq(grid->height, 10);
    ck_assert_int_eq(grid->width, 10);
    grid_destroy(grid);
}
END_TEST

Suite* simple_suite(void) {
    Suite* s = suite_create("Simple Tests");
    TCase* tc = tcase_create("Core");
    tcase_add_test(tc, test_simple_position);
    tcase_add_test(tc, test_simple_grid);
    suite_add_tcase(s, tc);
    return s;
}

int main(void) {
    int number_failed;
    Suite* s = simple_suite();
    SRunner* sr = srunner_create(s);
    
    srunner_run_all(sr, CK_VERBOSE);
    number_failed = srunner_ntests_failed(sr);
    srunner_free(sr);
    
    return (number_failed == 0) ? 0 : 1;
}
