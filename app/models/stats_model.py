from app import db
from datetime import datetime

class Stats(db.Model):
    __tablename__ = "stats"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    race_result_id = db.Column(db.Integer, db.ForeignKey("race_result.id"), nullable=False)

    wall_jump = db.Column(db.Interval)
    dash = db.Column(db.Interval)
    double_jump = db.Column(db.Interval)
    grotto_skip = db.Column(db.Integer)
    enter_ginso = db.Column(db.Interval)
    bash = db.Column(db.Interval)
    swamp_entry = db.Column(db.Integer)
    stomp = db.Column(db.Interval)
    kuro_cs_skip = db.Column(db.Integer)
    charge_flame = db.Column(db.Interval)
    fast_stompless = db.Column(db.Integer)
    glide = db.Column(db.Interval)
    sorrow_bash = db.Column(db.Integer)
    charge_jump = db.Column(db.Interval)
    sunstone = db.Column(db.Interval)
    climb = db.Column(db.Interval)
    grenade = db.Column(db.Interval)
    enter_horu = db.Column(db.Interval)
    door_warp = db.Column(db.Integer)
    grenade_jump = db.Column(db.Integer)