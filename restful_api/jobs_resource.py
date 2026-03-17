from flask_restful import Resource, abort

from flask import jsonify

from data import db_session
from data.__all_models import Jobs

from .reqparser import job_parser as parser

def abort_if_job_not_found(job_id):
    session = db_session.create_session()
    job = session.query(Jobs).get(job_id)

    if not job:
        abort(404, message=f"job {job_id} not found")


class jobsResource(Resource):
    def get(self, job_id):
        abort_if_job_not_found(job_id)

        session = db_session.create_session()
        job = session.query(Jobs).get(job_id)

        return jsonify({'job': job.to_dict(only=('team_leader', 'job', 'hazard_category', 'work_size', 'collaborators', 'is_finished'))})
    
    def delete(self, job_id):
        abort_if_job_not_found(job_id)

        session = db_session.create_session()
        job = session.query(Jobs).get(job_id)

        session.delete(job)
        session.commit()

        return jsonify({'success': 'OK'})


class jobsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        jobs = session.query(Jobs).all()
        return jsonify({
            'job': [ item.to_dict(only=('team_leader', 'job', 'hazard_category', 'work_size', 'collaborators', 'is_finished')) for item in jobs]
        })
    
    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()

        job = Jobs(
            team_leader=args['team_leader'],
            job=args['job'],
            hazard_category=args['hazard_category'],
            work_size=args['work_size'],
            collaborators=args['collaborators'],
            is_finished=args['is_finished']
        )

        session.add(job)
        session.commit()

        return jsonify({'id': job.id})
