# Code Listing #1

"""

Maximum subarray problem - original version

"""

import itertools

# max_subarray: v1
def max_subarray(sequence):
    """ Find sub-sequence in sequence having maximum sum """
    # ところで例えば [0, 2, 3] は [0, 1, 2, 3, 4, 5] の
    # subseequence といえるだろうか？

    sums = []

    for i in range(len(sequence)):
        # Create all sub-sequences in given size
        for sub_seq in itertools.combinations(sequence, i):
            sub_seq_sum = sum(sub_seq)
            # Append sum
            print(f'{sub_seq} => {sub_seq_sum}')
            sums.append(sum(sub_seq))

    return max(sums)
