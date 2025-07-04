from marshmallow import Schema, fields

class ImageAnalysisRequestSchema(Schema):
    image_url = fields.Url(required=True)

class ImageAnalysisRequestWithFile(Schema):
    description = fields.Str(missing=None)

