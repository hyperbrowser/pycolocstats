class: CommandLineTool
cwlVersion: v1.0
id: giggle
baseCommand:
  - bash
  - entrypoint.sh

inputs:
  index_i:
    type:
      type: array
      items: File
  index_s:
    type: boolean?
  index_o:
    type: string
  index_f:
    type: boolean?

  search_i:
    type: string
  search_q:
    type: File
  search_o:
    type: boolean?
  search_c:
    type: boolean?
  search_s:
    type: boolean?
  search_v:
    type: boolean?
  search_g:
    type: int?
  search_l:
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
          /root/giggle/bin/giggle index -o $(inputs.index_o) -i ${
            var files = '';
            for (var i = 0; i < inputs.index_i.length; i++) {
              files += inputs.index_i[i].path + ' ';
            }
            return files;
          }
          /root/giggle/bin/giggle search -i $(inputs.search_i) -q $(inputs.search_q.path)
          chmod 755 -R $(inputs.index_o) $(inputs.search_i)
