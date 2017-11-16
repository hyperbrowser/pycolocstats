class: CommandLineTool
cwlVersion: v1.0
id: calculator
baseCommand:
  - Rscript
  - calculator.r
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
label: calculator
requirements:
  - class: DockerRequirement
    dockerPull: 'conglomerate/calculator:latest'
  - class: InitialWorkDirRequirement
    listing:
      - entryname: calculator.r
        entry: |-
          args <- commandArgs(TRUE)
          operation <- args[1]
          t1 <- args[2]
          t2 <- args[3]
          chrlen <- args[4]
          a <- as.double(args[5])
          b <- as.double(args[6])
          c <- as.double(args[7])
          print(paste(readLines(t1), collapse="\n"))
          print(paste(readLines(t2), collapse="\n"))
          print(paste(readLines(chrlen), collapse="\n"))
          switch(operation,
          add={
            print(a+b)
          },
          subtract={
            print(a-b)
          },
          factorial={
            print(factorial(c))
          },
          {
             print("function not found")
          }
          )
