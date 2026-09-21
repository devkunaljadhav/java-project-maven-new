import sys

import requests

OLLAMA_URL = "http://172.31.41.103:11434/api/generate"
MODEL = "dgpl/dgpl-linux-assistant:latest"


def review_code(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            code = file.read()

        prompt = f"""
You are an experienced Java code reviewer working inside a CI/CD pipeline.

Review the following Java source code carefully.

Analyze the code for:

1. Bugs
2. Security issues
3. Exception handling
4. Null handling
5. Code quality
6. Performance issues
7. Maintainability
8. Java best-practice violations

For every important issue, provide:

- Severity: Critical / High / Medium / Low
- Problem
- Explanation
- Suggested Fix

Also provide a short overall summary.

If there are no significant issues, clearly say:

"No significant issues found."

File:
{file_path}

Java Code:

```java
{code}
```
"""

        print("Sending code to Ollama...")

        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "prompt": prompt,
                "stream": False,
            },
            timeout=300,
        )

        response.raise_for_status()

        result = response.json()

        return result.get("response", "No response received from Ollama.")

    except FileNotFoundError:
        print(f"ERROR: File not found: {file_path}")
        sys.exit(1)

    except requests.exceptions.ConnectionError:
        print("ERROR: Cannot connect to Ollama.")
        print(f"Ollama URL: {OLLAMA_URL}")
        sys.exit(1)

    except requests.exceptions.Timeout:
        print("ERROR: Ollama request timed out.")
        sys.exit(1)

    except requests.exceptions.RequestException as e:
        print(f"ERROR: Ollama API request failed: {e}")
        sys.exit(1)

    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)


def main():
    if len(sys.argv) != 2:
        print("Usage:")
        print("python3 code_review.py <java_file>")
        sys.exit(1)

    file_path = sys.argv[1]

    print()
    print("=" * 70)
    print("AI CODE REVIEW")
    print("=" * 70)
    print(f"File  : {file_path}")
    print(f"Model : {MODEL}")
    print("=" * 70)
    print()

    review = review_code(file_path)

    print(review)

    print()
    print("=" * 70)
    print("END AI CODE REVIEW")
    print("=" * 70)


if __name__ == "__main__":
    main()