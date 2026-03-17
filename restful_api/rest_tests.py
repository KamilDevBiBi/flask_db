from requests import get, post, delete


print(get("http://127.0.0.1:8080/api/v2/users/11").json())

print(delete("http://127.0.0.1:8080/api/v2/users/11").json())

print(delete("http://127.0.0.1:8080/api/v2/users/99").json())



print(get("http://127.0.0.1:8080/api/v2/users").json())

user = {
    'name': "shakalaka",
    'email': 'abduroziiik@mail.ru',
    'from_city': 'Klarnet',
    'password': '12300321'
}
print(post("http://127.0.0.1:8080/api/v2/users", json=user).json())

bad_user = {
    'name': "shakalaka",
    'email': 'abduroziiik@mail.ru',
    'from_city': 'Klarnet'
}
print(post("http://127.0.0.1:8080/api/v2/users", json=bad_user).json())