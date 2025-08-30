from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required, get_jwt_identity


# We will create an 'extensions.py' file for this to avoid circular imports.
from .. import db
from ..models import Post, User
from ..schemas import PostSchema

# Create a Blueprint
posts_bp = Blueprint('posts', __name__)

# Instantiate schemas
post_schema = PostSchema()
posts_schema = PostSchema(many=True)


# GET: read all the post
@posts_bp.route("/posts", methods=["GET"])
def get_posts():
    """
    Get a list of all posts
    This endpoint returns a list of all posts in the database.
    ---
    tags:
      - Posts
    responses:
      200:
        description: A list of posts.
        content:
          application/json:
            schema:
              type: array
              items: PostSchema
    """
    # get all the post.
    posts = Post.query.all()

    # change the posts obj into json string (dump)
    results = posts_schema.dump(posts)

    return jsonify(results), 200

# GET: read a specific post
@posts_bp.route("/posts/<post_id>", methods=["GET"])
def get_post(post_id):
    # get the post with this id
    post = Post.query.get_or_404(post_id)

    # change the post obj into json string (dump)
    result = post_schema.dump(post)

    return jsonify(result), 200


# create post
@posts_bp.route("/posts", methods=['POST'])
@jwt_required() # <-- Add the decorator to protect this route
def create_post():
    """
    Create a new post
    This endpoint creates a new post for the authenticated user.
    ---
    tags:
      - Posts
    security:
      - Bearer: []
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              title:
                type: string
                example: "My Awesome Blog Post"
              content:
                type: string
                example: "This is the content of my post."
            required:
              - title
              - content
    responses:
      201:
        description: Post created successfully.
        content:
          application/json:
            schema: PostSchema
      401:
        description: Unauthorized (invalid or missing token).
    """
    post_data = request.get_json()
    try:
        # NOTE: We will remove user_id from the schema soon. For now, we ignore it.
        validated_data = post_schema.load(post_data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    # THIS IS THE SECURE WAY:
    # Get the user ID from the JWT token instead of the request body
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    new_post = Post(
        title=validated_data['title'],
        content=validated_data['content'],
        author=user
    )
    # ... (rest of the function is the same)
    db.session.add(new_post)
    db.session.commit()
    result = post_schema.dump(new_post)
    return jsonify(result), 201


# NEW: Get all posts by a specific user
@posts_bp.route("/users/<int:user_id>/posts", methods=['GET'])
def get_posts_by_user(user_id):
    # Find the user or return 404
    user = User.query.get_or_404(user_id)
    # The 'user.posts' relationship gives us all the posts for that user
    result = posts_schema.dump(user.posts)
    return jsonify(result)



# PUT: update a post
@posts_bp.route("/posts/<post_id>", methods=["PUT"])
def update_post(post_id):
    # get the post obj of post_id.
    post = Post.query.get_or_404(post_id)

    # receive the json string from the user in dictionary form.
    data = request.get_json()

    # validate the data using schema
    try:
        data = post_schema.load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    # data is valid
    # update the post obj
    post.title = data["title"]
    post.content = data["content"]

    # save this changes to db
    db.session.commit()

    # convert post obj into json string
    result = post_schema.dump(post)
    return jsonify(result), 200


# DELETE: delete a post
@posts_bp.route("/posts/<post_id>", methods=["DELETE"])
def delete_post(post_id):
    # get the post obj of post_id.
    post = Post.query.get_or_404(post_id)
    
    # delete the post obj from db.
    db.session.delete(post)

    # save this changes to db
    db.session.commit()

    return "", 204




