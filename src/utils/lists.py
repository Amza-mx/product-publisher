# Description: Utility functions for list operations

def make_chunks(items: list, chunk_size: int) -> list:
    """Function to split a list into chunks of n size"""

    for i in range(0, len(items), chunk_size):
        yield items[i:i + chunk_size]
