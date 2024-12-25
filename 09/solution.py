from copy import deepcopy


def main():
    udm = get_input()
    defrag = defragment_1(deepcopy(udm))
    print('Ans1:', checksum(defrag))
    defrag = defragment_2(deepcopy(udm))
    print('Ans2:', checksum(defrag))


def get_input(infile='input.txt'):
    with open(infile) as f:
        disk_map = f.read().strip()
    udm = []
    fid = 0
    free = False
    result = []
    pos = 0
    for c in disk_map:
        bl = int(c)
        file_id = None if free else fid
        if bl:
            udm.append([file_id, pos, bl])
        if free:
            fid += 1
        free ^= True
        pos += bl
    return udm


def defragment_1(defrag):
    ri = len(defrag) - 1
    li = 0
    
    while True:
        rb_id, rb_pos, rb_size  = defrag[ri]
        while rb_id is None:
            ri -= 1
            rb_id, rb_pos, rb_size = defrag[ri]
        lb_id, lb_pos, lb_size = defrag[li]
        while lb_id is not None:
            li += 1
            lb_id, lb_pos, lb_size = defrag[li]
       
        if li >= ri:
            break
    
        if rb_size <= lb_size:
            defrag[li] = [rb_id, lb_pos, rb_size]
            if rb_size < lb_size:
                defrag.insert(li + 1, [None, lb_pos + rb_size, lb_size - rb_size])
                # adjust indices due to insertion
                ri += 1
            defrag[ri] = [None, rb_pos, rb_size]
            ri -= 1
            li += 1
        elif rb_size > lb_size:
            defrag[li] = [rb_id, lb_pos, lb_size]
            defrag[ri] = [rb_id, rb_pos, rb_size - lb_size]
            li += 1
    
    return defrag


def defragment_2(defrag):
    ri = len(defrag) - 1
    li = 0
    
    while ri > 0:
        rb_id, rb_pos, rb_size = defrag[ri]
        while rb_id is None:
            ri -= 1
            rb_id, rb_pos, rb_size = defrag[ri]
        
        li = 0
        lb_id, lb_pos, lb_size = defrag[li]
        while not (lb_id is None and lb_size >= rb_size):
            li += 1
            if li >= ri:
                break
            lb_id, lb_pos, lb_size = defrag[li]
    
        if li >= ri:  # space not found
            ri -= 1
            continue
    
        defrag[li] = [rb_id, lb_pos, rb_size]
        if lb_size > rb_size:
            defrag.insert(li+1, [None, lb_pos + rb_size, lb_size - rb_size])
            ri += 1
        defrag[ri] = [None, rb_pos, rb_size]
        ri -= 1
        li += 1
    return defrag
    

def checksum(defrag):
    cksum = 0
    for fid, pos, size in defrag:
        if fid is not None:
            cksum += fid * sum(range(pos, pos+size))
    return cksum


if __name__ == '__main__':
    main()