#!/usr/bin/env python3
"""Rotate a matrix by 90 degrees.

Usage: ./rotate_matrix [OPTION] ...

Options:
    -h, --help\tPrint this message.
    -m, --mode\tCreate ("create") the matrix yourself or generate an enumerated one (any other string, default).
    -n, --dim\tDimension of the matrix. Will be prompted if not set.
"""

import getopt
import sys

def create_matrix(dim):
    """Create the matix from user input.

    Args:
        dim: Dimension of the matrix.

    Returns:
        User-defined matrix as a nested list.

    Raises:
        Error if unsymmetric matrix is created.
    """
    matr = []
    for i in range(dim):
        matr.append(input("Type line {}: ".format(str(i+1))).split()) # Get one line as input, separated by spaces.
        if len(matr[i]) != dim:
            sys.exit("ERROR: Only symmetric matrices allowed.")
    return matr

def generate_matrix(dim):
    """Generate the matrix with enumarated elements.

    Args:
        dim: Dimension of the matrix.

    Returns:
        Generated matrix as a nested list.
    """
    matr = []
    for i in range(dim):
        # Start by 1 and increase the number for each new element by one.
        matr.append(list(range((i+1)*dim-dim+1, (i+1)*dim+1)))
    return matr

def print_matrix(matr):
    """Print the matrix in a user-readable way.

    Allows for good readablity as long as the dimensionality of the matrix is small enough
    to avoid linebreaks (about dim<=25).

    Args:
        matr: Matrix as a nested list.
    """
    for line in matr:
        for entry in line:
            print("\t{}".format(str(entry)), end="")
        print("\n")

def rotate_matrix(matr):
    """Rotate the matrix by 90 degrees.

    Achieved by using only one temporal variable 'tmp'. Start in the middle and
    rotate each cycle individually. Uses helper functions odd(dim, cycle) and get_cycle(cycle, dim).

    Args:
        matr: Matrix as a nested list.

    Returns:
        Rotated matrix as a nested list.
    """
    dim = len(matr)
    cycles = int(dim/2)
    for cycle in range(cycles):
        rot, size = get_cycle(cycle, dim)
        # Now loop over one side of the cycle and rotate the elements around.
        # Looping over one side is enough since we rotate each next element until the cylce is complete.
        # E.g. dim=3: a11 -> a13 (upper side), a13 -> a33 (right side), a33 -> a31 and a31 -> a11 (lower side).
        # Each element moves by a distance given by the dimension of the (sub-)matrix minus one.
        for i in range(size): # size returned by get_cycle is the step size of the rotation.
            # upper side
            tmp = matr[rot[i+size][0]][rot[i+size][1]] # Store element to be replaced in temporal variable.
            matr[rot[i+size][0]][rot[i+size][1]] = matr[rot[i][0]][rot[i][1]] # Put new variable in the right place.
            matr[rot[i][0]][rot[i][1]] = tmp # Free temporal variable by storing it in initial element.
            # right side
            tmp = matr[rot[i+2*size][0]][rot[i+2*size][1]]
            matr[rot[i+2*size][0]][rot[i+2*size][1]] = matr[rot[i][0]][rot[i][1]]
            matr[rot[i][0]][rot[i][1]] = tmp
            # lower side
            tmp = matr[rot[i+3*size][0]][rot[i+3*size][1]]
            matr[rot[i+3*size][0]][rot[i+3*size][1]] = matr[rot[i][0]][rot[i][1]]
            # Now the temporal variable is assigned initial element, i.e. the cycle is complete.
            matr[rot[i][0]][rot[i][1]] = tmp
    return matr

def odd(dim, cycle):
    """Check if dimension if odd and if so increase cycle number by one.

    Args:
        dim: Dimension of the matrix.
        cycle: Number of the current cycle.

    Returns:
        Adapted cycle number.
    """
    if dim%2 != 0:
        cycle += 1
    return cycle

def get_cycle(cycle, dim):
    """Get the rotation cycle of a (sub-)matrix.

    Fill a list with tupel of the indices of the rotation cycle. This can be later used
    to access the corresponding entries in the matrix.

    Args:
        dim: Dimension of the matrix.
        cycle: Number of the current cycle.

    Returns:
        List of tupels with rotation cycle indices and size(length) of the upper side of the (sub-)matrix.
    """
    cycle_rot = []
    init = int(dim/2)
    size = 0
    # Four for loops which go clockwise around each side of the cycle and append a tupel of the indices to the list.
    # upper side
    for i in range(init-cycle-1, init+odd(dim, cycle)+1):
        cycle_rot.append((init-cycle-1, i))
    size = len(cycle_rot)-1
    # right side
    for i in range(init-cycle, init+odd(dim, cycle)+1):
        cycle_rot.append((i, init+odd(dim, cycle)))
    # lower side (go backwards)
    for i in range(init+odd(dim, cycle)-1, init-cycle-2, -1):
        cycle_rot.append((init+odd(dim, cycle), i))
    # left side (go backwards)
    for i in range(init+odd(dim, cycle)-1, init-cycle-1, -1):
        cycle_rot.append((i, init-cycle-1))
    return cycle_rot, size

def main():
    """Main function: Process input data and rotate the created/generated matrix."""
    if len(sys.argv) == 1:
        print("Using default settings. Call {} -h for more options.".format(sys.argv[0]))
    dim = None
    create = False
    try:
        opts = getopt.getopt(sys.argv[1:], "hm:n:", ["help", "mode=", "dim="])[0]
    except getopt.GetoptError as err:
        print(__doc__)
        sys.exit(err)

    for opt, arg in opts:
        if opt in ["-h", "--help"]:
            sys.exit(__doc__)
        elif opt in ["-m", "--mode"]:
            if arg == "create":
                create = True
        elif opt in ["-n", "--dim"]:
            dim = int(arg)

    if dim is None:
        dim = int(input("Type dimension: "))
    if create:
        matr = create_matrix(dim)
    else:
        matr = generate_matrix(dim)

    print("Input Matrix:\n")
    print_matrix(matr)
    print("Rotated Matrix:\n")
    print_matrix(rotate_matrix(matr))

if __name__ == '__main__':
    main()
