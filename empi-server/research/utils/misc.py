from nanoid import generate


def generate_nanoid():
    return generate(alphabet="2346789ABCDFGHJLKMNPQRTVWXY-", size=20)
