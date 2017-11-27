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
      - "null"
      - type: array
        items: File
  - id: minOverlap
    type: int?
  - id: cores
    type: int?
  - id: redefineUserSets
    type: boolean?
  - id: fast
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

label: lola
requirements:
  - class: DockerRequirement
    dockerPull: 'conglomerate/lola:latest'
  - class: InlineJavascriptRequirement
  - class: InitialWorkDirRequirement
    listing:
      - entryname: entrypoint.sh
        entry: |-
          su biodocker
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
          # use this for loading LOLACore_170206 collection:
          # regionDB = loadRegionDB('/home/biodocker/LOLACore_170206/scratch/ns5bc')
          regionDB = loadRegionDB('regiondb')
          locResults = runLOLA(userset, useruniverse, regionDB, minOverlap = $(inputs.minOverlap ? inputs.minOverlap : 1), cores = $(inputs.cores ? inputs.cores : 1), redefineUserSets = $(inputs.redefineUserSets ? inputs.redefineUserSets.toString().toUpperCase() : 'FALSE'))
          print(locResults)
          writeCombinedEnrichment(locResults, outFolder= "lolaResults", includeSplits=TRUE)
          con <- file("UniverseAppropriateness.txt")
          sink(con, append=TRUE)
          sink(con, append=TRUE, type="message")
          checkUniverseAppropriateness(userset, useruniverse, cores = cores = $(inputs.cores ? inputs.cores : 1), fast = $(inputs.fast ? inputs.fast.toString().toUpperCase() : 'FALSE'))