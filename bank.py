from datetime import datetime

# User
class User:
    def __init__(self, name, email, phone, password, type) -> None:
        self.name = name
        self.email = email
        self.phone = phone
        self.password = password
        self.type = type
        self.balance = 0
        self.loan_balance = 0
        self.loan_counter = 0
        self.ac_no = "201" + self.phone

    def show_user_info(self):
        print(
            f"City Bank Ltd.\nCongratulations! Account registration successfull.\n\nAccount information:\nName: {self.name}\nEmail: {self.email}\nPhone: {self.phone}\nAccount No: {self.ac_no}\nAccount Type: {self.type}\nAccount Balance: {self.balance} BDT\n\nN.B.: Do not share your information with others. Thank You."
        )
# Transaction History Class
class History:
    def __init__(self,ac_no, transaction_type, amount, balance, date) -> None:
        self.ac_no = ac_no
        self.transaction_type = transaction_type
        self.amount = amount
        self.main_balance = balance
        self.date = date.strftime("%Y-%m-%d %I:%M:%S %p")

    def show_history(self):
        print(f'Date: {self.date}, Type: {self.transaction_type}, Amount: BDT. {self.amount}, Balance: BDT. {self.main_balance}')

# Bank Class
class Bank(User):
    def __init__(self) -> None:
        self.users = []
        self.history = []
        self.user_log_dic = {}
        self.bank_balance = pow(10, 9)
        self.bank_loan_balance = 0
        self.logged_user = None
        self.loan_access = True
        # Admin Account
        admin = User('admin', 'admin@citybank.com', '01700010000', 'admin123', 'admin')
        admin.ac_no = 'Default Account'
        admin.balance = self.bank_balance
        self.users.append(admin)
        self.user_log_dic['admin@citybank.com'] = 'admin123'
        self.user_log_dic['01700010000'] = 'admin123'


    def open_user_ac(self, name, email, phone, password, ac_type):  # Open new account
        self.user_log_dic[email] = password
        self.user_log_dic[phone] = password
        new_user = User(name, email, phone, password, ac_type)
        self.users.append(new_user)
        new_user.show_user_info()

    def ac_log_in(self, email_or_phone, password):  # Log in account
        if self.user_log_dic[email_or_phone] == password:
            print("Log In successfull")
            for user in self.users:
                if user.email == email_or_phone or user.phone == email_or_phone:
                    self.logged_user = user
                    break
        else:
            print(
                "The information you provided is incorrect! Pleasy try with correct information"
            )

    def check_balance(self):  # Account Holder can check Balance
        print(f"\nYour current balance is: {self.logged_user.balance} BDT")

    def deposit_money(self, amount): # Account Holder can deposit Balance
        if amount > 0:
            self.logged_user.balance += amount
            self.bank_balance += amount
            self.history.append(History(self.logged_user.ac_no, 'Deposit', amount, self.logged_user.balance, datetime.now()))
            print(f'BDT. {amount} deposit is successfull, remaining balance: {self.logged_user.balance} BDT.')
        else:
            print(f'Enter a valid amount of money')

    def withdraw_money(self,amount): # Account Holder can withdraw Balance
        if amount > 0 and amount <= self.logged_user.balance and amount <= self.bank_balance:
            self.logged_user.balance -= amount
            self.bank_balance -= amount
            self.history.append(History(self.logged_user.ac_no, 'Withdraw', amount, self.logged_user.balance, datetime.now()))
            print(f'BDT. {amount} withdrawal is successfull, remaining balance: {self.logged_user.balance} BDT.')
        elif amount <= self.bank_balance:
            print('The bank is bankrupt')
        else:
            print('Withdrawal amount exceeded')

    def transaction_history(self): # Account Holder can view transaction history
        print(f'\nTransaction History for Mr/s. {self.logged_user.name}:')
        for history_entry in self.history:
            if history_entry.ac_no == self.logged_user.ac_no:
                {history_entry.show_history()}

    def take_loan(self, amount): # Account Holder can take loan (max 2 times)
        if self.loan_access == False:
            print('\nLoan feature currently disabled.')
            return
        if self.logged_user.loan_counter == 2:
            print('\nYou have reached the maximum limit for loans.')
            return
        self.logged_user.balance += amount
        self.logged_user.loan_balance += amount
        self.bank_loan_balance += amount
        self.bank_balance -= amount
        self.logged_user.loan_counter += 1
        self.history.append(History(self.logged_user.ac_no, 'Loan', amount, self.logged_user.balance, datetime.now()))
        print(f'\nBDT. {amount} loan successfully has been added to your account. Your current balance is BDT. {self.logged_user.balance} and Loan to pay is BDT. {self.logged_user.loan_balance}')

    def transfer_money(self,amount, other_ac_no): # Account Holder can transfer money to other accounts
        isValid = False
        if amount <= self.logged_user.balance:
            for user in self.users:
                if user.ac_no == other_ac_no:
                    isValid = True
                    other_user = user
                    break
            if isValid:
                self.logged_user.balance -= amount
                other_user.balance += amount
                self.history.append(History(self.logged_user.ac_no, f'Money Transfer{other_user.ac_no}', amount, self.logged_user.balance, datetime.now()))
                print(f'BDT. {amount} has been successfully transfered. Remaining Balance BDT. {self.logged_user.balance}')
            else:
                print('Account Does not exist')
        else:
            print(f'\nYou have reached the maximum limit for loans. Your balance is BDT. {self.logged_user.balance}')

    # Admin Access Only
    def delete_account(self, acno_or_email_or_phone): # Delete user account
        if acno_or_email_or_phone == 'admin@citybank.com' or acno_or_email_or_phone == '01700010000' or acno_or_email_or_phone == 'Default Account':
            print('\nYou can not delete admin account.')
            return
        found = False
        for user in self.users:
            if user.ac_no == acno_or_email_or_phone or user.email == acno_or_email_or_phone or user.phone == acno_or_email_or_phone:
                delete_user = user
                found = True
                break
        if found:
            self.users.remove(delete_user)
            self.user_log_dic[delete_user.email] = None
            self.user_log_dic[delete_user.phone] = None
            delete_user = None
            print(f'\nAccount successfully deleted.')
        else:
            print(f'\nNo account found with {acno_or_email_or_phone}')

    def all_account_list(self): # View all registered account
        if len(self.users) < 2:
            print('\nCurrently we do not have any user.')
            return
        print('\nAll User List:')
        i = 1
        for user in self.users:
            if user.name == 'admin':
                continue
            print(
            f"{i}. Name: {user.name}, Email: {user.email}, Phone: {user.phone}, Account No: {user.ac_no}, Account Type: {user.type}, Account Balance: {user.balance} BDT, Loan Amount: {user.loan_balance} BDT\n"
        )
            i += 1

    def check_bank_balance(self): # Check main balance of bank
        print(f'\nCurrent Bank Balance is {self.bank_balance} BDT.')

    def check_loan_balance(self): # Check total given loan
        print(f'\nCurrent Loan Amount is {self.bank_loan_balance} BDT.')

    def loan_feature(self, access): # Turn on/off loan feature as need
        if access == 'on':
            print('\nLoan feature has been enabled.')
            self.loan_access = True
        else:
            print('\nLoan feature has been disabled.')
            self.loan_access = False

def main():
    bank = Bank()
    while True:
        print('\nWelcome to the City Bank Ltd.')
        print('\nPress 1 to Create an account')
        print('Press 2 to Log in as user')
        print('Press 3 to Log in as admin')
        print('Press 4 to Exit')
        op = input('\nEnter your option: ')

        # Create Account
        if op == '1':
            name = input('\nEnter your Full Name: ')
            email = input('Enter your Email: ')
            phone = input('Enter your Phone Number: ')
            password = input('Enter your Password: ')
            print('\nPress 1 to open Savings Account')
            print('Press 2 to open Current Account')
            type_op = input('\nEnter your option: ')
            if type_op == '1':
                bank.open_user_ac(name, email, phone, password, 'Savings')
            elif type_op == '2':
                bank.open_user_ac(name, email, phone, password, 'Current')
        
        # User Login
        elif op == '2':
            email_or_phone = input('\nEnter your Email or Phone Number: ')
            password = input('Enter your Password: ')
            bank.ac_log_in(email_or_phone, password)
            while True:
                print('\nPress 1 to deposit money')
                print('Press 2 to withdraw money')
                print('Press 3 to check available balance')
                print('Press 4 to see transaction history')
                print('Press 5 to take a loan')
                print('Press 6 to transfer money')
                print('Press 7 to return main menu')
                type_op = input('\nEnter your option: ')
                if type_op == '1':
                    amount = int(input('\nEnter deposit amount: '))
                    bank.deposit_money(amount)
                elif type_op == '2':
                    amount = int(input('\nEnter withdraw amount: '))
                    bank.withdraw_money(amount)
                elif type_op == '3':
                    bank.check_balance()
                elif type_op == '4':
                    bank.transaction_history()
                elif type_op == '5':
                    amount = int(input('\nEnter loan amount: '))
                    bank.take_loan(amount)
                elif type_op == '6':
                    amount = int(input('\nEnter transfer amount: '))
                    ac_no = input('Enter A/C number: ')
                    bank.transfer_money(amount, ac_no)
                elif type_op == '7':
                    break
        
        # Admin Login
        elif op == '3':
            password = input('Enter ADMIN Password: ') # Password: admin123
            bank.ac_log_in('admin@citybank.com',password)
            while True:
                print('\nPress 1 to Create an account')
                print('Press 2 to Delete an user account')
                print('Press 3 to see all user account list')
                print('Press 4 to see total available balance of the bank')
                print('Press 5 to see total loan amount')
                print('Press 6 to turn on or off the loan feature')
                print('Press 7 to return main menu')
                type_op = input('\nEnter your option: ')
                if type_op == '1':
                    name = input('\nEnter your Full Name: ')
                    email = input('Enter your Email: ')
                    phone = input('Enter your Phone Number: ')
                    password = input('Enter your Password: ')
                    print('\nPress 1 to open Savings Account')
                    print('Press 2 to open Current Account')
                    ac_type = input('\nEnter your option: ')
                    if ac_type == '1':
                        bank.open_user_ac(name, email, phone, password, 'Savings')
                    elif ac_type == '2':
                        bank.open_user_ac(name, email, phone, password, 'Current')
                elif type_op == '2':
                    ac_no_or_email_or_phone = input('\nEnter A/C no or email or phone: ')
                    bank.delete_account(ac_no_or_email_or_phone)
                elif type_op == '3':
                    bank.all_account_list()
                elif type_op == '4':
                    bank.check_bank_balance()
                elif type_op == '5':
                    bank.check_loan_balance()
                elif type_op == '6':
                    if bank.loan_access == True:
                        print('\nLoan feature is currently on, press 1 to turn off it.')
                        x = input('Enter your option: ')
                        if x == '1':
                            bank.loan_feature('off')
                    else:
                        print('\nLoan feature is currently off, press 1 to turn on it.')
                        x = input('Enter your option: ')
                        if x == '1':
                            bank.loan_feature('on')
                elif type_op == '7':
                    break
        elif op == '4':
            print()
            break
if __name__ == '__main__':
    main()