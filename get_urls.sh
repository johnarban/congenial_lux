#!/usr/bin/bash
# ------------------------------------------------------------------------------
#   Helper functions
# ------------------------------------------------------------------------------

# use grep and sed to extract url from log
# usage: extract_url <log_file>
extract_url() {
    # from https://superuser.com/a/686530
    grep http $1 | sed 's/http/\nhttp/g' | grep ^http | sed 's/\(^http[^ <]*\)\(.*\)/\1/g' | sort -u

}
