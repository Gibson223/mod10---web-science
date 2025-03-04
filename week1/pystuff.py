def convert_dict(pairs):
    value_dict = dict()
    for key, value in pairs.items():
        print(key, value)
        #         print(value_dict[value])
        value_dict.setdefault(value, [])
        value_dict[value].append(key)
    #         value_dict[value] += key
    return value_dict


test = {
    ("334823", "961828"): 2,
    ("285065", "961828"): 1,
    ("324264", "392383"): 2,
    ("455179", "774010"): 1,
    ("108601", "197132"): 1,
    ("205592", "976868"): 1,
    ("401918", "561122"): 1,
    ("18282", "77884"): 2,
    ("136755", "992566"): 3,
    ("125539", "18962"): 3,
    ("136755", "661899"): 3,
    ("285065", "415679"): 2,
    ("58492", "922964"): 4,
    ("554748", "77884"): 1,
    ("426379", "661899"): 2,
    ("328364", "823308"): 1,
    ("18962", "765796"): 1,
    ("596394", "823308"): 2,
    ("189478", "839316"): 1,
    ("546780", "951483"): 2,
    ("579593", "770688"): 1,
    ("206983", "922044"): 1,
    ("240196", "860536"): 1,
    ("617192", "897180"): 1,
    ("642886", "87926"): 1,
    ("472261", "987963"): 2,
    ("275101", "821062"): 1,
    ("447275", "651254"): 3,
    ("601018", "934806"): 2,
    ("381169", "905252"): 1,
    ("408600", "511834"): 1,
    ("497356", "652681"): 1,
    ("420475", "957680"): 3,
    ("265464", "77884"): 1,
    ("982590", "992566"): 1,
    ("506221", "897180"): 1,
    ("150506", "797484"): 1,
    ("470130", "923963"): 1,
    ("258071", "506221"): 1,
    ("32000", "679997"): 2,
    ("240448", "957680"): 1,
    ("163154", "394792"): 1,
    ("439118", "836381"): 1,
    ("265264", "902949"): 1,
    ("554016", "625839"): 1,
    ("651254", "818346"): 4,
    ("222739", "482236"): 1,
    ("645671", "96857"): 2,
}

print(convert_dict(test))

