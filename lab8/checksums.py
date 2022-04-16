def is_pow2(num):
    return (num != 0 and ((num - 1) & num == 0))

def calculate_checksum(bytes):
    bytes_splited = [bytes[i:i+2] for i in range(0, len(bytes), 2)]
    nums = [int.from_bytes(bt, 'little') for bt in bytes_splited]
    nums_sum = sum(nums)

    return nums_sum ^ ((2 << 32) - 1)

def verify_checksum(bytes, checksum):
    chcs = (((2<<32) - 1) ^ calculate_checksum(bytes)) + checksum

    return is_pow2(chcs + 1)


