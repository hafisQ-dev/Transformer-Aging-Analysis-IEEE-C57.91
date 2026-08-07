import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#TIME AND PARAMETER INITIALIZATION 
time_index = pd.date_range(start="2026-04-30 00:00", periods=96, freq="15min")
S_nom = 100  # Nominal Capacity (kW) 
x = np.linspace(0, 2*np.pi, 96)

# Ambient Temperature 
amb_temp_avg = 25 + 10 * np.sin(x - np.pi/2) 


noise = np.random.normal(0, 2, 96)   # Random Noise
base_load_trend = 60 + 15 * np.sin(x - np.pi/1.5)
base_load = base_load_trend + noise

#EV CHARGING SCENARIOS 
# Uncontrolled Charging
EV_load_uncontrolled = np.zeros(96)
EV_load_uncontrolled[72:96] = np.random.normal(50, 5, 24)  #starts at peak hours (18:00)

# Smart Charging / Akıllı Şarj
EV_load_smart = np.zeros(96)
EV_load_smart[0:40] = np.random.normal(30, 5, 40)  #off-peak hours

#DYNAMIC THERMAL MODEL (IEEE C57.91)
def thermal_metrics(ev_load):
    to = 3.0           # Oil Time Constant (hours) 
    K = (base_load + ev_load) / S_nom # Loading Factor 
    
    # Standard Constants 
    dt_teta_to = 55    # Rated Top-Oil Rise (K) 
    dt_teta_hs = 80    # Rated Hot-Spot Rise (K)
    n, m = 0.8, 0.8    # Exponential Constants 
    gradient = dt_teta_hs - dt_teta_to # Winding-to-Oil Gradient 

    top_oil_temp = np.zeros(96)
    hot_spot_temp = np.zeros(96)
    top_oil_temp[0] = amb_temp_avg[0] # Initial condition 
    dt = 0.25 # Time step (15 min) 

    # Differential Equation for Dynamic Temperature 
     #AI was used for this step
    for i in range(1, 96):
        # Steady-state target 
        target_to = amb_temp_avg[i] + dt_teta_to * (K[i]**2)**n
        
        # Euler Method for Thermal Inertia
        d_to = (target_to - top_oil_temp[i-1]) * (dt / to)
        top_oil_temp[i] = top_oil_temp[i-1] + d_to
    
        # Calculation of Hot-Spot Temperature 
        hot_spot_temp[i] = top_oil_temp[i] + gradient * (K[i]**2)**m
    
    # Aging Acceleration Factor (FAA) 
    faa = np.exp(15000/383 - 15000/(hot_spot_temp + 273))
    return faa, hot_spot_temp

# CALCULATIONS AND ANALYSIS 
faa_uncontrolled, hs_uncontrolled = thermal_metrics(EV_load_uncontrolled)
L_uncontrolled = faa_uncontrolled * 0.25 # Loss of Life in hours

faa_smart, hs_smart = thermal_metrics(EV_load_smart)
L_smart = faa_smart * 0.25

# Console Outputs 
print(f"{'--- SMART CHARGING SCENARIO ---':^40}")
print(f"Daily Loss of Life / Günlük Ömür Kaybı: {L_smart.sum():.2f} hours")
print(f"Max Hot-Spot Temp / Maks. Sıcak Nokta: {hs_smart.max():.2f} °C\n")

print(f"{'--- UNCONTROLLED SCENARIO ---':^40}")
print(f"Daily Loss of Life / Günlük Ömür Kaybı: {L_uncontrolled.sum():.2f} hours")
print(f"Max Hot-Spot Temp / Maks. Sıcak Nokta: {hs_uncontrolled.max():.2f} °C")

#VISUALIZATION 
plt.style.use('ggplot')
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12,8), sharex=True)

# Graph 1: Load Profiles 
ax1.plot(time_index, base_load, label='Sadece Baz Yük Altında', color='gray', linestyle='--', alpha=0.6)
ax1.plot(time_index, base_load + EV_load_uncontrolled, label='Kontrolsüz Şarj', color='tab:red', linewidth=2)
ax1.plot(time_index, base_load + EV_load_smart, label='Akıllı Şarj', color='tab:green', linewidth=2)
ax1.axhline(S_nom, color='black', linestyle=':', label='Nominal Kapasite (100kW)')
ax1.set_title('Trafo Yüklenme Profilleri Karşılaştırması', fontsize=12)
ax1.set_ylabel('Güç (kW)')
ax1.legend(loc='upper left', fontsize=7)

# Graph 2: Hot-Spot Temperature 
ax2.plot(time_index, hs_uncontrolled, label='Kontrolsüz Yüklenme için Hot-Spot Temp', color='tab:red', linewidth=2)
ax2.plot(time_index, hs_smart, label='Akıllı Şarj için  Hot-Spot Temp', color='tab:green', linewidth=2)
ax2.axhline(y=110, color='blue', linestyle=':', label='IEEE C57.91 Kritik Eşik (110°C)')
ax2.set_title('Hot-SpotSıcaklığı Karşılaştırma', fontsize=12)
ax2.set_ylabel('Sıcaklık (°C)')
ax2.legend(loc='upper left', fontsize=7)

# Graph 3: Aging Acceleration Factor (FAA)
ax3.fill_between(time_index, faa_uncontrolled, color='tab:red', alpha=0.2, label='Kontrolsüz Şarj Ömür Kaybı')
ax3.fill_between(time_index, faa_smart, color='tab:green', alpha=0.2, label='Akıllı Şarj Ömür Kaybı')
ax3.plot(time_index, faa_uncontrolled, color='tab:red', linewidth=1.5)
ax3.plot(time_index, faa_smart, color='tab:green', linewidth=1.5)
ax3.set_title('FAA & Loss of Life Alanı', fontsize=12)
ax3.set_ylabel('FAA')
ax3.set_xlabel('Zaman (24saat)')
ax3.legend(loc='upper left', fontsize=7)

plt.tight_layout()
plt.show()


