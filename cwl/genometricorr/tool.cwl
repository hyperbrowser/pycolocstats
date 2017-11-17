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
      position: 0
  - id: t2
    type: File
    inputBinding:
      position: 1
  - id: chrlen
    type: File
    inputBinding:
      position: 2
  - id: t1Format
    type: string
  - id: t2Format
    type: string
  - id: doMapping
    type: boolean

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
          do.mapping=$(inputs.doMapping.toString().toUpperCase())

          [chromosomes]
          chr1
          chr2
          chr3

          [chromosomes.length]
          chr1=249250621

          [options]
          add.chr.as.prefix=FALSE
          awhole.only=FALSE
          suppress.evaluated.length.warning=FALSE
          cut.all.over.length=FALSE
          keep.distributions=TRUE
          showTkProgressBar=FALSE
          showProgressBar=FALSE

          [tests]
          ecdf.area.permut.number=10
          mean.distance.permut.number=10
          jaccard.measure.permut.number=10
          random.seed=1248312

      - entryname: genometricorr.r
        entry: |-
          library("GenometriCorr")
          config <- new("GenometriCorrConfig", "conf.ini")
          conf_res <- run.config(config)
          print(conf_res)
