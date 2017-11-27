class: CommandLineTool
cwlVersion: v1.0
id: giggle
baseCommand:
  - bash
  - entrypoint.sh

inputs:
  - id: index_i
    type:
      type: array
      items: File
  - id: index_s
    type: boolean?
  - id: index_o
    type: string
  - id: index_f
    type: boolean?

  - id: search_i
    type: string
  - id: search_q
    type: File
  - id: search_o
    type: boolean?
  - id: search_c
    type: boolean?
  - id: search_s
    type: boolean?
  - id: search_v
    type: boolean?
  - id: search_g
    type: int?
  - id: search_l
    type: boolean?

outputs:
  stdout:
    type: stdout
  stderr:
    type: stderr
  output:
    type: Directory
    outputBinding:
      glob: '.'

label: giggle
requirements:
  - class: DockerRequirement
    dockerPull: 'conglomerate/giggle:latest'
  - class: InlineJavascriptRequirement
  - class: InitialWorkDirRequirement
    listing:
      - entryname: entrypoint.sh
        entry: |-
          su biodocker
          /home/biodocker/giggle/bin/giggle index -o $(inputs.index_o) -i ${
            var files = '';
            for (var i = 0; i < inputs.index_i.length; i++) {
              files += inputs.index_i[i].path + ' ';
            }
            return files;
          }
          /home/biodocker/giggle/bin/giggle search -i $(inputs.search_i) -q $(inputs.search_q.path)