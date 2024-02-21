def encrypt(passwd):
    new_passwd = ""
    alpha = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ~!@#$%^&*()_+=-0987654321\|/.,<>?;:"
    for i in range(len(passwd)):
        w = passwd[i]
        a = alpha.index(w)
        a = (a + 10) % len(alpha)
        new_passwd += alpha[a]
    return new_passwd

# def decrypt(new_passwd):
#     passwd = ""
#     alpha = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ~!@#$%^&*()_+=-0987654321\|/.,<>?;:"
#     for i in range(len(new_passwd)):
#         w = new_passwd[i]
#         a = alpha.index(w)
#         a = (a - 10) % 87
#         passwd += alpha[a]
#     return passwd


if __name__ == "__main__":
    a = encrypt("Aaditya@01234")
    print(a)
    # print(decrypt(a))
    # print(encrypt(input()))
    # print(decrypt(input()))
    