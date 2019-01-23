from flask import request, jsonify
from datetime import datetime
from restapi.models.redflag_models import Interventions


class InterventionsController():

    def __init__(self):
        pass

    def create_intervention(self):

        interventions = Interventions()
        data = request.get_json()
        created_by = request.headers['user_id']
        status = "draft"
        images = data.get("images")
        videos = data.get("videos")
        comment = data.get("comment")
        location = data.get("location")

        postman_strings = [status, images, videos, comment, location]
        postman_data = [status, images, videos, comment, location, created_by]

        for value in postman_strings:
            if not isinstance(value, str):
                return jsonify({
                    "status": "404",
                    "message": "'{}' should be a string".format(value)
                })
        for v in postman_data:
            if not v:
                return jsonify({
                    "status": "400",
                    "message": "{} field is missing".format(v)
                })

        interventions.create_intervention(location=data['location'],
                                          status=data['status'],
                                          images=data['images'],
                                          videos=data['videos'],
                                          comment=data['comment'],
                                          created_by=request.headers['user_id']
                                          )

        return jsonify({
            "status": 201,
            "data": {
                "id": "1",
                "message": "Created intervention record"
            }
        })

    def get_all_interventions(self):
        pass

    def get_a_single_intervention(self, redflag_id):
        pass

    def delete_intervention(self, redflag_id):
        pass

    def update_intervention_status(self, redflag_id):
        pass

    def update_intervention_location(self, redflag_id):
        pass

    def update_intervention_comment(self, redflag_id):
        pass
