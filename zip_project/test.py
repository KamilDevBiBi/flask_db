from requests import get, post, delete, put

# print(get("http://127.0.0.1:8080/api/jobs").json())
# print(get("http://127.0.0.1:8080/api/jobs/1").json())
# print(get("http://127.0.0.1:8080/api/jobs/37").json())
# print(get("http://127.0.0.1:8080/api/jobs/russiaaa").json())

# job = {
#     'team_leader': 2,
#     'job': 'very nice job',
#     'work_size': 32,
#     'collaborators': '5, 2, 3',
#     'hazard_category': 2,
#     'is_finished': False
# }
# print(post("http://127.0.0.1:8080/api/jobs", json=job).json())


# # В теле запроса находится пустой json
# print(post("http://127.0.0.1:8080/api/jobs", json={}).json())


# # В json отсутствует поле work_size
# without_worksize_job = {
#     'team_leader': 2,
#     'job': 'amazing job without worksize',
#     'collaborators': '1, 2, 3, 4, 5',
#     'hazard_category': 1,
#     'is_finished': True
# }
# print(post("http://127.0.0.1:8080/api/jobs", json=without_worksize_job).json())


# print(delete("http://127.0.0.1:8080/api/jobs/9"))

# print(delete("http://127.0.0.1:8080/api/jobs/9"))
# print(delete("http://127.0.0.1:8080/api/jobs/923432"))

# print(get("http://127.0.0.1:8080/api/jobs").json())


# job = {
#     'team_leader': 3,
#     'job': 'changed job',
#     'work_size': 23,
#     'collaborators': '5, 4, 3',
#     'hazard_category': 3,
#     'is_finished': False
# }
# print(put("http://127.0.0.1:8080/api/jobs/8", json=job).json())


# print(put("http://127.0.0.1:8080/api/jobs/90", json=job).json())

# bad_job = {
#     'team_leader': 3,
#     'job': 'changed job',
#     'collaborators': '5, 4, 3',
#     'hazard_category': 3,
#     'is_finished': False
# }
# print(put("http://127.0.0.1:8080/api/jobs/8", json=bad_job).json())

# print(put("http://127.0.0.1:8080/api/jobs/8", json={}).json())


# print(get("http://127.0.0.1:8080/api/jobs").json())