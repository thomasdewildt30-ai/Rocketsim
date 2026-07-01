import matplotlib.pyplot as plt
import numpy as np
import time as ti
start = ti.time()

# Simulation setup
step = 0.01              # Timestep in seconds

# Rocket stats
mr = 40                 # Mass rocket in kg
mf = 80                 # Mass fuel in kg

k = 0.05                # Air friction coefficient

# Rocket engine stats
g0 = 9.81               # Referecne value engine
ISP = 500               # Engine efficincy value
Fstuw = 2500            # Initial rocket thrust in Newton

# Earth information
R = 6371000             # Radius earth
mass_Earth = 6*10**24   # Mass of the Earth
G = 6.7*10**-11         # Gravitational constant



pstate = [[0.1,1000],[0.2, 750],[0.3,500]]                                  # Parachuteparameters, in the form [new k, activation height]
stagestate = [[1500, 1600, 0.5* mr, True,0],[10000, 1300, 0.3*mr, True,1]]  # Stage parameters, in the form [activation height, new thrust, new rocket mass, switch,index]

# Setup
t = h = v = flm = Fres = 0
tl, hl, vl, al, gl, adl, flwl, fstuwl, effl, fresl,stagelist = ([] for _ in range(11))
x = True
mtot = mr+mf
axlist = [(0,0),(0,1),(0,2),(1,0),(1,1),(1,2),(2,0),(2,1),(2,2)]
titles = ["Height (km)","Velocity (m/s)","Acceleration (m/s²)","Gravity (m/s²)","Air Density (kg/m³)","Air Resistance (N)","Thrust (N)","Efficiency (%)","Net Force (N)"]
y_labels = ["Km", "m/s", "m/s²","m/s²", "kg/m³", "N","N","%", "N"]
xlines = [True,True,True,
          False,False,True,
          True,False,True]

def trap(ht, Fstuwt, mrt, ss, l):
    global h, Fstuw, mr
    if h > ht and ss:
        Fstuw = Fstuwt
        mr = mrt
        stagestate[l][3] = False
        stagelist.append(t)

        
def parachute(kp, hp):
    global k, h, v
    if v < 0 and h < hp:
        k = kp

while True:
    
    g =  G * mass_Earth/(R+h)**2
    ad = np.exp(-h / 8500)

    for p in pstate:
        parachute(*p)
    
    for stage in stagestate:
        trap(*stage)
    
       
    if mtot > mr:
        eff = 1 - (ad * 0.15)
        Fs = Fstuw * eff
        fflow = Fstuw/(g0*ISP)
        mf -= fflow * step
        mtot = mr + mf
        flm += step
    else:
        Fs = 0
        eff = 0
        fflow = 0
    if h >= 0:
        Fz = mtot * -g
        Fn = 0
    if h == 0 and Fres < 0:
        Fn = -Fz
    
    Flw = ad * -k * v * abs(v)
    Fres = Fz + Fs + Flw + Fn
    a = Fres / mtot
    v = v + a * step
    h = h + v * step
    h = max(h, 0)

    if v < 0 and h == 0:
        v = 0
    for list1,listv in zip([tl,hl,vl,al,gl,adl,flwl,fstuwl,effl,fresl],[t,h/1000,v,a,g,ad*1.225,abs(Flw),Fs,eff*100,Fres]):
        list1.append(listv)
    t += step
    
    # break functie
    l10h = 0
    if t > 5:
        for q in range(1, 11):
            l10h += hl[-q]
        if l10h < 0.0001: 
            break

# Graph drawing
# === Results ===
print(f"""Simulation time: {t:.1f} s
Max height: {max(hl):.2f} km
Max velocity: {max(vl):.1f} m/s
Max acceleration: {max(al):.1f} m/s²
Fuel burn time: {flm:.1f} s""")

fig, ax = plt.subplots(3, 3)

for (i,j), list2,name, y_label,xline in zip(axlist,[hl, vl, al, gl, adl, flwl, fstuwl, effl, fresl],titles,y_labels,xlines):
    ax[i,j].plot(tl,list2)
    ax[i,j].set_title(name)
    ax[i,j].set_ylabel(y_label)
    ax[i,j].grid(True)
    if xline:
        ax[i,j].axhline(0,color = "black")


ax[0,0].axvline(flm,linestyle=":",color="black")
ax[0,1].axvline(flm,linestyle=":",color="black")
for stage in stagelist:
    for (i, j) in [(0,0),(0,1),(0,2),(2,0),(1,2),(2,2)]:
        ax[i,j].axvline(stage, linestyle=":", color="red")
ax[2,2].axvline(flm,linestyle=":",color="black")

plt.tight_layout()
print(f"Runtime:{round(ti.time()-start,2)}")
plt.show()
