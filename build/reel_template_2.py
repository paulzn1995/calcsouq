import sys, json, subprocess, os
from reel import *  # helpers (W,H,FPS,F,colours,ease,eb,seg,ctext,BG_D,endcard)
MC=json.load(open("mc.json"))

def lakh(x):
    return f"₹{x/1e5:.1f} lakh" if x<1e7 else f"₹{x/1e7:.2f} crore"
def bar(d,x,y,w,h,col): d.rounded_rectangle([x,y,x+w,y+h],18,fill=col)

def sipreel(i):
    t=i/FPS; im=BG_D.copy(); d=ImageDraw.Draw(im)
    if t<3.2:
        a=ease(seg(t,0,0.35)); ctext(d,520+60*(1-a),"₹10,000 a month",F("k",104),WHITE)
        b=ease(seg(t,0.2,0.55)); ctext(d,650+60*(1-b),"for 15 years.",F("k",104),WHITE)
        c=ease(seg(t,0.5,0.9)); ctext(d,800+60*(1-c),"What does it become?",F("k",76),GOLD)
        for k,(lab) in enumerate(["A   ₹18 lakh","B   ₹50 lakh","C   ₹87 lakh"]):
            s=eb(seg(t,1.0+k*0.25,1.5+k*0.25))
            if s>0:
                w=int(700*s); y=950+k*150
                d.rounded_rectangle([W/2-w/2,y,W/2+w/2,y+115],58,fill=(44,47,53),outline=(80,84,92),width=3)
                if s>0.7: ctext(d,y+58,lab,F("b",56),WHITE)
        if t>2.4: ctext(d,1440,"Guess first, then watch",F("s",44),MUTE)
    elif t<10.4:
        u=t-3.2; ctext(d,300,"Same ₹10,000. Three choices.",F("k",62),WHITE)
        rows=[("Just save it",1800000,(120,126,135),0.0),("Invest at 12%*",5045760,(120,170,240),1.6),("Raise it 10% every year*",8683849,GOLD,3.4)]
        for k,(lab,val,col,st) in enumerate(rows):
            p=ease(seg(u,st,st+1.5))
            if u<st: continue
            y=480+k*330
            d.text((110,y),lab,font=F("b",50),fill=WHITE)
            bar(d,110,y+80,int(860*val/8683849*p)+6,90,col)
            ctext(d,y+230,lakh(val*p),F("k",84),col if k else WHITE,x=W/2)
        if u>5.3:
            s=eb(seg(u,5.3,5.9)); w=int(780*s)
            d.rounded_rectangle([W/2-w/2,1500,W/2+w/2,1610],55,fill=GOLD)
            if s>0.7: ctext(d,1555,"Answer: C · ₹86.8 lakh",F("k",52),INK)
        if u>1: d.text((110,1680),"*Assumed 12% a year, compounded monthly. Not guaranteed.",font=F("r",30),fill=MUTE)
    else:
        endcard(d,(t-10.4)/2.6,"Free SIP calculator")
    return im

def mcreel(i):
    t=i/FPS; im=BG_D.copy(); d=ImageDraw.Draw(im)
    if t<2.6:
        a=ease(seg(t,0,0.35)); ctext(d,560+60*(1-a),"Same strategy.",F("k",112),WHITE)
        b=ease(seg(t,0.25,0.6)); ctext(d,710+60*(1-b),"1,000 traders.",F("k",112),GOLD)
        c=ease(seg(t,0.7,1.1)); ctext(d,880+40*(1-c),"45% win rate · 2:1 reward · 200 trades",F("s",44),WHITE)
        if t>1.4: ctext(d,1040,"Who ends up where?",F("b",64),MUTE)
    elif t<10.6:
        u=t-2.6; ctext(d,300,"Every line = one trader",F("k",64),WHITE)
        x0,x1,y0,y1=110,970,520,1300; lo,hi=8000,35000
        d.line([x0,y1,x1,y1],fill=(70,73,80),width=3)
        yb=y1-(10000-lo)/(hi-lo)*(y1-y0); d.line([x0,yb,x1,yb],fill=(90,94,100),width=2)
        pass
        p=ease(seg(u,0,3.6)); nn=max(2,int(200*p))
        for k,path in enumerate(MC["paths"]):
            col=(GREEN if k==1 else RED if k==0 else (120,126,135))
            wdt=6 if k<2 else 2
            pts=[(x0+(x1-x0)*j/200, y1-(path[j]-lo)/(hi-lo)*(y1-y0)) for j in range(0,nn+1,2)]
            if k>=2: d.line(pts,fill=col,width=wdt)
        for k in (1,0):
            path=MC["paths"][k]; pts=[(x0+(x1-x0)*j/200, y1-(path[j]-lo)/(hi-lo)*(y1-y0)) for j in range(0,nn+1,2)]
            d.line(pts,fill=(GREEN if k==1 else RED),width=7)
        d.rounded_rectangle([x0,yb+10,x0+250,yb+60],12,fill=(36,38,43)); d.text((x0+14,yb+16),"start 10,000",font=F("s",30),fill=WHITE)
        if u>3.8:
            s=ease(seg(u,3.8,4.4))
            ctext(d,1400,f"Best: {MC['hi']:,.0f}",F("k",70),GREEN)
            ctext(d,1490,f"Worst: {MC['lo']:,.0f}",F("k",70),RED)
        if u>5.4:
            s=eb(seg(u,5.4,6.0)); w=int(900*s)
            d.rounded_rectangle([W/2-w/2,1580,W/2+w/2,1690],55,fill=GOLD)
            if s>0.7: ctext(d,1635,"One trader lost 22 times in a row",F("k",46),INK)
        d.text((110,1730),"Monte Carlo simulation · education, not advice",font=F("r",30),fill=MUTE)
    else:
        endcard(d,(t-10.6)/2.4,"Strategy simulator")
    return im

def render(fn,name,secs):
    if len(sys.argv)>2:
        for s in map(float,sys.argv[2].split(",")): fn(int(s*FPS)).save(f"{name}-still-{s}.png")
        return
    p=subprocess.Popen(["ffmpeg","-y","-loglevel","error","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(FPS),"-i","-","-c:v","libx264","-preset","veryfast","-crf","20","-pix_fmt","yuv420p","-movflags","+faststart",f"{name}.tmp.mp4"],stdin=subprocess.PIPE)
    for i in range(secs*FPS): p.stdin.write(fn(i).tobytes())
    p.stdin.close(); assert p.wait()==0; os.replace(f"{name}.tmp.mp4",f"{name}.mp4")
if sys.argv[1]=="S": render(sipreel,"sip",13)
else: render(mcreel,"mc",13)
