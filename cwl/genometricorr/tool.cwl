class: CommandLineTool
cwlVersion: v1.0
id: genometricorr
baseCommand:
  - Rscript
  - genometricorr.r
inputs:
  - id: operation
    type: string
    inputBinding:
      position: 0
  - id: t1
    type: File
    inputBinding:
      position: 1
  - id: t2
    type: File
    inputBinding:
      position: 2
  - id: chrlen
    type: File
    inputBinding:
      position: 3
  - id: a
    type: float?
    inputBinding:
      position: 4
  - id: b
    type: float?
    inputBinding:
      position: 5
  - id: c
    type: int?
    inputBinding:
      position: 6
outputs:
  stdout:
    type: stdout
  stderr:
    type: stderr
label: genometricorr
requirements:
  - class: DockerRequirement
    dockerPull: 'conglomerate/genometricorr:latest'
  - class: InitialWorkDirRequirement
    listing:
      - entryname: genometricorr.r
        entry: |-
          library("GenometriCorr")
          library("rtracklayer")
          library("TxDb.Hsapiens.UCSC.hg19.knownGene")
          refseq <- transcripts(TxDb.Hsapiens.UCSC.hg19.knownGene)
          cpgis <- import(system.file("extdata", "UCSCcpgis_hg19.bed", package = "GenometriCorr"))
          seqinfo(cpgis) <- seqinfo(TxDb.Hsapiens.UCSC.hg19.knownGene)[seqnames(seqinfo(cpgis))]
