from sqlite3 import connect
from CommonDefinitions import category_names_lst, priority_names_lst
from NotePureData_classdef import NotePureData

# DB: establishment
db_name = 'ToDoListPOC.sqlite'
conn = connect(db_name)
c = conn.cursor()

# creation of tables
def db_init():
    """This function creates tables notes, categories, priorities, and populates categories and priorities tables"""

    sqlcmd_crtable_notes = 'create table if not exists notes (n_id integer primary key, ctgr_id integer not null, n_description varchar not null, n_date varchar not null, prrt_id integer not null, foreign key (ctgr_id) references categories(c_id), foreign key (prrt_id) references priorities(p_id))'
    c.execute(sqlcmd_crtable_notes)

    sqlcmd_crtable_categories = 'create table if not exists categories (c_id integer primary key, c_description varchar)'
    c.execute(sqlcmd_crtable_categories)
    # filling data into table categories
    db_fill_categories()

    sqlcmd_crtable_priorities = 'create table if not exists priorities (p_id integer primary key, p_description varchar)'  # P_BGCOLOR too??? NOT SURE WHETHER MECESSARY AT ALL
    c.execute(sqlcmd_crtable_priorities)
    # filling data into table priorities
    db_fill_priorities()

def db_fill_categories():
    """This function populates categoties table with names stored in the category_names_lst"""

    for val in category_names_lst:
        sqlcmd_insert_category = f"insert into categories(c_description) select '{val}' val where not exists (select 1 from categories where c_description = val)"  # for every record to be inserted only once
        c.execute(sqlcmd_insert_category)
    conn.commit()

def db_fill_priorities():
    """This function populates priority table with names stored in the priority_names_lst"""

    for val in priority_names_lst:
        # each record is to be inserted only once
        sqlcmd_insert_priority = f"insert into priorities(p_description) select '{val}' val where not exists (select 1 from priorities where p_description = val)"

        # each record is to be inserted only once NOT IN USE: bgcolor values currently are not to be stored
        # sqlcmd_insert_bgcolor = f"insert into priorities(p_bgcolor) select '{val}' val where not exists (select 1 from priorities where p_bgcolor = val)"

        c.execute(sqlcmd_insert_priority)
    conn.commit()

# DB: connection termination
def db_terminate():
    c.close()
    conn.close()

# functions that execute SQL queries and statements
def db_select_notes():
    """This function reads and returns details of all existing notes"""

    sqlcmd_select_notes = 'select n_id, c_description, n_description, n_date, p_description from notes, priorities, categories where ctgr_id = c_id and prrt_id = p_id'
    c.execute(sqlcmd_select_notes)
    conn.commit()  # looks like not necessary in case of SELECT statement
    return c.fetchall()

def db_get_max_noteid():
    """This function returns the highest id number of all notes stored in the database"""

    sqlcmd_select_max_id = 'select max(n_id) from notes'
    c.execute(sqlcmd_select_max_id)
    conn.commit()  # looks like not necessary in case of SELECT statement
    return c.fetchone()[0]  # also return c.fetchall()[0][0] works :)

def db_insert_note(note_data_container): # NEW VERSION
    """This function adds new note record to the database"""

    if isinstance(note_data_container, NotePureData):
        note_category = note_data_container.category
        note_priority = note_data_container.priority
        note_id = note_data_container.id
        note_descr = note_data_container.description
        note_date = note_data_container.date
    elif isinstance(note_data_container, tuple):
        note_category = note_data_container[1]
        note_priority = note_data_container[4]
        note_id = note_data_container[0]
        note_descr = note_data_container[2]
        note_date = note_data_container[3]

    sqlcmd_select_c_id = f"select c_id from categories where c_description = '{note_category}'"
    sqlcmd_select_p_id = f"select p_id from priorities where p_description = '{note_priority}'"
    sqlcmd_insert_note = f"insert into notes(n_id, ctgr_id, n_description, n_date, prrt_id) values ('{note_id}', ({sqlcmd_select_c_id}), '{note_descr}', '{note_date}', ({sqlcmd_select_p_id}))"
    c.execute(sqlcmd_insert_note)
    conn.commit()

def db_delete_note(note_id):
    """This function deletes record of the specified note from the database"""

    sqlcmd_delete_note = f"delete from notes where n_id = '{note_id}'"
    c.execute(sqlcmd_delete_note)
    conn.commit()

def db_update_note(note_data_container): # NEW VERSION
    """This function updates details of the specified note; accepts note details either as tuple or as object of type NotePureData"""

    if type(note_data_container) == NotePureData:
        note_category = note_data_container.category
        note_priority = note_data_container.priority
        note_id = note_data_container.id
        note_descr = note_data_container.description
        note_date = note_data_container.date
    elif type(note_data_container) == tuple:
        note_category = note_data_container[1]
        note_priority = note_data_container[4]
        note_id = note_data_container[0]
        note_descr = note_data_container[2]
        note_date = note_data_container[3]

    sqlcmd_select_c_id = f"select c_id from categories where c_description = '{note_category}'"
    sqlcmd_select_p_id = f"select p_id from priorities where p_description = '{note_priority}'"

    # updating all the columns i.e. including values that actually haven't been changed
    # sqlcmd_update_note = f"update notes set n_description = '{note_descr}', n_date = '{note_date}', prrt_id = ({sqlcmd_select_p_id}) where n_id = '{note_id}'"

    # upgraded SQL statement: updates only if new value differs from the old value
    subselect = f"select notes.ctgr_id, notes.n_description, notes.n_date, notes.prrt_id except select ctgr_id = ({sqlcmd_select_c_id}), n_description = '{note_descr}', n_date = '{note_date}', prrt_id = ({sqlcmd_select_p_id})"
    sqlcmd_update_note = f"update notes set ctgr_id = ({sqlcmd_select_c_id}), n_description = '{note_descr}', n_date = '{note_date}', prrt_id = ({sqlcmd_select_p_id}) where n_id = '{note_id}' and exists ({subselect})"
    c.execute(sqlcmd_update_note)
    conn.commit()

def db_clean_tbl_notes():
    """This functions deletes all records fron the notes table"""

    sqlcmd_clean_tbl_notes = f'delete from notes'
    c.execute(sqlcmd_clean_tbl_notes)
    conn.commit()

'''
# NOT IN USE
def db_select_priorities():
    sqlcmd_select_p_descr = 'select p_description from priorities'
    c.execute(sqlcmd_select_p_descr)
    conn.commit()  # looks like not necessary in case of SELECT statement
    return c.fetchall()
'''