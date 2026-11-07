from django import template

register = template.Library()

@register.filter(name='is_liked_by')
def is_liked_by(post, user):
    return post.is_liked_by(user)

@register.filter(name='is_bookmarked_by')
def is_bookmarked_by(post, user):
    return post.is_bookmarked_by(user)

