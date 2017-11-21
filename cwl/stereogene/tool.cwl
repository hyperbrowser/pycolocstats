class: CommandLineTool
cwlVersion: v1.0
id: stereogene
baseCommand:
  - bash
  - entrypoint.sh

inputs:
  - id: chrlen
    type: File
  - id: t1
    type: File
  - id: t2
    type: File

outputs:
  stdout:
    type: stdout
  stderr:
    type: stderr
  output:
    type: Directory
    outputBinding:
      glob: '.'

label: stereogene
requirements:
  - class: DockerRequirement
    dockerPull: 'conglomerate/stereogene:latest'
  - class: InlineJavascriptRequirement
  - class: InitialWorkDirRequirement
    listing:
      - entryname: entrypoint.sh
        entry: |-
          cp $(inputs.t1.path) .
          cp $(inputs.t2.path) .
          cp $(inputs.chrlen.path) .
          /root/stereogene/src/StereoGene -chrom $(inputs.chrlen.basename) $(inputs.t1.basename) $(inputs.t2.basename)