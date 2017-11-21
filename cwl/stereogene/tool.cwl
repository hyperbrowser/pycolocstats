class: CommandLineTool
cwlVersion: v1.0
id: stereogene
baseCommand:
  - bash
  - entrypoint.sh

inputs:
  - id: t1
    type: File
  - id: t2
    type: File
  - id: chrom
    type: File
    inputBinding:
      prefix: -chrom
  - id: v
    type: boolean?
    inputBinding:
      prefix: -v
  - id: syntax
    type: boolean?
    inputBinding:
      prefix: -syntax
  - id: verbose
    type: int?
    inputBinding:
      prefix: -verbose
  - id: s
    type: boolean?
    inputBinding:
      prefix: -s
  - id: silent
    type: int?
    inputBinding:
      prefix: -silent
  - id: bin
    type: int?
    inputBinding:
      prefix: -bin
  - id: clear
    type: int?
    inputBinding:
      prefix: -clear
  - id: c
    type: boolean?
    inputBinding:
      prefix: -c
  - id: cfg
    type: File?
    inputBinding:
      prefix: -cfg
  - id: profPath
    type: string?
    inputBinding:
      prefix: -profPath
  - id: trackPath
    type: string?
    inputBinding:
      prefix: -trackPath
  - id: resPath
    type: string?
    inputBinding:
      prefix: -resPath
  - id: confounder
    type: string?
    inputBinding:
      prefix: -confounder
  - id: statistics
    type: string?
    inputBinding:
      prefix: -statistics
  - id: params
    type: string?
    inputBinding:
      prefix: -params
  - id: log
    type: string?
    inputBinding:
      prefix: -log
  - id: BufSize
    type: int?
    inputBinding:
      prefix: -BufSize
  - id: bpType
    type: string?
    inputBinding:
      prefix: -bpType
  - id: pcorProfile
    type: string?
    inputBinding:
      prefix: -pcorProfile
  - id: NA
    type: boolean?
    inputBinding:
      prefix: -NA
  - id: threshold
    type: int?
    inputBinding:
      prefix: -threshold
  - id: kernelSigma
    type: float?
    inputBinding:
      prefix: -kernelSigma
  - id: wSize
    type: int?
    inputBinding:
      prefix: -wSize
  - id: maxNA
    type: float?
    inputBinding:
      prefix: -maxNA
  - id: maxZero
    type: float?
    inputBinding:
      prefix: -maxZero
  - id: nShuffle
    type: int?
    inputBinding:
      prefix: -nShuffle
  - id: outSpectr
    type: int?
    inputBinding:
      prefix: -outSpectr
  - id: outChrom
    type: int?
    inputBinding:
      prefix: -outChrom
  - id: writeDistr
    type: int?
    inputBinding:
      prefix: -writeDistr
  - id: r
    type: boolean?
    inputBinding:
      prefix: -r
  - id: crossWidth
    type: boolean?
    inputBinding:
      prefix: -crossWidth
  - id: Distances
    type: boolean?
    inputBinding:
      prefix: -Distances
  - id: outLC
    type: int?
    inputBinding:
      prefix: -outLC
  - id: lc
    type: boolean?
    inputBinding:
      prefix: -lc
  - id: LCScale
    type: string?
    inputBinding:
      prefix: -LCScale
  - id: L_FDR
    type: float?
    inputBinding:
      prefix: -L_FDR
  - id: R_FDR
    type: float?
    inputBinding:
      prefix: -R_FDR
  - id: outRes
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
    dockerPull: 'conglomerate/stereogene:latest'
  - class: InlineJavascriptRequirement
  - class: InitialWorkDirRequirement
    listing:
      - entryname: entrypoint.sh
        entry: |-
          cp $(inputs.t1.path) .
          cp $(inputs.t2.path) .
          /root/stereogene/src/StereoGene "$@" $(inputs.t1.basename) $(inputs.t2.basename)