import password_generator
import sql_statement as sql
import db_connect
import master_password
import argparse
import getpass
import sys
import hashlib


def main():

    my_parser = argparse.ArgumentParser(
        description="Password Manager Vault: Create, Add and Delete URL, Username, Password", usage="[options]")

    master_password_input = getpass.getpass('Master Password: ').encode()

    second_FA_location = "test".encode()

    master_password_hash = hashlib.sha256(
        master_password_input+second_FA_location).hexdigest()

    if master_password.query_master_pwd(master_password_input, second_FA_location):
        connection = db_connect.connection_db()
        print("Successfully Authenticated!!")

    else:
        print("Failed to authenticate into server. Run the program again")
        sys.exit()

    my_parser.add_argument("-a", "--add", type=str, nargs=2,
                           help="Add new entry", metavar=("[URL]", "[USERNAME]"))
    my_parser.add_argument("-q", "--query", type=str, nargs=1,
                           help="Look up entry by URL", metavar="[URL]")
    my_parser.add_argument("-l", "--list", action="store_true",
                           help="List all entries in the password list")
    my_parser.add_argument("-d", "--delete", type=str,
                           nargs=1, help="Delete entry by URL", metavar="[URL]")
    my_parser.add_argument("-ap", "--add_password", type=str, nargs=3,
                           help="Add manual password", metavar=("[URL]", "[USERNAME]", "[PASSWORD]"))
    my_parser.add_argument("-uurl", "--update_url", type=str, nargs=2,
                           help="Update a URL", metavar=("[OLD_URL]", "[NEW_URL]"))
    my_parser.add_argument("-uuname", "--update_username", type=str, nargs=2,
                           help="Update username of a URL", metavar=("[URL]", "[USERNAME]"))
    my_parser.add_argument("-upasswd", "--update_password", type=str, nargs=2,
                           help="Update password of a URL", metavar=("[URL]", "[PASSWORD]"))

    args = my_parser.parse_args()

    cursor = connection.cursor()

    connection.commit()

    if args.add:
        URL = args.add[0]
        USERNAME = args.add[1]
        PASSWORD = password_generator.password_gen(20)
        password_official = master_password.encrypt_password(
            PASSWORD, master_password_hash)
        cursor.execute(sql.insert_db_row(), (URL, USERNAME, password_official))
        print(
            f"Record Added: \n\n URL: {URL} \n Username: {USERNAME}\n Password: {PASSWORD}\n Encrypted Password: {password_official}")

    if args.query:
        URL = args.query[0]
        cursor.execute(sql.select_db_entry(), (URL, ))
        record = cursor.fetchone()

        if bool(record):
            password_field = record[2]
            decrypt_password = master_password.decrypt_password(
                password_field, master_password_hash)

            print(
                f"Record: \n URL: {record[0]}, Username: {record[1]}, Password: {decrypt_password.decode('utf-8')}")
            print(
                f"Record  with encrypted: \n URL: {record[0]}, Username: {record[1]}, Password: {record[2]}")

        else:
            print(f"Could not find record matching the value {URL}")

    if args.delete:
        URL = args.delete[0]
        cursor.execute(sql.delete_db_row(), (URL, ))
        print("Record deleted")

    if args.add_password:
        URL = args.add_password[0]
        USERNAME = args.add_password[1]
        PASSWORD = args.add_password[2]
        password_official = master_password.encrypt_password(
            PASSWORD, master_password_hash)
        cursor.execute(sql.insert_db_row(), (URL, USERNAME, password_official))
        print("Record added with custom password")

    if args.update_url:
        old_URL = args.update_url[0]
        new_URL = args.update_url[1]
        cursor.execute(sql.update_db_url(), (new_URL, old_URL))

    if args.update_username:
        URL = args.update_username[0]
        new_username = args.update_username[1]
        cursor.execute(sql.update_db_usrname(), (URL, new_username))

    if args.update_password:
        URL = args.update_password[0]
        new_password = args.update_password[1]
        cursor.execute(sql.update_db_passwd(), (URL, new_password))

    if args.list:
        cursor.execute(sql.list_records())
        record = cursor.fetchall()

        for i in range(len(record)):
            entry = record[i]
            for j in range(len(entry)):
                titles = ["URL: ", "Username: ", "Password: "]
                if titles[j] == "Password: ":
                    bytes_row = entry[j]
                    password = master_password.decrypt_password(
                        bytes_row, master_password_hash)
                    print("Password: " + str(password.decode('utf-8')))

                else:
                    print(titles[i]+entry[j])

            print("-------------------------------")

    connection.commit()

    cursor.close()


main()
