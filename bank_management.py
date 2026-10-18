import sqlite3

# ---------------- DATABASE CONNECTION ----------------
conn = sqlite3.connect("bank.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS accounts(
    acc_no INTEGER PRIMARY KEY,
    name TEXT,
    balance REAL
)
""")
conn.commit()


# ---------------- BANK CLASS ----------------
class Bank:

    # Create Account
    def create_account(self):
        try:
            acc_no = int(input("Enter Account Number: "))
            name = input("Enter Customer Name: ")
            balance = float(input("Enter Initial Balance: "))

            cursor.execute("INSERT INTO accounts VALUES(?,?,?)",
                           (acc_no, name, balance))
            conn.commit()

            print("Account Created Successfully")

        except Exception as e:
            print("Error:", e)


    # Deposit
    def deposit(self):
        try:
            acc_no = int(input("Enter Account Number: "))
            amount = float(input("Enter Amount to Deposit: "))

            cursor.execute("SELECT balance FROM accounts WHERE acc_no=?", (acc_no,))
            data = cursor.fetchone()

            if data:
                new_balance = data[0] + amount
                cursor.execute("UPDATE accounts SET balance=? WHERE acc_no=?",
                               (new_balance, acc_no))
                conn.commit()
                print("Deposit Successful")
            else:
                print("Account not found")

        except:
            print("Invalid Input")


    # Withdraw
    def withdraw(self):
        try:
            acc_no = int(input("Enter Account Number: "))
            amount = float(input("Enter Amount to Withdraw: "))

            cursor.execute("SELECT balance FROM accounts WHERE acc_no=?", (acc_no,))
            data = cursor.fetchone()

            if data:
                if data[0] >= amount:
                    new_balance = data[0] - amount
                    cursor.execute("UPDATE accounts SET balance=? WHERE acc_no=?",
                                   (new_balance, acc_no))
                    conn.commit()
                    print("Withdrawal Successful")
                else:
                    print("Insufficient Balance")
            else:
                print("Account not found")

        except:
            print("Invalid Input")


    # Display Single Account
    def display(self):
        try:
            acc_no = int(input("Enter Account Number: "))
            cursor.execute("SELECT * FROM accounts WHERE acc_no=?", (acc_no,))
            data = cursor.fetchone()

            if data:
                print("\nAccount Number:", data[0])
                print("Name:", data[1])
                print("Balance:", data[2])
            else:
                print("Account not found")

        except:
            print("Invalid Input")


    # Insert Multiple Records (User Input)
    def insert_multiple(self):
        try:
            n = int(input("Enter number of records to insert: "))
            records = []

            for i in range(n):
                print(f"\nEnter details for record {i+1}")
                acc_no = int(input("Account Number: "))
                name = input("Customer Name: ")
                balance = float(input("Balance: "))

                records.append((acc_no, name, balance))

            cursor.executemany("INSERT INTO accounts VALUES(?,?,?)", records)
            conn.commit()

            print("Multiple records inserted successfully")

        except Exception as e:
            print("Error:", e)


    # Display All Accounts
    def display_all(self):
        cursor.execute("SELECT * FROM accounts")
        data = cursor.fetchall()

        if data:
            print("\n--- All Accounts ---")
            for row in data:
                print("Acc No:", row[0], "| Name:", row[1], "| Balance:", row[2])
        else:
            print("No records found")


    # ---------------- DELETE ALL RECORDS ----------------
    def delete_all(self):
        try:
            confirm = input("Are you sure you want to delete ALL records? (yes/no): ")

            if confirm.lower() == "yes":
                cursor.execute("DELETE FROM accounts")
                conn.commit()
                print("All records deleted")
            else:
                print("Operation cancelled")

        except:
            print("Error occurred")


# ---------------- MAIN PROGRAM ----------------
bank = Bank()

while True:

    print("\n------ BANK MANAGEMENT SYSTEM ------")
    print("1. Create Account")
    print("2. Deposit")
    print("3. Withdraw")
    print("4. Display Single Account")
    print("5. Insert Multiple Records (User Input)")
    print("6. Display All Accounts")
    print("7. Delete ALL Records")
    print("8. Exit")

    try:
        choice = int(input("Enter your choice: "))

        if choice == 1:
            bank.create_account()

        elif choice == 2:
            bank.deposit()

        elif choice == 3:
            bank.withdraw()

        elif choice == 4:
            bank.display()

        elif choice == 5:
            bank.insert_multiple()

        elif choice == 6:
            bank.display_all()

        elif choice == 7:
            bank.delete_all()

        elif choice == 8:
            print("Thank You")
            break

        else:
            print("Invalid Choice")

    except:
        print("Please enter valid number")


conn.close()
