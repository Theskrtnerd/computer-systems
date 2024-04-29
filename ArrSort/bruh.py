def merge(arr, r4, r5, r6):
    i = r4
    j = r5 + 1
    
    while i <= r5 and j <= r6:
        if arr[i] <= arr[j]:
            i += 1
        else:
            temp = arr[j]
            for k in range(j, i, -1):
                arr[k] = arr[k - 1]
            arr[i] = temp
            i += 1
            j += 1
            r5 += 1
    
def merge_sort(arr):
    r2 = len(arr)
    r3 = 1
    
    while r3 < r2:
        r4 = 0
        while r4 < r2 - 1:
            r7 = r2 - 1
            r5 = r3+r4-1
            r5 = min(r5, r7)
            r6 = r5+r3
            r6 = min(r6, r7)
            merge(arr, r4, r5, r6)
            r4 += 2 * r3
        r3 *= 2

import random
large_list = list(range(-10, 10, 1))
random.shuffle(large_list)

# Example usage:
arr = [-2,1,-4,3]
print(arr)
merge_sort(arr)
print("Merge Sorted array is:", arr)
