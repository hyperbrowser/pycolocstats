class: CommandLineTool
cwlVersion: v1.0
id: stereogene
baseCommand:
  - bash
  - entrypoint.sh

inputs:
  chrom:
    type: File
    inputBinding:
      prefix: -chrom
      position: 0
  query:
    type: File
    inputBinding:
      position: 1
  reference:
    type: File
    inputBinding:
      position: 2
  v:
    type: boolean?
    inputBinding:
      prefix: -v
  syntax:
    type: boolean?
    inputBinding:
      prefix: -syntax
  verbose:
    type: int?
    inputBinding:
      prefix: -verbose
  s:
    type: boolean?
    inputBinding:
      prefix: -s
  silent:
    type: int?
    inputBinding:
      prefix: -silent
  bin:
    type: int?
    inputBinding:
      prefix: -bin
  clear:
    type: int?
    inputBinding:
      prefix: -clear
  c:
    type: boolean?
    inputBinding:
      prefix: -c
  cfg:
    type: File?
    inputBinding:
      prefix: -cfg
  profPath:
    type: string?
    inputBinding:
      prefix: -profPath
  trackPath:
    type: string?
    inputBinding:
      prefix: -trackPath
  resPath:
    type: string?
    inputBinding:
      prefix: -resPath
  confounder:
    type: string?
    inputBinding:
      prefix: -confounder
  statistics:
    type: string?
    inputBinding:
      prefix: -statistics
  params:
    type: string?
    inputBinding:
      prefix: -params
  log:
    type: string?
    inputBinding:
      prefix: -log
  BufSize:
    type: int?
    inputBinding:
      prefix: -BufSize
  bpType:
    type: string?
    inputBinding:
      prefix: -bpType
  pcorProfile:
    type: string?
    inputBinding:
      prefix: -pcorProfile
  NA:
    type: boolean?
    inputBinding:
      prefix: -NA
  threshold:
    type: int?
    inputBinding:
      prefix: -threshold
  kernelSigma:
    type: float?
    inputBinding:
      prefix: -kernelSigma
  wSize:
    type: int?
    inputBinding:
      prefix: -wSize
  maxNA:
    type: float?
    inputBinding:
      prefix: -maxNA
  maxZero:
    type: float?
    inputBinding:
      prefix: -maxZero
  nShuffle:
    type: int?
    inputBinding:
      prefix: -nShuffle
  outSpectr:
    type: int?
    inputBinding:
      prefix: -outSpectr
  outChrom:
    type: int?
    inputBinding:
      prefix: -outChrom
  writeDistr:
    type: int?
    inputBinding:
      prefix: -writeDistr
  r:
    type: boolean?
    inputBinding:
      prefix: -r
  crossWidth:
    type: boolean?
    inputBinding:
      prefix: -crossWidth
  Distances:
    type: boolean?
    inputBinding:
      prefix: -Distances
  outLC:
    type: int?
    inputBinding:
      prefix: -outLC
  lc:
    type: boolean?
    inputBinding:
      prefix: -lc
  LCScale:
    type: string?
    inputBinding:
      prefix: -LCScale
  L_FDR:
    type: float?
    inputBinding:
      prefix: -L_FDR
  R_FDR:
    type: float?
    inputBinding:
      prefix: -R_FDR
  outRes:
    type: string?
    inputBinding:
      prefix: -outRes

outputs:
  stdout:
    type: stdout
  stderr:
    type: stderr
  output:
    type: Directory
    outputBinding:
      glob: '.'

label: stereogene
requirements:
  - class: DockerRequirement
    dockerPull: 'colocstats/stereogene:latest'
  - class: InlineJavascriptRequirement
  - class: InitialWorkDirRequirement
    listing:
      - entryname: entrypoint.sh
        entry: |-
          cp $(inputs.chrom.path) .
          cp $(inputs.query.path) .
          cp $(inputs.reference.path) .
          /root/stereogene/src/StereoGene -chrom $(inputs.chrom.basename) $(inputs.query.basename) $(inputs.reference.basename) \$(echo "$@" | sed 's@/private/[^ ]*@@g' | sed 's@/var/[^ ]*@@g' | sed 's@-chrom[^ ]*@@g')
          Rscript *_report.r
          chmod a+w -R *.html