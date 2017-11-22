class: CommandLineTool
cwlVersion: v1.0
id: intervalstats
baseCommand:
  - IntervalStats

inputs:
  - id: q
    type: File
    inputBinding:
      prefix: -q
  - id: r
    type: File
    inputBinding:
      prefix: -r
  - id: d
    type: File
    inputBinding:
      prefix: -d
  - id: o
    type: string
    inputBinding:
      prefix: -o

outputs:
  stdout:
    type: stdout
  stderr:
    type: stderr
  output:
    type: Directory
    outputBinding:
      glob: '.'

label: intervalstats
requirements:
  - class: DockerRequirement
    dockerPull: 'conglomerate/intervalstats:latest'
