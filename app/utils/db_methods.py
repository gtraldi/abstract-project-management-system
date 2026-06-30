import sqlite3
import os

DB_PATH = "GestaoProjetos.db"

def get_connection():
    """Create and return a database connection."""
    return sqlite3.connect(DB_PATH)

def create_database() -> None:
    """Initialize the database and create tables if they do not exist."""
    with get_connection() as connection:
        cursor = connection.cursor()
        
        users_table = """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name VARCHAR(20) NOT NULL,
            last_name VARCHAR(60),
            cpf VARCHAR(15) NOT NULL UNIQUE,
            password VARCHAR(80) NOT NULL,
            email VARCHAR(50),
            user_type VARCHAR(80) NOT NULL,
            master_password VARCHAR(80)
        )"""
        
        projects_table = """
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            manager_cpf VARCHAR(15) NOT NULL,
            employee_ids TEXT NOT NULL,
            project_name VARCHAR(100) NOT NULL,
            employee_count INTEGER NOT NULL,
            purpose VARCHAR(100),
            description TEXT,
            status VARCHAR(80) NOT NULL,
            created_at VARCHAR(10),
            budget REAL,
            FOREIGN KEY(manager_cpf) REFERENCES users(cpf)
        )"""
        
        tasks_table = """
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT NOT NULL,
            project_id INTEGER,
            employee_id INTEGER,
            deadline VARCHAR(25),
            FOREIGN KEY (project_id) REFERENCES projects(id),
            FOREIGN KEY (employee_id) REFERENCES users(id)
        )"""
        
        history_table = """
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            activity_type VARCHAR(64) NOT NULL,
            project_id INTEGER,
            employee_id INTEGER,
            date VARCHAR(25),
            FOREIGN KEY (project_id) REFERENCES projects(id),
            FOREIGN KEY (employee_id) REFERENCES users(id)
        )"""
        
        cursor.execute(users_table)
        cursor.execute(projects_table)
        cursor.execute(tasks_table)
        cursor.execute(history_table)
        connection.commit()

def verify_login(login_cpf: str, password: str) -> bool:
    """Verify if user login credentials are valid."""
    try:
        with get_connection() as connection:
            cursor = connection.cursor()
            query = "SELECT password FROM users WHERE cpf = ?"
            cursor.execute(query, (login_cpf,))
            row = cursor.fetchone()
            if row:
                stored_password = row[0]
                if stored_password == password:
                    print("\n\033[1mWelcome! Access Connected!\033[0m")
                    return True
                else:
                    print("\n\033[1mIncorrect Password!\033[0m")
                    return False
            else:
                print("\n\033[1mUser not registered!\033[0m")
                return False
    except sqlite3.Error as e:
        print(f"Database error during login verification: {e}")
        return False

def verify_manager(manager_cpf: str) -> bool:
    """Verify if a user exists with the given manager CPF."""
    try:
        with get_connection() as connection:
            cursor = connection.cursor()
            query = "SELECT id FROM users WHERE cpf = ?"
            cursor.execute(query, (manager_cpf,))
            if cursor.fetchone():
                return True
            else:
                print("\n\033[1mInvalid CPF! Try again\n\033[0m")
                return False
    except sqlite3.Error as e:
        print(f"Database error during manager verification: {e}")
        return False

def get_user_type(login_cpf: str) -> str:
    """Get the user type (U, G, GM) for a given login CPF."""
    try:
        with get_connection() as connection:
            cursor = connection.cursor()
            query = "SELECT user_type FROM users WHERE cpf = ?"
            cursor.execute(query, (login_cpf,))
            row = cursor.fetchone()
            if row:
                return row[0]
            return None
    except sqlite3.Error as e:
        print(f"Database error getting user type: {e}")
        return None

def verify_master_manager(login_cpf: str, master_password: str) -> bool:
    """Verify credentials for privilege access (Gerente Master)."""
    try:
        with get_connection() as connection:
            cursor = connection.cursor()
            query = "SELECT id FROM users WHERE cpf = ? AND user_type = 'GM' AND master_password = ?"
            cursor.execute(query, (login_cpf, master_password))
            return cursor.fetchone() is not None
    except sqlite3.Error as e:
        print(f"Database error during master manager verification: {e}")
        return False

def verify_project_id(project_id: int) -> int:
    """Verify if a project exists and return its ID, otherwise return None."""
    try:
        with get_connection() as connection:
            cursor = connection.cursor()
            query = "SELECT id FROM projects WHERE id = ?"
            cursor.execute(query, (project_id,))
            row = cursor.fetchone()
            if row:
                return row[0]
            else:
                print("\n\033[1mInvalid ID! Project not found, try again\n\033[0m")
                return None
    except sqlite3.Error as e:
        print(f"Database error during project ID verification: {e}")
        return None

def register_user(first_name: str, last_name: str, email: str, login_cpf: str, password: str, user_type: str, master_password: str = None) -> None:
    """Register a new user in the database."""
    try:
        with get_connection() as connection:
            cursor = connection.cursor()
            query = """
                INSERT INTO users (first_name, last_name, email, cpf, password, user_type, master_password)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """
            cursor.execute(query, (first_name, last_name, email, login_cpf, password, user_type, master_password))
            connection.commit()
    except sqlite3.Error as e:
        raise Exception(f"Database error during user registration: {e}")

def get_user_id_by_cpf(cpf: str) -> list:
    """Retrieve user ID(s) associated with a CPF."""
    try:
        with get_connection() as connection:
            cursor = connection.cursor()
            query = "SELECT id FROM users WHERE cpf = ?"
            cursor.execute(query, (cpf,))
            return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Database error retrieving user ID: {e}")
        return []

def get_all_projects() -> list:
    """Get all projects from the database."""
    try:
        with get_connection() as connection:
            cursor = connection.cursor()
            query = "SELECT * FROM projects"
            cursor.execute(query)
            return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Database error retrieving all projects: {e}")
        return []

def get_projects_by_manager(manager_cpf: str) -> list:
    """Get projects managed by a specific manager CPF."""
    try:
        with get_connection() as connection:
            cursor = connection.cursor()
            query = "SELECT * FROM projects WHERE manager_cpf = ?"
            cursor.execute(query, (manager_cpf,))
            return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Database error retrieving projects by manager: {e}")
        return []

def get_username_by_cpf(cpf: str) -> str:
    """Get user's first name by their CPF."""
    try:
        with get_connection() as connection:
            cursor = connection.cursor()
            query = "SELECT first_name FROM users WHERE cpf = ?"
            cursor.execute(query, (cpf,))
            row = cursor.fetchone()
            if row:
                return row[0]
            return None
    except sqlite3.Error as e:
        print(f"Database error retrieving username: {e}")
        return None

def create_project(manager_cpf: str, employee_ids: str, project_name: str, employee_count: int, purpose: str, description: str, created_at: str, budget: float) -> None:
    """Insert a new project record into the database."""
    try:
        with get_connection() as connection:
            cursor = connection.cursor()
            query = """
                INSERT INTO projects (manager_cpf, employee_ids, project_name, employee_count, purpose, description, status, created_at, budget)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            cursor.execute(query, (manager_cpf, employee_ids, project_name, employee_count, purpose, description, 'To Do', created_at, budget))
            connection.commit()
    except sqlite3.Error as e:
        raise Exception(f"Database error during project creation: {e}")

def create_task(project_id: int, description: str) -> None:
    """Create a task for a project, assigning it to the project's primary user/employee."""
    try:
        with get_connection() as connection:
            cursor = connection.cursor()
            
            query_user = "SELECT employee_ids FROM projects WHERE id = ?"
            cursor.execute(query_user, (project_id,))
            row = cursor.fetchone()
            if not row:
                raise Exception("Project not found.")
            
            emp_ids_str = row[0].replace("[", "").replace("]", "").strip()
            first_emp_id = int(emp_ids_str.split(",")[0].strip())
            
            query_task = """
                INSERT INTO tasks (description, project_id, employee_id)
                VALUES (?, ?, ?)
            """
            cursor.execute(query_task, (description, project_id, first_emp_id))
            connection.commit()
    except sqlite3.Error as e:
        raise Exception(f"Database error during task creation: {e}")