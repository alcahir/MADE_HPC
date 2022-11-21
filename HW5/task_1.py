from mpi4py import MPI
from random import randint, choice


NAMES = ["John", "Angie", "Fedor", "Vova", "Sashka", "Victor"]


def main():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    if rank == 0:
        next_rank = randint(1, size - 1)
        msg = [(rank, NAMES[rank]), (next_rank, NAMES[next_rank])]
        comm.ssend(msg, dest=next_rank)
    else:
        msg = comm.recv()
        curr_rank, curr_name = msg[-1]
        available_processors = [
            rank for rank in range(size)
            if rank not in [prev_rank[0] for prev_rank in msg]
        ]
        print(msg)
        if available_processors:
            next_rank = choice(available_processors)
            msg.append((next_rank, NAMES[next_rank]))
            comm.ssend(msg, next_rank)


if __name__ == "__main__":
    main()
