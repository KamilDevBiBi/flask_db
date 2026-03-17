from flask_restful import reqparse

user_parser = reqparse.RequestParser()
user_parser.add_argument('name', required=True)
user_parser.add_argument('email', required=True)
user_parser.add_argument('from_city', required=True)
user_parser.add_argument('password', required=True)

job_parser = reqparse.RequestParser()
job_parser.add_argument('team_leader', required=True, type=int)
job_parser.add_argument('job', required=True)
job_parser.add_argument('work_size', required=True, type=int)
job_parser.add_argument('collaborators', required=True)
job_parser.add_argument('hazard_category', required=True, type=int)
job_parser.add_argument('is_finished', required=True, type=bool)