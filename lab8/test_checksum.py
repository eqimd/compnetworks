from checksums import calculate_checksum, verify_checksum


s = b'sdfklasdjgkldj'
print(verify_checksum(s, calculate_checksum(s)))
print(verify_checksum(s, 78126783))