from utility.hash_utils import hash_string_256, hash_block


class Verification:

    @staticmethod
    def valid_block(transaction, last_hash, proof):
        guess = (str([tx.to_ordered_dict() for tx in transaction]) + str(last_hash) + str(proof)).encode()
        guess_hash = hash_string_256(guess)
        # print(guess_hash)
        return guess_hash[0:2] == '00'

    @classmethod
    def verify_blockchain(cls, blockchain):
        """verify the blockchain and if it's true returns true else false"""
        for (index, block) in enumerate(blockchain):
            if index == 0:
                continue
            if block.previous_hash != hash_block(blockchain[index - 1]):
                return False
            if not cls.valid_block(block.transaction[:-1], block.previous_hash, block.proof):
                print('Invalid chain')
                return False
            return True

    @staticmethod
    def verify_transaction(transaction, get_balance):
        """verify transaction by checking whether sender has sufficient coins
        arguments:
        :transaction:the transaction to be verified
        """
        sender_balance = get_balance()
        return sender_balance >= transaction.amount

    @classmethod
    def verify_transactions(cls, open_transactions, get_balance):
        """verify all open transactions"""
        return all([cls.verify_transaction(tx, get_balance) for tx in open_transactions])
