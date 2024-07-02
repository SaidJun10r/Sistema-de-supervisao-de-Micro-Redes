from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

# Criando PDF
cnv = canvas.Canvas("meu_pdf.pdf", pagesize=A4)

cnv.drawString(10, 20, "Controle, Supervisão e Automação de Microredes")
cnv.drawString(10, 10, "Said Ernandes de Moura Júnior")

cnv.save()