// -*- flycheck-clang-include-path: libarchive-3.2.1/libarchive; -*-

#include "archive.h"
#include <stdlib.h>
#include <stdio.h>

int main(int argc, char **argv) {
    struct archive *a;
    struct archive_entry *entry;
    int r;

    a = archive_read_new();
    archive_read_support_filter_bzip2(a);
    archive_read_support_format_mtree(a);
    // archive_read_support_filter_all(a);
    // archive_read_support_format_all(a);
    r = archive_read_open_filename(a, argv[1], 10240); // Note 1
    if (r != ARCHIVE_OK)
        exit(1);
    r = archive_read_free(a);  // Note 3
    if (r != ARCHIVE_OK)
        exit(1);
}
