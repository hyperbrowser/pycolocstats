class: CommandLineTool
cwlVersion: v1.0
id: geometricorr
baseCommand:
  - Rscript
  - geometricorr.r
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
  - id: a
    type: float?
    inputBinding:
      position: 3
  - id: b
    type: float?
    inputBinding:
      position: 4
  - id: c
    type: int?
    inputBinding:
      position: 5
outputs:
  stdout:
    type: stdout
  stderr:
    type: stderr
label: geometricorr
requirements:
  - class: DockerRequirement
    dockerPull: 'conglomerate/geometricorr:latest'
  - class: InitialWorkDirRequirement
    listing:
      - entryname: geometricorr.r
        entry: |-
          library("GenometriCorr")
          library("rtracklayer")
          library("TxDb.Hsapiens.UCSC.hg19.knownGene")
          refseq <- transcripts(TxDb.Hsapiens.UCSC.hg19.knownGene)
          cpgis <- import(system.file("extdata", "UCSCcpgis_hg19.bed", package = "GenometriCorr"))
          seqinfo(cpgis) <- seqinfo(TxDb.Hsapiens.UCSC.hg19.knownGene)[seqnames(seqinfo(cpgis))]
