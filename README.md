# Attendance Management System

## Overview

This Attendance Management System is a comprehensive solution designed for HR and Admin departments to efficiently manage employee attendance, leaves, holidays, and related administrative tasks. It seamlessly integrates with Microsoft Dynamics NAV 2018 for employee master data and ZK attendance devices for capturing real-time attendance logs.

## Key Features

*   **Microsoft Dynamics NAV 2018 Integration:**
    *   Synchronizes employee data directly from Dynamics NAV 2018.
    *   Facilitates adding synced employees to ZK attendance devices.
*   **ZK Attendance Device Integration:**
    *   Connects with ZK biometric/card attendance devices.
    *   Retrieves raw attendance logs for processing.
*   **Shift Management:**
    *   Allows HR users to create, define, and manage various work shifts.
    *   Supports two shift types:
        *   **Continuous Shifts:** Rotate on a daily basis or change every day, following a defined pattern.
        *   **Non-Continuous Shifts:** Standard work shifts that typically rotate on a weekly basis, also adhering to a specified pattern.
    *   **Shift Patterns:** Each shift type includes patterns that define the work schedule. For instance, a pattern might consist of alternating "Work Day" and "Rest Day". The rotation of these patterns depends on the shift type (daily for continuous, weekly for non-continuous).
    *   Assign specific shifts to individual employees or groups.
*   **Attendance Data Processing & Reporting:**
    *   Fetches attendance data from connected ZK devices.
    *   Compiles raw punch data into an easily understandable and structured format.
    *   Generates attendance history reports, accurately reflecting work hours, late arrivals, early departures, and absences, taking shift patterns into account.
*   **Leave Management:**
    *   Enables creation and management of custom leave types (e.g., Annual Leave, Sick Leave, Casual Leave, Unpaid Leave).
    *   Allows active employees (or HR on their behalf) to apply for leaves.
    *   Automatically calculates employees' annual leave balances based on their employment date, accrued leave policies, and taken leaves.
*   **Holiday Management:**
    *   Provides a module to create and manage a list of company-wide public and optional holidays.
    *   Holidays are automatically considered in attendance compilation and leave calculations.
*   **Accurate Attendance History:**
    *   All approved leaves and declared holidays are integrated into the compiled attendance records to provide an accurate and complete history of an employee's presence and absence.
*   **Device Management:**
    *   Synchronize the system time of connected ZK attendance devices with the server time.
    *   Add new employees to devices or update existing employee information on devices.
    *   Option to retrieve raw, unprocessed attendance data directly from devices for auditing or troubleshooting.
*   **Approval Workflows:**
    *   Implemented approval system for leave requests submitted by employees.
    *   Approval mechanism for the creation or modification of holiday entries.
*   **Overtime Calculation (Under Development):**
    *   Includes logic for calculating employee overtime based on their attendance and shift schedules.
    *   **Note:** The feature to automatically add/update the calculated overtime and posting the balance to Microsoft Dynamics NAV 2018 is currently under development and not yet functional.

## Tech Stack

*   **Backend:** Django (Python)
*   **Frontend:** Django Templates with Tailwind CSS
*   **Database:** PostgreSQL

## Future Enhancements

*   **Complete Overtime Calculation & NAV Integration:** Finalize the development of the overtime calculation module and implement the functionality to update overtime balances in Microsoft Dynamics NAV 2018.
*   **Enhanced Reporting & Analytics:** Introduce more detailed reports, dashboards, and data visualization for attendance trends, leave patterns, etc.
*   **Employee Self-Service Portal:** Allow employees to view their attendance, apply for leaves, and check their leave balances directly.
*   **Notifications:** Implement email or in-app notifications for leave approvals, attendance discrepancies, etc.
