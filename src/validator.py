def validate_unique(new, curr_list):
    '''
    This function wrapper ensures that the new item
    does not exist in the current list of items.
    '''
    return new not in curr_list

def validate_chars(new):
    '''
    This function wrapper ensures that the new item
    does not contain any forbidden characters for a
    file name.
    '''
    invalid_chars = '<>:"/\\|?!*'
    for char in invalid_chars:
        if char in new:
            return False
    return True