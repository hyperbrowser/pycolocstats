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
  - id: t1
    type: File
    inputBinding:
      position: 4
  - id: t2
    type: File
    inputBinding:
      position: 5
outputs:
  output:
    type: stdout
stderr: error.txt
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
          t1 <- args[3]
          t2 <- args[4]
          print(t1)
          print(t2)
          sample(1:max,n,replace=T)
