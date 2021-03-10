from functools import reduce
import json
from block import Block

from transaction import Transaction
from utility.hash_utils import hash_block
from utility.verification import Verification

# initialize blockchain.

MINING_REWARDS = 10


class Blockchain:
    def __init__(self, hosting_node_id):
        genesis_block = Block(0, '', [], 100, 0)
        self.__chain = [genesis_block]
        self.__open_transactions = []
        self.load_file()
        self.hosting_node = hosting_node_id

    @property
    def chain(self):
        return self.__chain[:]

    @chain.setter
    def chain(self, val):
        self.__chain = val

    def get_chain(self):
        return self.__chain[:]

    def get_open_transactions(self):
        return self.__open_transactions[:]

    def load_file(self):
        try:
            with open('blockchain.txt', mode='r') as f:
                # file_content = pickle.loads(f.read())
                file_content = f.readlines()
                # print(file_content)
                # global blockchain
                # global open_transactions
                # blockchain = file_content['chain']
                # open_transactions = file_content['ot']
                blockchain = json.loads(file_content[0][:-1])
                updated_blockchain = []
                for block in blockchain:
                    converted_tx = [
                        Transaction(
                            tx['sender'],
                            tx['recipient'],
                            tx['amount'],
                        )
                        for tx in block["transaction"]
                    ]
                    updated_block = Block(
                        block['index'],
                        block['previous_hash'],
                        converted_tx,
                        block['proof'],
                        block['time'],
                    )
                    updated_blockchain.append(updated_block)

                self.chain = updated_blockchain
                open_transactions = json.loads(file_content[1])
                updated_transactions = []
                for block in open_transactions:
                    updated_transaction = Transaction(
                        block['sender'],
                        block['recipient'],
                        block['amount'],
                    )
                    updated_transactions.append(updated_transaction)
                self.__open_transactions = updated_transactions
        except (IOError, IndexError):
            print('file not found!!!!')
        finally:
            print("cleanup !!")

    def save_file(self):
        try:
            with open('blockchain.txt', mode='w') as f:
                savable_chain = [
                    block.__dict__ for block in
                    [
                        Block(
                            block_el.index,
                            block_el.previous_hash,
                            [tx.__dict__ for tx in block_el.transaction],
                            block_el.proof,
                            block_el.time
                        )
                        for block_el in self.__chain
                    ]
                ]
                f.write(json.dumps(savable_chain))
                f.write('\n')
                savable_tx = [tx.__dict__ for tx in self.__open_transactions]
                f.write(json.dumps(savable_tx))
                # save_data = {
                #    'chain': blockchain,
                #    'ot': open_transactions,
                # }
                # f.write(pickle.dumps(save_data))
        except IOError:
            print("error!")

    def proof_of_work(self):
        last_blockchain = self.__chain[-1]
        last_block = hash_block(last_blockchain)
        proof = 0
        verifierB = Verification()
        while not verifierB.valid_block(self.__open_transactions, last_block, proof):
            proof += 1
        return proof

    def get_balance(self):
        """ get the balance of the account """
        participant = self.hosting_node
        tx_sender = [[tx.amount for tx in block.transaction
                      if tx.sender == participant]
                     for block in self.__chain]
        open_tx_senders = [tx.amount for tx in self.__open_transactions
                           if tx.sender == participant]
        tx_sender.append(open_tx_senders)
        amount_sent = reduce(
            lambda tx_sum, tx_amt: tx_sum + sum(tx_amt)
            if len(tx_amt) > 0 else tx_sum + 0,
            tx_sender, 0)
        tx_recipient = [[tx.amount for tx in block.transaction
                         if tx.recipient == participant]
                        for block in self.__chain]
        amount_received = reduce(
            lambda tx_sum, tx_amt: tx_sum + sum(tx_amt)
            if len(tx_amt) > 0 else tx_sum + 0,
            tx_recipient, 0)
        print(tx_sender)
        print(open_tx_senders)
        print(tx_recipient)
        return amount_received - amount_sent

    def get_last_transaction(self):
        """Access the first index of the blockchain """
        if len(self.__chain) < 1:
            return None
        return self.__chain[-1]

    def add_transaction(self, recipient, sender, amount=1.0):
        """ Add new block to the blockchain
        arguments:
        :sender: The sender of crypto.
        :recipient: The recipient of the crypto.
        :amount: The amount of crypto.
        """
        # transactions = {
        #   "sender": sender,
        #  "recipient": recipient,
        # "amount": amount,
        # }
        transactions = Transaction(sender, recipient, amount)
        verifier = Verification()
        if verifier.verify_transaction(transactions, self.get_balance):
            self.__open_transactions.append(transactions)
            self.save_file()
            return True
        return False

    def mine_block(self):
        last_block = self.__chain[-1]
        hashed_block = hash_block(last_block)
        # print(hashed_block)
        proof = self.proof_of_work()
        # reward_transaction = {
        #   "sender": 'MINING',
        #  "recipient": owner,
        # 'amount': MINING_REWARDS,
        # }
        reward_transaction = Transaction('MINING', self.hosting_node, MINING_REWARDS)
        copied_transaction = self.__open_transactions[:]
        copied_transaction.append(reward_transaction)
        # block = {
        #   "previous_hash": hashed_block,
        #  "index": len(blockchain),
        # "transactions": copied_transaction,
        # "proof": proof
        # }
        block = Block(
            len(self.__chain),
            hashed_block,
            copied_transaction,
            proof
        )

        self.__chain.append(block)
        self.__open_transactions = []
        self.save_file()
        return True
