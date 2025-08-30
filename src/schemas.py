# src/schemas.py

from marshmallow import Schema, fields

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)

    # NEW: Add this Meta class
    class Meta:
        # Explicitly list the fields to include in the documentation
        fields = ('id', 'username')

class PostSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    content = fields.Str(required=True)
    author = fields.Nested(UserSchema(only=("username",)), dump_only=True)

    # NEW: Add this Meta class
    class Meta:
        # Explicitly list the fields to include in the documentation
        fields = ('id', 'title', 'content', 'author')