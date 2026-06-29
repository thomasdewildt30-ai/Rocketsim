import matplotlib.pyplot as plt
import numpy as np

step = 0.1
mr = 20
mf = 100
fflow = 1
Fstuw = 2500
it = 10000
k = 0.017

# Setup
t = 0
h = 0
v = 0
tl = []
hl = []
vl = []
al = []
gl = []
adl = []
flwl = []
fstuwl = []
effl = []
fresl = []

flw = 0
g = 9.81
R = 6371000
x = True

def trap(ht, Fstuwt, mrt, fflowt):
    global h, Fstuw, mr, fflow, x
    if h > ht and x:
        Fstuw = Fstuwt
        mr = mrt
        fflow = fflowt
        x = False
       
def parachute(kp, hp):
    global k, h, v
    if v < 0 and h < hp:
        k = kp
       
for i in range(it):
    Fn = 0
    R = 6371000
    g = 9.81 * (R / (R + h))**2
    ad = np.exp(-h / 8500)
    mtot = mr + mf
    eff = 1 - (ad * 0.5)
    
    parachute(0.05, 2500)
    parachute(0.1, 1500)
   
    Flw = ad * -k * v * abs(v)
    trap(1500, 1600, 12, 0.6)
    
    if h >= 0:
        Fz = mtot * -g
    if h == 0:
        Fn = -Fz
        
    if mtot > mr:
        Fs = Fstuw * eff
        mf -= fflow * step
    else:
        Fs = 0
        
    Fres = Fz + Fs + Flw + Fn
    a = Fres / mtot
    v = v + a * step
    h = h + v * step
    h = max(h, 0)
    if v < 0 and h == 0:
        v = 0
        
    t += step
    tl.append(t)
    hl.append(h / 1000)
    vl.append(v)
    al.append(a)
    gl.append(g)
    adl.append(ad * 1.225)
    flwl.append(Flw)
    fstuwl.append(Fs)
    effl.append(eff * 100)
    fresl.append(Fres)
    l10h = 0
    if t > 5:
        for q in range(10):
            l10h += hl[i-q]
        if l10h < 0.1: break

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

plt.tight_layout()
plt.show()
