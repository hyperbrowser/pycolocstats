class: CommandLineTool
cwlVersion: v1.0
id: calculator
baseCommand:
  - Rscript
  - calculator.r
inputs:
  - id: operation
    type:
      type: enum
      symbols:
        - add
        - subtract
        - factorial
      name: operation
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
