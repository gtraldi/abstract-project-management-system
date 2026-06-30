import os
import pytest
import app.utils.db_methods as db_service

# Override the database path for testing
TEST_DB_PATH = "TestGestaoProjetos.db"
db_service.DB_PATH = TEST_DB_PATH

@pytest.fixture(autouse=True)
def setup_teardown_db():
    # Setup: ensure clean database for each test
    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)
    db_service.create_database()
    
    yield
    
    # Teardown: clean up database file
    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)

def test_database_initialization():
    assert os.path.exists(TEST_DB_PATH)

def test_register_and_verify_login():
    # Register a standard user
    db_service.register_user(
        first_name="Jane",
        last_name="Doe",
        email="jane.doe@example.com",
        login_cpf="12345678901",
        password="securepassword",
        user_type="U"
    )
    
    # Test valid login
    assert db_service.verify_login("12345678901", "securepassword") is True
    
    # Test incorrect password
    assert db_service.verify_login("12345678901", "wrongpassword") is False
    
    # Test non-registered user
    assert db_service.verify_login("99999999999", "anypassword") is False

def test_get_user_type():
    db_service.register_user(
        first_name="Alice",
        last_name="Smith",
        email="alice@example.com",
        login_cpf="98765432109",
        password="managerpass",
        user_type="G",
        master_password="privpassword"
    )
    
    assert db_service.get_user_type("98765432109") == "G"
    assert db_service.get_user_type("00000000000") is None

def test_verify_master_manager():
    db_service.register_user(
        first_name="Bob",
        last_name="Johnson",
        email="bob@example.com",
        login_cpf="11111111111",
        password="bobpass",
        user_type="GM",
        master_password="supersecret"
    )
    
    # Correct master credentials
    assert db_service.verify_master_manager("11111111111", "supersecret") is True
    
    # Wrong master password
    assert db_service.verify_master_manager("11111111111", "wrongsecret") is False

def test_create_and_verify_project():
    # Register manager and employee
    db_service.register_user(
        first_name="Manager",
        last_name="M",
        email="m@example.com",
        login_cpf="22222222222",
        password="mpass",
        user_type="G"
    )
    db_service.register_user(
        first_name="Employee",
        last_name="E",
        email="e@example.com",
        login_cpf="33333333333",
        password="epass",
        user_type="U"
    )
    
    # Verify manager exists
    assert db_service.verify_manager("22222222222") is True
    assert db_service.verify_manager("99999999999") is False
    
    # Create project
    db_service.create_project(
        manager_cpf="22222222222",
        employee_ids="[2]",
        project_name="Web Dev",
        employee_count=1,
        purpose="Portfolio",
        description="Build a nice website",
        created_at="30/06/2026",
        budget=5000.0
    )
    
    projects = db_service.get_all_projects()
    assert len(projects) == 1
    assert projects[0][3] == "Web Dev"  # Project name
    assert projects[0][9] == 5000.0    # Budget
    
    # Verify project ID
    proj_id = projects[0][0]
    assert db_service.verify_project_id(proj_id) == proj_id
    assert db_service.verify_project_id(999) is None
