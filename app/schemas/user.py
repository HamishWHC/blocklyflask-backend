import bcrypt
from marshmallow import fields, validate, post_load, validates_schema, ValidationError, pre_load

from app import marshmallow
from app.models import User


# A schema is a class that determines how an object is serialised/deserialised to/from JSON format.
# This schema determines this for user accounts.
# The schema inherits (extends in JS/Java terms) from marshmallow.ModelSchema,
# which is a schema that works with a DB model object rather than a standard Python class or dictionary.
class UserSchema(marshmallow.ModelSchema):
    class Meta:  # Creates the child-class Meta to define some schema configuration.
        model = User  # Uses the User model as the model to serialise/deserialise to/from.
        # Each item here is a field on a User model that needs to be serialised and/or deserialised.
        fields = ("id", "email", "projects", "username", "password", "gravatar_link")

    # The ID is dump (to user) only, since it is created/set by the server. It is an integer.
    id = fields.Integer(dump_only=True)

    # The email is a string, which must match an email validation pattern (same one as sign-up component).
    email = fields.String(required=True, validate=validate.Regexp(r"^[^@]+@[^@]+\.[^@]+$"))
    # The username is a string, with the same validation requirements as the sign-up component.
    username = fields.String(required=True,
                             validate=[validate.Regexp(r"^[a-zA-Z_\-0-9]{6,20}$"), validate.Length(min=6, max=20)])
    # The password is a string, with the same requires as the sign-up component, however, for security,
    # the password is load (from user) only to prevent the password (even in hashed form) from being transmitted
    # (unless it is being set of course).
    password = fields.String(required=True, validate=[validate.Length(min=8)], load_only=True)

    # The user's projects are nested within the schema, allowing the frontend to perform less requests to gather
    # all the data it requires. It is dump only as it is difficult to validate and act on nested data.
    # The many parameter is set to true since multiple projects are associated with one user.
    projects = fields.Nested("ProjectSchema", exclude=("user", "root_directory"), many=True, dump_only=True)

    # The Gravatar link is a link created from the hash of the user's email to create a deterministic (same every time),
    # random avatar (the profile images on the project list page). These cannot be set, so are dump only.
    gravatar_link = fields.String(dump_only=True)

    @validates_schema  # Indicates this will validate multiple fields.
    def uniquity_checks(self, data, **kwargs) -> None:
        # First it looks for a user with the given username, that is not itself
        # (if a user changes their email, but not their username,
        # the username must not be marked as taken by themselves).
        if User.query.filter(
            User.username == data.get("username", ""),
            # This get the user ID from the 'context' of the schema,
            # which is set when it needs to be used. 0 is the default,
            # which will match no users, as the user IDs start at 1.
            User.id != self.context.get("user_id", 0)
        ).first() is not None:  # i.e. if there IS a user matching the condition.
            # Raises a validation error, which is caught by the endpoint and the message is sent to the API caller.
            raise ValidationError("Username already in use.", "username")

        # Same deal as the username, but for the email.
        elif User.query.filter(
            User.email == data.get("email", ""),
            User.id != self.context.get("user_id", 0)
        ).first() is not None:
            raise ValidationError("Email already in use.", "email")

    # Tells marshmallow to perform this code after the validation, but before returning an object to the API to process.
    @post_load(pass_original=True)
    def post_process(self, obj, original_data, **kwargs):
        # Whenever the password is set, hash it using a randomised 'salt' so that it cannot be read by anyone.
        # The encodes and decodes are to convert between bytes objects and strings as needed by Python/Bcrypt.
        obj.hashed_password = bcrypt.hashpw(original_data["password"].encode(), bcrypt.gensalt()).decode()

        # Email and username are made lowercase to prevent case-sensitivity in the database.
        obj.email = original_data["email"].lower()
        obj.username = original_data["username"].lower()
        return obj
