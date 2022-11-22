import sys

from mpi4py import MPI
import numpy as np


def get_rules(binary):
    bin_len = len(binary)
    val = list(map(int, "0" * (8 - bin_len) + binary if bin_len < 8 else binary))
    return {
        "111": val[0],
        "110": val[1],
        "101": val[2],
        "100": val[3],
        "011": val[4],
        "010": val[5],
        "001": val[6],
        "000": val[7]
    }


def generate_sequence(arr):
    seq = []
    for idx in range(1, len(arr) - 1):
        curr_val = arr[idx]
        left_neighbor = arr[idx - 1]
        right_neighbor = arr[idx + 1]
        triplet = "".join(map(str, [left_neighbor, curr_val, right_neighbor]))
        seq.append(template[triplet])
    return seq


def main():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    count = vector_size // size
    residuals = vector_size % size

    if residuals and rank == size - 1:
        count += residuals

    sub_arr = list(np.random.binomial(1, 0.5, count))
    print(f"Rank={rank}.\nInitial samples={sub_arr}")
    prev_rank = rank - 1 if rank - 1 >= 0 else size - 1
    next_rank = rank + 1 if rank + 1 < size else 0
    comm.isend(sub_arr[0], prev_rank, tag=int("".join([str(rank), str(prev_rank)])))
    comm.isend(sub_arr[-1], next_rank, tag=int("".join([str(rank), str(next_rank)])))
    left_ghost = comm.recv(source=prev_rank, tag=int("".join([str(prev_rank), str(rank)])))
    right_ghost = comm.recv(source=next_rank, tag=int("".join([str(next_rank), str(rank)])))
    arr = [left_ghost] + sub_arr + [right_ghost]
    arr = generate_sequence(arr)
    print(f"Rank={rank}.\nAfter iteration={arr}\n")
    arr = comm.gather(arr, root=0)

    if rank == 0:
        print("Response", arr, "\n")


if __name__ == "__main__":
    vector_size = int(sys.argv[-1])
    ruler = int(sys.argv[-2])
    template = get_rules(bin(ruler)[2:])
    main()
