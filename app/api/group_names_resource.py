from flask_restful import Resource

from app.models import GroupName
from app.schemas import GroupNameSchema


class GroupNamesResource(Resource):
    schema = GroupNameSchema(many=True)

    # Returns a list of all group names
    def get(self):
        group_names = GroupName.query.all()
        return self.schema.dump(group_names)
