class Profile:
    name: str = string(unique=True)
    age: int | None = integer()
    user: User = relaytion(User)
    hashtags: [HashTags] = relation([HashTags])