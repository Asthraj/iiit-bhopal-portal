# IIIT Bhopal Academic Portal

A Django-based academic portal built specifically for **Indian Institute of Information Technology, Bhopal**.

## Features

- **Role-based access** — Faculty (Teacher) and Student accounts
- **Branch support** — IT, CS, and ECE branches with tailored subject lists
- **Subjects** — Create and manage branch-specific subjects; enrol students
- **Assignments** — Faculty can post assignments with file attachments and due dates
- **Submissions** — Students submit work; faculty grade with marks and remarks
- **Notes** — Faculty upload study materials per subject
- **IIIT Bhopal branding** — Institute logo, navy/gold colour scheme, footer

## Branches & Subjects

The portal ships with a management command to seed 15 default subjects per branch:

```bash
python manage.py seed_subjects --teacher <faculty_username>
```

**CS:** Discrete Mathematics, Data Structures & Algorithms, Theory of Computation, Compiler Design, Computer Architecture, OS, DBMS, AI, Computer Networks, Algorithm Design, Distributed Systems, Computer Graphics, Machine Learning, NLP, Software Engineering

**IT:** Programming for Problem Solving, Data Structures, Web Technologies, DBMS, Computer Networks, OS, Software Engineering, Cloud Computing, IoT & Embedded Systems, Machine Learning, Cyber Security, Mobile App Development, Big Data Analytics, HCI, Information Security

**ECE:** Circuit Theory, Electronic Devices & Circuits, Signals & Systems, Digital Electronics, Analog Communication, Digital Communication, VLSI Design, Microprocessors & Interfacing, Wireless Communication, Embedded Systems, RF & Microwave Engineering, DSP, Control Systems, Optical Communication, Antenna & Wave Propagation

## Setup

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py seed_subjects --teacher <superuser_username>
python manage.py runserver
```

## Deployment

See `render.yaml` for Render.com deployment configuration.
