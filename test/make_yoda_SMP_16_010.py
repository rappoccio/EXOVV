
outf=open("CMS_2018_SMP_16_010.yoda","w")
for i in range(1,13):
  inf=open("SMP-16-010_yodas/rawout_fullxs_normalized"+str(i)+".yoda")
  for l in inf.readlines():
     num=str(i)
     if len(num)==1: num="0"+num
     if "---" in l: continue
     outf.write(l.replace("/proj_2d_response_nomnomnormalized"+str(i),"/REF/CMS_2018_SMP_16_010/d"+num+"-x01-y01").replace("SCATTER2D_V2","SCATTER2D").replace("Title: ","IsRef=1").replace(": ","="))
     if "END" in l: break
  inf.close()
  inf=open("SMP-16-010_yodas/rawout_fullxs_normalized_softdrop"+str(i)+".yoda")
  for l in inf.readlines():
     if "---" in l: continue
     outf.write(l.replace("/proj_2d_response_softdrop_nomnomnormalized_softdrop"+str(i),"/REF/CMS_2018_SMP_16_010/d"+str(i+12)+"-x01-y01").replace("SCATTER2D_V2","SCATTER2D").replace("Title: ","IsRef=1").replace(": ","="))
     if "END" in l: break
  inf.close()   
outf.close()     