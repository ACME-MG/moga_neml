params = (1,2,3,4,5)
def incorporate(params):
    fixed_indexes = [0,1,3]
    params = list(params)
    for fixed_index in fixed_indexes:
        params.insert(fixed_index, "A")
    return tuple(params)
new_params = incorporate(params)

def func(a,b,c,d,e,f,g,h):
    print(a,b,c,d,e,f,g,h)

func(*new_params)