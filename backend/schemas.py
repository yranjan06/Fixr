from marshmallow import Schema, fields, validate, validates_schema, ValidationError
import re

class UserBaseSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=[
        validate.Length(min=12),
        validate.Regexp(r'[A-Z]', error='Password must contain an uppercase letter'),
        validate.Regexp(r'[a-z]', error='Password must contain a lowercase letter'),
        validate.Regexp(r'[0-9]', error='Password must contain a number'),
        validate.Regexp(r'[!@#$%^&*]', error='Password must contain a special character')
    ])
    full_name = fields.Str(required=True, validate=validate.Length(min=2, max=255))
    address = fields.Str(validate=validate.Length(max=500))
    pin_code = fields.Str(validate=validate.Regexp(r'^\d{5,6}$', error='Pin code must be 5 or 6 digits'))

class CustomerSchema(UserBaseSchema):
    pass

class ProfessionalSchema(UserBaseSchema):
    service_type = fields.Str(required=True, validate=validate.OneOf(
        ['plumber', 'electrician', 'carpenter', 'painter']))
    experience_years = fields.Int(validate=validate.Range(min=0, max=100))
    
    @validates_schema
    def validate_certifications(self, data, **kwargs):
        if 'certifications' not in self.context.get('files', {}):
            raise ValidationError('Certification document is required')
