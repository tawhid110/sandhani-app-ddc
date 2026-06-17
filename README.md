# 🩸 Sandhani Medical Record System

## Overview
This is an offline, standalone desktop application built with Python and Tkinter, specifically designed for a medical clinic environment. It streamlines the creation of patient blood screening and blood donation cross-matching reports for fast-paced, offline office setups (including legacy systems like Windows 7).

## Features
* **Automated Patient Memory:** Automatically saves and retrieves returning patient data using a local CSV database. Example: Searching for a patient like "Abu Sayed" by his phone number instantly auto-fills his past medical forms.
* **Two Dedicated Clinical Workflows:**
    * *Blood Screening:* Tracks 5 mandatory rapid tests (HBsAg, HCV, HIV, Malaria, VDRL) and Blood Glucose values. Hides unused tests to keep printed reports clean.
    * *Donation & Cross-Matching:* Tracks dual Donor/Recipient profiles, Blood Bag Numbers, precise ABO/Rh typing, and strict cross-match compatibility decisions.
* **Offline PDF Generation:** Uses the `ReportLab` engine to generate professional, printable medical PDF reports instantly directly to the desktop.
* **Data Validation Locks:** Built-in UI safety locks prevent clinical typing errors (e.g., blocking letters in the Age or Phone Number text boxes).

## Tech Stack
* **Language:** Python 3.12
* **GUI Interface:** Tkinter (Modern Clam Theme)
* **PDF Generation:** ReportLab
* **Deployment:** PyInstaller
