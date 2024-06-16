import numpy as np

def get_user_input():
    print("Enter the array elements separated by spaces (e.g., 0 0 0 ...):")
    print("Enter each row of the array as a separate line.")
    print("Press Enter twice to finish input.")
    
    # Initialize an empty list to store rows
    rows = []
    
    # Read rows until empty line
    while True:
        row_input = input().strip()
        if not row_input:
            break
        row = list(map(float, row_input.split()))
        rows.append(row)
    
    # Convert the list of rows to a numpy array
    array = np.array(rows)
    return array

# Get user input for the array
data_array = get_user_input()

# Reshape the array to match the input shape expected by the model
data_array_reshaped = data_array.reshape(1, 8, 8, 17)

# Display the reshaped array
print("Reshaped array:")
print(data_array_reshaped)
