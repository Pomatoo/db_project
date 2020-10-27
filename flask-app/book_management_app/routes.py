from book_management_app import app
from book_management_app.models import Review
from flask import request


# /review [GET, POST] -> Retrieve review,  post a review

@app.route('/review', methods=['GET', 'POST'])
def review(course):
    if request.method == 'GET':
        pass
    else:
        pass

    return



#
# # Course enrollment, enroll/drop a course
# # Student id is required in the request body
# @app.route('/enrollment/<course>', methods=['POST', 'DELETE'])
# def course_enrollment(course):
#     ############################## Validation ##############################
#     student_id = request.json.get('id')
#     if not student_id:
#         return jsonify({'Error': 'id is required for course enrollment'}), 400
#     elif not student_id.isdigit():
#         return jsonify({'Error': 'id must be digits'}), 400
#     elif not student_manager.get_student_by_id(student_id):
#         return jsonify({'Error': 'Student %s is not enrolled in SUTD, call Admin' % student_id}), 400
#
#     if not course:
#         return jsonify({'Info': 'Usage: /enrollment/<course name>'}), 400
#     elif not course_manager.get_course(course):
#         return jsonify({'Error': 'Course %s is not available' % course}), 400
#     elif course_manager.get_course(course)['vacancy'] < 1:
#         return jsonify({'Info': 'Course %s no vacancy' % course})
#     ############################## Validation ##############################
#
#     # Add course
#     if request.method == 'POST':
#         student_manager.enroll_course(student_id, course)
#         course_manager.update_vacancy(course, -1)
#         return jsonify(student_manager.get_student_by_id(student_id))
#
#     # Drop course
#     elif request.method == 'DELETE':
#         student_manager.drop_course(student_id, course)
#         course_manager.update_vacancy(course, -1)
#         return jsonify(student_manager.get_student_by_id(student_id))
#
#     return 'None'
#
#
# # Admin Operations, authentication needed
# # username,password need to be set in request body
# # Admin can view and edit students' profile
# @app.route('/students/<student_id>', methods=['GET'])
# @app.route('/students', methods=['GET', 'POST', 'DELETE'], defaults={'student_id': None})
# def student_management(student_id):
#     # Authentication
#     username = request.json.get('username')
#     password = request.json.get('password')
#     if username is None or password is None:
#         return jsonify({'Error': 'Missing Username or Password'}), 401
#     elif username != ADMIN or password != PASSWORD:
#         return jsonify({'Error': 'Unauthorized User'}), 401
#
#     # Get, return student(s) profile
#     if request.method == 'GET':
#         if student_id is None:
#             return jsonify(student_manager.get_all_students())
#         else:
#             student_info = student_manager.get_student_by_id(student_id)
#             if student_info is None:
#                 return jsonify({'Info': 'Student %s is not enrolled in SUTD' % student_id})
#             return jsonify(student_info)
#
#     # Post, add students
#     # {'students':{'id1':info, 'id2':info2}}
#     elif request.method == 'POST':
#         students = request.json.get('students')
#         for each_id in students.keys():
#             student_manager.add_student(each_id, students[each_id])
#
#     # Delete, remove students by id
#     # {'students' : ['id1', 'id2']}
#     elif request.method == 'DELETE':
#         students = request.json.get('students')
#         for each_id in students:
#             student_manager.remove_student(each_id)
#
#     return jsonify(student_manager.get_all_students())
