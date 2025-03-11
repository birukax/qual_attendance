import requests
from .models import Employee, Department
from decouple import config
from requests_ntlm import HttpNtlmAuth
import requests


def employee_get():
    url = config("NAV_EMPLOYEES")
    user = config("NAV_INSTANCE_USER")
    password = config("NAV_INSTANCE_PASSWORD")
    auth = HttpNtlmAuth(user, password)
    try:
        response = requests.get(url, auth=auth)
        if response.ok:
            data = response.json()
            for emp in data["value"]:
                exists = Employee.objects.filter(employee_id=emp["No"])
                if emp["Termination_Date"] > emp["Employment_Date"]:
                    termination_date = emp["Termination_Date"]
                else:
                    termination_date = None
                if Department.objects.filter(
                    code=emp["Global_Dimension_1_Code"]
                ).exists():
                    department = Department.objects.get(
                        code=emp["Global_Dimension_1_Code"]
                    )
                else:
                    department = None
                if exists.exists():
                    exists = exists.first()
                    exists.name = emp["FullName"]
                    exists.department = department
                    exists.employment_date = emp["Employment_Date"]
                    exists.termination_date = termination_date
                    exists.status = emp["Status"]
                    exists.save()
                else:
                    employee = Employee(
                        employee_id=emp["No"],
                        name=emp["FullName"],
                        department=department,
                        employment_date=emp["Employment_Date"],
                        termination_date=termination_date,
                        status=emp["Status"],
                    )
                    employee.save()
        else:
            print(response.headers)
            response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}")  # Handle errors
        if "Kerberos" in str(e): #This could indicate that the SPN is missing or incorrect
            print("The error might be Kerberos related. Check the SPN for the service.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def department_get():
    url = config("NAV_DEPARTMENTS")
    user = config("NAV_INSTANCE_USER")
    password = config("NAV_INSTANCE_PASSWORD")
    auth = HttpNtlmAuth(user, password)

    try:
        response = requests.get(url, auth=auth)
        if response.ok:
            data = response.json()
            for dept in data["value"]:
                exists = Department.objects.filter(code=dept["Code"])
                if exists.exists():
                    exists = exists.first()
                    exists.department = dept["Name"]
                    exists.save()
                else:
                    department = Department(
                        code=dept["Code"],
                        name=dept["Name"],
                    )
                    department.save()
        else:
            print(response.status_code, response.reason)
    except Exception as e:
        print(e)
