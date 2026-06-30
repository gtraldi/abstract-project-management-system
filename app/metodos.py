import app.utils.db_methods as db_service
import classes as cl

def login_access() -> str:
    menu = """
                             Project Management System
                             
    1 - Login
    2 - Register User
    """

    menu_option = 0
    success = False
    login_cpf = ""
    
    while not success:
        while menu_option not in [1, 2]:
            print(menu)
            try:
                menu_option = int(input("Select an option: "))
            except ValueError:
                print("\n\033[1mPlease enter a valid number!\033[0m")
                continue
                
            if menu_option == 1:
                login_cpf, password = cl.User.login()
                success = db_service.verify_login(login_cpf, password)
            elif menu_option == 2:
                login_cpf, password = cl.User.register()
                success = True
            else:
                print("\n\033[1mPlease select a valid option!\033[0m")
        
        if not success:
            menu_option = 0

    return login_cpf

def main_menu(login_cpf: str) -> None:
    user_type = str(db_service.get_user_type(login_cpf))

    if user_type == "U":
        menu_text = """
                                    Project Management System
        
        1 - Project Progress                                       3 - Exit Program
        2 - Communication                                            
        """
    
        menu_option = None
        while menu_option != 0:
            print(menu_text)
            try:
                menu_option = int(input("Select an option: "))
            except ValueError:
                print("Invalid Option! Please enter a number!")
                continue

            if menu_option == 1:
                menu_option = cl.User.project_progress()
            elif menu_option == 2:
                menu_option = cl.User.communication()
            elif menu_option == 3:
                print("Exiting program!")
                menu_option = 0
            else:
                print("Invalid Option! Try again!")   

    elif user_type == "G":
        menu_text = """
                                        Project Management System
            
            1 - Create Project                                         6 - Generate Reports
            2 - Assign Tasks                                           7 - Communication
            3 - Project Progress                                       8 - Budgets
            4 - Project Dashboard                                      9 - Activity History
            5 - Deadline Management                                    10 - Exit Program                                  
        """

        menu_option = None
        while menu_option != 0:
            print(menu_text)
            try:
                menu_option = int(input("Select an option: "))
            except ValueError:
                print("Invalid Option! Please enter a number!")
                continue
                
            if menu_option == 1:
                menu_option = cl.Manager.create_project()
            elif menu_option == 2:
                menu_option = cl.Manager.assign_task()
            elif menu_option == 3:
                menu_option = cl.Manager.project_progress()
            elif menu_option == 4:
                menu_option = cl.Manager.project_dashboard()
            elif menu_option == 5:
                menu_option = cl.Manager.deadline_management()
            elif menu_option == 6:
                menu_option = cl.Manager.generate_report()
            elif menu_option == 7:
                menu_option = cl.User.communication()
            elif menu_option == 8:
                menu_option = cl.Manager.check_budget()
            elif menu_option == 9:
                menu_option = cl.Manager.activity_history()
            elif menu_option == 10:
                print("Exiting program!")
                menu_option = 0
            else:
                print("Incorrect Option! Try again!")
    
    elif user_type == "GM":
        menu_text = """
                                        Project Management System
            
            1 - Create Project                                         7 - Communication
            2 - Assign Tasks                                           8 - Budgets
            3 - Project Progress                                       9 - Activity History
            4 - Project Dashboard                                      10 - System Settings
            5 - Deadline Management                                    11 - Exit Program 
            6 - Generate Reports                             
        """

        menu_option = None
        while menu_option != 0:
            print(menu_text)
            try:
                menu_option = int(input("Select an option: "))
            except ValueError:
                print("Invalid Option! Please enter a number!")
                continue
                
            if menu_option == 1:
                menu_option = cl.Manager.create_project()
            elif menu_option == 2:
                cl.Manager.assign_task()
            elif menu_option == 3:
                menu_option = cl.User.project_progress()
            elif menu_option == 4:
                cl.Manager.project_dashboard()
            elif menu_option == 5:
                cl.Manager.deadline_management()
            elif menu_option == 6:
                cl.Manager.generate_report()
            elif menu_option == 7:
                menu_option = cl.User.communication()
            elif menu_option == 8:
                menu_option = cl.Manager.check_budget()
            elif menu_option == 9:
                menu_option = cl.Manager.activity_history()
            elif menu_option == 10:
                cl.MasterManager.system_configuration()
            elif menu_option == 11:
                print("Exiting program!")
                menu_option = 0
            else:
                print("Incorrect Option! Try again!")

def main() -> None:
    db_service.create_database()
    print("Database tables initialized successfully.")