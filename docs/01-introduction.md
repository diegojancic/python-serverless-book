# Chapter 1: Introduction

> 📝 **Context and Current Relevance**: This chapter and the approaches described throughout this book were conceptualized in 2019. Since then, the development landscape has evolved considerably with the rise of AI-assisted development, improved containerization technologies, and new cloud-native patterns.
>
> While serverless architectures and the technologies presented (AWS Lambda, Python/Django, etc.) remain valuable tools in the developer's toolkit, the "perfect stack" for any given project today might look different based on factors like team expertise, AI tooling integration, modern containerization approaches, and specific use cases.
>
> This content remains useful for understanding serverless concepts and learning these foundational technologies, but consider current best practices and emerging patterns when making architectural decisions for new projects.

## A Brief History of Hosting Providers

A couple of decades ago, when the Internet was still not very popular, if you wanted to host a website, you would usually grab a computer and connect it to the Internet. It didn't take long until hosting providers started to appear.

A traditional hosting provider sometimes required an upfront payment to set up the server and put it online. Nowadays there's usually no upfront cost, but it still has some inconveniences. They usually sell shared servers where you upload the website code and they put it online, or dedicated servers. A dedicated server is, basically, a piece of hardware that they rent to you and you own during the term of the contract. If that hardware fails, you have to contact support and wait for it to be replaced. The advantage with dedicated servers is that you control the OS and you can install whatever you want, which is necessary to execute long-running processes. The problem we all have faced at some point is that if the server goes down, it takes a while for them to restore it. You can ideally have more than one server in case one goes down, but for that you have to rent another server and configure the database and web servers to be fault tolerant, which is not always a simple task.

In the mid-2000s, as virtualization software and processors got cheaper and more efficient, the Cloud was born. The cloud is just a name for a set of systems running virtualized over real hardware. The great advantage with the cloud is that if you need to buy a new server, you just need a few clicks and the server is online in a matter of minutes. Even more, if you need 10 servers, you just do a few more clicks. The beauty of the cloud is that if you decide to turn them off, you can just do so and pay only for the time those servers were running. Because everything was virtualized, no real hardware was purchased, and after you turned off the computers, everything is gone.

The Cloud server providers go even further with this—you can now create and destroy in a matter of seconds hard drives with arbitrary capacities (not just 100GB, 500GB, 1TB, etc.), GPUs, or entire networks. This is great for when you don't have a stable demand of users 24x7, which is usually the case. When people go to sleep at night, you can turn off 90% of your servers and save money; during peak hours you can launch tens or even hundreds of servers to provide the best user experience. With such a setup you save money and provide a great user experience at the same time. Those are the reasons why people fell in love with the Cloud.

Even when the Cloud has important advantages over traditional hosting providers, there are still huge challenges IT admins and developers have to face. Maintaining a server is not an easy task. For example, installing the security updates the OS provides sometimes requires restarting the server or at least some of the services running. That creates some downtime and can produce a huge problem if the installation fails. Also, developing an application to work on a web farm (i.e., many, many servers) is not easy: one server can end up reading stale data because a cache is outdated, or multiple servers might attempt to save conflicting data at the same time. Some of these problems still remain and will probably always be a problem to take into account. We, as developers, can follow some practices to reduce those problems as much as possible.

Aiming to solve some of those problems, a few years ago a new movement started, called *serverless computing*. Serverless doesn't mean that there are actually no servers; instead, it means that the servers are actually hidden from the developer's point of view. A serverless infrastructure executes the code on demand, and you only pay for the exact time that code took to execute. When there are no users connected, you pay nothing.

What's even more interesting is that the provider handles the allocation of resources automatically, so if all of a sudden there's a peak of a thousand users, you are covered. That creates a much more dynamic platform than traditional cloud computing servers. Note that Serverless is part of the Cloud computing idea, but it's reduced to the smallest possible piece.

The challenge with the serverless model used to be that it required programming the web app in a very specific style or required specific libraries which tied you up to a specific provider. This is no longer the case, and we'll explore the options as we dive into each of the technologies.

## Our Software Stack

As we go on, our stack will consist of the following technologies:

### Linux

Linux will be the base of our software stack as it's the most used OS for servers. However, we didn't pick it because it's the most used operating system; instead, we are going to be using some tools and services that already run on Linux, so we need to build from there. It's entirely possible to develop on Mac or Windows, but our code will ultimately run on Linux.

### AWS Lambda

AWS Lambda is the next thing, and this is the first thing we will really care about. AWS Lambda is the serverless provider and runs on a custom version of Linux. We will deploy our code to be run on top of it, although during development we will explore other options both for testing and for production.

### Python

This is one of the most popular languages nowadays. It was created in 1991 and is used extensively for academic research, small and big companies. Google officially supports Python in many of its libraries and services, and some of them, such as TensorFlow, are built exclusively for Python. Because of its wide use in the academic community, Python is incredibly useful for a wide range of applications; some of the most complex algorithms are implemented in this language, making it a very good option for developing Machine Learning, computer vision, or any kind of first-rate applications.

### Django/Flask

Django is the last piece in our stack. Django is a web framework for Python. It provides many of the most common tools we need when building a web application. It's a very fast alternative for building quick prototypes and has a huge community supporting it. It's not just for prototyping though; it can be used in production environments with no problem. There are other perfectly valid alternatives, such as Flask or Tornado, but since they require more work to be set up initially, we are going to use them only in a few examples.

## Chapter Guide

> **Note:** Chapters are building blocks (chapters are pretty independent)

In the second chapter, we are going to introduce the basic building blocks we need to create our application. We are going to learn to use the tools we need to have the website running on our development computer. That includes the basic language syntax, the package manager (PIP), Django, and some basic libraries for the client side.

In the third chapter, we are going to tackle the first problem: the management of libraries, versions, and dependencies. There are two options to explore there, and we are going to explore both. This is a very important step not only to solve the problems with versioning and dependencies, but also to reduce problems later when deploying our code to the cloud.

The next step in our journey is to dive into the AWS ecosystem. AWS is Amazon's cloud provider, and it has a plethora of options. When starting with it, it's necessary to understand how users, permissions, storage, and services work. We are also going to explore some optional, but very useful, services that will allow our applications to run faster and smoother.

Once we have explored the basics of AWS, in chapter five we'll introduce one of the newest services from Amazon and also one of the core concepts of this book: Lambda. You can think of Lambda as our hosting provider. This is what ultimately will allow us to go serverless a few chapters later.

When we have Lambda set up, we are in conditions to build our full application in chapter six. We are going to do it by hand at first so we can explore in depth how the entire process works, from the client in the browser to the core running in the server. This is not only a perfectly valid way to build a web application, but also will help understand what role each component plays.

Chapter seven is an incredible step forward. Using a small tool called Zappa, we will publish an entire website to a serverless environment. This is just a simple step but that allows us to develop and deploy our code in a completely new way. There's going to be a before and after this chapter—the big jump is going to happen here, and it's where everything is going to make sense.

As a final step, in chapter eight, we are going to introduce database connections. We will explore the options we have for the problems or side effects that serverless comes with. We are going to connect to a database and a cache service to store information and session information. This will be the last important step we will take in this journey.

At the end, we will recap and try to put everything together. There's a lot of work ahead in the next chapters. I doubt you will want to go back after going serverless, and I hope you find it fascinating the same way I do.

Before we dive into each technology, let's first go through the basic foundations behind why we picked them in the first place.

## Why The Perfect Stack

Perfect is just a saying really; no stack is perfect. However, this stack is near perfect for certain scenarios. Let's start mentioning other cases where other technologies might be a better choice. If a developer or a team of developers have good experience in another technology that would do the job fine and there's no reason to move to a different technology, then that's probably the way to go. All new technologies have some learning curve that cannot be avoided, and that means a lot of time is spent on the learning phase, which translates directly to higher costs, at least in the short term.

The second case where this stack is not the best is if you are developing anything that is not a web application publicly accessible. If you are required to host a web application in a private network, in a specific geographical location, or develop something that's not a web application such as a mobile app or a desktop app, then this software stack just will not work. Also, some web applications with some very specific requirements might not be able to work well enough or just not work at all in AWS Lambda.

That being said, there are many sites that can be developed this way. Online utilities, CRMs, private portals, and so on. For startups or small businesses, the advantage is even larger because of the limited budget and resources they might have.

These are the main advantages:

**Cost:** Keeping costs low is always important. It is possible to run a service entirely free for the first year and even keep the costs very low after that. Calculating the cost is rather complicated and depends on a lot of factors. We will dedicate a few pages exclusively to this later, but it's enough for now to say that it is inexpensive compared to other similar solutions.

**Mature:** When developing a new product or service, it's very important to think long-term. By using well-known technologies (e.g., Python and Django) and very large service providers (e.g., Amazon AWS), we can make sure we will not be forced to migrate to a different technology soon. The main technologies described are very well supported, and that's one of the key arguments we used to pick this stack.

**Quick Prototyping:** Minimizing the time-to-market of a product can be the difference between success and failure. The frameworks we will start using are very simple and flexible. This allows us to create a minimum viable product, or MVP, very quickly.

**Scalability and Reliability:** As the service starts being used, keeping it up and running starts to cost more and more resources. Setting up a failover cluster for a web server or a database server can be really complicated, and scaling on demand requires a lot of configuration. Fortunately, the serverless infrastructure takes care of this issue seamlessly. The less time we spend on setting up servers and configuring backup procedures, the more time we will have to take care of everything else.

**No Lock-In:** Another aspect to take into account is that we do not want to be dependent on a service that might become too expensive or go out of business in the future for some reason. We will be using AWS Lambda, so we will be locked into this particular provider in a sense. However, because of the tools we will be using, it's fairly easy to migrate to another provider and even stop using a serverless architecture and deploy our code on a traditional server.

## What Is Serverless?

Serverless was mentioned a few times already, but it is necessary to make clear what this new thing is exactly. As explained before, serverless is a term that is used to mean that there are no servers to manage from a user's point of view. However, the servers are running there, and we only need to deploy our code.

There are several providers, the main ones being Amazon AWS Lambda, Google Cloud Functions, and Microsoft Azure Functions. Once an event triggers a function in those services, the code gets executed and a result is returned. All of those providers charge us for only the time it took their services to run our code, rounded up to the nearest 100ms.

For example, if we want to do a simple function that returns a *"Hello World"*, that function should execute in under 100ms and we pay only something around 0.00002 cents of a dollar for that. We would need to execute that function 100 thousand times to pay $0.02 or 2 cents.

The serverless providers usually allow more than one language to be used to run the code. Azure currently allows NodeJS, C#, F#, Python, PHP, Bash, Batch, and PowerShell. Amazon AWS supports NodeJS, Java, C#, and Python. Google Cloud only supports NodeJS. Depending on the language, some scripts will run faster and consume less memory than others. Also, there are other differences between those providers to take into account, such as the deployment options, the maximum execution time, the available triggers, and so on.

In our case, we will be using AWS to run our examples. However, it is possible to use other providers, given the limitations they might have.

We will go back to this topic in a few chapters. In the next chapter, we will start building our web application and running it locally. Once we have everything running locally and have understood some basic concepts, we will be ready to deploy it serverless.

---

[← Previous: Preface](00-preface.md) | [Next: Chapter 2 - Web Development Essentials →](02-web-development-essentials.md)