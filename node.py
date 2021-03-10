from blockchain import Blockchain
# from uuid import uuid4
from utility.verification import Verification


class Node:
    def __init__(self):
        # self.id = str(uuid4())
        self.id = "visith"
        self.blockchain = Blockchain(self.id)

    @staticmethod
    def get_transaction_value():
        """Returns the input of the user (a new transaction) as a float"""
        tx_recipient = input("Enter the name of recipient: ")
        # get user input transform it from a string to a float and stores it in user_input
        tx_amount = float(input("Enter transaction amount : "))
        return tx_recipient, tx_amount

    @staticmethod
    def get_user_choice():
        """ Get user input on which option to choose"""
        user_option = input("Select an option: ")
        return user_option

    def print_blockchain(self):
        """ print the current blockchain blocks"""
        for block in self.blockchain.chain:
            print("updated blockchain")
            print(block)
        else:
            print("-" * 20)

    def listen_to_input(self):

        waiting_for_input = True

        while waiting_for_input:
            print("Please choose")
            print("1: Add new transaction")
            print("2: Output blocks in blockchain")
            print("3: Mine a new block")
            print("4: print transaction validity")
            print("q: Quit")
            user_choice = self.get_user_choice()
            verify = Verification()

            if user_choice == '1':
                txdata = self.get_transaction_value()
                txrecipient, txamount = txdata
                if self.blockchain.add_transaction(self.id, txrecipient, amount=txamount):
                    print("transaction received")
                else:
                    print("transaction rejected")
                print(self.blockchain.get_open_transactions())
            elif user_choice == '2':
                self.print_blockchain()
            elif user_choice == '3':
                print("New block is mined!")
                if self.blockchain.mine_block():
                    self.blockchain.open_transactions = []
            elif user_choice == '4':
                if verify.verify_transactions(self.blockchain.get_open_transactions(), self.blockchain.get_balance):
                    print("All transactions are verified")
                else:
                    print("there are invalid transactions")
            elif user_choice == "q":
                print("exit blockchain")
                waiting_for_input = False
            else:
                print("Invalid input, please choose valid input from list!")
            if not verify.verify_blockchain(self.blockchain.chain):
                self.print_blockchain()
                print("Invalid blockchain")
                break
            print(f'Balance of {self.id} is {self.blockchain.get_balance():.2f}')
        else:
            print("user left!")
        print("done!")


if __name__ == '__main__':
    # execute node
    node = Node()
    node.listen_to_input()
