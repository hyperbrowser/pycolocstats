class: CommandLineTool
cwlVersion: v1.0
id: genometricorr
baseCommand:
  - Rscript
  - genometricorr.r

inputs:
  query:
    type: File
  reference:
    type: File
  chromosomes_length:
    type: File
    inputBinding:
      loadContents: true
  chromosomes:
    type: File?
    inputBinding:
      loadContents: true
  t1Format:
    type: string?
  t2Format:
    type: string?
  doMapping:
    type: boolean?
  addChrAsPrefix:
    type: boolean?
  awholeOnly:
    type: boolean?
  suppressEvaluatedLengthWarning:
    type: boolean?
  cutAllOverLength:
    type: boolean?
  keepDistributions:
    type: boolean?
  ecdfPermNum:
    type: int?
  meanPermNum:
    type: int?
  jaccardPermNum:
    type: int?
  randomSeed:
    type: int?

outputs:
  stdout:
    type: stdout
  stderr:
    type: stderr
  output:
    type: Directory
    outputBinding:
      glob: '.'

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
          query=$(inputs.query.path)
          $(inputs.t1Format ? 'query.format=' + inputs.t1Format : '')
          reference=$(inputs.reference.path)
          $(inputs.t2Format ? 'reference.format=' + inputs.t2Format : '')
          $(inputs.doMapping ? 'do.mapping=' + inputs.doMapping : '')

          [chromosomes]
          $(inputs.chromosomes ? inputs.chromosomes.contents : '')

          [chromosomes.length]
          $(inputs.chromosomes_length.contents.replace(/\t/g, '='))

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
          res_df <- do.call(cbind,conf_res)
          res_df <- as.data.frame(cbind(rownames(res_df),res_df))
          colnames(res_df)[1] <- "genomet.arguments"
          write.table(res_df, "GenometriCorr_Output.txt",row.names=F,quote=F,sep='\t')

