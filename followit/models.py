from django.db import models
from django.contrib.contenttypes.models import ContentType
from followit.compat import USER_MODEL_CLASS_NAME

class FollowRecord(models.Model):
    user = models.ForeignKey(USER_MODEL_CLASS_NAME, on_delete=models.CASCADE)
    content_type = models.ForeignKey(
                            ContentType,
                            related_name='followed_record_contenttype',
                            on_delete=models.CASCADE
                        )
    object_id = models.PositiveIntegerField(db_index=True)
