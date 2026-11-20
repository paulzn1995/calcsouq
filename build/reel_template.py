import sys, subprocess, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter
W,H,FPS=1080,1920,30
I="/usr/share/fonts/opentype/inter/"
def F(w,s): return ImageFont.truetype(I+{"k":"Inter-Black","b":"Inter-Bold","s":"Inter-SemiBold","r":"Inter-Regular"}[w]+".otf",s)
INK=(21,23,26); GOLD=(245,195,0); OFF=(246,246,244); WHITE=(255,255,255); MUTE=(160,165,172); RED=(235,87,87); GREEN=(46,184,114)
def ease(t): t=max(0,min(1,t)); return 1-(1-t)**3
def eb(t): t=max(0,min(1,t)); c=1.7; return 1+(c+1)*(t-1)**3+c*(t-1)**2
def seg(t,a,b): return max(0,min(1,(t-a)/(b-a)))
def ctext(d,y,txt,font,fill,x=W/2): d.text((x,y),txt,font=font,fill=fill,anchor="mm")
def bg(dark=True):
    im=Image.new("RGB",(W,H),INK if dark else OFF); d=ImageDraw.Draw(im)
    # soft gold glow
    g=Image.new("L",(W,H),0); gd=ImageDraw.Draw(g); gd.ellipse([-300,-200,900,700],fill=70 if dark else 50); g=g.filter(ImageFilter.GaussianBlur(160))
    im.paste(Image.new("RGB",(W,H),GOLD),(0,0),g); return im
BG_D=bg(True)
def endcard(d,t,title):
    a=ease(seg(t,0,0.5))
    ctext(d,760-60*(1-a),title,F("k",88),GOLD)
    ctext(d,870,"Free · no sign-up · private",F("s",44),WHITE)
    s=eb(seg(t,0.25,0.8)); w=int(720*s); 
    if w>20: d.rounded_rectangle([W/2-w/2,1000,W/2+w/2,1130],65,fill=GOLD)
    if s>0.6: ctext(d,1065,"calcsouq.com",F("k",62),INK)
    if t>0.6: ctext(d,1200,"Link in bio ↗",F("b",46),WHITE)
def phone(d,x,y,w,h):
    d.rounded_rectangle([x,y,x+w,y+h],60,fill=(36,38,43),outline=(70,73,80),width=6)
    d.rounded_rectangle([x+24,y+24,x+w-24,y+h-24],40,fill=OFF)
def person(d,cx,cy,s,col=(120,126,135)):
    d.ellipse([cx-60*s,cy-150*s,cx+60*s,cy-30*s],fill=col)
    d.rounded_rectangle([cx-120*s,cy,cx+120*s,cy+170*s],int(90*s),fill=col)

def reelA(i):
    t=i/FPS; im=BG_D.copy(); d=ImageDraw.Draw(im)
    if t<2.2:
        a=ease(seg(t,0,0.35)); ctext(d,640+80*(1-a),"Photo",F("k",150),WHITE)
        b=ease(seg(t,0.15,0.5)); ctext(d,800+80*(1-b),"rejected?",F("k",150),GOLD)
        c=eb(seg(t,0.55,1.0))
        if c>0:
            sh=int(10*math.sin(t*40)) if 1.0<t<1.5 else 0
            w=int(820*c); d.rounded_rectangle([W/2-w/2+sh,980,W/2+w/2+sh,1110],65,fill=RED)
            if c>0.7: ctext(d,1045,"“File must be under 30 KB”",F("b",46),WHITE,W/2+sh)
    elif t<7.6:
        u=t-2.2; ctext(d,330,"Fix it in 10 seconds",F("k",70),WHITE)
        phone(d,190,430,700,1060)
        p=ease(seg(u,0.3,3.6))
        # photo card shrinking
        cw=int(520-300*p); ch=int(cw*4/3); cx,cy=W/2,860
        d.rounded_rectangle([cx-cw/2,cy-ch/2,cx+cw/2,cy+ch/2],24,fill=(210,222,235))
        person(d,cx,cy+ch*0.18,cw/520*1.6,(95,105,120))
        if u>3.4:
            bh=int(ch*0.17); d.rectangle([cx-cw/2,cy+ch/2-bh,cx+cw/2,cy+ch/2],fill=WHITE)
            ctext(d,cy+ch/2-bh/2,"YOUR NAME · 21/11/26",F("b",max(14,int(cw/14))),INK)
        kb=3200*(1-p)+18*p
        lab=f"{kb/1024:.1f} MB" if kb>1024 else f"{kb:.0f} KB"
        ctext(d,1250,lab,F("k",110),INK if kb<=30 else RED)
        dims="3024 × 4032" if p<0.5 else "150 × 200 px"
        ctext(d,1345,dims,F("s",44),(95,99,104))
        d.rounded_rectangle([290,1400,790,1424],12,fill=(225,225,220)); d.rounded_rectangle([290,1400,290+500*p,1424],12,fill=GOLD)
        if u>4.0:
            s=eb(seg(u,4.0,4.6)); w=int(560*s)
            d.rounded_rectangle([W/2-w/2,1560,W/2+w/2,1680],60,fill=GREEN)
            if s>0.7: ctext(d,1620,"✓ Under 30 KB · ready",F("b",46),WHITE)
    else:
        endcard(d,(t-7.6)/2.4,"Free photo resizer")
    return im

def reelB(i):
    t=i/FPS; im=BG_D.copy(); d=ImageDraw.Draw(im)
    cols=[(240,140,120),(120,170,240),(150,210,150),(240,200,110),(190,150,230)]
    if t<2.2:
        a=ease(seg(t,0,0.35)); ctext(d,620+80*(1-a),"5 photos",F("k",160),WHITE)
        b=ease(seg(t,0.2,0.55)); ctext(d,790+80*(1-b),"→ 1 PDF?",F("k",160),GOLD)
        for k in range(5):
            s=eb(seg(t,0.6+k*0.1,1.0+k*0.1))
            if s>0:
                x=170+k*160; y=1010; w=int(130*s); h=int(170*s)
                d.rounded_rectangle([x-w/2+65,y,x+w/2+65,y+h],16,fill=cols[k])
        ctext(d,1300,"for forms, assignments, receipts",F("s",46),MUTE)
    elif t<7.6:
        u=t-2.2; ctext(d,330,"Done on your phone",F("k",70),WHITE)
        # pdf doc
        dx,dy,dw,dh=W/2-230,640,460,600
        d.rounded_rectangle([dx,dy,dx+dw,dy+dh],30,fill=WHITE)
        d.polygon([(dx+dw-110,dy),(dx+dw,dy+110),(dx+dw-110,dy+110)],fill=(225,225,220))
        d.rounded_rectangle([dx+40,dy+dh-120,dx+200,dy+dh-40],18,fill=RED); ctext(d,dy+dh-80,"PDF",F("k",48),WHITE,dx+120)
        for k in range(5):
            s=ease(seg(u,0.2+k*0.45,0.8+k*0.45))
            sx,sy=170+k*160+65,1100; ex,ey=W/2+(k-2)*18,dy+180+k*14
            x=sx+(ex-sx)*s; y=sy+(ey-sy)*s; sc=1-0.35*s
            w=130*sc; h=170*sc
            if s<1 or True: d.rounded_rectangle([x-w/2,y-h/2,x+w/2,y+h/2],14,fill=cols[k],outline=WHITE,width=4)
        n=min(5,int(seg(u,0.2,2.8)*5+0.999)) if u>0.2 else 0
        ctext(d,1340,f"{n} {'page' if n==1 else 'pages'}",F("k",100),GOLD)
        if u>3.2:
            s=eb(seg(u,3.2,3.8)); w=int(640*s)
            d.rounded_rectangle([W/2-w/2,1480,W/2+w/2,1600],60,fill=GREEN)
            if s>0.7: ctext(d,1540,"✓ 1 PDF · ready to upload",F("b",46),WHITE)
    else:
        endcard(d,(t-7.6)/2.4,"Free JPG to PDF")
    return im

def render(fn,name,secs=10):
    n=secs*FPS
    if len(sys.argv)>2:
        for s in map(float,sys.argv[2].split(",")): fn(int(s*FPS)).save(f"{name}-still-{s}.png")
        return
    p=subprocess.Popen(["ffmpeg","-y","-loglevel","error","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(FPS),"-i","-","-c:v","libx264","-preset","veryfast","-crf","20","-pix_fmt","yuv420p","-movflags","+faststart",f"{name}.tmp.mp4"],stdin=subprocess.PIPE)
    for i in range(n): p.stdin.write(fn(i).tobytes())
    p.stdin.close(); assert p.wait()==0
    import os; os.replace(f"{name}.tmp.mp4",f"{name}.mp4")
which=sys.argv[1]
render(reelA if which=="A" else reelB, "reelA" if which=="A" else "reelB")
