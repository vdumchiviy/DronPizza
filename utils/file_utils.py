import csv
from schemas.pizzabase import PizzaTask


filename_tasks = "tasks.csv"
csv_tasks = open(filename_tasks, "r")
reader_tasks = csv.DictReader(csv_tasks)


def get_new_task_from_csv(filename_tasks=filename_tasks):
    for row in reader_tasks:
        pizza_task = PizzaTask.parse_obj(row)
        yield pizza_task


# def get_new_task_from_csv(filename_tasks=filename_tasks):
#     with open(filename_tasks, "r") as csv_tasks:
#         reader = csv.DictReader(csv_tasks)
#         for row in reader:
#             pizza_task = PizzaTask.parse_obj(row)
#             yield pizza_task
