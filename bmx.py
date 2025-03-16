import hashlib
import numpy as np
import random
import time
from multiprocessing import shared_memory

class BMX:
    def __init__(self, mode='light'):
        """
        Initialize the BMX proof-of-work algorithm in light or fast mode.
        
        :param mode: Either 'light' or 'fast'. Determines memory usage and speed.
        """
        self.mode = mode
        self.shared_mem = None
        self.memory_size = 256 * 1024 * 1024 if mode == 'light' else 2080 * 1024 * 1024
        self.setup_shared_memory()

    def setup_shared_memory(self):
        """Set up shared memory for the mining process."""
        self.shared_mem = shared_memory.SharedMemory(create=True, size=self.memory_size)
        self.mem_buffer = np.ndarray(shape=(self.memory_size // 8,), dtype=np.uint64, buffer=self.shared_mem.buf)

    def mine(self, target_difficulty):
        """Perform mining using Proof of Work (PoW) with SHA-256."""
        nonce = 0
        target = target_difficulty  # Mining difficulty: we want to mine below this value
        start_time = time.time()

        while True:
            # Create a random data block as input for mining
            block_data = self.generate_block_data(nonce)
            
            # Perform hashing (SHA-256)
            result = hashlib.sha256(block_data).hexdigest()

            # Check if the result satisfies the target difficulty
            if int(result, 16) < target:
                print(f"Block mined with nonce: {nonce}")
                print(f"Hash: {result}")
                print(f"Time taken: {time.time() - start_time} seconds")
                return result, nonce
            
            nonce += 1

    def generate_block_data(self, nonce):
        """Generate block data to hash, incorporating shared memory."""
        # Combine shared memory content and nonce for mining
        block_data = self.mem_buffer.tobytes() + nonce.to_bytes(8, byteorder='big')
        return block_data

    def stop(self):
        """Clean up shared memory."""
        self.shared_mem.unlink()


if __name__ == '__main__':
    # Initialize BMX in light mode
    bmx_miner = BMX(mode='light')
    
    try:
        target_difficulty = 0x00000FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF  # Set a mining difficulty
        result, nonce = bmx_miner.mine(target_difficulty)
    finally:
        bmx_miner.stop()
