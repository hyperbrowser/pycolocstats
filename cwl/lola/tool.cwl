class: CommandLineTool
cwlVersion: v1.0
id: lola
baseCommand:
  - bash
  - entrypoint.sh

inputs:
  - id: userset
    type: File
  - id: useruniverse
    type: File
  - id: regiondb
    type:
      type: array
      items: File
outputs:
  stdout:
    type: stdout
  stderr:
    type: stderr
  output:
    type: Directory
    outputBinding:
      glob: '.'

label: lola
requirements:
  - class: DockerRequirement
    dockerPull: 'conglomerate/lola:latest'
  - class: InlineJavascriptRequirement
  - class: InitialWorkDirRequirement
    listing:
      - entryname: entrypoint.sh
        entry: |-
          cp $(inputs.userset.path) .
          cp $(inputs.useruniverse.path) .
          mkdir -p regiondb/collection/regions
          cp ${
            var files = '';
            for (var i = 0; i < inputs.regiondb.length; i++) {
              files += inputs.regiondb[i].path + ' ';
            }
            return files;
          } regiondb/collection/regions
          Rscript lola.r

      - entryname: lola.r
        entry: |-
          library("LOLA")
          library("GenomicRanges")
          regionset_1 = readBed('$(inputs.userset.basename)')
          userset = GRanges(regionset_1)
          regionset_2 = readBed('$(inputs.useruniverse.basename)')
          useruniverse = GRanges(regionset_2)
          regionDB = loadRegionDB('regiondb')
          locResults = runLOLA(userset, useruniverse, regionDB, cores=4)
          print(locResults)
          writeCombinedEnrichment(locResults, outFolder= "lolaResults", includeSplits=TRUE)