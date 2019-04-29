def binary_search(list_data, num):  # non-recursion
    low = 0
    high = len(list_data)-1
    while low <= high:
        mid = int((low + high)/2)
        if num < list_data[mid]:
            low = mid - 1
        elif num > list_data[mid]:
            high = mid + 1
        else:
            return mid
    return None


def binary_search_rec(list_data, left, right, num):  # recursion
    if left > right:
        return -1
    mid = (left + right) // 2
    if num < list_data[mid]:
        right = mid - 1
    elif num > list_data[mid]:
        left = mid + 1
    else:
        return mid
    return binary_search_rec(list_data, left, right, num)


m = [1, 2, 3, 4, 8, 9, 11, 12, 14, 18, 19, 20, 28]
print(binary_search(m, 14))
print(binary_search_rec(m, 0, len(m) - 1, 14))
