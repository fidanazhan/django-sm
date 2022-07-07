from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
@stringfilter
def upto(value, delimiter=None):
    return value.split(delimiter)[0]
upto.is_safe = True

@register.filter
def user_liked_in_post(user, post):

    liked_obj = post.post_liked.filter(user=user)
    # print(liked_obj)
    return liked_obj

@register.filter
def user_liked_in_comment(user, comment):

    liked_obj = comment.comment_liked.filter(user=user)
    # print(liked_obj)
    return liked_obj