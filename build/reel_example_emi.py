import os
import sys, os, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reel_fx import *
DUR=14
def L(x): return f"₹{x/1e5:.1f} lakh"
def frame(i):
    t=i/FPS
    if t<3.2:
        im=scene_bg(t,"night",3); 
        kinetic(im,"₹10 lakh loan.",560,t,0.05,120,WHITE)
        kinetic(im,"What do you",680,t,0.45,80,GOLD); kinetic(im,"REALLY pay back?",790,t,0.65,80,GOLD)
        souq(im,W/2,1250,0.95,t,"thinking")
        speech(im,W/2+180,1010,"Guess first!",1.2,t,44)
        im=punch(im,t,0.05)
    elif t<8.2:
        u=t-3.2; im=scene_bg(t,"sky",5); d=ImageDraw.Draw(im)
        kinetic(im,"9% interest · 20 years",330,t,3.2,64,WHITE)
        # bars
        p1=ease(seg(u,0.3,1.4)); p2=ease(seg(u,1.6,3.0))
        base=1250; sc=620/2159342
        d.rounded_rectangle([180,base-1e6*sc*p1,460,base],30,fill=WHITE)
        d.rounded_rectangle([620,base-1159342*sc*p2,900,base],30,fill=RED)
        d.text((320,base+60),"Loan",font=F("b",48),fill=WHITE,anchor="mm"); d.text((760,base+60),"Interest",font=F("b",48),fill=WHITE,anchor="mm")
        if p1>0: d.text((320,base-1e6*sc*p1-60),L(count(0,1e6,t,3.5,4.6)),font=F("k",58),fill=WHITE,anchor="mm")
        if p2>0: d.text((760,base-1159342*sc*p2-60),L(count(0,1159342,t,4.8,6.2)),font=F("k",58),fill=GOLD,anchor="mm")
        coins_stack(d,120,1650,int(1+8*p2),46); coins_stack(d,960,1650,int(1+10*p2),46)
        souq(im,W/2,1620,0.55,t,"shocked" if u>3 else "thinking")
        im=shake(im,t,6.2,22)
        pill(im,W/2,520,"EMI ₹8,997 a month",t,3.6,GOLD,INK,52)
    elif t<11.2:
        u=t-8.2; im=scene_bg(t,"night",7); rays(im,W/2,820,t,GOLD,30)
        d=ImageDraw.Draw(im)
        kinetic(im,"You pay back",520,t,8.25,80,WHITE)
        v=count(1e6,2159342,t,8.4,9.6); d.text((W/2,700),L(v),font=F("k",150),fill=GOLD,anchor="mm")
        sparkles(im,W/2,700,t,9.6,4,16,320,GOLD)
        pill(im,W/2,900,"More than DOUBLE the loan",t,9.7,RED,WHITE,48)
        souq(im,W/2-230,1380,0.7,t,"wink",wave=True)
        speech(im,W/2+150,1160,"10 years? Interest ₹5.2 lakh",10.1,t,40)
    else:
        im=scene_bg(t,"night",9); endcard(im,t,11.25,"Free EMI calculator"); souq(im,W/2,1500,0.6,t,"happy",wave=True)
        confetti(im,t,11.3,5,60)
    return im
if len(sys.argv)>1:
    for s in map(float,sys.argv[1].split(",")): frame(int(s*FPS)).save(f"emi-{s}.png")
else:
    p=subprocess.Popen(["ffmpeg","-y","-loglevel","error","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(FPS),"-i","-","-c:v","libx264","-preset","veryfast","-crf","20","-pix_fmt","yuv420p","emi.tmp.mp4"],stdin=subprocess.PIPE)
    for i in range(DUR*FPS): p.stdin.write(frame(i).tobytes())
    p.stdin.close(); assert p.wait()==0; os.replace("emi.tmp.mp4","emi_v.mp4")
