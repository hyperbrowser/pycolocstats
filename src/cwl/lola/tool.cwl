class: CommandLineTool
cwlVersion: v1.0
id: lola
baseCommand:
  - bash
  - entrypoint.sh

inputs:
  userset:
    type: File
  useruniverse:
    type: File
  regiondb:
    type:
      - "null"
      - type: array
        items: File
  trackIndex:
    type: string?
  genome:
    type: string?
  trackCollection:
    type: string?
  minOverlap:
    type: int?
  cores:
    type: int?
  redefineUserSets:
    type: boolean?
  fast:
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
    dockerPull: 'colocstats/lola:latest'
  - class: InlineJavascriptRequirement
  - class: InitialWorkDirRequirement
    listing:
      - entryname: entrypoint.sh
        entry: |-
          cp $(inputs.userset.path) .
          cp $(inputs.useruniverse.path) .
          mkdir -p regiondb/collection/regions
          cp ${
            if (inputs.regiondb != null) {
              var files = '';
              for (var i = 0; i < inputs.regiondb.length; i++) {
                files += inputs.regiondb[i].path + ' ';
              }
              return files;
            }
            return '';
          } regiondb/collection/regions
          Rscript lola.r
          wget -nv https://hyperbrowser.uio.no/hb/static/hyperbrowser/files/pycolocstats/lola/web.tar.gz
          tar xf web.tar.gz
          rm web.tar.gz
          rm web/allEnrichments.tsv
          mkdir -p lolaResults
          mv web/* lolaResults
          rm -rf web

      - entryname: lola.r
        entry: |-
          library("LOLA")
          library("GenomicRanges")
          library("simpleCache")
          regionset_1 = readBed('$(inputs.userset.basename)')
          userset = GRanges(regionset_1)
          regionset_2 = readBed('$(inputs.useruniverse.basename)')
          useruniverse = GRanges(regionset_2)
          # use this for loading LOLACore_170206 collection:
          # regionDB = loadRegionDB(dbLocation='/regiondb/LOLACore_170206/hg19/', collections=c('codex'))
          ${
            if (inputs.regiondb != null) {
              return "regionDB = loadRegionDB('regiondb')";
            } else if (inputs.trackIndex != null && inputs.genome != null && inputs.trackCollection != null) {
              return "regionDB = loadRegionDB(dbLocation='/regiondb/" + inputs.trackIndex + "/" + inputs.genome + "', collections=c('" + inputs.trackCollection + "'))";
            } else {
              throw 'You should specify either regiondb or reference collection!';
            }
          }
          locResults = runLOLA(userset, useruniverse, regionDB, minOverlap = $(inputs.minOverlap ? inputs.minOverlap : 1), cores = $(inputs.cores ? inputs.cores : 1), redefineUserSets = $(inputs.redefineUserSets ? inputs.redefineUserSets.toString().toUpperCase() : 'FALSE'))
          print(locResults)
          writeCombinedEnrichment(locResults, outFolder= "lolaResults", includeSplits=TRUE)
          con <- file("UniverseAppropriateness.txt")
          sink(con, append=TRUE)
          sink(con, append=TRUE, type="message")
          checkUniverseAppropriateness(userset, useruniverse, cores = cores = $(inputs.cores ? inputs.cores : 1), fast = $(inputs.fast ? inputs.fast.toString().toUpperCase() : 'FALSE'))