import functools

# initialize blockchain.

MINING_REWARDS = 10

genesis_block = {
    "previous_hash": '',
    "index": 0,
    "transactions": []
}
blockchain = [genesis_block]
open_transactions = []
owner = 'visith'
participants = {'visith'}


def get_last_transaction():
    """Access the first index of the blockchain """
    if len(blockchain) < 1:
        return None
    return blockchain[-1]


def verify_transaction(transaction):
    """verify transaction by checking whether sender has sufficient coins
    arguments:
    :transaction:the transaction to be verified
    """
    sender_balance = get_balance(transaction['sender'])
    return sender_balance >= transaction['amount']


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
    if verify_transaction(transactions):
        open_transactions.append(transactions)
        participants.add(sender)
        participants.add(recipient)
        return True
    return False


def get_transaction_value():
    """Returns the input of the user (a new transaction) as a float"""
    tx_recipient = input("Enter the name of recipient: ")
    # get user input transform it from a string to a float and stores it in user_input
    tx_amount = float(input("Enter transaction amount : "))
    return tx_recipient, tx_amount


def mine_block():
    last_block = blockchain[-1]
    hashed_block = hash_block(last_block)
    # print(hashed_block)
    reward_transaction = {
        "sender": 'MINING',
        "recipient": owner,
        'amount': MINING_REWARDS,
    }
    copied_transaction = open_transactions[:]
    copied_transaction.append(reward_transaction)
    block = {
        "previous_hash": hashed_block,
        "index": len(blockchain),
        "transactions": copied_transaction,
    }
    blockchain.append(block)
    return True


def print_blockchain():
    """ print the current blockchain blocks"""
    for block in blockchain:
        print("updated blockchain")
        print(block)
    else:
        print("-" * 20)


def get_balance(participant):
    """ get the balance of the account
    arguments:
    :participant: the person whose account balance is calculated
    """
    tx_sender = [[tx['amount'] for tx in block['transactions']
                  if tx['sender'] == participant]
                 for block in blockchain]
    open_tx_senders = [tx['amount'] for tx in open_transactions if tx['sender'] == participant]
    tx_sender.append(open_tx_senders)
    amount_sent = functools.reduce(
        lambda tx_sum, tx_amt: tx_sum + sum(tx_amt)
        if len(tx_amt) > 0 else tx_sum + 0,
        tx_sender, 0)
    tx_recipient = [[tx['amount'] for tx in block['transactions']
                     if tx['recipient'] == participant]
                    for block in blockchain]
    amount_received = functools.reduce(
        lambda tx_sum, tx_amt: tx_sum + sum(tx_amt)
        if len(tx_amt) > 0 else tx_sum + 0,
        tx_recipient, 0)
    return amount_received - amount_sent


def hash_block(block):
    """Hashes the block
    Arguments:
        :block: block that should be hashed
    """
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
        if block['previous_hash'] != hash_block(blockchain[index - 1]):
            return False
        return True


def verify_transactions():
    """verify all open transactions"""
    return any([verify_transaction(tx) for tx in open_transactions])


waiting_for_input = True

while waiting_for_input:
    print("Please choose")
    print("1: Add new transaction")
    print("2: Output blocks in blockchain")
    print("3: Mine a new block")
    print("4: Participants in the transactions")
    print("5: print transaction validity")
    print("d: Manipulate the blocks")
    print("q: Quit")
    user_choice = get_user_choice()

    if user_choice == '1':
        txdata = get_transaction_value()
        txrecipient, txamount = txdata
        if add_transaction(txrecipient, amount=txamount):
            print("transaction received")
        else:
            print("transaction rejected")
        print(open_transactions)
    elif user_choice == '2':
        print_blockchain()
    elif user_choice == '3':
        print("New block is mined!")
        if mine_block():
            open_transactions = []
    elif user_choice == '4':
        print(participants)
    elif user_choice == '5':
        if verify_transactions():
            print("All transactions are verified")
        else:
            print("there are invalid transactions")
    elif user_choice == "q":
        print("exit blockchain")
        waiting_for_input = False
    elif user_choice == 'd':
        if len(blockchain) >= 1:
            blockchain[0] = {
                "previous_hash": '',
                "index": 0,
                "transactions": [{
                    "sender": "Max",
                    "recipient": "Visith",
                    "amount": 100,
                }]
            }
    else:
        print("Invalid input, please choose valid input from list!")
    if not verify_blockchain():
        print_blockchain()
        print("Invalid blockchain")
        break
    print(f'Balance of {owner} is {get_balance(owner):.2f}')
else:
    print("user left!")
print("done!")
