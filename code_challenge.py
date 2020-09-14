a = {
  "cat": "bob",
  "dog": 23,
  19: 18,
  90: "fish"
}

def sum_dict(a):
  
    sum = 0
    
    for key in a:
        if type(a[key]) is int:
            sum += a[key]

    return sum


print(sum_dict(a))




