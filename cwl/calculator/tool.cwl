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
  - id: a
    type: float?
    inputBinding:
      position: 1
  - id: b
    type: float?
    inputBinding:
      position: 2
  - id: c
    type: int?
    inputBinding:
      position: 3
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
    dockerPull: 'conglomerate/calculator:latest'
  - class: InitialWorkDirRequirement
    listing:
      - entryname: calculator.r
        entry: |-
          args <- commandArgs(TRUE)
          operation <- args[1]
          a <- as.double(args[2])
          b <- as.double(args[3])
          c <- as.double(args[4])
          t1 <- args[5]
          t2 <- args[6]
          print(t1)
          print(t2)
          switch(operation, 
          add={
            a+b
          },
          subtract={
            a-b 
          },
          factorial={
            factorial(c)
          },
          {
             print("function not found")
          }
          )
