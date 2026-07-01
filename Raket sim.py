import matplotlib.pyplot as plt
import numpy as np
import time as ti
start = ti.time()

# Simulation setup
step = 0.1              # Timestep in seconds

# Rocket stats
mr = 40                 # Mass rocket in kg
mf = 80                 # Mass fuel in kg
k = 0.05                # Air friction coefficient

# Rocket engine stats
g0 = 9.81               # Referecne value engine
ISP = 250               # Engine efficincy value
Fstuw = 2500            # Initial rocket thrust in Newton

# Earth information
R = 6371000             # Radius earth
mass_Earth = 6*10**24   # Mass of the Earth
G = 6.7*10**-11         # Gravitational constant



pstate = [[0.1,1000],[0.2, 750],[0.3,500]] # Parachuteparameters, in the form [new k, activation height]
stagestate = [[1500, 1600, 0.5* mr, True,0],[10000, 1300, 0.3*mr, True,1]] # Stage parameters, in the form [activation height, new thrust, new rocket mass, switch,index]

# Setup
t = h = v = flm = Fres = 0

tl, hl, vl, al, gl, adl, flwl, fstuwl, effl, fresl = ([] for _ in range(10))

x = True

mtot = mr+mf

def trap(ht, Fstuwt, mrt, ss, l):
    global h, Fstuw, mr
    if h > ht and ss:
        Fstuw = Fstuwt
        mr = mrt
        stagestate[l][4] = False
        
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
fig, ax = plt.subplots(3, 3)
ax[0,0].plot(tl, hl)
ax[0,1].plot(tl, vl)
ax[0,2].plot(tl, fstuwl)
ax[1,0].plot(tl, al)
ax[1,1].plot(tl, gl)
ax[1,2].plot(tl, effl)
ax[2,0].plot(tl, adl)
ax[2,1].plot(tl, flwl)
ax[2,2].plot(tl, fresl)

ax[0,0].set_title("Height (km)")
ax[0,1].set_title("Velocity (m/s)")
ax[0,2].set_title("Thrust (N)")
ax[1,0].set_title("Acceleration (m/s²)")
ax[1,1].set_title("Gravity (m/s²)")
ax[1,2].set_title("Efficiency (%)")
ax[2,0].set_title("Air Density (kg/m³)")
ax[2,1].set_title("Air Resistance (N)")
ax[2,2].set_title("Net Force (N)")

ax[0,0].set_ylabel("km")
ax[0,1].set_ylabel("m/s")
ax[0,2].set_ylabel("N")
ax[1,0].set_ylabel("m/s²")
ax[1,1].set_ylabel("m/s²")
ax[2,0].set_ylabel("kg/m³")
ax[2,1].set_ylabel("N")
ax[2,2].set_ylabel("N")

ax[0,0].grid(True)
ax[0,1].grid(True)
ax[0,2].grid(True)
ax[1,0].grid(True)
ax[1,1].grid(True)
ax[1,2].grid(True)
ax[2,0].grid(True)
ax[2,1].grid(True)
ax[2,2].grid(True)

ax[0,0].axhline(0,color="black")
ax[0,1].axhline(0,color="black")
ax[0,2].axhline(0,color="black")
ax[1,0].axhline(0,color="black")
ax[2,0].axhline(0,color="black")
ax[2,1].axhline(0,color="black")
ax[2,2].axhline(0,color="black")

ax[0,0].axvline(flm,linestyle=":",color="black")
ax[0,1].axvline(flm,linestyle=":",color="black")
ax[2,2].axvline(flm,linestyle=":",color="black")

plt.tight_layout()
print(ti.time()-start)
plt.show()
