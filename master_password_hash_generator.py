from hashlib import sha256


def master_password_gen():
    master_password = input('Enter your password: ').encode()
    compile_factor_together = sha256(master_password).hexdigest()
    print(f"Master Password: {compile_factor_together}")


master_password_gen()
