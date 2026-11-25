import cv2, numpy as np, json
from PIL import Image
def limpiar(cuerpo, mascara):
    im=np.array(Image.open(cuerpo).convert('RGBA'))
    m=np.array(Image.open(mascara).convert('L'))>128
    rgb=im[:,:,:3].astype(int); r,g,b=rgb[...,0],rgb[...,1],rgb[...,2]
    dentro=cv2.erode(m.astype(np.uint8),np.ones((7,7),np.uint8))>0
    tinte=((g-np.maximum(r,b))>3)|((r-np.maximum(g,b))>6)
    cara=cv2.dilate((dentro&tinte).astype(np.uint8),np.ones((23,23),np.uint8))&dentro.astype(np.uint8)
    bgr=cv2.cvtColor(im[:,:,:3],cv2.COLOR_RGB2BGR)
    sin=cv2.inpaint(bgr,cara*255,15,cv2.INPAINT_TELEA); sin=np.where(m[:,:,None],sin,bgr)
    sin=cv2.cvtColor(sin,cv2.COLOR_BGR2RGB).astype(np.float32)
    inner=cv2.erode(m.astype(np.uint8),np.ones((15,15),np.uint8)).astype(np.float32)
    w=cv2.GaussianBlur(inner,(0,0),5)[:,:,None]; blur=cv2.GaussianBlur(sin,(0,0),25)
    limpio=(sin*(1-w)+blur*w).clip(0,255)
    return im, limpio, m
def capa(im, limpio, zona):
    """RGBA de lo que brilla sobre la pantalla limpia, solo en 'zona' (bool)."""
    o=im[:,:,:3].astype(np.float32); r,g,b=o[...,0],o[...,1],o[...,2]
    t=np.maximum(g-np.maximum(r,b), r-np.maximum(g,b))
    a=np.clip((t-4)/70.0,0,1)*zona
    rgba=np.dstack([o, a*255]).clip(0,255).astype(np.uint8)
    return rgba
def recorta(rgba, nombre):
    ys,xs=np.where(rgba[:,:,3]>3); x0,x1,y0,y1=xs.min()-4,xs.max()+5,ys.min()-4,ys.max()+5
    Image.fromarray(rgba[y0:y1,x0:x1]).save(f'piezas/{nombre}.png')
    return dict(x0=int(x0),y0=int(y0),w=int(x1-x0),h=int(y1-y0),cx=(x0+x1)/2,cy=(y0+y1)/2)
info={}
for est in ['sonriente','dormido']:
    im,limpio,m=limpiar(f'arte/Nori_adulto_{est}_cuerpo.png',f'arte/Nori_adulto_{est}_pantalla.png')
    if est=='sonriente':
        out=np.dstack([limpio,im[:,:,3]]).astype(np.uint8); Image.fromarray(out).save('piezas/cuerpo_sin_cara.png')
    rgb=im[:,:,:3].astype(int); r,g,b=rgb[...,0],rgb[...,1],rgb[...,2]
    dentro=cv2.erode(m.astype(np.uint8),np.ones((7,7),np.uint8))>0
    verde=dentro&((g-np.maximum(r,b))>40); rojo=dentro&((r-np.maximum(g,b))>40)
    for nombre,mk in [('verde',verde),('rojo',rojo)]:
        n,lab,st,cen=cv2.connectedComponentsWithStats(mk.astype(np.uint8),8)
        comps=[(i,st[i]) for i in range(1,n) if st[i][4]>30]
        for i,s in comps:
            zona=(cv2.dilate((lab==i).astype(np.uint8),np.ones((17,17),np.uint8))>0)&dentro
            print(est,nombre,i,'x',s[0],'y',s[1],'w',s[2],'h',s[3],'area',s[4])
            info[f'{est}_{nombre}_{i}']=recorta(capa(im,limpio,zona.astype(np.float32)),f'{est}_{nombre}_{i}')
json.dump(info,open('piezas/info.json','w'),indent=1)
