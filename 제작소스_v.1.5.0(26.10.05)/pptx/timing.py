import sys,re,zipfile,shutil
src,dst=sys.argv[1],sys.argv[2]
def timing(spid,dur_ms,auto,full):
    if auto:
        cond='<p:cond delay="indefinite"/><p:cond evt="onBegin" delay="0"><p:tn val="2"/></p:cond>'; node='afterEffect'
    else:
        cond='<p:cond delay="indefinite"/>'; node='clickEffect'
    fs=' fullScrn="1"' if full else ''
    return ('<p:timing><p:tnLst><p:par><p:cTn id="1" dur="indefinite" restart="never" nodeType="tmRoot"><p:childTnLst>'
      '<p:seq concurrent="1" nextAc="seek"><p:cTn id="2" dur="indefinite" nodeType="mainSeq"><p:childTnLst>'
      f'<p:par><p:cTn id="3" fill="hold"><p:stCondLst>{cond}</p:stCondLst><p:childTnLst>'
      '<p:par><p:cTn id="4" fill="hold"><p:stCondLst><p:cond delay="0"/></p:stCondLst><p:childTnLst>'
      f'<p:par><p:cTn id="5" presetID="1" presetClass="mediacall" presetSubtype="0" fill="hold" nodeType="{node}"><p:stCondLst><p:cond delay="0"/></p:stCondLst><p:childTnLst>'
      f'<p:cmd type="call" cmd="playFrom(0.0)"><p:cBhvr><p:cTn id="6" dur="{dur_ms}" fill="hold"/><p:tgtEl><p:spTgt spid="{spid}"/></p:tgtEl></p:cBhvr></p:cmd>'
      '</p:childTnLst></p:cTn></p:par></p:childTnLst></p:cTn></p:par></p:childTnLst></p:cTn></p:par>'
      '</p:childTnLst></p:cTn><p:prevCondLst><p:cond evt="onPrev" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:prevCondLst>'
      '<p:nextCondLst><p:cond evt="onNext" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:nextCondLst></p:seq>'
      f'<p:video{fs}><p:cMediaNode vol="80000"><p:cTn id="7" fill="hold" display="0"><p:stCondLst><p:cond delay="indefinite"/></p:stCondLst></p:cTn>'
      f'<p:tgtEl><p:spTgt spid="{spid}"/></p:tgtEl></p:cMediaNode></p:video>'
      '</p:childTnLst></p:cTn></p:par></p:tnLst></p:timing>')
import json,os
VJ={v['name']:v['dur'] for v in json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'vids.json')))} if os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)),'vids.json')) else {}
DEF={'intro_video':164500,'promo_video':82500}
zin=zipfile.ZipFile(src); zout=zipfile.ZipFile(dst,'w',zipfile.ZIP_DEFLATED)
for it in zin.infolist():
    d=zin.read(it.filename)
    if re.match(r'ppt/slides/slide\d+\.xml$',it.filename):
        x=d.decode('utf8')
        mm=re.search(r'<p:cNvPr id="(\d+)" name="([^"]+)"><a:hlinkClick r:id="" action="ppaction://media"/>',x)
        if mm:
            spid,name=mm.group(1),mm.group(2)
            dur=VJ.get(name,DEF.get(name,5000))
            x=x.replace('<a:hlinkClick r:id="" action="ppaction://media"/>','')
            x=x.replace('</p:sld>',timing(spid,dur,True,False)+'</p:sld>'); d=x.encode('utf8')
    comp=zipfile.ZIP_STORED if it.filename.endswith('.mp4') else zipfile.ZIP_DEFLATED
    zout.writestr(it,d,compress_type=comp)
zout.close(); print('ok',dst)
