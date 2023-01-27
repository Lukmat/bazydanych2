from neo4j import GraphDatabase


class Database:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def getEmployees(self):
        with self.driver.session() as session:
            return session.read_transaction(self._get_employees)
        
    @staticmethod
    def _get_employees(tx):
        result = tx.run('MATCH (m:Employee) RETURN m').data()
        return result

    def addEmployee(self, name, department):
        with self.driver.session() as session:
            return session.execute_write(self._add_employee, name, department)

    @staticmethod
    def _add_employee(tx, name, department):
        result = tx.run("CREATE (a:Employee) "
                        "SET a.name = $name, "
                        "SET a.department = $department "
                        "RETURN a", name=name, department=department)
        return result.single()

    def deleteEmployee(self, id):
        with self.driver.session() as session:
            return session.write_transaction(self._delete_employee, id)

    @staticmethod
    def _delete_employee(tx, id):
        result = tx.run('MATCH (m:Employee) WHERE m.id=$id DETACH DELETE m', id=id)
        return result

    def getSubordinates(self, id):
        with self.driver.session() as session:
            return session.read_transaction(self._get_subordinates, id)

    @staticmethod
    def _get_subordinates(tx, id):
        result = tx.run('MATCH (m: Employee { id: $id })-[:MANAGES]->(s: Employee) RETURN s', id=id).data()
        return result

    def getDepartmentOfEmployee(self, id):
        with self.driver.session() as session:
            return session.read_transaction(self._get_subordinates, id)

    @staticmethod
    def _getDepartmentOfEmployee(tx, id):
        result = tx.run('MATCH (d: Department)<-[:WORKS_IN]-(e: Employee{ id: $id }) RETURN d', id=id).data()
        return result

    def getDepartments(self):
        with self.driver.session() as session:
            return session.read_transaction(self._getDepartments)

    @staticmethod
    def _getDepartments(tx):
        result = tx.run('MATCH (d: Department) RETURN d').data()
        return result

    def getDepartmentsEmployees(self, id):
        with self.driver.session() as session:
            return session.read_transaction(self._getDepartmentsEmployees, id)

    @staticmethod
    def _getDepartmentsEmployees(tx, id):
        result = tx.run('MATCH (e: Employee)-[:WORKS_IN]->(d: Department{ id: $id }) RETURN e', id=id).data()
        return result
