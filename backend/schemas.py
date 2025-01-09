from marshmallow import Schema, fields, validate

class UserBaseSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=8))
    full_name = fields.Str(required=True)
    address = fields.Str()
    pin_code = fields.Str(validate=validate.Length(min=5, max=10))

class CustomerSchema(UserBaseSchema):
    pass

class ProfessionalSchema(UserBaseSchema):
    service_type = fields.Str(required=True, validate=validate.OneOf(
        ['plumber', 'electrician', 'carpenter', 'painter']))
    experience_years = fields.Int(validate=validate.Range(min=0, max=100))