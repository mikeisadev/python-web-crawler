def checkIfInputIsType(i, type, retryText):
    try:
        match type:
            case 'int': int(i)
            case 'str': str(i)
    except:
        checkIfInputIsType( input(retryText), type, retryText )
    
    return i

checkIfInputIsType('frgege', 'int', 'The input must be an integer: ')