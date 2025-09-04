# Chapter 8: Chalice

We got to the last of our frameworks for developing and deploying Python applications in AWS Lambda. Chalice is Amazon's own framework for building serverless applications with Python.

> **Note**: This chapter appears to be incomplete in the source material. Chalice is AWS's official framework for building serverless applications with Python, offering a Flask-like experience with built-in AWS integrations.

For a comprehensive guide on Chalice, please refer to the [official AWS Chalice documentation](https://chalice.readthedocs.io/en/latest/).

Key features of Chalice include:
- Simple, Flask-like decorator syntax
- Automatic AWS resource provisioning
- Built-in support for AWS services
- Local development server
- Easy deployment commands

## Basic Example

Here's a simple Chalice application structure:

```python
from chalice import Chalice

app = Chalice(app_name='hello-world')

@app.route('/')
def index():
    return {'hello': 'world'}

@app.route('/hello/{name}')
def hello_name(name):
    return {'hello': name}
```

For detailed tutorials and advanced usage, consult the official Chalice documentation and AWS serverless application examples.

---

[← Previous: Chapter 7 - Deployment Tools II: Serverless Framework](07-deployment-tools-serverless.md) | [Next: Chapter 9 - Understanding Function Performance →](09-understanding-function-performance.md)