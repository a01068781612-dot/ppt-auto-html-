import cv2,numpy as np
im=cv2.imread('images/1.webp');H,W=im.shape[:2]
hsv=cv2.cvtColor(im,cv2.COLOR_BGR2HSV)
bright=((hsv[:,:,2]>190)&(hsv[:,:,1]<50)).astype(np.uint8)
def disk(cx,cy,r):
    m=np.zeros((H,W),np.uint8);cv2.circle(m,(cx,cy),r,1,-1);return m
tri=np.zeros((H,W),np.uint8);cv2.fillPoly(tri,[np.array([(552,470),(552,542),(610,507)],np.int32)],1);tri=cv2.dilate(tri,np.ones((7,7),np.uint8))
icon=lambda reg:cv2.dilate(bright&reg,np.ones((3,3),np.uint8),iterations=3)&cv2.dilate(reg,np.ones((5,5),np.uint8))
masks=[tri,icon(disk(417,510,42)),icon(disk(726,511,42))]
extra=np.zeros((H,W),np.uint8);extra[505:545,515:555]=1;extra[440:600,840:]=1
out=im.copy();pending=np.clip(sum(masks),0,1).astype(np.uint8)
for i,m0 in enumerate(masks):
  for b0 in range(455,565,12):
    m=m0.copy();m[:b0]=0;m[b0+12:]=0
    ys,xs=np.nonzero(m)
    if len(ys)==0:continue
    ring=cv2.dilate(m,np.ones((13,13),np.uint8))&(1-pending)
    ry,rx=np.nonzero(ring);best=None
    for strict in (True,False):
      cands=[s*(16*k+d) for k in range(1,8) for d in (-1,0,1) for s in (-1,1)] if strict else [d for d in range(-140,141) if abs(d)>=10]
      for dx in cands:
        if (xs+dx).min()<0 or (xs+dx).max()>=W or (rx+dx).min()<0 or (rx+dx).max()>=W:continue
        if pending[ys,xs+dx].any() or extra[ys,xs+dx].any():continue
        ok=pending[ry,rx+dx]==0
        if ok.sum()<20:continue
        err=((out[ry[ok],rx[ok]].astype(int)-out[ry[ok],rx[ok]+dx].astype(int))**2).mean()
        if best is None or err<best[0]:best=(err,dx)
      if best:break
    dx=best[1];out[ys,xs]=out[ys,xs+dx]
  pending=np.clip(pending-m0,0,1).astype(np.uint8)
M=np.clip(sum(masks),0,1).astype(np.uint8)
e=(cv2.dilate(M,np.ones((3,3),np.uint8))-cv2.erode(M,np.ones((3,3),np.uint8))).astype(bool)
bl=cv2.GaussianBlur(out,(3,3),0);out[e]=bl[e]
cv2.imwrite('scratchpad/kbs/full.png',out)
cv2.imwrite('scratchpad/kbs/frame.png',out[190:764,6:1137])
z=np.vstack([im[440:580,330:810],out[440:580,330:810]]);cv2.imwrite('scratchpad/kbs/cmp.png',cv2.resize(z,None,fx=2,fy=2))
# info (i) icon on sky
mi=np.zeros((H,W),np.uint8);cv2.circle(mi,(1109,217),17,1,-1)
mi=cv2.dilate(((hsv[:,:,2]>200)&(hsv[:,:,1]<40)).astype(np.uint8)&mi,np.ones((3,3),np.uint8),iterations=2)
out=cv2.inpaint(out,mi*255,7,cv2.INPAINT_TELEA)
cv2.imwrite('scratchpad/kbs/full.png',out)
cv2.imwrite('scratchpad/kbs/frame.png',out[190:758,6:1137])
