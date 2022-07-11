from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import SubmitField, IntegerField


class FileUploadForm(FlaskForm):
	upload_file = FileField("Peak area file")
	Internal_standard = IntegerField("Internal standard feature number")
	Sample_metadata = FileField("Sample metadata")
	Feature_metadata = FileField("Feature metadata")
	submit = SubmitField("Submit")