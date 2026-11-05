# Triggering my first CI/CD run!

def add_numbers(a, b):
    return a + b

if __name__ == "__main__":
    result = add_numbers(5, 5)
    print(f"--- PYTHON OUTPUT: 5 + 5 is {result} ---")
    assert result == 10, "Math is broken!"
    print("All internal Python checks passed successfully!")
