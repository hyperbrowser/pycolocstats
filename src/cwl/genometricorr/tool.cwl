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
    dockerPull: 'colocstats/genometricorr:latest'
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

          output_rows <- c("query.population",
          "reference.population",
          "query.coverage",
          "reference.coverage",
          "relative.distances.ks.p.value",
          "relative.distances.ecdf.deviation.area",
          "relative.distances.ecdf.area.correlation",
          "query.reference.intersection",
          "query.reference.union",
          "jaccard.measure",
          "projection.test.p.value",
          "projection.test.lower.tail",
          "projection.test.obs.to.exp",
          "scaled.absolute.min.distance.sum",
          "relative.distances.ecdf.deviation.area.p.value",
          "scaled.absolute.min.distance.sum.p.value",
          "scaled.absolute.min.distance.sum.lower.tail",
          "jaccard.measure.p.value",
          "jaccard.measure.lower.tail")
          temp1 <- lapply(conf_res,function(x){x[output_rows]})
          temp2 <- do.call(cbind,temp1)
          temp3 <- as.data.frame(temp2)
          new_res <- apply(temp3,2,as.character)
          final_res <- as.data.frame(cbind(rownames(temp3),new_res))
          colnames(final_res)[1] <- "genomet.arguments"
          write.table(final_res, "GenometriCorr_Output.txt",row.names=F,quote=F,sep='\t')


