import app.utils.db_methods as db_service
import time
from datetime import datetime

class User:
    @staticmethod
    def login() -> tuple:
        menu = """
                             Project Management System                    
        """
        print(menu)
        login_cpf = input("Enter your access credential (CPF): ")
        password = input("Enter your password: ")
        return login_cpf, password
    
    @staticmethod
    def register() -> tuple:
        login_cpf = ""
        password = ""

        menu = """
                             Project Management System                    
        """
        print(menu)
        user_type = input("User Type (User (U), Manager (G), Master Manager (GM)): ")
        if user_type in ["U", "G", "GM"]:
            if user_type in ["G", "GM"]:
                first_access = input("First Access? (y/n): ")
                if first_access == "y":
                    user_type = "GM"
                    print("Register Master Manager details")
                    first_name = input("Enter your first name: ")
                    last_name = input("Enter your last name: ")
                    email = input("Enter your email: ")
                    login_cpf = input("Enter your CPF (numbers only): ")
                    password = input("Enter your password: ")
                    master_password = input("Create your privileged access password: ")

                    db_service.register_user(first_name, last_name, email, login_cpf, password, user_type, master_password)
                    print("\n\033[1mRegistration completed successfully!\n\033[0m")
                elif first_access == "n":
                    login_gm = input("Enter CPF with privileged access: ")
                    master_password = input("Enter password for privileged access: ")
                    permission = db_service.verify_master_manager(login_gm, master_password)
                    if permission:
                        first_name = input("Enter your first name: ")
                        last_name = input("Enter your last name: ")
                        email = input("Enter your email: ")
                        login_cpf = input("Enter your CPF (numbers only): ")
                        password = input("Enter your password: ")
                        master_password = input("Create your privileged access password: ")
                        db_service.register_user(first_name, last_name, email, login_cpf, password, user_type, master_password)
                        print("\n\033[1mRegistration completed successfully!\n\033[0m")
                    else:
                        print("\n\033[1mAccess denied! You do not have permission!\n\033[0m")

            elif user_type == "U":
                first_name = input("Enter your first name: ")
                last_name = input("Enter your last name: ")
                email = input("Enter your email: ")
                login_cpf = input("Enter your CPF (numbers only): ")
                password = input("Enter your password: ")

                db_service.register_user(first_name, last_name, email, login_cpf, password, user_type)
                print("\n\033[1mRegistration completed successfully!\n\033[0m")
        else:
            print("\n\033[1mPlease enter a valid user type!\033[0m")

        return login_cpf, password
    
    @staticmethod
    def project_progress() -> None:
        user_id = []
        user_projects = []

        while len(user_id) <= 0:
            menu = """
                                Project Management System                    
            """
            print(menu)
            cpf = input("Enter your CPF: ")
            user_id = db_service.get_user_id_by_cpf(cpf)

            if len(user_id) <= 0:
                print("\n\033[1mInvalid User!\n\033[0m")
                menu = """
                                        Project Management System

                1 - Back to main menu                               2 - Try again                    
                """
                opc_menu = None
                while opc_menu != '1': 
                    print(menu)
                    opc_menu = input("Select an option: ")
                    if opc_menu == '1':
                        return None
                    elif opc_menu == '2':
                        break
                    else:
                        print("Select a valid option!")
            
        user_id_val = user_id[0][0]
        projects = db_service.get_all_projects()

        for project in projects:
            emp_ids = str(project[2])
            if len(emp_ids) > 0:
                ids_list = emp_ids.replace("[", "").replace("]", "").split(",")
                for i in range(len(ids_list)):
                    ids_list[i] = ids_list[i].strip()
                
                if str(user_id_val) in ids_list:
                    user_projects.append(project)

        if len(user_projects) > 0:
            for project in user_projects:
                print(f"\n\033[1mProject Name\033[0m: {str(project[3])} - \033[1mStatus\033[0m: {str(project[7])}")
        else:
            print("No projects found!")

        time.sleep(5)

        opc_menu = None
        while opc_menu != '1':
            menu = """
                             Project Management System
            
1 - Back to main menu                                                    
            """
            print(menu)
            opc_menu = input("Select an option: ")
            if opc_menu == '1':
                return None
            else:
                print("Select a valid option!")

    @staticmethod
    def communication() -> None:
        user_id = []
        user_projects = []

        while len(user_id) <= 0:
            menu = """
                                Project Management System                    
            """
            print(menu)
            cpf = input("Enter your CPF: ")
            user_id = db_service.get_user_id_by_cpf(cpf)

            if len(user_id) <= 0:
                print("\n\033[1mInvalid User!\n\033[0m")
                menu = """
                                        Project Management System

                1 - Back to main menu                               2 - Try again                    
                """
                opc_menu = None
                while opc_menu != '1': 
                    print(menu)
                    opc_menu = input("Select an option: ")
                    if opc_menu == '1':
                        return None
                    elif opc_menu == '2':
                        break
                    else:
                        print("Select a valid option!")
        
        user_id_val = user_id[0][0]
        projects = db_service.get_all_projects()

        for project in projects:
            emp_ids = str(project[2])
            if len(emp_ids) > 0:
                ids_list = emp_ids.replace("[", "").replace("]", "").split(",")
                for i in range(len(ids_list)):
                    ids_list[i] = ids_list[i].strip()
                
                if str(user_id_val) in ids_list:
                    user_projects.append(project)
        
        if len(user_projects) > 0:
            for project in user_projects:
                print(f"\n\033[1mProject ID\033[0m: {str(project[0])} - \033[1mProject Name\033[0m: {str(project[3])} - \033[1mManager CPF\033[0m: {str(project[1])}")
        else:
            print("No projects found!")

        time.sleep(5)

        opc_menu = None
        while opc_menu != '0':
            menu = """
                                    Project Management System
            
            1 - Send Message                                          2 - Back to main menu                                                    
            """
            print(menu)
            opc_menu = input("Select an option: ")
            if opc_menu == '1':
                cpf_gerente = input("Enter the CPF of the manager responsible for this project: ")
                nome_gerente = db_service.get_username_by_cpf(cpf_gerente)

                if nome_gerente:
                    print(f"Chat with Manager {nome_gerente.title()}")
                    input("Type your message: ")
                    print("Sending message...")
                    time.sleep(3)
                    print("Message sent!")
                    time.sleep(2)
                else:
                    print("\n\033[1mInvalid CPF!\n\033[0m")
                    opc_menu = None
            elif opc_menu == '2':
                break
            else:
                print("Select a valid option!")


class Manager(User):
    @staticmethod
    def create_project() -> None:
        user_id = []
        list_ids = []
        verifica = False
        opc_menu = None

        while len(user_id) <= 0 or not verifica:
            menu = """
                                Project Management System                    
            """
            print(menu)
            cpf_gerente = input("Enter your CPF: ")
            verifica = db_service.verify_manager(cpf_gerente)
            
            if not verifica:    
                menu = """
                                            Project Management System
            
                1 - Back to main menu                                        2 - Try again                                                   
                """
                print(menu)
                opc_menu = input("Select an option: ")
                while opc_menu != '0':
                    if opc_menu == '1':
                        return None
                    elif opc_menu == '2':
                        break
                    else:
                        print("\n\033[1mSelect a valid option!\n\033[0m")
            else:
                qtd_funcionarios = input("Enter the number of employees working on the project: ")

                i = 0
                while i != int(qtd_funcionarios):
                    cpf_usuario = input("Enter the CPF of the employee who will work on the project: ")
                    user_id = db_service.get_user_id_by_cpf(cpf_usuario)

                    if len(user_id) <= 0:
                        print("\n\033[1mInvalid User!\n\033[0m")
                        menu = """
                                                Project Management System
                
                        1 - Back to main menu                                        2 - Try again                     
                        """
                        opc_menu = None
                        while opc_menu != '1': 
                            print(menu)
                            opc_menu = input("Select an option: ")
                            if opc_menu == '1':
                                return None
                            elif opc_menu == '2':
                                break
                            else:
                                print("Select a valid option!")
                    else:
                        i += 1
                        user_id_val = str(user_id[0][0])
                        if user_id_val in list_ids:
                            print("\nThis user has already been added!\n")
                        else:
                            list_ids.append(user_id_val)
                
                id_usuarios = ""
                for id_val in list_ids:
                    id_usuarios = id_usuarios + f"{id_val}, "

                id_usuarios = f"[{id_usuarios}]"
                        
                nome_projeto = input("Enter project name: ")
                finalidade = input("Enter project purpose: ")
                descricao = input("Enter project description: ")
                data_criacao = datetime.now().strftime("%d/%m/%Y")
                orcamento = float(input("Enter budget allocated for the project: "))

                db_service.create_project(cpf_gerente, id_usuarios, nome_projeto, qtd_funcionarios, finalidade, descricao, data_criacao, orcamento)
                print("Creating project...")
                time.sleep(3)
                print("Project created successfully!")
                time.sleep(2)
                return None
    
    @staticmethod
    def project_progress() -> None:
        projetos = []
        while len(projetos) <= 0:
            menu = """
                                Project Management System                    
            """
            print(menu)
            cpf_gerente = input("Enter your CPF: ")
            verifica = db_service.verify_manager(cpf_gerente)
            if not verifica:
                menu = """
                                            Project Management System
            
                1 - Back to main menu                                        2 - Try again                                                   
                """
                print(menu)
                opc_menu = input("Select an option: ")
                while opc_menu != '0':
                    if opc_menu == '1':
                        return None
                    elif opc_menu == '2':
                        break
                    else:
                        print("\n\033[1mSelect a valid option!\n\033[0m")
            else:
                projetos = db_service.get_projects_by_manager(cpf_gerente)

                if len(projetos) > 0:
                    for project in projetos:
                        print(f"\n\033[1mProject ID\033[0m: {str(project[0])} - \033[1mProject Name\033[0m: {str(project[3])} - " \
                              + f"\033[1mStatus\033[0m: {str(project[7])} - \033[1mManager CPF\033[0m: {str(project[1])} - " \
                              + f"\033[1mEmployee IDs\033[0m: {str(project[2])} - \033[1mEmployee Count\033[0m: {str(project[4])}")
                    time.sleep(5)
                else:
                    print("No projects found!")
                    time.sleep(5)
                    
                    opc_menu = None
                    while opc_menu != '1':
                        menu = """
                                        Project Management System
                        
            1 - Back to main menu                                                    
                        """
                        print(menu)
                        opc_menu = input("Select an option: ")
                        if opc_menu == '1':
                            return None
                        else:
                            print("Select a valid option!")

    @staticmethod
    def assign_task() -> None:
        verifica = False
        while not verifica:
            menu = """
                                    Project Management System                    
                """
            print(menu)
            id_projeto = input("Enter the project ID: ")
            verifica = db_service.verify_project_id(id_projeto)

            if not verifica:
                menu = """
                                            Project Management System
            
                1 - Back to main menu                                        2 - Try again                                                   
                """
                print(menu)
                opc_menu = input("Select an option: ")
                while opc_menu != '0':
                    if opc_menu == '1':
                        return None
                    elif opc_menu == '2':
                        break
                    else:
                        print("\n\033[1mSelect a valid option!\n\033[0m")
            else:
                descricao = input("Enter task description: ")
                db_service.create_task(id_projeto, descricao)

                print("\nAssigning task...")
                time.sleep(2)
                print("Task created successfully!")
                time.sleep(2)
                return None

    @staticmethod
    def project_dashboard() -> None:
        pass
        
    @staticmethod
    def deadline_management() -> None:
        pass
        
    @staticmethod
    def generate_report() -> None:
        pass
        
    @staticmethod
    def check_budget() -> None:
        pass
        
    @staticmethod
    def activity_history() -> None:
        pass


class MasterManager(Manager):
    @staticmethod
    def system_configuration() -> None:
        pass