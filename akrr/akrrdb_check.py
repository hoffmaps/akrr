import os
import sys
import inspect

#modify python_path so that we can get /src on the path
cur_dir=os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
if (cur_dir+"/../../src") not in sys.path:
    sys.path.append(cur_dir+"/../../src")

from util import logging as log
import akrr

# Attempt to import MySQL, if it's not there then we'll exit out and notify the
# user and blow up.
try:
    import MySQLdb
    mysql_available = True
except ImportError, e:
    mysql_available = False


def check_rw_db(connection_func, pre_msg, post_msg):
    """
    Check that the user has the correct privileges to the database
    at the end of the connection provided by 'connection_func'. Specifically, checking
    for read / write permissions ( and create table ).

    :type connection_func function
    :type pre_msg str
    :type post_msg str

    :param connection_func: the function that will provide a (connection, cursor) tuple.
    :param pre_msg:         a message to be provided to the user before the checks begin.
    :param post_msg:        a message to be provided to the user after the checks are successful
    :return: true if the database is available / the provided user has the correct privileges.
    """
    success = False
    log.info(pre_msg)

    try:
        connection, cursor = connection_func()

        try:
            with connection:
                result = cursor.execute("CREATE TABLE CREATE_ME(`id` INT NOT NULL PRIMARY KEY, `name` VARCHAR(48));")
                success = True if result == 0 else False

                if success:
                    log.info(post_msg, success)
                else:
                    log.error(post_msg, success)

        except MySQLdb.MySQLError, e:
            log.error('Unable to create a table w/ the provided username. {0}: {1}', e.args[0], e.args[1])

        connection, cursor = connection_func()
        try:
            with connection:
                cursor.execute("DROP TABLE CREATE_ME;")
        except MySQLdb.MySQLError, e:
            log.error('Unable to drop the table created to check permissions. {0}: {1}', e.args[0], e.args[1])

    except MySQLdb.MySQLError, e:
        log.error('Unable to connect to Database. {0}: {1}', e.args[0], e.args[1])

    return success


def check_r_db(connection_func, pre_msg, post_msg):
    """
    Check that the user has the correct privileges to the database
    at the end of the connection provided by 'connection_func'.
    Specifically checking for read permissions.

    :type connection_func function
    :type pre_msg str
    :type post_msg str

    :param connection_func: the function that will provide a (connection, cursor) tuple.
    :param pre_msg:         a message to be provided to the user before the checks begin.
    :param post_msg:        a message to be provided to the user after the checks are successful
    :return: true if the database is available / the provided user has the correct privileges.
    """
    success = False
    log.info(pre_msg)

    try:
        connection, cursor = connection_func()

        try:
            with connection:
                result = cursor.execute("SELECT COUNT(*) FROM `modw`.`resourcefact`;")
                success = True if result >= 0 else False

                if success:
                    log.info(post_msg, success)
                else:
                    log.error(post_msg, success)

        except MySQLdb.MySQLError, e:
            log.error('Unable to select from `modw`.`resourcefact`. {0}: {1}', e.args[0], e.args[1])

    except MySQLdb.MySQLError, e:
        log.error('Unable to connect to Database. {0}: {1}', e.args[0], e.args[1])

    return success

def akrrdb_check():

    # CHECK: to make sure that we have MySQL drivers before continuing.
    if not mysql_available:
        log.error("Unable to find MySQLdb. Please install MySQLdb for python before running this script again.")
        exit(1)

    # CHECK: the akrr db
    akrr_ok = check_rw_db(akrr.getDB,
                      "Checking 'mod_akrr' Database / User privileges...",
                      "'mod_akrr' Database check complete - Status: {0}")





    # Check: the app_kernel db
    app_kernel_ok = check_rw_db(akrr.getAKDB,
                             "Checking 'mod_appkernel' Database / User privileges...",
                             "'mod_appkernel' Database check complete - Status: {0}")

    # CHECK: the XDMoD db
    xdmod_ok = check_r_db(akrr.getXDDB,
                          "Checking 'modw' Database / User privileges...",
                          "'modw' Database check complete - Status: {0}")

    # DETERMINE: whether or not everything passed.
    overall_success = akrr_ok and app_kernel_ok and xdmod_ok

    if overall_success:
        log.info("All Databases / User privileges check out!")
    else:
        log.error("One or more of the required databases and their required users ran into a problem. Please take note of the previous messages, correct the issue and re-run this script.")
        exit(1)

if __name__ == '__main__':
    akrrdb_check()
    