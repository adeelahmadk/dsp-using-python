# Convolution of long sequence using overlap and add method
import numpy as np


def conv_overlap_add(h, x, N1):
    """
    Computes response of a system (h) for a
    long input sequence (x) using overlap & add (N1).
    """
    Nx = len(x)
    Nh = len(h)
    N2 = N1 + Nh - 1
    Idx1 = np.linspace(0, Nh - 2, Nh - 1).astype('int')
    Idx2 = np.linspace(N1, N2 - 1, Nh - 1).astype('int')
    Idx3 = np.linspace(0, N1 + Nh - 2, N1 + Nh - 1).astype('int')
    y_OA1 = np.zeros(N2)
    y_OA2 = np.zeros(N2)
    y_OA = np.zeros(Nx + Nh - 1)
    y_cnt = int(0)
    
    while y_cnt < Nx:
        x2 = x[y_cnt : y_cnt + N1]
        x_cnt = 0
        while x_cnt < N2:
            h_cnt = 0
            sum1 = 0
            while h_cnt < Nh:
                x_idx = x_cnt + h_cnt - Nh + 1
                if x_idx >= N1:
                    break;
                h_idx = Nh - 1 - h_cnt
                if x_idx < 0:
                    sum1 += 0
                else:
                    sum1 += x2[x_idx] * h[h_idx]
                h_cnt += 1
            y_OA1[x_cnt] = sum1
            x_cnt += 1
        
        if y_cnt > 0:
            y_OA1[Idx1] = y_OA1[Idx1] + y_OA2[Idx2]
        
        y_OA2[0:N2] = y_OA1[0:N2]
        Idx4 = Idx3 + y_cnt
        y_OA[Idx4] = y_OA1[0:N2]
        y_cnt += N1
    
    return y_OA


def main():
    x = np.linspace(1, 12, 12)
    h = [-1, -2, -3]
    Nx = len(x)

    ### linear conv
    y_linear = np.convolve(x, h)
    print(f'x(n): {x}')
    print(f'h(n): {h}')
    print(f'y_linear(n): {y_linear}')

    ### overlap and add
    N1 = 4
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

    tmp_y_oa = conv_overlap_add(h, x, N1)
    y_OA = np.zeros(Nx)
    y_OA[0:Nx] = tmp_y_oa[0:Nx]
    # cumulative absolute difference in results
    Diff = np.sum(np.abs(y_linear[0:Nx] - y_OA))

    print(f'y_overlap_and_add: {y_OA}')
    print(f'Diff = {Diff}')


if __name__ == '__main__':
    main()

