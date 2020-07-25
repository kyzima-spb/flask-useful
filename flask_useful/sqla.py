import re

from sqlalchemy import exists


def generate_slug(session, slug_field, slug):
    """
    Generates a unique slug based on the passed value.

    Arguments:
        session: SQLAlchemy session.
        slug_field: Model attribute containing slug.
        slug (str): The desired slug value.
    """
    if not session.query(exists().where(slug_field == slug)).scalar():
        return slug

    default = f'{slug}-1'

    like = f'{slug}-%'
    query = session.query(slug_field) \
                   .filter(slug_field.like(like)) \
                   .order_by(slug_field.desc())
    found = [i for i, in query]

    if not found:
        return default

    pattern = re.compile(r'^%s-([0-9]+$)' % slug, re.I)

    for i in found:
        match = pattern.match(i)
        if match:
            return '{}-{}'.format(slug, int(match.group(1)) + 1)

    return default
