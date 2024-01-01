Payment API v5 Documentation
This documentation provides a concise overview of the Payment-api version 5, For Learning.
---
### Advantages
Lowest Cost: Strives to minimize expenses.
Easy Data Visualization: Simplifies the process of visualizing data.
Free Data Viewing: No need to pay within the app for viewing data.
Enhanced Security: Ensures a more secure environment by your own.
### Disadvantage
Hard to Configure: The configuration process may pose challenges.
Using a few of personal Google Drive Storage.
### Prerequisites
iOS version 12 (2-1-2024)
iPhone, Ipad, All apple products that can using Get Content Of Properties
### Project Inception
Started this project two years ago during the early days of my college journey. The goal was to record and visualize income and expenses in daily routines.
---
## Story
### First Version
Created a website using Django Python framework.
Limited understanding during this early phase.
So I had try it with Flask Connected to Google Sheet API
### Second Version
Began learning Fast-API but had limited knowledge about APIs.
Continued learning and found Fast-API to work well.
Faced challenges in choosing a database.
### Third Version
Integrated Fast-API with SQLite And Start Wokring with CRUD, Models, Database and more.
Advantage: Fast
Disadvantages: included real-time monitoring challenges and the need for a personal VPS.
### Fourth Version
Utilized Google App Scripts directly connected to Google Sheet API.
Faced slowness in queries, possibly due to suboptimal code.
Benefits included using a single product for free under a 300 university license credit.
Disadvantage: Slow (Or maybe it's just because of mine for wrote bad at code)

### Fifth Version (Current)
Using Fast-API connected to Firebase.
Public API with ngrok, running on a Raspberry Pi 4.
Connected API to iOS through shortcuts.
Implemented HTTP methods in each input function.
Back-end utilizes the snapshot module from Firebase for real-time data reading.
Integration with Google App Scripts to update Google Sheet API.
Advantage: Fast
Disadvantage: Personal VPS Require


### Future
I had began learning about Machine Learning
But then i realise THE Payment prediction isn't accurate, it does need require same daily rountine for every second since you woke up for real-long time

## URL
### Google Sheet Template
https://docs.google.com/spreadsheets/d/1TNyTIq7hWbffzr9DAgGne_bcxVAaY4JOQgfSOigQKIw/edit?usp=sharing

### Firebase Path Example
/ Wallet
        / Wallet 1
        / Wallet 2
        / Wallet 3
        / Card 1
        / Card 2
        / Card 3
/ Transaction
            / (Obj) {action: 'income: expnese', types: income || expense types, amount, add_pn, amount, more}