**UW HusKey Manager**

This project is a Dockerized password management application developed for the University of Washington cybersecurity program. It is designed to showcase secure storage practices, role-based access controls, and common web vulnerability testing.

**Core Components**

The repository is structured to support a full-stack environment using PHP 7.4 and a MySQL database. It utilizes Docker Compose to orchestrate the services, providing an isolated and reproducible setup for development and testing.

**Features**

* Vault Management: Separate vaults for different organizational roles such as Developers, HR, and Executives.
* Permission Logic: Granular control over user actions including viewing, editing, and ownership of vaults.
* Account Workflow: Support for user registration requests and administrative approval.
* Secure Logging: Integration with Monolog and Loggly for external event tracking.
* Security Testing: A suite of pytest scripts designed to test for vulnerabilities like SQL injection and path traversal.

**Setup Instructions**

Begin by cloning the repository to your local machine. Ensure that Docker and Docker Compose are running. Open a terminal in the project root and run the command: docker-compose up --build. Once the containers are healthy, the application will be accessible via your local web server.

**Directory Layout**

* certs/: Stores root certificates and private keys for the local environment.
* database/: Contains the SQL scripts used to initialize the database schema and sample roles.
* php/: Houses the Dockerfile and configuration for the backend PHP-FPM service.
* pytest/: Includes automated test cases for functional verification and security audits.
* webapp/: The primary application directory containing PHP files, assets, and dependencies.

**Security Disclaimer**

This application is intended for educational purposes. The initial database setup contains sample cleartext passwords that must be changed before any deployment. It is essential to manage sensitive credentials using environment variables and to verify that your .env file is excluded from version control.

**Credits**

Alex Lin
University of Washington
