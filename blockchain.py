# initialize blockchain.

genesis_block = {
    "previous_hash": '',
    "index": 0,
    "transactions": []
}
blockchain = [genesis_block]
open_transactions = []
owner = 'visith'


def get_last_transaction():
    """Access the first index of the blockchain """
    if len(blockchain) < 1:
        return None
    return blockchain[-1]


def add_transaction(recipient, sender=owner, amount=1.0):
    """ Add new block to the blockchain
    arguments:
    :sender: The sender of crypto.
    :recipient: The recipient of the crypto.
    :amount: The amount of crypto.
    """
    transactions = {
        "sender": sender,
        "recipient": recipient,
        "amount": amount,
    }
    open_transactions.append(transactions)


def get_transaction_value():
    """Returns the input of the user (a new transaction) as a float"""
    tx_recipient = input("Enter the name of recipient: ")
    # get user input transform it from a string to a float and stores it in user_input
    tx_amount = float(input("Enter transaction amount : "))
    return tx_recipient, tx_amount


def mine_block():
    last_block = blockchain[-1]
    hashed_block = hash_block(last_block)
    print(hashed_block)
    block = {
        "previous_hash": hashed_block,
        "index": len(blockchain),
        "transactions": open_transactions
    }
    blockchain.append(block)


def print_blockchain():
    """ print the current blockchain blocks"""
    for block in blockchain:
        print("updated blockchain")
        print(block)
    else:
        print("-" * 20)


def hash_block(block):
    """Hashes the block"""
    return '-'.join(str(block[key]) for key in block)


def get_user_choice():
    """ Get user input on which option to choose"""
    user_option = input("Select an option: ")
    return user_option


def verify_blockchain():
    """verify the blockchain and if it's true returns true else false"""
    for (index, block) in enumerate(blockchain):
        if index == 0:
            continue
        if block['previous_hash'] == hash_block(blockchain[index - 1]):
            pass


waiting_for_input = True

while waiting_for_input:
    print("Please choose")
    print("1: Add new transaction")
    print("2: Output blocks in blockchain")
    print("3: Mine a new block")
    print("d: Manipulate the blocks")
    print("q: Quit")
    user_choice = get_user_choice()

    if user_choice == '1':
        txdata = get_transaction_value()
        txrecipient, txamount = txdata
        add_transaction(txrecipient, amount=txamount)
        print(open_transactions)
    elif user_choice == '2':
        print_blockchain()
    elif user_choice == '3':
        print("New block is mined!")
        mine_block()
    elif user_choice == "q":
        print("exit blockchain")
        waiting_for_input = False
    elif user_choice == 'd':
        if len(blockchain) >= 1:
            blockchain[0] = [2]
    else:
        print("Invalid input, please choose valid input from list!")
    # if not verify_blockchain():
    #     print_blockchain()
    #    print("Invalid blockchain")
    #    break
else:
    print("user left!")
print("done!")
