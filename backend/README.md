# Cloudmeet Backend

## Overview

The Cloudmeet backend provides a robust serverless architecture built on AWS Lambda functions to handle core meeting management operations. This component serves as the primary data processing layer, managing meeting operations, automated summarization, and notification systems while integrating seamlessly with MongoDB for data persistence.

## Architecture

The backend is structured as a collection of AWS Lambda functions, each designed for specific business operations:

### Lambda Functions

- **`create_meeting.py`**: Handles the creation and scheduling of new meetings with comprehensive validation and data storage
- **`generate_summary.py`**: Processes meeting notes through advanced language models to generate intelligent, actionable summaries
- **`send_reminder.py`**: Manages automated notification systems to send timely reminders to meeting participants

### Core Services

- **`email_service.py`**: Provides email functionality for notifications and communications
- **`llm_service.py`**: Interfaces with large language models for AI-powered content processing and summarization
- **`mongo_service.py`**: Handles all database operations and data management with MongoDB

## Key Features

- **Serverless Architecture**: Scalable AWS Lambda functions for optimal performance and cost efficiency
- **AI-Powered Processing**: Integration with advanced language models for intelligent content analysis
- **Automated Workflows**: Background processing for reminders and notifications
- **Data Integrity**: Robust database operations with comprehensive error handling
- **RESTful API Design**: Clean and consistent API endpoints for frontend integration

## Deployment

The backend includes automated deployment scripts (`deploy.sh`) for seamless AWS infrastructure provisioning and function updates.

## Testing

Comprehensive test suite included to ensure reliability and maintainability of all backend operations.
