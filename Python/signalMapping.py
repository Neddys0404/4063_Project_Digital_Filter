import pandas as pd

def map_to_0_255(value):
    # Cap the value between -5 and 5
    capped = max(min(value, 5), -5)
    # Map from [-5, 5] to [0, 255]
    return int((capped + 5) * 255 / 10)

# Load your CSV file
df = pd.read_table('./Python/4063_Project_noise.txt')  # Replace with your filename

# Apply mapping to the second column (index 1 or by name if available)
df['mapped_result'] = df.iloc[:, 1].apply(map_to_0_255)
df = df.drop(columns='result')

# Save the result to a new CSV file
df.to_csv('./Python/mapped_results.csv', index=False)

print("Mapping completed. Output saved to 'mapped_results.csv'.")
