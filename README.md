# django-order-system
Asynchronous order processing system built with Django and Celery

Still in development...

## Project Overview

This project is an asynchronous order processing system built with Django and Celery. It demonstrates how to offload time-consuming tasks, such as payment processing, invoice generation, and email notifications, to background workers. The system ensures faster response times and better scalability by using Redis as a message broker.

## Key Features
### 🔄 Asynchronous Order Processing

When a customer places an order, the system queues the payment processing task in Celery.
The payment validation runs in the background, avoiding slow HTTP responses.

### 📄 Automated Invoice Generation

After a successful payment, the system creates a PDF invoice asynchronously using Celery.
The invoice is saved in the database and can be downloaded by the customer.

### 📧 Email Notifications

Once the order is completed, the system sends an email confirmation to the customer asynchronously via Celery.