### UW HusKey Manager

This project is a containerized password management application developed as part of my cybersecurity coursework at the University of Washington. It serves as a practical demonstration of secure software development, role-based access control (RBAC), and defensive programming against common web vulnerabilities.

---

### Project Overview

The **HusKey Manager** is designed to simulate an organizational credential management system. It provides a structured environment to manage sensitive information across different departments while enforcing strict security boundaries.

* **Role-Based Access Control:** Implements a multi-tiered permission system (Owner, Editor, Viewer) to govern access to departmental vaults.
* **Security Auditing:** Features a dedicated testing suite to identify and mitigate critical vulnerabilities such as SQL Injection (SQLi) and Path Traversal.
* **Centralized Logging:** Integrated with Monolog and Loggly for secure, off-site event tracking and system monitoring.
* **Containerized Architecture:** Built using a microservices approach with PHP 7.4-FPM and MySQL, orchestrated via Docker for environment parity and isolation.

---

### Technical Architecture

The application is structured to decouple the presentation layer from the core business logic and database management:

| Component | Responsibility |
| :--- | :--- |
| **Backend** | PHP 7.4-FPM handling authentication logic and vault operations. |
| **Database** | MySQL instance managing RBAC tables and encrypted credential storage. |
| **Web Server** | Nginx configured for secure request routing and static asset serving. |
| **Testing** | Automated `pytest` suite for functional and security regression testing. |

---

### Security & Defensive Implementation

A primary focus of this project was the implementation of defensive security measures:

* **Environment Secret Management:** Sensitive configurations (like Loggly tokens) are managed via environment variables to prevent credential leakage in source control.
* **SQL Injection Prevention:** Core authentication and database interactions are designed to resist SQLi attacks through parameterized queries and input validation.
* **Automated Security Scans:** The included testing suite validates the efficacy of security patches against known exploit vectors, ensuring the integrity of the "Remediation" logic.
* **Access Logging:** All informational and error events are dispatched to a remote logging service, providing an audit trail that is resilient to local system compromise.

---

### Key Directory Structure

* `database/`: SQL schemas and initialization scripts for the RBAC framework.
* `php/`: Docker configurations for the backend environment.
* `pytest/`: Comprehensive security and functional test cases.
* `webapp/`: The core application logic, including vault management and authentication components.
