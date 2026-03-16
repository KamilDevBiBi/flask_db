from flask import Blueprint, jsonify, make_response, request

from . import db_session
from .__all_models import Jobs

blueprint = Blueprint(
    "jobs_api", __name__,
    template_folder="templates"
)

@blueprint.route("/api/jobs")
def get_all_jobs():
    session = db_session.create_session()
    jobs = session.query(Jobs).all()
    return jsonify(
        {
            'jobs': [
                item.to_dict(only=(
                'id', 'job', 'team_leader', 'work_size', 'collaborators', 'start_date', 'end_date', 'is_finished', 'hazard_category')
                ) for item in jobs
            ]
        }
    )


@blueprint.route("/api/jobs/<int:job_id>")
def get_one_job(job_id):
    session = db_session.create_session()
    job = session.query(Jobs).filter(Jobs.id == job_id).first()

    if not job:
        return make_response(jsonify({'error': 'Not found'}), 404)
    else:
        return jsonify(
            {
                'job': job.to_dict(
                    only=('id', 'job', 'team_leader', 'work_size', 'collaborators', 
                          'start_date', 'end_date', 'is_finished', 'hazard_category')
                    )
            }
        )


@blueprint.route("/api/jobs", methods=["POST"])
def create_new_job():
    print(request.json)
    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)
    
    job_data = ['team_leader', 'job', 'collaborators', 'work_size', 'is_finished', 'hazard_category']
    if not all(key in request.json for key in job_data):
        return make_response(jsonify({'error': 'Bad request'}, 400))
    
    job = Jobs(
        team_leader=request.json['team_leader'],
        job=request.json['job'],
        work_size=request.json['work_size'],
        collaborators=request.json['collaborators'],
        is_finished=request.json['is_finished'],
        hazard_category=request.json['hazard_category']
    )

    session = db_session.create_session()
    session.add(job)
    session.commit()

    return jsonify({'id': job.id})


@blueprint.route("/api/jobs/<int:job_id>", methods=["DELETE"])
def delete_job(job_id):
    session = db_session.create_session()
    job = session.query(Jobs).filter(Jobs.id == job_id).first()

    if not job:
        return make_response(jsonify({'error': 'Not found'}), 404)
    
    session.delete(job)
    session.commit()

    return jsonify({'success': 'OK'})


@blueprint.route("/api/jobs/<int:job_id>", methods=["PUT"])
def edit_job(job_id):
    session = db_session.create_session()
    job = session.query(Jobs).filter(Jobs.id == job_id).first()

    if not job:
        return make_response(jsonify({'error': 'Not found'}), 404)
    
    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)
    
    job_data = ['team_leader', 'job', 'collaborators', 'work_size', 'is_finished', 'hazard_category']
    if not all(key in request.json for key in job_data):
        return make_response(jsonify({'error': 'Bad request'}, 400))
    
    json_data = request.json
    job.team_leader = json_data['team_leader']
    job.job = json_data['job']
    job.work_size = json_data['work_size']
    job.collaborators = json_data['collaborators']
    job.hazard_category = json_data['hazard_category']
    job.is_finished = json_data['is_finished']

    session.commit()
    return jsonify({'success': 'OK', 'id': job.id})
