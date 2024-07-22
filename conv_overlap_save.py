# Convolution of long sequence using overlap and save method
import numpy as np


def conv_overlap_save(h, x, N1):
    """
    Computes response of a system (h) for a
    long input sequence (x) using overlap (N1) & save.
    """
    Nx = len(x)
    Nh = len(h)
    N2 = N1
    Idx1 = np.linspace(0, Nh - 2, Nh - 1).astype('int')
    Idx2 = np.linspace(N1 - Nh + 1, N1 - 1, Nh - 1).astype('int')
    Idx3 = np.linspace(0, N1 - 1, N1).astype('int')
    y_OS1 = np.zeros(N2)
    y_OS2 = np.zeros(N2)
    y_OS = np.zeros(Nx)
    y_cnt = int(0)
    
    while y_cnt < Nx:
        x2 = x[y_cnt : y_cnt + N1]
        x_cnt = 0
        while x_cnt < N2:
            h_cnt = 0
            sum1 = 0
            while h_cnt < Nh:
                x_idx = x_cnt + h_cnt - Nh + 1
                if x_idx < 0:
                    x_idx += N1

                h_idx = Nh - 1 - h_cnt
                if x_idx >= N1:
                    break

                sum1 += x2[x_idx] * h[h_idx]
                h_cnt += 1

            y_OS1[x_cnt] = sum1
            x_cnt += 1
        
        if y_cnt > 0:
            y_OS1[Idx1] = y_OS2[Idx2]
        
        y_OS2[0:N2] = y_OS1[0:N2]
        Idx4 = Idx3 + y_cnt
        y_OS[Idx4] = y_OS1[0:N2]
        y_cnt += N1 - Nh + 1
        if Idx4[N1 - 1] >= Nx - 1:
            break
    
    return y_OS


def main():
    ### sequences
    x = np.linspace(1, 14, 14)
    h = [-1, -2, -3]

    Nx = len(x)
    Nh = len(h)

    ### linear conv
    y_linear = np.convolve(x, h)

    print(f'x(n): {x}')
    print(f'h(n): {h}')

    ### overlap and save
    N1 = 6
    # zero pad for a sequence of indivisible length 
    md = np.mod(Nx, N1)
    if md > 0:
        cnt = int(0)
        while md > 0:
            cnt += 1
            md = np.mod(Nx + cnt, N1)
        
        x2 = np.zeros(Nx+cnt)  # pad with cnt no. of zeros
        x2[0:Nx] = x[0:Nx]
        x = x2

    y_OS = conv_overlap_save(h, x, N1)
    WrongResult_Loc = np.linspace(0, Nh - 2, Nh - 1).astype('int')
    # cumulative absolute difference in results
    Diff = np.sum(np.abs(y_linear[Nh:Nx] - y_OS[Nh:Nx]))

    print(f'y_linear(n):\n{y_linear}')
    print(f'y_overlap_and_save:\n{y_OS}')
    print(f'Wrong result at sample number: {WrongResult_Loc}, '
            f'with values: {y_OS[WrongResult_Loc]}')
    print(f'Diff in results = {Diff}')


if __name__ == '__main__':
    main()

