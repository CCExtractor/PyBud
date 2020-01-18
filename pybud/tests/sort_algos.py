def bubble_sort(input_list):
    # Swap the elements to arrange in order
    for iter_num in range(len(input_list) - 1, 0, -1):
        for idx in range(iter_num):
            if input_list[idx] > input_list[idx + 1]:
                temp = input_list[idx]
                input_list[idx] = input_list[idx + 1]
                input_list[idx + 1] = temp
    return input_list


def merge_sort(input_list):
    if len(input_list) <= 1:  # list has 1 element or less, already sorted
        return input_list

    # Find the middle point and divide it
    middle = len(input_list) // 2
    left_list = input_list[:middle]
    right_list = input_list[middle:]

    left_list = merge_sort(left_list)
    right_list = merge_sort(right_list)
    return list(merge(left_list, right_list))


# Merge the sorted halves
def merge(left_half, right_half):
    res = []
    while len(left_half) != 0 and len(right_half) != 0:
        if left_half[0] < right_half[0]:
            res.append(left_half[0])
            left_half.remove(left_half[0])
        else:
            res.append(right_half[0])
            right_half.remove(right_half[0])
    if len(left_half) == 0:
        res = res + right_half
    else:
        res = res + left_half
    return res


def insertion_sort(input_list):
    for i in range(1, len(input_list)):
        j = i - 1
        nxt_element = input_list[i]
        # Compare the current element with next one
        while (input_list[j] > nxt_element) and (j >= 0):
            input_list[j + 1] = input_list[j]
            j = j - 1
        input_list[j + 1] = nxt_element
    return input_list


def shell_sort(input_list):
    gap = len(input_list) // 2
    while gap > 0:
        for i in range(gap, len(input_list)):
            temp = input_list[i]
            j = i
            # Sort the sub list for this gap

            while j >= gap and input_list[j - gap] > temp:
                input_list[j] = input_list[j - gap]
                j = j - gap
            input_list[j] = temp
        # Reduce the gap for the next element
        gap = gap // 2
    return input_list


def selection_sort(input_list):
    for idx in range(len(input_list)):
        min_idx = idx
        for j in range(idx + 1, len(input_list)):
            if input_list[min_idx] > input_list[j]:
                min_idx = j
        # Swap the minimum value with the compared value
        input_list[idx], input_list[min_idx] = input_list[min_idx], input_list[idx]
    return input_list
