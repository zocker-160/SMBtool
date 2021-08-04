import newGameLib
from newGameLib import *
import Blender	


getAll=1

def setBox(box,meshList):
	E=[[],[],[]]
	for mesh in meshList:
		for n in range(len(mesh.vertPosList)):
			x,y,z=mesh.vertPosList[n]
			E[0].append(x)
			E[1].append(y)
			E[2].append(z)	
	skX=(box[3]-box[0])/(max(E[0])-min(E[0]))
	skY=(box[4]-box[1])/(max(E[1])-min(E[1]))
	skZ=(box[5]-box[2])/(max(E[2])-min(E[2]))
	sk=min(skX,skY,skZ)
	trX1=(box[3]+box[0])/2#-(max(E[0])+min(E[0]))/2
	trY1=(box[4]+box[1])/2#-(max(E[1])+min(E[1]))/2
	trZ1=(box[5]+box[2])/2#-(max(E[2])+min(E[2]))/2
	
	trX=-(max(E[0])+min(E[0]))/2
	trY=-(max(E[1])+min(E[1]))/2
	trZ=-(max(E[2])+min(E[2]))/2
	#print trX,trY,trZ
	#print skX,skY,skZ
	
	for mesh in meshList:
		for n in range(len(mesh.vertPosList)):
			x,y,z=mesh.vertPosList[n]
			mesh.vertPosList[n]=[x+trX,y+trY,z+trZ]
		for n in range(len(mesh.vertPosList)):
			x,y,z=mesh.vertPosList[n]
			mesh.vertPosList[n]=[x*skX,y*skY,z*skZ]
		for n in range(len(mesh.vertPosList)):
			x,y,z=mesh.vertPosList[n]
			mesh.vertPosList[n]=[x+trX1,y+trY1,z+trZ1]
		#mesh.draw()	

	
		
def smbParser(filename,g):


	dirPath=g.dirname+os.sep+g.basename+'_files'
	if os.path.exists(dirPath)==False:os.makedirs(dirPath)
	


	g.word(4)
	fileCount=g.i(1)[0]
	g.word(g.i(1)[0])
	A=g.i(9)
	nodeList=[]
	for m in range(A[6]):
		start=g.tell()
		B=g.i(7)
		t=g.tell()
		g.i(3)
		name=g.word(g.i(1)[0])
		g.i(10)
		info=[]
		nodeList.append([B,name,info,start])
		g.seek(t+B[5])
	
	start=0	
	for i,node in enumerate(nodeList):
		if node[0][1] in [0]:
			headPath=dirPath+os.sep+os.path.basename(node[1]+'.meshinfo')
			new=open(headPath,'wb')
			g.seek(node[3])
			new.write(g.read(node[0][5]+28))
			new.close()
			
		"""if node[0][1] in [6]:#gr2
			headPath=dirPath+os.sep+os.path.basename(node[1])
			new=open(headPath,'wb')
			g.seek(node[3])
			new.write(g.read(node[0][5]+28))
			new.close()"""
			
		if node[0][1] in [1]:
			headPath=dirPath+os.sep+os.path.basename(node[1]+'.imageinfo')
			new=open(headPath,'wb')
			g.seek(node[3])
			new.write(g.read(node[0][5]+28))
			new.close()
			
		if node[0][1] in [1]:
			dataPath=dirPath+os.sep+os.path.basename(node[1]+'.data')
			new=open(dataPath,'wb')
			g.seek(A[0]+A[2]+node[0][4])
			if i<len(nodeList)-1:
				new.write(g.read(nodeList[i+1][0][4]-nodeList[i][0][4]))
			new.close()
			
		if node[0][1] in [6]:
			dataPath=dirPath+os.sep+os.path.basename(node[1])
			new=open(dataPath,'wb')
			g.seek(A[0]+A[2]+node[0][4])
			if i<len(nodeList)-1:
				new.write(g.read(nodeList[i+1][0][4]-nodeList[i][0][4]))
			new.close()
			
		if node[0][1] in [20]:
			headPath=dirPath+os.sep+g.basename+'_'+str(i).zfill(2)+'.skeleton'
			new=open(headPath,'wb')
			g.seek(node[3])
			new.write(g.read(node[0][5]+28))
			new.close()
		
	start=0	
	for i,node in enumerate(nodeList):
		#print i,node[1]
		end=node[0][3]
		if end-start>0:
			if nodeList[i-1][0][1] in [0,1]:
				filePath=dirPath+os.sep+os.path.basename(nodeList[i-1][1]+'.data')
				new=open(filePath,'wb')
				g.seek(A[0]+start)
				new.write(g.read(end-start))
				new.close()
				
			if nodeList[i-1][0][1] in [0]:
				filePath=dirPath+os.sep+os.path.basename(nodeList[i-1][1]+'.data2')
				new=open(filePath,'wb')
				g.seek(A[0]+A[2])
				new.write(g.read(A[3]))
				new.close()
		start=end
	if nodeList[i][0][1] in [0,1]:
		filePath=dirPath+os.sep+os.path.basename(nodeList[i][1]+'.data')
		new=open(filePath,'wb')
		g.seek(A[0]+nodeList[i][0][3])
		new.write(g.read(A[2]-nodeList[i][0][3]))
		new.close()
		
		
def meshinfoParser(filename,g):	
	HEAD=g.i(10)
	
	model=Model(filename)
	model.meshBindBoneList=[]
	model.meshBindBoneList1=[]
	model.boneMapInfoList=[]
	model.meshListBB=[]
	model.texDiffList=[]
	model.geoName=g.word(g.i(1)[0])
	g.i(2)
	g.i(g.i(1)[0]*2)
	g.i(3)
	g.f(1)
	model.boundingBox=g.f(6)
	C=g.i(3)
	for n in range(C[2]):		
		D=g.i(12)
		g.f(3)
		g.i(2)
		g.f(6)
		g.word(g.i(1)[0])
		g.word(g.i(1)[0])
		g.word(g.i(1)[0])
		g.f(4)
		#print hex(g.tell()),n,"[",D[2],"]",D
		if D[2]==6:
			g.word(g.i(1)[0])
			g.i(2)
			g.word(g.i(1)[0])
			model.texDiffList.append(g.dirname+os.sep+os.path.basename(g.word(g.i(1)[0])).split('.')[0]+'.dds')
			g.word(g.i(1)[0])
			g.i(1)
			g.word(g.i(1)[0])
			g.B(13)
		if D[2]==3:
			g.word(g.i(1)[0])
			g.i(2)
			g.word(g.i(1)[0])
			fu = g.word(g.i(1)[0])
			x = os.path.basename(fu)
			split = x.split('.')[0]
			texName= g.dirname+os.sep+split+'.dds'
			model.texDiffList.append(texName)
			g.seek(84,1)								
			if n>0 and n<6:
				g.seek(-1,1)
			if n==8:
				g.seek(11,1)
		if D[2]==2:
			g.word(g.i(1)[0])
			g.i(2)
			g.word(g.i(1)[0])
			fu = g.word(g.i(1)[0])
			x = os.path.basename(fu)
			split = x.split('.')[0]
			texName= g.dirname+os.sep+split+'.dds'
			model.texDiffList.append(texName)
			g.word(g.i(1)[0])
			g.i(2)
			g.word(g.i(1)[0])
			g.i(2)
			g.word(g.i(1)[0])
			g.seek(20,1)#???
		if D[2]==1:
			g.word(g.i(1)[0])
			g.i(2)
			g.word(g.i(1)[0])
			fu = g.word(g.i(1)[0])
			if fu != None:
				x = os.path.basename(fu)
				split = x.split('.')[0]
				texName= g.dirname+os.sep+split+'.dds'
				model.texDiffList.append(texName)
			g.i(2)
			g.word(g.i(1)[0])
		if D[2]==0:	
			E=g.i(4)
			flag=g.i(1)[0]	
			#print flag,g.tell(),n,C[2]	
			if flag!=737893 and flag>10:
				g.seek(-4,1)
				fu = g.word(g.i(1)[0])
				if fu != None:
					x = os.path.basename(fu)
					split = x.split('.')[0]
					texName= g.dirname+os.sep+split+'.dds'
					model.texDiffList.append(texName)
				K=g.i(2)					
				g.word(g.i(1)[0])
			else:
				g.seek(-4,1)
				model.texDiffList.append('None')
		
	count=g.i(1)[0]
	for n in range(count):
		g.i(3)
		g.H(1)	
		g.i(5)
		g.i(2)
		g.word(g.i(1)[0])
		g.i(2)
		g.word(g.i(1)[0])
		g.i(6)
		g.word(g.i(1)[0])
		g.i(2)
		g.word(g.i(1)[0])
		g.i(9)
	count=g.i(1)[0]
	for n in range(count):
		mesh=Mesh()
		model.meshList.append(mesh)
		mesh.a=None
		mesh.b=None
		mesh.c=None
		a=g.H(21)
		b=g.i(10)
		mesh.a=a
		mesh.b=b
		if b[8]==0:
			mesh.c=g.i(2)
	if g.tell()<g.fileSize():	
		D=g.i(4)
		if D[0]==10:
			model.boneNameList=g.word(D[3]).split('|')
			count=g.i(1)[0]
			for m in range(count):
				g.f(7)	
			count=g.i(1)[0]
			model.meshBindBoneList=[]
			model.meshBindBoneList1=[]
			for n in range(count):
				model.meshBindBoneList.append(g.B(2))	
			count=g.i(1)[0]
			model.boneMapInfoList=[]
			for n in range(count):
				model.boneMapInfoList.append(g.B(4))
				print n,model.boneMapInfoList[-1]	
			count=g.i(1)[0]
			for n in range(count):
				model.meshBindBoneList1.append(g.B(4))	
			count=g.i(1)[0]
			model.boneMap=[]
			for n in range(count):
				model.boneMap.append(g.B(1)[0])
			g.i(3)
		else:
			g.seek(-16,1)
		
	#print model.texDiffList
	#print "<",g.basename,">"	
	dataPath=g.dirname+os.sep+g.basename+'.geo.data'
	#print dataPath
	if os.path.exists(dataPath)==True:	
		file=open(dataPath,'rb')
		p=BinaryReader(file)
		for i,mesh in enumerate(model.meshList):
			mat=Mat()
			mesh.matList.append(mat)
			mat.TRISTRIP=True
			try:
				mat.diffuse=model.texDiffList[i]
				if os.path.exists(mat.diffuse)==False:
					print 'no image:',mat.diffuse
			except:
				print 'no image:',mat.diffuse
			p.seek(mesh.b[7])
			#print i,mesh.b,"seek:",hex(mesh.b[7])
			if mesh.b[5]==0:
				for m in range(mesh.b[3]):
					mesh.vertPosList.append(p.f(3))
			elif mesh.b[5]==87:#?				
				for m in range(mesh.b[3]):
					mesh.vertUVList.append(p.short(2,'h',11))
					mesh.vertPosList.append(p.f(3))
			elif mesh.b[5]==89:
				for m in range(mesh.b[3]):
					mesh.skinIndiceList.append(p.B(2))
					mesh.skinWeightList.append(p.B(2))
					mesh.vertUVList.append(p.short(2,'h',11))
					mesh.vertPosList.append(p.f(3))
			elif mesh.b[5]==108:#?
				for m in range(mesh.b[3]):
					mesh.vertUVList.append(p.short(2,'h',11))
					p.B(4)
					mesh.vertPosList.append(p.f(3))
			elif mesh.b[5]==112:#?
				for m in range(mesh.b[3]):
					mesh.vertUVList.append(p.short(2,'h',11))
					p.B(4)
					mesh.vertPosList.append(p.short(3,'h',16))
			elif mesh.b[5]==114:
				for m in range(mesh.b[3]):
					mesh.skinIndiceList.append(p.B(2))
					mesh.skinWeightList.append(p.B(2))
					mesh.vertUVList.append(p.short(2,'h',11))
					mesh.vertPosList.append(p.short(3,'h',16))
			elif mesh.b[5]==116:
				for m in range(mesh.b[3]):
					mesh.vertUVList.append(p.short(2,'h',11))
					p.B(4)
					mesh.vertPosList.append(p.short(3,'h',16))
			elif mesh.b[5]==119:
				for m in range(mesh.b[3]):
					mesh.skinIndiceList.append(p.B(2))
					mesh.skinWeightList.append(p.B(2))
					mesh.vertUVList.append(p.short(2,'h',11))
					p.B(4)
					mesh.vertPosList.append(p.short(3,'h',16))
			elif mesh.b[5]==121:
				for m in range(mesh.b[3]):
					mesh.vertUVList.append(p.short(2,'h',11))
					p.B(4)
					mesh.vertPosList.append(p.short(3,'h',16))
			elif mesh.b[5]==122:
				for m in range(mesh.b[3]):
					mesh.skinIndiceList.append(p.B(2))
					mesh.skinWeightList.append(p.B(2))
					mesh.vertUVList.append(p.short(2,'h',11))
					p.B(4)
					mesh.vertPosList.append(p.short(3,'h',16))
			else:
				print 'UNKNOW MESH TYPE:',mesh.b[5]
				break

			if mesh.c is not None:
				p.seek(mesh.b[9])
				p.H(4)				
				while(True):
					B=p.H(2)
					t=p.tell()
					if B[1]==24572:
						indiceList=p.H(4094)
						mesh.indiceList.extend(indiceList)
						p.seek(t+8188)
					else:
						indiceCount=mesh.c[1]-len(mesh.indiceList)-1	
						indiceList=	p.H(indiceCount)
						mesh.indiceList.extend(indiceList)
						break
			else:
				data2Path=g.dirname+os.sep+g.basename+'.geo.data2'
				#print data2Path
				if os.path.exists(data2Path)==True:
				
					file2=open(data2Path,'rb')
					r=BinaryReader(file2)
					r.seek(HEAD[4]+mesh.b[9])
					#print r.tell()
					mesh.indiceList=r.H(mesh.b[8])
					file2.close()
			if mesh.b[5] not in [0,89]:
				model.meshListBB.append(mesh)
				
				"""skin=Skin()
				for boneMapInfo in model.boneMapInfoList:
					if boneMapInfo[0]==i:
						idStart=boneMapInfo[1]
						idCount=boneMapInfo[2]
						skin.boneMap=model.boneMap[idStart:idStart+idCount]
						mesh.boneNameList=model.boneNameList
				mesh.skinList.append(skin)
				mesh.BINDSKELETON='armature'
				mesh.draw()"""
			#else:
			#	model.meshListBB.append(mesh)
				
				
		file.close()		
				
		box=model.boundingBox
		if len(model.meshListBB)>0:
			setBox(box,model.meshListBB)
			
		for i,mesh in enumerate(model.meshList):
			skin=Skin()
			
			
			for info in model.boneMapInfoList:
				if info[0]==i:
					print '0',i,info,len(model.boneNameList)
					idStart=info[1]
					idCount=info[2]
					skin.boneMap=model.boneMap[idStart:idStart+idCount]
					mesh.boneNameList=model.boneNameList
			for info in model.meshBindBoneList:
				if info[0]==i:
					print '1',i,info,len(model.boneNameList)
					skin.boneMap=[info[1]]
					mesh.boneNameList=model.boneNameList
					for m in range(len(mesh.vertPosList)):
						mesh.skinIndiceList.append([0])
						mesh.skinWeightList.append([1.0])
			"""for info in model.meshBindBoneList1:
				print i,info
				if info[0]==i:
					skin.boneMap=[info[1]]
					mesh.boneNameList=model.boneNameList
					for m in range(len(mesh.vertPosList)):
						mesh.skinIndiceList.append([0])
						mesh.skinWeightList.append([1.0])"""
						
			mesh.skinList.append(skin)
			
			
			
			mesh.BINDSKELETON='armature'
			mesh.draw()	
		
	
def skeletoninfoParser(filename,g):	
	HEAD=g.i(7)
	#g.logskip=True
	skeleton=Skeleton()
	skeleton.ARMATURESPACE=True
	skeleton.NICE=True
	skeleton.BINDMESH=True
	C=g.i(4)
	g.word(C[3])
	size=g.i(1)[0]
	t1=g.tell()
	g.seek(t1+size)
	boneCount=g.i(1)[0]
	
	txt=open('hashlist.txt','w')
	
	for n in range(boneCount):
		bone=Bone()
		skeleton.boneList.append(bone)
		bone.matrix=Matrix4x4(g.f(16)).invert()
		g.i(2)
		g.f(7)
		D=g.i(3)
		bone.parentID=D[1]
		bone.hash=str(D[0])
		
	for n in range(boneCount):
		bone=skeleton.boneList[n]
		off=g.i(1)[0]
		tn=g.tell()
		g.seek(t1+off)				
		bone.name=g.find('\x00')[-25:]
		g.seek(tn)
		txt.write(bone.hash+':'+bone.name+'\n')
	skeleton.draw()
	#g.logskip=False
	txt.close()
		
def imageinfoParser(filename,g):
	g.i(10)
	name=g.word(g.i(1)[0])
	g.i(4)
	g.B(1)
	info=g.i(9)
	
	dataPath=filename.replace('.imageinfo','.data')
	#print dataPath
	if os.path.exists(dataPath)==True:
	
		file=open(dataPath,'rb')
		p=BinaryReader(file)
	
	
		obrazek=Obrazek()
		filePath=g.dirname+os.sep+g.basename
		#print info
		obrazek.wys=info[2]
		obrazek.szer=info[3]
		if info[1]==12:
			obrazek.format='DXT1'
			obrazek.name=filePath+'.dds'
			obrazek.wys=info[3]
			obrazek.szer=info[2]
		if info[1]==15:
			obrazek.format='DXT5'
			obrazek.name=filePath+'.dds'
			obrazek.wys=info[3]
			obrazek.szer=info[2]
		if info[1]==18:
			obrazek.format='tga32'
			obrazek.name=filePath+'.tga'
		if info[1]==14:
			obrazek.format='DXT3'
			obrazek.name=filePath+'.dds'
			obrazek.wys=info[3]
			obrazek.szer=info[2]
		obrazek.data=p.read(p.fileSize())
		obrazek.save()
		
		file.close()
		
def gr2Parser(filename,p):
	
	hashPath='hashlist.txt'
	hashList={}
	if os.path.exists(hashPath)==True:
		txt=open(hashPath,'r')
		for line in txt.readlines():
			if ':' in line:
				split=line.strip().split(':')
				#print split
				hashList[split[0]]=split[1]
		
	
	p.i(20)
	p.i(6)
	p.f(12)
	p.i(2)
	A=p.i(14)
	p.f(10)
	
	p.i(8)
	action=Action()
	action.BONESORT=True
	action.BONESPACE=True
	for m in range(A[3]):
		bone=ActionBone()
		bone.name=str(m)
		action.boneList.append(bone)
		bone.info=p.i(16)
		bone.name=str(bone.info[0])
		if str(bone.info[0]) in hashList:
			bone.name=hashList[str(bone.info[0])]
		
	for bone in action.boneList:
		if bone.info[2]>0:
			p.seek(bone.info[3])
			for m in range(bone.info[2]):
				time=p.f(1)[0]*33
				bone.posFrameList.append(time)
			p.seek(bone.info[5])
			for m in range(bone.info[2]):
				bone.posKeyList.append(VectorMatrix(p.f(3)))
		if bone.info[7]>0:	
			p.seek(bone.info[8])
			for m in range(bone.info[7]):
				time=p.f(1)[0]*33
				bone.rotFrameList.append(time)
			p.seek(bone.info[10])
			for m in range(bone.info[7]):
				bone.rotKeyList.append(QuatMatrix(p.f(4)).resize4x4())
			#break	
	action.draw()
	action.setContext()	
	
def Parser(filename):	
	print '='*70
	print filename
	print '='*70
	ext=filename.split('.')[-1].lower()	
	
	if ext=='smb':
		file=open(filename,'rb')
		g=BinaryReader(file)
		smbParser(filename,g)
		file.close()	
	
	if ext=='meshinfo':

				
		file=open(filename,'rb')
		g=BinaryReader(file)
		#g.logOpen()
		meshinfoParser(filename,g)
		#g.logClose()
		file.close()	
	
	if ext=='skeleton':
		file=open(filename,'rb')
		g=BinaryReader(file)
		skeletoninfoParser(filename,g)
		file.close()

		if getAll==1:	
		
			for file in os.listdir(os.path.dirname(filename)):
				if file.split('.')[-1].lower()=='imageinfo':
					filePath=os.path.dirname(filename)+os.sep+file
					file=open(filePath,'rb')
					g=BinaryReader(file)
					imageinfoParser(filePath,g)
					file.close()	
					
			
			for file in os.listdir(os.path.dirname(filename)):
				if file.split('.')[-1].lower()=='meshinfo':
					#print file
					filePath=os.path.dirname(filename)+os.sep+file
					file=open(filePath,'rb')
					g=BinaryReader(file)
					#g.logOpen()
					meshinfoParser(filePath,g)
					#g.logClose()
					file.close()
	
	if ext=='imageinfo':
		for file in os.listdir(os.path.dirname(filename)):
			if file.split('.')[-1].lower()=='imageinfo':
				filePath=os.path.dirname(filename)+os.sep+file
				file=open(filePath,'rb')
				g=BinaryReader(file)
				imageinfoParser(filePath,g)
				file.close()	
	
	if ext=='gr2':		
		file=open(filename,'rb')
		g=BinaryReader(file)		
		gr2Parser(filename,g)
		file.close()
 
	
Blender.Window.FileSelector(Parser,'import','select: *.smb, *.skeleton, *.meshinfo, *.imageinfo') 
	