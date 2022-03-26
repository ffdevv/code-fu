from PyPDF2 import PdfFileMerger
import sys

def pdfmerge(files,output_filename):
	pdfs = files
	merger = PdfFileMerger()
	for pdf in pdfs:
		merger.append(open(pdf, 'rb'))
	with open(output_filename, 'wb') as fout:
		merger.write(fout)
	print("pdf creato!")

if __name__ == '__main__':
	if len(sys.argv[1:])<1:
		files=[file.strip() for file in input("Inserisci nomi files da unire separati da virgola (es. pdf1.pdf, pdf2.pdf):\n").split(",")]
	else:
		files=sys.argv[1:]
	output_filename=input("nome file destinazione: ")

	pdfmerge(files,output_filename)
