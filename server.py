import requests

EMPLOYEES_ENDPOINT = "https://gist.githubusercontent.com/chancock09/6d2a5a4436dcd488b8287f3e3e4fc73d/raw/fa47d64c6d5fc860fabd3033a1a4e3c59336324e/employees.json"


def get_org_chart():
    response = requests.get(EMPLOYEES_ENDPOINT)
    response.raise_for_status()
    return response.json()


def build_tree(employee_id, children, local_managers):
    if not children:
        return {employee_id: list()}
    return {employee_id: list(build_tree(x, local_managers.get(x), local_managers) for x in children)}

def print_tree(tree, employees_by_id, level):
    for root, leafs in tree.items():
        print(f"{'-'*level} {employees_by_id[root]['name']}")
        for leaf in leafs:
            print_tree(leaf, employees_by_id, level+1)


def process_org_chart():
    employees_data = get_org_chart()
    hierarchy_tree = list()
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

    # tree = build_tree(None, tree_head, local_managers)
    # We could have multiple high level managers but for this particular example there is only one
    tree_head = tree_head[0]
    tree = build_tree(tree_head, local_managers[tree_head], local_managers)

    print_tree(tree, employees_by_id, 0)





if __name__ == "__main__":
    process_org_chart()
