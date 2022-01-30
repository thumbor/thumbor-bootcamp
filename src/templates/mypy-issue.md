## Areas of Expertise

MyPy, static typing

You will learn more about how to use statically typed python code. [mypy](http://mypy-lang.org/) is an optional static type checker for python. It provides compile-time type checking.

## Summary

In this task you'll fix `{{ filepath }}` to be typed.

## Involved Modules

* [thumbor](https://github.com/thumbor/thumbor/) - [{{ filepath }}](https://github.com/thumbor/thumbor/blob/master/{{ filepath }})

## Task Relevance

Providing type safety is important both for thumbor and the projects that depend on it. This way we can eliminate type errors, like `None` where you don't expect `None` or an integer where you expect a string.

## How to complete this task?

To complete this task, read [mypy docs on how to get started](https://mypy.readthedocs.io/en/latest/getting_started.html) and run `mypy {{ filepath }}` from thumbor's virtualenv.

When creating this task, this was the output of running `mypy {{ filepath }}`:

```
{{ mypy_output }}
```

This gives you all errors in the file you will fix. Don't worry if there are types of other packages (other thumbor files or thumbor dependencies) failing. If that's the case we can ignore these for now using this kind of annotation:

```python
import module_without_mypy  # type: ignore
```

For more details check [this page](https://mypy.readthedocs.io/en/latest/existing_code.html#start-small).

Once you get to a point where running `mypy {{ filepath }}` returns no errors, go ahead and submit a PR. The output should look like this:

```
Success: no issues found in 1 source file
```

## Task Workflow

The workflow for completing tasks in thumbor goes like this:

1. [Fork the involved repositories](http://help.github.com/fork-a-repo/)
2. In each repository there's a documentation on how to install dependencies and initialize your environment
3. Hack, in no particular order:
    - Write code & tests
    - Write new tests
    - Write docs
    - Improve design
    - Check that all tests pass
    - Repeat until you're satisfied
4. [Submit a pull request](https://docs.github.com/en/github/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request).
