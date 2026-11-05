# Triggering my first CI/CD run!

def add_numbers(a, b):
    return a + b

if __name__ == "__main__":
    result = add_numbers(10, 10)
    print(f"--- PYTHON OUTPUT: 10 + 10 is {result} ---")
    assert result == 20, "Math is broken!"
    print("All internal Python checks passed successfully!")
