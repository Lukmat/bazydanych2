from flask import Flask, jsonify, request
import os
from neo import Database

app = Flask(__name__)

uri = os.getenv('URI')
user = os.getenv("USERNAME")
password = os.getenv("PASSWORD")

database = Database(uri, user, password)


@app.route("/employees", methods=['GET'])
def getEmployees():
    employees = database.getEmployees()
    result = [{'id': result['id'], 'name': result['name'], 'department': result['department']} for result in employees]
    return jsonify(result)

@app.route("/employees", methods=['POST'])
def addEmployee():
    dane = request.get_json()
    name = dane['name']
    department = dane['department']
    result = database.addEmployee(name, department)
    return jsonify(result)


@app.route("/employees/:id", methods=['PUT'])
def changeEmployee():
    dane = request.get_json()
    name = dane['name']
    department = dane['department']
    id = dane['id']
    result = database.changeEmployee(name, department, id)
    return jsonify(result)


@app.route('/employees/:id', methods=["DELETE"])
def deleteEmployee(id):
    result = database.deleteEmployee(id)
    if result:
        response = {'status': 'deleted employee'}
        return jsonify(response)
    else:
        response = {'message': 'Employee not found'}
        return jsonify(response), 404


@app.route('/employees/:id/subordinates', methods=['GET'])
def getSubordinates(id):
    subordinates = database.getSubordinates(id)
    result = [{'subordinate': result['s']} for result in subordinates]
    return jsonify(result)


@app.route('/employees/:id/department', methods=['GET'])
def getDepartmentOfEmployee(id):
    result = database.getDepartmentOfEmployee(id)
    return result


@app.route('/departments/all', methods=['GET'])
def getDepartments():
    departments = database.getDepartments()
    result = [{'department': result['d']} for result in departments]
    return jsonify(result)


@app.route('/departments/:id/employees', methods=['GET'])
def getDepartmentsEmployees(id):
    employees = database.getDepartmentsEmployees(id)
    result = [{'employee': result['e']} for result in employees]
    return jsonify(result)
