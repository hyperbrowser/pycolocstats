class: CommandLineTool
cwlVersion: v1.0
id: giggle
baseCommand:
  - bash
  - entrypoint.sh

inputs:
  index_i:
    type:
      - "null"
      - type: array
        items: File
  index_o:
    type: string
  index_s:
    type: boolean?
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
    type: long?
  search_l:
    type: boolean?

  trackIndex:
    type: string?
  genome:
    type: string?
  trackCollection:
    type: string?

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
    dockerPull: 'conglomerate/giggle_test:latest'
  - class: InlineJavascriptRequirement
  - class: InitialWorkDirRequirement
    listing:
      - entryname: entrypoint.sh
        entry: |-
          mkdir input_files
          cp ${
            if (inputs.index_i != null) {
              var files = '';
              for (var i = 0; i < inputs.index_i.length; i++) {
                files += inputs.index_i[i].path + ' ';
              }
              return files;
            } else if (inputs.trackIndex != null && inputs.genome != null && inputs.trackCollection != null) {
              return '/regiondb/' + inputs.trackIndex + '/' + inputs.genome + '/' + inputs.trackCollection + '/regions/*';
            } else {
              throw 'You should specify either index_i or reference collection!';
            }
          } input_files/
          /root/giggle/scripts/sort_bed "input_files/*bed" input_files &> /dev/null
          /root/giggle/bin/giggle index \\\
          -o $(inputs.index_o) \\\
          -i "input_files/*gz" \\\
          $(inputs.index_s ? '-s' : '') \\\
          $(inputs.index_f ? '-f' : '')

          mkdir search_file
          ${
            if (inputs.search_q.path.endsWith('gz')) {
                return 'cp ' + inputs.search_q.path + ' search_file/'
              } else {
                return '/root/giggle/scripts/sort_bed ' + inputs.search_q.path + ' search_file &> /dev/null'
              }
          }

          #hackish way of accessing the query file, we assume

          /root/giggle/bin/giggle search \\\
          -i $(inputs.search_i) \\\
          -q search_file/\$(ls -Art search_file | tail -n 1)\\\
          $(inputs.search_o ? '-o' : '') \\\
          $(inputs.search_c ? '-c' : '') \\\
          $(inputs.search_s ? '-s' : '') \\\
          $(inputs.search_v ? '-v' : '') \\\
          $(inputs.search_g ? '-g ' + inputs.search_g : '') \\\
          $(inputs.search_l ? '-l' : '')

          chmod 755 -R $(inputs.index_o) $(inputs.search_i)
