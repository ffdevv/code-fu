from PyPDF2 import PdfFileWriter, PdfFileReader
import sys

def pdfsplit(file,intervals):
	def splitInterval(interval):
		sp1=interval.split("-")
		if len(sp1)>1:
			ifrom=sp1[0]
			ito=sp1[1]
		elif len(sp1)==1:
			ifrom=sp1[0]
			ito=sp1[0]
		if ifrom=="":
			ifrom="1" #la prima
		if ito=="":
			ito="-1"	#l'ultima
		if not (ifrom.isdigit() and ito.isdigit()):
			print ("Errore negli intervalli: \n%s -> %s - %s" % (interval, ifrom, ito))
			quit()
		else:
			ifrom=int(ifrom)
			ito=int(ito)
		return ifrom, ito

	def mkIntervals(start,stop,step):
		#crea lista di intervalli
		lista=[]
		sta=start
		while (sta+step)<=(stop+1):
			lista.append("-".join((str(sta),str(sta+step-1))))
			sta+=step

		#se esiste aggiunge la coda rimanente
		ncoda=(stop+1-start) % step
		if  ncoda != 0:
			lista.append("-".join((str(stop-ncoda+1),str(stop))))

		return lista


	pdfi = PdfFileReader(open(file,'rb'))

	if intervals==[""]:
		intervals=[str(num) for num in range(1,pdfi.numPages+1)]

	for interval in intervals:
		if "*" in interval:
			intervals.extend(mkIntervals(1,pdfi.numPages,int(interval.replace("*",""))))
			continue
		pdfo=PdfFileWriter()
		pagefrom,pageto=splitInterval(interval)
		if pageto==-1:
			pageto = pdfi.numPages

		for i in range(pagefrom,pageto+1):
			pdfo.addPage(pdfi.getPage(i-1))
		
		fileout=file.replace(".pdf","") + "_" + str(pagefrom) + "-"+str(pageto) + ".pdf"
		with open(fileout, 'wb') as fout:
			pdfo.write(fout)
		print (f"{fileout} creato!")

if __name__ == '__main__':
	if len(sys.argv[1:])<1:
		file=input("Inserisci nome file pdf:\n").strip()
	else:
		file=sys.argv[1]
	
	if len(sys.argv[2:])<1:
		intervals=[interval.strip() for interval in input("Inserisci intervalli separati da virgola (es: -9,10,11-20,21- oppure ogni 5*):\n").replace(" ","").split(",")]
	else:
		intervals="".join(sys.argv[2:]).replace(" ","").split(",")

	pdfsplit(file,intervals)
