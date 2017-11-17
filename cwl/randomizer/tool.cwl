class: CommandLineTool
cwlVersion: v1.0
id: calculator
baseCommand:
  - Rscript
  - randomizer.r
inputs:
  - id: max
    type: int
    inputBinding:
      position: 0
  - id: 'n'
    type: int
    inputBinding:
      position: 1
  - id: chrlen
    type: File
    inputBinding:
      position: 2
outputs:
  stdout:
    type: stdout
  stderr:
    type: stderr
label: calculator
requirements:
  - class: DockerRequirement
    dockerPull: 'conglomerate/randomizer:latest'
  - class: InitialWorkDirRequirement
    listing:
      - entryname: randomizer.r
        entry: |-
          args <- commandArgs(TRUE)
          max <- as.integer(args[1])
          n <- as.integer(args[2])
          chrlen <- args[3]
          print(paste(readLines(chrlen), collapse="\n"))
          print(sample(1:max,n,replace=T))
