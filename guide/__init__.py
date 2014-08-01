from django.contrib.comments.models import Comment, FreeComment
from django.core.mail import send_mail
from django.dispatch import dispatcher
from django.db.models import signals

def comment_notification(sender, instance):
    subject = 'New Comment on %s' % instance.get_content_object().name
    msg = 'Comment text:\n\n%s\n\nEdit/delete comment: http://pdxguide.org/admin/comments/freecomment/%s/' % (instance.comment, instance.id)
    # send_mail(subject, msg, 'noreply@pdxguide.org', ['tfrindustries@gmail.com', 'natebeaty@gmail.com'])
    send_mail(subject, msg, 'noreply@pdxguide.org', 'tfrindustries@gmail.com')

dispatcher.connect(comment_notification, sender=FreeComment, signal=signals.post_save)
dispatcher.connect(comment_notification, sender=Comment, signal=signals.post_save)

