import bcrypt


class User:
    def __init__(self, username, password_hash):
        self.username = username
        self.password_hash = password_hash  # Store as a string

    def verify(self, password):
        """Check if the given password matches the stored hash."""
        return bcrypt.checkpw(password.encode("utf-8"), self.password_hash.encode("utf-8"))

    def to_dict(self):
        return{
            'id': self.get_key(),
            'username': self.username,
            'hash': self.password_hash
        }

    @classmethod
    def build(cls, dict):
        return cls(dict['username'], dict['password_hash'])

    def get_key(self):
        return self.username.lower()


if __name__ == "__main__":
    salt = bcrypt.gensalt(13)
    print(bcrypt.hashpw("t".encode(), salt))