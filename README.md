# Tally Backup System

Docker-based Windows and TallyPrime environment with an Ubuntu-side backup service.

## Overview

This project runs Windows 11 with TallyPrime inside a Docker container on an Ubuntu server.

TallyPrime generates its normal database backups into a shared directory. The shared directory is mapped between the Windows container and the Ubuntu host.

A separate backup container runs cron jobs and Python scripts to preserve Tally backup data on Ubuntu.

## Architecture

```text
                         Ubuntu Server
                              |
                       Docker Compose
                              |
              +---------------+---------------+
              |                               |
              v                               v
       Windows Container              Tally Backup Container
              |                               |
          Windows 11                         |
              |                               |
          TallyPrime                         |
              |                               |
       Tally creates backup                  |
              |                               |
              v                               |
    shared/Tally_Backups <-------------------+
              |
              v
       Ubuntu Host Storage
       backups/tally/
       ├── 15min/
       └── daily/
