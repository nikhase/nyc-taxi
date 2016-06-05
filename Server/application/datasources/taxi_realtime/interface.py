import db_access


def search(args):

    result = db_access.getData(args, radius=0.5)
    return result

