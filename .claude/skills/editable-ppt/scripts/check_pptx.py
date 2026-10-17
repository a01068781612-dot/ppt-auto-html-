import zipfile,re,sys,collections
P=sys.argv[1]; z=zipfile.ZipFile(P); names=z.namelist()
print('media:',collections.Counter(n.rsplit('.',1)[-1] for n in names if n.startswith('ppt/media/')))
pres=z.read('ppt/presentation.xml').decode()
rels=z.read('ppt/_rels/presentation.xml.rels').decode()
rid=dict(re.findall(r'Id="(rId\d+)"[^>]*Target="(slides/slide\d+\.xml)"',rels))
rid.update({a:b for b,a in re.findall(r'Target="(slides/slide\d+\.xml)"[^>]*Id="(rId\d+)"',rels)})
order=[rid[r] for r in re.findall(r'<p:sldId [^>]*r:id="(rId\d+)"',pres)]
print('slides',len(order))
faces=collections.Counter(); bad=[]; tot=0; empty=[]; genname=[]
for i,f in enumerate(order,1):
    x=z.read('ppt/'+f).decode()
    nm=re.search(r'<p:cSld name="([^"]*)"',x); nm=nm.group(1) if nm else None
    if not nm or not nm.startswith(f'{i}.'): bad.append((i,'slide name',nm))
    objs=re.findall(r'<p:cNvPr id="\d+" name="([^"]*)"',x)
    g=[o for o in objs if re.match(r'^(Image|Text|Shape|Picture|Rectangle|TextBox)\s*\d+$',o)]
    if g: genname.append((i,g[:3]))
    if 'type="title"' not in x: bad.append((i,'no title ph'))
    if re.search(r'videoFile|<p:video|\.mp4',x): bad.append((i,'video'))
    for rpr in re.findall(r'<a:rPr[^>]*?(?:/>|>.*?</a:rPr>)',x,re.S):
        tot+=1
        la=re.search(r'<a:latin typeface="([^"]*)"',rpr); ea=re.search(r'<a:ea typeface="([^"]*)"',rpr); cs=re.search(r'<a:cs typeface="([^"]*)"',rpr)
        b=' b="1"' in rpr
        key=(la and la.group(1), ea and ea.group(1), cs and cs.group(1), b)
        faces[key]+=1
        if not la or not ea or not la.group(1).startswith('Pretendard'): bad.append((i,'run font',key))
    npic=x.count('<p:pic>'); nsp=x.count('<p:sp>'); ntx=x.count('<a:t>')
    if ntx==0: empty.append(i)
    if i in (2,3,4,5,62,70,119): print(i,nm,'pic',npic,'sp',nsp,'text',ntx)
print('runs',tot); [print(' ',k,v) for k,v in faces.most_common()]
print('bad',bad[:20],len(bad)); print('generic names',genname[:10]); print('no-text slides',empty)
th=[n for n in names if n.startswith('ppt/theme/')]
for t in th:
    x=z.read(t).decode(); print(t, re.findall(r'<a:(?:latin|ea) typeface="([^"]*)"',x)[:4], re.findall(r'script="Hang" typeface="([^"]*)"',x))
