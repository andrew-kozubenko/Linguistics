# example_usage_ontology.py
from ontology_repository import OntologyRepository

URI = "neo4j://127.0.0.1:7687"
USER = "neo4j"
PASSWORD = "78907890"

repo = OntologyRepository(URI, USER, PASSWORD)

# 1. Создадим корневой класс
person_class = repo.create_class("Person", "Человек")
print("Создан класс:", person_class)

# 2. Создадим подкласс Employee с родителем Person
employee_class = repo.create_class("Employee", "Работник компании", parent_uri=person_class["uri"])
print("Создан подкласс:", employee_class)

# 3. Создадим подкласс Employer с родителем Person
employer_class = repo.create_class("Employer", "Работодатель компании", parent_uri=person_class["uri"])
print("Создан подкласс:", employer_class)

# 4. Добавим атрибуты к Employee
age_attr = repo.add_class_attribute(employee_class["uri"], "age")
print("Добавлен DatatypeProperty:", age_attr)
works_in_attr = repo.add_class_object_attribute(employee_class["uri"], "worksFor", range_class_uri=employer_class["uri"])
print("Добавлен ObjectProperty:", works_in_attr)

# 5. Создадим объект класса Employee
emp1 = repo.create_object(employee_class["uri"], "Дубина Дубно", "Разработчик")
print("Создан объект:", emp1)

# 6. Получим сигнатуру класса Employee
signature = repo.collect_signature(employee_class["uri"])
print("Сигнатура класса Employee:", signature)

# 7. Получим сигнатуру класса Employer
signature = repo.collect_signature(employer_class["uri"])
print("Сигнатура класса Employer:", signature)

# 8. Получим родителей и потомков Employee и Person
parents = repo.get_class_parents(employee_class["uri"])
children = repo.get_class_children(employee_class["uri"])
print("Родители Employee:", parents)
print("Потомки Employee:", children)

parents = repo.get_class_parents(person_class["uri"])
children = repo.get_class_children(person_class["uri"])
print("Родители Person:", parents)
print("Потомки Person:", children)

# 9. Обновим класс
updated_class = repo.update_class(employee_class["uri"], "Employee", "Сотрудник компании")
print("Обновлённый класс:", updated_class)

# 10. Создадим подкласс Programmer с родителем Employer
programmer_class = repo.create_class("Programmer", "Программист компании", parent_uri=employee_class["uri"])
print("Создан подкласс:", programmer_class)

# 11. Добавим атрибуты к Programmer
age_attr = repo.add_class_attribute(programmer_class["uri"], "age")
print("Добавлен DatatypeProperty:", age_attr)
works_in_attr = repo.add_class_object_attribute(programmer_class["uri"], "worksFor", range_class_uri=employer_class["uri"])
print("Добавлен ObjectProperty:", works_in_attr)

# 12. Создадим объект класса Programmer
pr1 = repo.create_object(programmer_class["uri"], "Димбель Рацель", "Разработчик")
print("Создан объект:", pr1)

# 13. Тестим оставшиеся методы
ontology = repo.get_ontology()
print("Онтология:", ontology)
ontology_parent_classes = repo.get_ontology_parent_classes()
print("Корневые классы:", ontology_parent_classes)
print("Класс Employee", repo.get_class(employee_class["uri"]))
print("Объекты класса Employee", repo.get_class_objects(employee_class["uri"]))

# 14. Удаляем атрибуты
repo.delete_class_object_attribute(works_in_attr["uri"])
print("Объетный атрибут удален у Programmer")
repo.delete_class_attribute(age_attr["uri"])
print("Атрибут удален у Programmer")

# 15. Удалим объект
repo.delete_object(emp1["uri"])
print("Объект удалён")
print("Объекты класса Employee", repo.get_class_objects(employee_class["uri"]))

# 16. Удаляет класс Employee вместе со всеми потомками, их объектами и атрибутами. (Должен удалиться и Programmer)
repo.delete_class(employee_class["uri"])
print("Класс Employee удалён")

repo.close()
