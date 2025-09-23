import argon2

class Hasher:
    def __init__(self):
        self.ph = argon2.PasswordHasher(
            time_cost=2,
            memory_cost=102400,
            parallelism=8,
            hash_len=32,
            salt_len=16
        )

    def hash_password(self, password):
        return self.ph.hash(password)

    def verify_password(self, password, hashed_password):
        try:
            return self.ph.verify(hashed_password, password)
        except:
            return False