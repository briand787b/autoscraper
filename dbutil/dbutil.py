def trim_fields(limits: dict, *vals: dict):
    '''
    trim_fields trims string fields according to limits
    specified in the `limits` argument.
    `limits` arg must be a dict of type str=>int
    `vals` can have elements of any type mapping
    '''
    if not vals:
        raise Exception('no values to trim')
    
    for field, lim in limits.items():
        for v in vals:
            try:
                actual = v.get(field)
                if not actual:
                    continue

                if type(actual) == str:
                    v[field] = actual[:lim]

                if type(actual) == list:
                    for i, elem in enumerate(actual):
                        v[field][i] = elem[:lim]

            except Exception as e:
                print(f'[ERROR] field: {field}, val: {v}, err: {e}')
                continue
