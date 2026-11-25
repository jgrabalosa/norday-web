# Nori de la app para la web: mira al cursor, respira, parpadea y se duerme. Escena para riv_create (rive-mcp-server 0.12).
import json
from PIL import Image
P='/home/claude/nori-web/piezas'; I=json.load(open(f'{P}/info.json'))
def recorta(src, caja, dst):
    im=Image.open(src).convert('RGBA').crop(caja); im.save(f'{P}/{dst}', optimize=True)
    return ((caja[0]+caja[2])/2, (caja[1]+caja[3])/2)
c_cuerpo=recorta(f'{P}/cuerpo_sin_cara.png',(256,270,768,896),'cuerpo_rec.png')
c_brote=recorta('/home/claude/nori-web/arte/Nori_adulto_sonriente_brote.png',(337,89,684,276),'brote_rec.png')
PIE=(512,894); ANC=(510,274); CARA=(514,451)
rel=lambda a,b:(a[0]-b[0],a[1]-b[1])
cen=lambda k:(I[k]['cx'],I[k]['cy'])
G=[]; IM=[]
def g(id,pos,parent=None,**kw): G.append(dict(id=id,x=pos[0],y=pos[1],**({'parent':parent} if parent else {}),**kw))
def im(id,png,pos,parent): IM.append(dict(id=id,pngPath=f'{P}/{png}',x=pos[0],y=pos[1],parent=parent))
OFF=(182,60)
g('rig',(PIE[0]-OFF[0],PIE[1]-OFF[1]))
g('respira',(0,0),'rig')
im('cuerpo','cuerpo_rec.png',rel(c_cuerpo,PIE),'respira')
g('broteBase',rel(ANC,PIE),'respira'); g('broteLook',(0,0),'broteBase'); g('broteSway',(0,0),'broteLook')
im('brote','brote_rec.png',rel(c_brote,ANC),'broteSway')
g('caraX',rel(CARA,PIE),'respira'); g('caraY',(0,0),'caraX')
g('despierta',(0,0),'caraY')
OJO_L=(439,442); OJO_R=(593,442)
g('ojoLG',rel(OJO_L,CARA),'despierta'); g('ojoRG',rel(OJO_R,CARA),'despierta')
im('ojoL','ojo_abierto.png',(0,0),'ojoLG'); im('ojoR','ojo_abierto.png',(0,0),'ojoRG')
im('boca','sonriente_verde_3.png',rel(cen('sonriente_verde_3'),CARA),'despierta')
g('mejX',(0,0),'caraX'); g('mejY',(0,0),'mejX')
for k in ['sonriente_rojo_1','sonriente_rojo_5']: im(k,f'{k}.png',rel(cen(k),CARA),'mejY')
g('dormida',(0,0),'caraY',opacity=0)
for k in ['dormido_verde_1','dormido_verde_2','dormido_verde_12']: im(k,f'{k}.png',rel(cen(k),CARA),'dormida')
g('zzzG',rel(cen('zzz'),PIE),'rig',opacity=0); im('zzz','zzz.png',(0,0),'zzzG')
def kf(*pares,e='ease-in-out'): return [dict(frame=f,value=v,**({'easing':e} if i else {})) for i,(f,v) in enumerate(pares)]
def tr(t,p,*pares,e='ease-in-out'): return dict(target=t,property=p,keyframes=kf(*pares,e=e))
A=[]
A.append(dict(name='respira',fps=60,duration=240,loop='loop',tracks=[
  tr('respira','scaleY',(0,1),(120,1.012),(240,1)), tr('respira','scaleX',(0,1),(120,0.995),(240,1)),
  tr('broteSway','rotation',(0,1.5),(75,-2.5),(135,0),(195,2.5),(240,1.5))]))
A.append(dict(name='parpadeo',fps=60,duration=330,loop='loop',tracks=[
  tr(o,'scaleY',(0,1),(170,1),(174,0.08),(181,1),(330,1)) for o in ('ojoLG','ojoRG')]))
CX=rel(CARA,PIE)[0]
for nom,rot,dx,bro in [('mx_izq',-3,-26,4),('mx_centro',0,0,0),('mx_der',3,26,-4)]:
    A.append(dict(name=nom,fps=60,duration=1,loop='oneShot',tracks=[
      dict(target='rig',property='rotation',keyframes=[dict(frame=0,value=rot)]),
      dict(target='caraX',property='x',keyframes=[dict(frame=0,value=CX+dx)]),
      dict(target='broteLook',property='rotation',keyframes=[dict(frame=0,value=bro)]),
      dict(target='mejX',property='x',keyframes=[dict(frame=0,value=-dx*0.5)])]))
for nom,dy in [('my_arriba',-16),('my_centro',0),('my_abajo',10)]:
    A.append(dict(name=nom,fps=60,duration=1,loop='oneShot',tracks=[dict(target='caraY',property='y',keyframes=[dict(frame=0,value=dy)]),dict(target='mejY',property='y',keyframes=[dict(frame=0,value=dy*0.5)])]))
ZY=rel(cen('zzz'),PIE)[1]
A.append(dict(name='despierta',fps=60,duration=1,loop='oneShot',tracks=[
  dict(target='despierta',property='opacity',keyframes=[dict(frame=0,value=1)]),
  dict(target='dormida',property='opacity',keyframes=[dict(frame=0,value=0)]),
  dict(target='zzzG',property='opacity',keyframes=[dict(frame=0,value=0)])]))
A.append(dict(name='dormida',fps=60,duration=180,loop='loop',tracks=[
  tr('despierta','opacity',(0,0),(180,0),e='linear'), tr('dormida','opacity',(0,1),(180,1),e='linear'),
  tr('zzzG','opacity',(0,0.85),(90,1),(180,0.85)), tr('zzzG','y',(0,ZY),(90,ZY-10),(180,ZY))]))
SM=dict(name='Nori',inputs=[dict(name='mirarX',type='number',initial=50),dict(name='mirarY',type='number',initial=50),dict(name='dormido',type='bool',initial=False)],
  layers=[
   dict(name='respirar',states=[dict(name='respira',animation='respira')],transitions=[dict(**{'from':'entry','to':'respira'})]),
   dict(name='parpadeo',states=[dict(name='parpadeo',animation='parpadeo')],transitions=[dict(**{'from':'entry','to':'parpadeo'})]),
   dict(name='mirarX',states=[dict(name='mx',blend1d=dict(input='mirarX',animations=[dict(animation='mx_izq',value=0),dict(animation='mx_centro',value=50),dict(animation='mx_der',value=100)]))],transitions=[dict(**{'from':'entry','to':'mx'})]),
   dict(name='mirarY',states=[dict(name='my',blend1d=dict(input='mirarY',animations=[dict(animation='my_arriba',value=0),dict(animation='my_centro',value=50),dict(animation='my_abajo',value=100)]))],transitions=[dict(**{'from':'entry','to':'my'})]),
   dict(name='dormir',states=[dict(name='despierta',animation='despierta'),dict(name='dormida',animation='dormida')],
        transitions=[dict(**{'from':'entry','to':'despierta'}),
                     dict(**{'from':'despierta','to':'dormida'},condition=dict(input='dormido',op='==',value=True),durationMs=450),
                     dict(**{'from':'dormida','to':'despierta'},condition=dict(input='dormido',op='==',value=False),durationMs=250)])])
spec=dict(outPath='/home/claude/nori-web/riv/nori_web.riv',scene=dict(artboard=dict(name='Nori',width=660,height=880),groups=G,images=IM,animations=A,stateMachine=SM))
json.dump(spec,open('/home/claude/nori-web/riv/crear.json','w'))
print('grupos',len(G),'imagenes',len(IM),'animaciones',len(A))
