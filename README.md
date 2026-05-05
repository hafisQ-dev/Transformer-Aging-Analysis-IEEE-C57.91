
# Transformer-Aging-Analysis-IEEE-C57.91
Transformer Aging Analysis according to IEEE C57.91 Standards

---

# Transformer Aging Analysis (IEEE C57.91)

This project provides a comprehensive thermal modeling and insulation life assessment tool for oil-immersed transformers, specifically focusing on the impact of **Electric Vehicle (EV) charging loads**. The analysis is built upon the international **IEEE C57.91** standards.

##  Project Goal
To simulate and quantify how dynamic loading conditions (Base Load + EV Charging) affect the **Hot-Spot Temperature** and the **Rate of Insulation Aging** in distribution transformers.

##  Methodology & Theoretical Background
The project implements the following academic frameworks:
*   **Thermal Modeling:** Calculation of Top-Oil and Hot-Spot temperatures using differential equations and exponential power-law relations (n=0.8, m=0.8).
*   **Arrhenius Theory:** Modeling the chemical degradation of cellulosic insulation as a function of temperature.
*   **Aging Acceleration Factor (FAA):** Quantifying the instantaneous aging rate relative to the 110°C reference point.
*   **Loss of Life (LoL):** Calculating the cumulative degradation of the transformer's life over a 24-hour cycle.

##  Technologies Used
*   **Python 3.x**
*   **Pandas & NumPy:** For time-series data manipulation and mathematical modeling.
*   **Matplotlib:** (Optional - if you added plots) For visualizing temperature and FAA trends.

##  Key Results
In the current simulation:
*   **Max Load Factor:** %95.84
*   **Peak Hot-Spot Temperature:** 114.74°C (Exceeding the 110°C threshold due to high ambient temperatures).
*   **Observation:** Even without exceeding %100 load, high ambient temperatures combined with EV peaks significantly accelerate the insulation aging.

##  How to Run
1. Clone the repository: `git clone [https://github.com/HafisQuliyev/Transformer-Aging-Analysis-IEEE.git](https://github.com/HafisQuliyev/Transformer-Aging-Analysis-IEEE.git)`
2. Install dependencies: `pip install pandas numpy`
3. Run the analysis: `python main.py`

##  Results and Visualizations
<img width="1217" height="1017" alt="Ekran görüntüsü 2026-05-04 232154" src="https://github.com/user-attachments/assets/3979dec3-42c3-4833-8825-575d4d52a338" />
