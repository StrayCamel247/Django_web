table_header = [{
    'keys': _,
    'title': _.capitalize(),
    'readOnly': False
    if _ in ['cost', 'num']
    else True}
    for _ in ['code', 'name', 'cost', 'num', 'trade', 'value', 'profit', 'rise', 'position', 'industry', 'pe_ratio', 'pb_ratio', 'ps_ratio', 'pcf_ratio', 'user_id']
]
