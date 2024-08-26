from app.models.reconhecimento_facial import ReconhecimentoFacial

#UPLOAD_FOLDER = 'app/static/img/pessoasDesaparecidas/'


rf = ReconhecimentoFacial()
rf.treinar_modelo()
