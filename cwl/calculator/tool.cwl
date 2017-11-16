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
          a <- as.double(args[4])
          b <- as.double(args[5])
          c <- as.double(args[6])
          print(t1)
          print(t2)
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
