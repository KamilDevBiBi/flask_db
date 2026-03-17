from requests import get, post, delete


# print(get("http://127.0.0.1:8080/api/v2/users/11").json())

# print(delete("http://127.0.0.1:8080/api/v2/users/11").json())

# print(delete("http://127.0.0.1:8080/api/v2/users/99").json())

# print(get("http://127.0.0.1:8080/api/v2/users").json())

# user = {
#     'name': "shakalaka",
#     'email': 'abduroziiik@mail.ru',
#     'from_city': 'Klarnet',
#     'password': '12300321'
# }
# print(post("http://127.0.0.1:8080/api/v2/users", json=user).json())

# bad_user = {
#     'name': "shakalaka",
#     'email': 'abduroziiik@mail.ru',
#     'from_city': 'Klarnet'
# }
# print(post("http://127.0.0.1:8080/api/v2/users", json=bad_user).json())

# print(post("http://127.0.0.1:8080/api/v2/users", json={}).json())


print(get("http://127.0.0.1:8080/api/v2/jobs/7").json())

print(delete("http://127.0.0.1:8080/api/v2/jobs/7").json())

print(delete("http://127.0.0.1:8080/api/v2/jobs/99").json())


print(get("http://127.0.0.1:8080/api/v2/jobs").json())

job = {
    "team_leader": 2,
    "job": "Разработка API",
    "work_size": 16,
    "collaborators": "3,4,5",
    "hazard_category": 3,
    "is_finished": False
}
print(post("http://127.0.0.1:8080/api/v2/jobs", json=job).json())

bad_job = {
    "team_leader": 2,
    "job": "Разработка API",
    "work_size": 16,
    "hazard_category": 3,
    "is_finished": False
}
print(post("http://127.0.0.1:8080/api/v2/jobs", json=bad_job).json())

print(post("http://127.0.0.1:8080/api/v2/jobs", json={}).json())
