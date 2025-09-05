# Serverless Web Apps with Python and AWS Lambda

## Building the Perfect Stack for Startups

> 📝 **Author's Note (2025)**: This book was originally written in 2019 but was never completed. While the core technologies and concepts covered (Python, Django, AWS Lambda, serverless architecture) remain valid and useful in many scenarios, the landscape has evolved significantly. 
>
> With advances in AI, containerization, and cloud platforms, today's recommendations for building scalable web applications might differ depending on your team's expertise, project requirements, and the current technology ecosystem. However, the fundamental principles and hands-on examples in this book still provide valuable learning opportunities.
>
> This book has been made publicly available in case it proves helpful to anyone interested in serverless development, Python web frameworks, or AWS Lambda. Feel free to use it as a learning resource, keeping in mind that some specific recommendations may no longer represent current best practices.

**Abstract:** Publishing a web application has evolved from having to purchase your own hardware a couple decades ago, to being able to create and destroy virtual servers in a matter of minutes by using cloud hosting services. In this book we'll go a step further and create web applications that can run on hundreds of servers without having to provision them in advance or manage the underlying infrastructure at all. We'll build highly scalable applications using Python and Django and deploy them worldwide, using Zappa, to AWS Lambda. Finally we'll build an entire serverless stack that grows (and shrinks!) as our demand changes.

## Table of Contents

- [**Preface**](00-preface.md)
  - [Who This Book Is For](00-preface.md#who-this-book-is-for)
  - [What This Book Is Not](00-preface.md#what-this-book-is-not)
  - [A Note to Windows Users](00-preface.md#a-note-to-windows-users)
  - [Online Resources](00-preface.md#online-resources)

- [**Chapter 1: Introduction**](01-introduction.md)
  - [A Brief History of Hosting Providers](01-introduction.md#a-brief-history-of-hosting-providers)
  - [Our Software Stack](01-introduction.md#our-software-stack)
  - [Chapter Guide](01-introduction.md#chapter-guide)
  - [Why The Perfect Stack](01-introduction.md#why-the-perfect-stack)
  - [What Is Serverless?](01-introduction.md#what-is-serverless)

- [**Chapter 2: Web Development Essentials**](02-web-development-essentials.md)
  - [Python](02-web-development-essentials.md#python)
  - [The PIP Package Manager](02-web-development-essentials.md#the-pip-package-manager)
  - [Django](02-web-development-essentials.md#django)

- [**Chapter 3: Environments**](03-environments.md)
  - [Virtual Environment (virtualenv)](03-environments.md#virtual-environment-virtualenv)
  - [Docker](03-environments.md#docker)

- [**Chapter 4: AWS Ecosystem**](04-aws-ecosystem.md)
  - [Billing and Free Tier (Disclaimer)](04-aws-ecosystem.md#billing-and-free-tier-disclaimer)
  - [Getting Started](04-aws-ecosystem.md#getting-started)
  - [Identity and Access Management (IAM)](04-aws-ecosystem.md#identity-and-access-management-iam)
  - [Simple Storage Service (S3)](04-aws-ecosystem.md#simple-storage-service-s3)
  - [CloudFront](04-aws-ecosystem.md#cloudfront)
  - [EC2 & RDS](04-aws-ecosystem.md#ec2--rds)
  - [Aurora Serverless](04-aws-ecosystem.md#aurora-serverless)
  - [SES](04-aws-ecosystem.md#ses)
  - [Understanding Pricing](04-aws-ecosystem.md#understanding-pricing)

- [**Chapter 5: Lambda Functions**](05-lambda-functions.md)
  - [Creating our first Lambda](05-lambda-functions.md#creating-our-first-lambda)
  - [Creating an Email Bot](05-lambda-functions.md#creating-an-email-bot)
  - [Running on Development](05-lambda-functions.md#running-on-development)
  - [Lambda Versioning](05-lambda-functions.md#lambda-versioning)
  - [Making our Lambda Public](05-lambda-functions.md#making-our-lambda-public)
  - [Execution Times](05-lambda-functions.md#execution-times)

- [**Chapter 6: Deployment Tools I: Zappa**](06-deployment-tools-zappa.md)
  - [Introducing Zappa](06-deployment-tools-zappa.md#introducing-zappa)
  - [Project setup](06-deployment-tools-zappa.md#project-setup)
  - [Setting up Zappa](06-deployment-tools-zappa.md#setting-up-zappa)
  - [Going live!](06-deployment-tools-zappa.md#going-live)
  - [Using HTTPS and a Custom Domain](06-deployment-tools-zappa.md#using-https-and-a-custom-domain)
  - [Connecting to a Database](06-deployment-tools-zappa.md#connecting-to-a-database)
  - [Database Security and VPC](06-deployment-tools-zappa.md#database-security-and-vpc)
  - [Serving Static Files](06-deployment-tools-zappa.md#serving-static-files)

- [**Chapter 7: Deployment Tools II: Serverless Framework**](07-deployment-tools-serverless.md)
  - [The Multi-* Framework](07-deployment-tools-serverless.md#multi-language-multi-platform)

- [**Chapter 8: Chalice**](08-chalice.md)

- [**Chapter 9: Understanding Function Performance**](09-understanding-function-performance.md)
  - [The HTTPS Request](09-understanding-function-performance.md#the-https-request)
  - [Benchmarking against EC2](09-understanding-function-performance.md#benchmarking-against-ec2)
  - [Lambda Execution Lifecycle](09-understanding-function-performance.md#lambda-execution-lifecycle)
  - [Framework Comparison](09-understanding-function-performance.md#framework-comparison)
  - [Digging Deeper with X-Ray](09-understanding-function-performance.md#digging-deeper-with-x-ray)
  - [Zappa's Slim Handler and Memory Usage](09-understanding-function-performance.md#zappas-slim-handler-and-memory-usage)

- [**Appendix A: Running Docker in Production**](appendix-a-docker-production.md)

---

*This book explores building scalable serverless applications using Python, Django, and AWS Lambda.*
