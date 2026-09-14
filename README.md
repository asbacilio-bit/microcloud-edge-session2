# MicroCloud-Edge — Business Resilience Simulator

Interactive simulator prepared for Session 2 of Management by Results.

## Purpose

The application simulates the resistance/resilience of the proposed business model under:

- External stress: demand decrease, competitor pressure, inflation and connectivity disruption.
- Internal stress: operating-cost increase, technical failures, productivity loss and support/maintenance increase.

It compares baseline vs. stressed:

- Revenue
- Costs
- Profit
- Profit margin
- Resilience score (0–100)

## Technology context

Selected ASPI technology: **Cloud and Edge Computing**.

The business model proposes an affordable Cloud-Edge digital service for MYPES. The first business application is inventory/sales management.

## Important modeling note

The simulator is a management model, not a technical validation of Cloud-Edge performance.

The "Connectivity impact reduction from Edge" parameter is an explicit assumption. It should later be validated against measurements from the physical Cloud-Edge prototype.

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy

Push `app.py` and `requirements.txt` to a GitHub repository and deploy the repository using Streamlit Community Cloud.

## Suggested repository name

`microcloud-edge-session2`

## Suggested presentation statement

> "We developed an interactive business resilience simulator to test our business model under internal and external stress. The model compares baseline and stressed financial performance and incorporates a Cloud-Edge resilience assumption related to connectivity disruption. This allows us to identify vulnerabilities before implementing the physical prototype."
