from marshmallow import Schema
from marshmallow import fields
from marshmallow import post_load

from app.models import GroupStandings
from app.models import QualifierStandings

class QualifierStandingsSchema(Schema):
    class Meta:
        ordered = True

    place = fields.Int()
    user = fields.Str()
    average_time = fields.TimeDelta(precision="milliseconds")

    @post_load
    def make_entrant(self, data, **kwargs):
        return QualifierStandings(**data)


class GroupStandingsSchema(Schema):
    class Meta:
        ordered = True

    class GroupRecordSchema(Schema):
        class Meta:
            ordered = True
        
        user = fields.Str()
        wins = fields.Int()
        losses = fields.Int()

    group = fields.Str()
    standings = fields.Nested(GroupRecordSchema, many=True)


    @post_load
    def make_entrant(self, data, **kwargs):
        return QualifierStandings(**data)

