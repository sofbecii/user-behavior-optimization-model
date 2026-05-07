# User Behavior & Product Attribute Optimization Model

## 📌 Project Overview
This project applies a deterministic optimization model (Linear Programming) to uncover the implicit weights users assign to product attributes. By analyzing a dataset of 515 users, the model identifies the critical discrepancies between **stated preferences** (what users say they want) and **revealed behaviors** (what actually drives their overall satisfaction).

## 🎯 Business Impact & Strategic Insights
* **Uncovered Heuristics:** Demonstrated that users simplify decision-making by focusing on a few dominant attributes, with more than half of the features falling to the minimum bounded weight (3%).
* **Demographic Segmentation:** Segmented data to reveal distinct user profiles, translating complex mathematical outputs into targeted product design recommendations.
* **Data-Driven Decision Making:** Proved that investing heavily in visually appealing elements (Animation & Sound) yields higher overall satisfaction than investing in cognitive attributes (Knowledge Improvement), contradicting users' explicit survey responses.

## 🛠️ Tools & Technologies Used
* **Python (Pandas):** Data cleaning, preprocessing, and exploratory data analysis (EDA).
* **GAMS:** Formulation and execution of the Linear Programming optimization models.
* **Mathematics:** Deterministic Optimization, Linear Programming, Statistical Analysis.

## 📂 Repository Structure
* `/data`: Cleaned dataset of 515 user surveys.
* `/scripts`: Python scripts for data manipulation and preparation.
* `/models`: GAMS (`.gms`) files containing the objective functions and constraints for the total sample and segmented demographics.

## 🚀 Methodology
The model minimizes the absolute deviation between a user's declared global rating and the reconstructed rating (a linear combination of 13 evaluated attributes). The objective function is constrained by lower (3%) and upper (50%) bounds to avoid degenerate solutions and capture realistic user heuristics.
