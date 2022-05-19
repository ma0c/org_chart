import requests
import sys

from django.conf import settings
from django.urls import path
from django.core.management import execute_from_command_line
from django.http import HttpResponse

settings.configure(
    DEBUG=True,
    SECRET_KEY='A-random-secret-key!',
    ROOT_URLCONF=sys.modules[__name__],
)

EMPLOYEES_ENDPOINT = "https://gist.githubusercontent.com/chancock09/6d2a5a4436dcd488b8287f3e3e4fc73d/raw/fa47d64c6d5fc860fabd3033a1a4e3c59336324e/employees.json"

EMPLOYEE_ORG_TREE_URL_NAME = "employee_org_tree"


def get_org_chart():
    response = requests.get(EMPLOYEES_ENDPOINT)
    response.raise_for_status()
    return response.json()


def build_tree(employee_id, children, local_managers):
    if not children:
        return dict()
    return {x: build_tree(x, local_managers.get(x), local_managers) for x in children}


def print_tree(tree, employees_by_id, level):
    render_value = "<ul>"
    for root, leaves in tree.items():
        render_value += f"<li>" \
                        f"{'  '*level} {employees_by_id[root]['title']}: {employees_by_id[root]['name']}"
        sorted_leaves = sorted(
            [
                (
                    leaf,
                    employees_by_id[leaf]['name'].split(" ")[1]
                )
                for leaf in leaves.keys()
            ],
            key=lambda x: x[1]
        )
        for leaf_key, _ in sorted_leaves:
            render_value += print_tree({leaf_key: leaves[leaf_key]}, employees_by_id, level+1)
        render_value += "</li>"
    render_value += "</ul>"
    return render_value


def process_org_chart():
    employees_data = get_org_chart()
    employees_by_id = {employee.get("id"): employee for employee in employees_data}
    local_managers = dict()
    processed_employees = list()
    for employee_id, employee in employees_by_id.items():
        if employee["manager_id"] not in processed_employees:
            processed_employees.append(employee["manager_id"])
            local_managers[employee["manager_id"]] = [employee_id]
        else:
            local_managers[employee["manager_id"]].append(employee_id)
    tree_head = local_managers.pop(None)

    tree = build_tree(None, tree_head, local_managers)
    return print_tree(tree, employees_by_id, 0)


def employee(request):
    return HttpResponse(process_org_chart(), headers={"Access-Control-Allow-Origin": "*"})


urlpatterns = [
    path('employee', employee, name=EMPLOYEE_ORG_TREE_URL_NAME)
]

if __name__ == '__main__':
    execute_from_command_line(sys.argv)
