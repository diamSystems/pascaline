
# Pascaline - A Python Superset

Pascaline is a programming language designed as a superset of Python. It extends Python's syntax and functionality, offering a cleaner and more flexible approach for certain use cases. Pascaline compiles directly to Python 3.12 bytecode and supports most Python features, while introducing enhancements to make code more readable and maintainable.

## Features

- **Syntax Extensions**: Pascaline introduces new syntactical elements and structure to enhance code readability.
- **Backward Compatibility**: Any valid Python code is also valid Pascaline code.
- **Transpiler**: The transpiler converts Pascaline code into Python code before execution, allowing seamless integration with Python libraries and tools.
- **Simplified Code**: Reduce boilerplate and write code that is clear and easy to maintain.
- **Comment Preservation**: Comments are preserved exactly; Pascaline leaves them untouched during transpilation.

## Usage

### Transpiling and Running

To transpile a `.pasc` file to Python, compile it to bytecode, and run it:

```bash
python pascaline.py run path/to/your/file.pasc
```

This command:
1. Converts your `.pasc` file to a `.py` file.
2. Compiles the Python code into bytecode.
3. Executes the bytecode with Python 3.12.

### Reverse Transpiling

To reverse transpile Python code back to Pascaline syntax (output is stored in-place):

```bash
python pascaline.py reverse path/to/your/file.py
```

## Syntax Overview

Pascaline is very similar to Python but introduces a few new keywords and syntax changes:

- **Function Declarations**: Use `fun` instead of `def`.
  
  ```pascaline
  fun greet(name):
      echo "Hello, " + name
  ```

- **Imports**: Use `use` instead of `import`.

  ```pascaline
  use math
  ```

- **Print Statement**: Use `echo` instead of `print`.

  ```pascaline
  echo "Hello, world!"
  ```

- **Return Statements**: Replace `=>` with `return` during transpilation, making the code more concise.

> **Note:** The transpiler leaves comments untouched. Use `#` for comments, as in Python.

## Example Code

Here's a simple example written in Pascaline:

```pascaline
fun factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n - 1)

fun main():
    number = 5
    result = factorial(number)
    echo "Factorial of " + number + " is " + result

main()
```

This code calculates the factorial of a number using a recursive function.

## Contributing

Contributions to Pascaline are welcome! To contribute:

1. Fork the repository.
2. Create a new branch for your changes.
3. Commit your changes.
4. Push your changes and open a pull request.

If you encounter any issues or have suggestions, please open an issue in the repository.

## License

Pascaline is open-source and released under the MIT License. See the [LICENSE](LICENSE) file for more information.

## Links

Currently no links. Coming soon though

---

© 2025 diam Systems Ltd. All rights reserved.
