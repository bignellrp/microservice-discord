# Microservice Architecture for Discord

Here is an example of how you can implement a Discord bot using a microservices architecture with a REST API gateway to avoid duplicated responses.

In this project I have implemented single server bot and web. The problem with this design is it wouldnt scale very well to multiple discord servers with many users.

https://github.com/bignellrp/footyapp

In a separate project I implemented a slash command version running in Lambda but this lacked the functionality of monitoring for user messages and had a slow spin up time when calling the Lambda.

https://github.com/bignellrp/serverless-footyapp

In this project I converted the original footyapp project to run in AWS ECS but without changing the bots architecure it still cannot scale as multiple tasks running this service would reply to user messages multiple times, duplicating messages.

https://github.com/bignellrp/terraform-aws-ecs

This new Microservice Discord project investigates the option of converting to a microservice architecture by splitting the bot into frontend and worker nodes.

In a microservices architecture, different components of the application are split into smaller, independent services that communicate with each other through APIs. In this example, we'll have the following components:

Discord Bot Service: This service handles interactions with the Discord API and processes messages from users.
Message Processing Service: This service receives messages from the Discord Bot Service and processes them before sending a response back.
REST API Gateway: This is an entry point for external requests to the microservices.
To avoid duplicated responses, we'll implement a mechanism to prevent multiple responses for the same message.

Here's a basic outline of the architecture and how the flow works:

The user sends a message in Discord.
The Discord Bot Service receives the message and sends it to the Message Processing Service through the REST API Gateway.
The Message Processing Service checks if it has processed this message before (by storing message IDs or some unique identifier in a database or cache).
If the message has not been processed, the Message Processing Service processes it, stores the message ID, and sends the response back to the Discord Bot Service.
The Discord Bot Service sends the response back to the user.
To implement this architecture, you can use different frameworks and tools, but here's a sample code structure in Python:

Discord Bot Service (using discord.py library):

bot.py

Message Processing Service (using Flask or any other web framework):

worker.py

With these modifications, we've added a basic authentication mechanism using an API key in the Authorization header. If the provided API key doesn't match the expected value, the server will return a 401 Unauthorized error. Additionally, we've implemented error handling for both services to catch specific exceptions and return appropriate HTTP error codes.

Please note that this example is still simplified, and in a real-world application, you may want to use a more secure and robust authentication mechanism, such as OAuth2, especially if your services are exposed to the internet. Also, consider using proper logging to capture errors and events for monitoring and debugging purposes.

In AWS ECS (Elastic Container Service), you can control the scaling behavior of your services using ECS Service Auto Scaling policies. To prevent the Discord Bot Service from scaling, while allowing the Message Processing Service to scale, you'll need to create separate ECS services for each service, and configure the appropriate auto-scaling settings for each service.

Here's a step-by-step guide to achieving this:

Create two ECS Task Definitions:

One for the Discord Bot Service: This task definition should contain the necessary configuration for your Discord bot container.
Another for the Message Processing Service: This task definition should contain the configuration for the message processing service container.
Create two ECS Services:

Discord Bot Service: This service will use the task definition for the Discord Bot container. Configure it with the desired number of tasks (e.g., 1) and disable auto-scaling for this service.
Message Processing Service: This service will use the task definition for the Message Processing container. Configure it with the desired number of tasks (e.g., 2) and enable auto-scaling for this service.
Configure Auto Scaling for the Message Processing Service:

You can use either EC2 Auto Scaling or Amazon ECS Service Auto Scaling, depending on your setup.
Set up the scaling policies and target metrics based on your application's requirements. For example, you might scale based on CPU utilization, request count, or any other relevant metric.
Set Up Load Balancing:

If you want to load balance the Message Processing Service, you can use an Application Load Balancer (ALB) or Network Load Balancer (NLB) with a target group.
Configure the load balancer to route traffic to the containers running the Message Processing Service.
Ensure that your Message Processing Service registers with the target group so that the load balancer can distribute incoming traffic to the containers.
Set Up Service Discovery (Optional):

If you want to enable communication between the Discord Bot Service and the Message Processing Service, you can use service discovery mechanisms like Amazon Route 53 Auto Naming or AWS Cloud Map. This way, the Discord Bot Service can easily locate the Message Processing Service without hardcoding IP addresses or DNS names.
With this setup, the Discord Bot Service will have a fixed number of tasks (scaling disabled), ensuring that it doesn't scale up or down based on demand. On the other hand, the Message Processing Service will scale automatically based on the auto-scaling policies you've set up, and incoming traffic will be load-balanced across the scaled instances.

Keep in mind that this is a high-level overview, and the actual implementation may vary depending on your specific use case and infrastructure setup. Also, consider the cost implications of scaling the Message Processing Service and adjust the scaling policies accordingly to optimize costs while ensuring sufficient capacity to handle incoming messages.
