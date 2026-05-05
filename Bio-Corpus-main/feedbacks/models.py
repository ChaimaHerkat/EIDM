"""
User feedback on articles — stored in MongoDB.
"""
from datetime import datetime
import mongoengine as me


class Feedback(me.Document):
    article_id = me.StringField(required=True)  # Mongo ObjectId of Article (string)
    username = me.StringField(required=True)
    rating = me.IntField(min_value=1, max_value=5, required=True)
    comment = me.StringField(default="")
    suggested_domain = me.StringField(default="")  # user can correct classification
    created_at = me.DateTimeField(default=datetime.utcnow)

    meta = {
        "collection": "feedbacks",
        "indexes": ["article_id", "username", "-created_at"],
        "ordering": ["-created_at"],
    }
