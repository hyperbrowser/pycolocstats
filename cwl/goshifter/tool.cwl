class: CommandLineTool
cwlVersion: v1.0
id: goshifter
baseCommand:
  - python
  - /root/goshifter/goshifter.py

inputs:
  i:
    type: File?
    inputBinding:
      prefix: -i
  s:
    type: File
    inputBinding:
      prefix: -s
  a:
    type: File
    inputBinding:
      prefix: -a
  p:
    type: int
    inputBinding:
      prefix: -p
  r:
    type: float?
    inputBinding:
      prefix: -r
  w:
    type: int?
    inputBinding:
      prefix: -w
  n:
    type: int?
    inputBinding:
      prefix: -n
  x:
    type: int?
    inputBinding:
      prefix: -x
  e:
    type: int?
    inputBinding:
      prefix: -e
  no-ld:
    type: boolean?
    inputBinding:
      prefix: --no-ld
  l:
    type: string?
    inputBinding:
      prefix: -l
  o:
    type: string?
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

label: goshifter
requirements:
  - class: DockerRequirement
    dockerPull: 'conglomerate/goshifter:latest'
