class: CommandLineTool
cwlVersion: v1.0
id: intervalstats
baseCommand:
  - IntervalStats

inputs:
  q:
    type: File
    inputBinding:
      prefix: -q
  r:
    type: File
    inputBinding:
      prefix: -r
  d:
    type: File
    inputBinding:
      prefix: -d
  o:
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
    dockerPull: 'colocstats/intervalstats:latest'
