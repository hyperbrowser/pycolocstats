class: CommandLineTool
cwlVersion: v1.0
id: genometricorr
baseCommand:
  - Rscript
  - genometricorr.r
inputs:
  - id: t1
    type: File
  - id: t2
    type: File
  - id: chrlen
    type: File
    inputBinding:
      loadContents: true
  - id: chrlist
    type: File?
    inputBinding:
      loadContents: true
  - id: t1Format
    type: string
  - id: t2Format
    type: string
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
          query.format=$(inputs.t1Format)
          reference=$(inputs.t2.path)
          reference.format=$(inputs.t2Format)
          $(inputs.doMapping ? 'do.mapping=' + inputs.doMapping : '')

          [chromosomes]
          $(inputs.chrlist ? inputs.chrlist.contents : '')

          [chromosomes.length]
          $(inputs.chrlen.contents.replace(/\t/g, '='))

          [options]
          showTkProgressBar=FALSE
          showProgressBar=FALSE
          $(inputs.addChrAsPrefix ? 'add.chr.as.prefix=' + inputs.addChrAsPrefix.toString().toUpperCase() : '')
          $(inputs.awholeOnly ? 'awhole.only=' + inputs.awholeOnly.toString().toUpperCase() : '')
          $(inputs.suppressEvaluatedLengthWarning ? 'suppress.evaluated.length.warning=' + inputs.suppressEvaluatedLengthWarning.toString().toUpperCase() : '')
          $(inputs.cutAllOverLength ? 'cut.all.over.length=' + inputs.cutAllOverLength.toString().toUpperCase() : '')
          $(inputs.keepDistributions ? 'keep.distributions=' + inputs.keepDistributions.toString().toUpperCase() : '')

          [tests]
          $(inputs.ecdfPermNum ? 'ecdf.area.permut.number=' + inputs.ecdfPermNum : '')
          $(inputs.meanPermNum ? 'mean.distance.permut.number=' + inputs.meanPermNum : '')
          $(inputs.jaccardPermNum ? 'jaccard.measure.permut.number=' + inputs.jaccardPermNum : '')
          $(inputs.randomSeed ? 'random.seed=' + inputs.randomSeed : '')

      - entryname: genometricorr.r
        entry: |-
          y <- gsub("\\\\n", "\n", readLines("conf.ini"))
          cat(y, file="conf.ini", sep="\n")
          library("GenometriCorr")
          config <- new("GenometriCorrConfig", "conf.ini")
          conf_res <- run.config(config)
          print(conf_res)
