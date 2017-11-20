class: CommandLineTool
cwlVersion: v1.0
id: genometricorr
baseCommand:
  - Rscript
  - genometricorr.r
inputs:
  - id: t1
    type: File
    inputBinding:
  - id: t2
    type: File
    inputBinding:
  - id: chrlen
    type: File
    inputBinding:
      loadContents: true
  - id: chrlist
    type: File?
    inputBinding:
      loadContents: true
  - id: t1Format
    type: string?
  - id: t2Format
    type: string?
  - id: doMapping
    type: boolean?
  - id: addChrAsPrefix
    type: boolean?
  - id: awholeOnly
    type: boolean?
  - id: suppressEvaluatedLengthWarning
    type: boolean?
  - id: cutAllOverLength
    type: boolean?
  - id: keepDistributions
    type: boolean?
  - id: ecdfPermNum
    type: int?
  - id: meanPermNum
    type: int?
  - id: jaccardPermNum
    type: int?
  - id: randomSeed
    type: int?

outputs:
  stdout:
    type: stdout
  stderr:
    type: stderr
label: genometricorr
requirements:
  - class: DockerRequirement
    dockerPull: 'conglomerate/genometricorr:latest'
  - class: InlineJavascriptRequirement
  - class: InitialWorkDirRequirement
    listing:
      - entryname: conf.ini
        entry: |-
          [data]
          query=$(inputs.t1.path)
          query.format=$(inputs.t1Format ? inputs.t1Format : 'bed')
          reference=$(inputs.t2.path)
          reference.format=$(inputs.t2Format ? inputs.t2Format : 'bed')
          do.mapping=$(inputs.doMapping ? inputs.doMapping.toString().toUpperCase() : 'FALSE')

          [chromosomes]
          $(inputs.chrlist ? inputs.chrlist.contents : '')
          [chromosomes.length]
          $(inputs.chrlen.contents)

          [options]
          add.chr.as.prefix=$(inputs.addChrAsPrefix ? inputs.addChrAsPrefix.toString().toUpperCase() : 'FALSE')
          awhole.only=$(inputs.awholeOnly ? inputs.awholeOnly.toString().toUpperCase() : 'FALSE')
          suppress.evaluated.length.warning=$(inputs.suppressEvaluatedLengthWarning ? inputs.suppressEvaluatedLengthWarning.toString().toUpperCase() : 'FALSE')
          cut.all.over.length=$(inputs.cutAllOverLength ? inputs.cutAllOverLength.toString().toUpperCase() : 'FALSE')
          keep.distributions=$(inputs.keepDistributions ? inputs.keepDistributions.toString().toUpperCase() : 'TRUE')
          showTkProgressBar=FALSE
          showProgressBar=FALSE

          [tests]
          ecdf.area.permut.number=$(inputs.ecdfPermNum ? inputs.ecdfPermNum : 10)
          mean.distance.permut.number=$(inputs.meanPermNum ? inputs.meanPermNum : 10)
          jaccard.measure.permut.number=$(inputs.jaccardPermNum ? inputs.jaccardPermNum : 10)
          random.seed=$(inputs.randomSeed ? inputs.randomSeed : 1248312)

      - entryname: genometricorr.r
        entry: |-
          y <- gsub("\\\\n", "\n", readLines("conf.ini"))
          cat(y, file="conf.ini", sep="\n")
          library("GenometriCorr")
          config <- new("GenometriCorrConfig", "conf.ini")
          conf_res <- run.config(config)
          print(conf_res)
