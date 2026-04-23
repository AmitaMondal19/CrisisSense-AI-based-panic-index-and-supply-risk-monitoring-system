# CrisisSense: AI-Based Panic Index and Supply Risk Monitoring System

## Overview

CrisisSense is a system designed to analyze situations where public perception and real-world conditions may not match. It combines social media signals with commodity price data to understand whether a situation reflects an actual crisis or only perceived panic.

The system generates a Panic Index and provides a decision output to help identify whether the situation is stable, needs monitoring, or may lead to a shortage.

---

## Problem Statement

During crisis situations, information spreads quickly through social media. This often leads to panic behavior such as hoarding or sudden demand spikes. However, these reactions are not always based on real shortages.

CrisisSense addresses this issue by comparing:

- Social signals (public perception)
- Market data (real-world conditions)

This helps distinguish between real crises and exaggerated or misleading situations.

---

## Features

- Social signal analysis using text data
- Machine learning model for panic detection (Logistic Regression)
- Keyword-based detection for additional validation
- Commodity price trend analysis
- Panic Index calculation
- Decision system (Do Not Panic, Monitor, Possible Shortage)
- City-wise comparison
- Interactive dashboard using Streamlit
- Map visualization of panic levels

---

## System Workflow

1. Social media text is analyzed using:
   - Keyword matching
   - Machine learning model

2. Commodity price data is analyzed for:
   - Price changes
   - Volatility

3. These signals are combined to calculate a Panic Index

4. The system compares perception and reality

5. A decision is generated based on the Panic Index

---

## Technologies Used

- Python
- Streamlit
- Scikit-learn
- Pandas
- NumPy
- Matplotlib
- Folium

---

## Project Structure

```
CrisisSense/
│
├── app.py
├── model.pkl
├── vectorizer.pkl
├── data/
│   ├── panic_data.csv
│   ├── price_data.csv
│
├── notebook/
│   └── model_training.ipynb
│
├── requirements.txt
└── README.md
```

---

## Installation and Setup

1. Clone the repository

```
git clone https://github.com/AmitaMondal19/CrisisSense.git
cd CrisisSense
```

2. Install dependencies

```
pip install -r requirements.txt
```

3. Run the application

```
python -m streamlit run app.py
```

---

## Model Details

- Model: Logistic Regression  
- Input: Text data from social signals  
- Feature extraction: TF-IDF vectorization  
- Output: Probability of panic-related content  

The model is trained using a disaster-related text dataset. The training process is available in the notebook folder.

---

## Key Concept

The system is based on the idea of comparing perception and reality:

- Perception: Social media signals indicating panic  
- Reality: Market data such as prices and trends  

If both align, it may indicate a real crisis.  
If they differ, it may indicate exaggerated or false panic.

---

## Possible Applications

- Monitoring supply chain disruptions  
- Identifying misinformation-driven panic  
- Supporting decision-making during crises  
- Early warning systems for demand spikes  
- Disaster and emergency response analysis  

---

## Limitations

- Uses simulated or limited datasets  
- Does not use real-time APIs  
- Accuracy depends on quality of training data  
- Limited to selected commodities and cities  

---

## Future Improvements

- Integration with real-time social media APIs  
- Integration with live market data sources  
- Use of advanced NLP models  
- Automated alerts and notifications  
- Expansion to more regions and data sources  

---

## Conclusion

CrisisSense demonstrates how combining machine learning with real-world data can help analyze crisis situations more effectively. It provides a structured way to understand whether a situation is genuinely critical or driven by perception.

---

## Team

- Amita Mondal  
- Anurag Saha  
- Arnabi Nandy
- Debjit Nandi
- Sinchita Banerjee
