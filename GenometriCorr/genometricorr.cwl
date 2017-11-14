class: CommandLineTool
cwlVersion: v1.0
id: genometricorr
baseCommand:
  - Rscript
  - GenometriCorr.r
inputs:
  - id: r
    type: float?
    inputBinding:
      position: 0
      prefix: '-r'
  - id: x
    type: float
    inputBinding:
      position: 0
outputs: []
label: genometricorr
requirements:
  - class: ResourceRequirement
    ramMin: 100
    coresMin: 1
  - class: DockerRequirement
    dockerPull: 'conglomerate/genometricorr:latest'
  - class: InitialWorkDirRequirement
    listing:
      - entryname: GenometriCorr.r
        entry: |-
          args <- commandArgs(TRUE)
          r <- as.double(args[1])
          x <- as.double(args[2])
          r*x
