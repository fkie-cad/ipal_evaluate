== Status ==
###IGNORE-LINE###
Using FIFO scheduling algorithm.
###IGNORE-LINE###
###IGNORE-LINE###
###IGNORE-LINE###
###IGNORE-LINE###
###IGNORE-LINE###
###IGNORE-LINE###
###IGNORE-LINE###
###IGNORE-LINE###
###IGNORE-LINE###
###IGNORE-LINE###
###IGNORE-LINE###


###IGNORE-LINE###
  Accuracy: 0.8329514684440742
  Affiliation-F0.1: .nan
  Affiliation-F0.5: .nan
  Affiliation-F1: .nan
  Affiliation-F10: .nan
  Affiliation-F2: .nan
  Affiliation-Precision: .nan
  Affiliation-Recall: 0.0
  Average-Time-to-Detection: .nan
  BATADAL: 0.25
  BATADAL-CLF: 0.5
  BATADAL-TTD: 0.0
  Detected-Scenarios: []
  Detected-Scenarios-Percent: 0.0
  Detection-Delay: 0
  F0.1: 0
  F0.5: 0
  F1: 0
  F10: 0
  F2: 0
  FPA: 0
  Fallout: 0.0
  Informedness: 0.0
  Inverse-Precision: 0.8329514684440742
  Inverse-Recall: 1.0
  Jaccard-Distance: 1.0
  Jaccard-Index: 0.0
  MCC: 0
  Markedness: -0.1670485315559258
  Missrate: 1.0
  NAB-score-default: 0.0
  NAB-score-low-fn: 0.0
  NAB-score-low-fp: 0.0
  Penalty-Score: 0
  Precision: 0
  Recall: 0.0
  Scenario-Recall:
    '1': 0.0
  TPA: 0
  _evaluation-config:
    alarm_gracetime: 0
###IGNORE-LINE###
    batadal_gamma: 0.5
    compresslevel: 6
    eTaPR_delta: 0.0
    eTaPR_theta_p: 0.5
    eTaPR_theta_r: 0.01
    fscore_beta: [0.1, 0.5, 1, 2, 10]
    input: output.state.gz
    log: 30
    logfile: logfile.txt
    logformat: '%(levelname)s:%(name)s: %(message)s'
    nab_profiles:
      default:
        nab_afn: -1
        nab_afp: -0.11
        nab_atp: 1
      reward_low_fn:
        nab_afn: -2.0
        nab_afp: -0.11
        nab_atp: 1
      reward_low_fp:
        nab_afn: -1
        nab_afp: -0.22
        nab_atp: 1
    output: evaluate.json
    timed_dataset: true
###IGNORE-LINE###
  _iids-config:
    alerts: null
    alerts_update: false
    combiner:
      _type: Matrix
      keys:
      - MinMax
      - Gradient
      - Exists
      lookahead: 0
      matrix:
      - - 0.1915194503788923
      - - 0.6221087710398319
      - - 0.4377277390071145
      model-file: model-combiner
      threshold: 0.7853585837137692
      use_scores: false
    combiner_config: config-combiner.json
    compresslevel: 6
    config: config-iids.json
    hostname: false
    idss:
      Exists:
        _type: ExistsIDS
        exclude: []
        model-file: Exists
        threshold: 10.0
      Gradient:
        _type: MinMax
        allow-none: false
        discrete_threshold: 10
        features: [state;1, state;2, state;3, state;4, state;5, state;6, state;7, state;8,
          state;9, state;10, state;11, state;12, state;13, state;14, state;15, state;16,
          state;17, state;18, state;19, state;20, state;21, state;22, state;23, state;24,
          state;25, state;26, state;27, state;28, state;29, state;30, state;31, state;32,
          state;33, state;34, state;35, state;36, state;37, state;38, state;39, state;40,
          state;41]
        model-file: Gradient
        preprocessors:
        - features: [state;1, state;2, state;3, state;4, state;5, state;6, state;7,
            state;8, state;9, state;10, state;11, state;12, state;13, state;14, state;15,
            state;16, state;17, state;18, state;19, state;20, state;21, state;22, state;23,
            state;24, state;25, state;26, state;27, state;28, state;29, state;30, state;31,
            state;32, state;33, state;34, state;35, state;36, state;37, state;38, state;39,
            state;40, state;41]
          method: Gradient
        save-training: null
        threshold: 1.0
        trainon: 1.0
      MinMax:
        _type: MinMax
        allow-none: false
        discrete_threshold: 10
        features: [state;1, state;2, state;3, state;4, state;5, state;6, state;7, state;8,
          state;9, state;10, state;11, state;12, state;13, state;14, state;15, state;16,
          state;17, state;18, state;19, state;20, state;21, state;22, state;23, state;24,
          state;25, state;26, state;27, state;28, state;29, state;30, state;31, state;32,
          state;33, state;34, state;35, state;36, state;37, state;38, state;39, state;40,
          state;41]
        model-file: MinMax
        preprocessors: []
        save-training: null
        threshold: 1.0
        trainon: 1.0
    live_ipal: null
###IGNORE-LINE###
    log: 30
    logfile: logfile.txt
    logformat: '%(levelname)s:%(name)s:%(message)s'
    output: test.ipal
    retrain: false
    train_combiner: null
    train_ipal: null
    train_state: null
###IGNORE-LINE###
###IGNORE-LINE###
  done: true
  eTaF0.1: 0
  eTaF0.5: 0
  eTaF1: 0
  eTaF10: 0
  eTaF2: 0
  eTaP: 0
  eTaR: 0
  fn: 802
  fp: 0
###IGNORE-LINE###
  iterations_since_restore: 1
###IGNORE-LINE###
###IGNORE-LINE###
###IGNORE-LINE###
###IGNORE-LINE###
###IGNORE-LINE###
###IGNORE-LINE###
  tn: 3999
  tp: 0
  training_iteration: 1
###IGNORE-LINE###
  
###IGNORE-LINE###
###IGNORE-LINE###
  Accuracy: 0.9825036450739429
###IGNORE-LINE###
###IGNORE-LINE###
###IGNORE-LINE###
###IGNORE-LINE###
###IGNORE-LINE###
###IGNORE-LINE###
###IGNORE-LINE###
  Average-Time-to-Detection: 5.0
  BATADAL: 0.9714419779279582
  BATADAL-CLF: 0.9491261531093497
  BATADAL-TTD: 0.9937578027465668
  Detected-Scenarios:
  - '1'
  Detected-Scenarios-Percent: 1.0
  Detection-Delay: 5
  F0.1: 0.9947952241742029
  F0.5: 0.9748512709572743
  F1: 0.9449541284403671
  F10: 0.8998690129009935
  F2: 0.9168362156663276
  FPA: 3
  Fallout: 0.0007501875468867217
  Informedness: 0.8982523062186993
  Inverse-Precision: 0.9801324503311258
  Inverse-Recall: 0.9992498124531133
  Jaccard-Distance: 0.10434782608695647
  Jaccard-Index: 0.8956521739130435
  MCC: 0.9363141534585618
  Markedness: 0.9759888039222862
  Missrate: 0.10099750623441396
  NAB-score-default: 83.47866918562391
  NAB-score-low-fn: 88.98577945708261
  NAB-score-low-fp: 66.9786691856239
  Penalty-Score: 3
  Precision: 0.9958563535911602
  Recall: 0.899002493765586
  Scenario-Recall:
    '1': 0.899002493765586
  TPA: 19
  _evaluation-config:
    alarm_gracetime: 0
###IGNORE-LINE###
    batadal_gamma: 0.5
    compresslevel: 6
    eTaPR_delta: 0.0
    eTaPR_theta_p: 0.5
    eTaPR_theta_r: 0.01
    fscore_beta: [0.1, 0.5, 1, 2, 10]
    input: output.state.gz
    log: 30
    logfile: logfile.txt
    logformat: '%(levelname)s:%(name)s: %(message)s'
    nab_profiles:
      default:
        nab_afn: -1
        nab_afp: -0.11
        nab_atp: 1
      reward_low_fn:
        nab_afn: -2.0
        nab_afp: -0.11
        nab_atp: 1
      reward_low_fp:
        nab_afn: -1
        nab_afp: -0.22
        nab_atp: 1
    output: evaluate.json
    timed_dataset: true
###IGNORE-LINE###
  _iids-config:
    alerts: null
    alerts_update: false
    combiner:
      _type: Matrix
      keys:
      - MinMax
      - Gradient
      - Exists
      lookahead: 0
      matrix:
      - - 0.7799758081188035
      - - 0.2725926052826416
      - - 0.2764642551430967
      model-file: model-combiner
      threshold: 0.8018721775350193
      use_scores: false
    combiner_config: config-combiner.json
    compresslevel: 6
    config: config-iids.json
    hostname: false
    idss:
      Exists:
        _type: ExistsIDS
        exclude: []
        model-file: Exists
        threshold: 10.0
      Gradient:
        _type: MinMax
        allow-none: false
        discrete_threshold: 10
        features: [state;1, state;2, state;3, state;4, state;5, state;6, state;7, state;8,
          state;9, state;10, state;11, state;12, state;13, state;14, state;15, state;16,
          state;17, state;18, state;19, state;20, state;21, state;22, state;23, state;24,
          state;25, state;26, state;27, state;28, state;29, state;30, state;31, state;32,
          state;33, state;34, state;35, state;36, state;37, state;38, state;39, state;40,
          state;41]
        model-file: Gradient
        preprocessors:
        - features: [state;1, state;2, state;3, state;4, state;5, state;6, state;7,
            state;8, state;9, state;10, state;11, state;12, state;13, state;14, state;15,
            state;16, state;17, state;18, state;19, state;20, state;21, state;22, state;23,
            state;24, state;25, state;26, state;27, state;28, state;29, state;30, state;31,
            state;32, state;33, state;34, state;35, state;36, state;37, state;38, state;39,
            state;40, state;41]
          method: Gradient
        save-training: null
        threshold: 1.0
        trainon: 1.0
      MinMax:
        _type: MinMax
        allow-none: false
        discrete_threshold: 10
        features: [state;1, state;2, state;3, state;4, state;5, state;6, state;7, state;8,
          state;9, state;10, state;11, state;12, state;13, state;14, state;15, state;16,
          state;17, state;18, state;19, state;20, state;21, state;22, state;23, state;24,
          state;25, state;26, state;27, state;28, state;29, state;30, state;31, state;32,
          state;33, state;34, state;35, state;36, state;37, state;38, state;39, state;40,
          state;41]
        model-file: MinMax
        preprocessors: []
        save-training: null
        threshold: 1.0
        trainon: 1.0
    live_ipal: null
###IGNORE-LINE###
    log: 30
    logfile: logfile.txt
    logformat: '%(levelname)s:%(name)s:%(message)s'
    output: test.ipal
    retrain: false
    train_combiner: null
    train_ipal: null
    train_state: null
###IGNORE-LINE###
###IGNORE-LINE###
  done: true
  eTaF0.1: 0.9506473260754612
  eTaF0.5: 0.9504270643119961
  eTaF1: 0.950079671277355
  eTaF10: 0.9495126939958487
  eTaF2: 0.9497325321029638
  eTaP: 0.9506588008394444
  eTaR: 0.949501246882793
  fn: 81
  fp: 3
###IGNORE-LINE###
  iterations_since_restore: 1
###IGNORE-LINE###
###IGNORE-LINE###
###IGNORE-LINE###
###IGNORE-LINE###
###IGNORE-LINE###
###IGNORE-LINE###
  tn: 3996
  tp: 721
  training_iteration: 1
###IGNORE-LINE###
  
###IGNORE-LINE###
###IGNORE-LINE###
  Accuracy: 0.9825036450739429
###IGNORE-LINE###
###IGNORE-LINE###
###IGNORE-LINE###
###IGNORE-LINE###
###IGNORE-LINE###
###IGNORE-LINE###
###IGNORE-LINE###
  Average-Time-to-Detection: 5.0
  BATADAL: 0.9714419779279582
  BATADAL-CLF: 0.9491261531093497
  BATADAL-TTD: 0.9937578027465668
  Detected-Scenarios:
  - '1'
  Detected-Scenarios-Percent: 1.0
  Detection-Delay: 5
  F0.1: 0.9947952241742029
  F0.5: 0.9748512709572743
  F1: 0.9449541284403671
  F10: 0.8998690129009935
  F2: 0.9168362156663276
  FPA: 3
  Fallout: 0.0007501875468867217
  Informedness: 0.8982523062186993
  Inverse-Precision: 0.9801324503311258
  Inverse-Recall: 0.9992498124531133
  Jaccard-Distance: 0.10434782608695647
  Jaccard-Index: 0.8956521739130435
  MCC: 0.9363141534585618
  Markedness: 0.9759888039222862
  Missrate: 0.10099750623441396
  NAB-score-default: 83.47866918562391
  NAB-score-low-fn: 88.98577945708261
  NAB-score-low-fp: 66.9786691856239
  Penalty-Score: 3
  Precision: 0.9958563535911602
  Recall: 0.899002493765586
  Scenario-Recall:
    '1': 0.899002493765586
  TPA: 19
  _evaluation-config:
    alarm_gracetime: 0
###IGNORE-LINE###
    batadal_gamma: 0.5
    compresslevel: 6
    eTaPR_delta: 0.0
    eTaPR_theta_p: 0.5
    eTaPR_theta_r: 0.01
    fscore_beta: [0.1, 0.5, 1, 2, 10]
    input: output.state.gz
    log: 30
    logfile: logfile.txt
    logformat: '%(levelname)s:%(name)s: %(message)s'
    nab_profiles:
      default:
        nab_afn: -1
        nab_afp: -0.11
        nab_atp: 1
      reward_low_fn:
        nab_afn: -2.0
        nab_afp: -0.11
        nab_atp: 1
      reward_low_fp:
        nab_afn: -1
        nab_afp: -0.22
        nab_atp: 1
    output: evaluate.json
    timed_dataset: true
###IGNORE-LINE###
  _iids-config:
    alerts: null
    alerts_update: false
    combiner:
      _type: Matrix
      keys:
      - MinMax
      - Gradient
      - Exists
      lookahead: 0
      matrix:
      - - 0.9581393536837052
      - - 0.8759326347420947
      - - 0.35781726995786667
      model-file: model-combiner
      threshold: 0.5009951255234587
      use_scores: false
    combiner_config: config-combiner.json
    compresslevel: 6
    config: config-iids.json
    hostname: false
    idss:
      Exists:
        _type: ExistsIDS
        exclude: []
        model-file: Exists
        threshold: 10.0
      Gradient:
        _type: MinMax
        allow-none: false
        discrete_threshold: 10
        features: [state;1, state;2, state;3, state;4, state;5, state;6, state;7, state;8,
          state;9, state;10, state;11, state;12, state;13, state;14, state;15, state;16,
          state;17, state;18, state;19, state;20, state;21, state;22, state;23, state;24,
          state;25, state;26, state;27, state;28, state;29, state;30, state;31, state;32,
          state;33, state;34, state;35, state;36, state;37, state;38, state;39, state;40,
          state;41]
        model-file: Gradient
        preprocessors:
        - features: [state;1, state;2, state;3, state;4, state;5, state;6, state;7,
            state;8, state;9, state;10, state;11, state;12, state;13, state;14, state;15,
            state;16, state;17, state;18, state;19, state;20, state;21, state;22, state;23,
            state;24, state;25, state;26, state;27, state;28, state;29, state;30, state;31,
            state;32, state;33, state;34, state;35, state;36, state;37, state;38, state;39,
            state;40, state;41]
          method: Gradient
        save-training: null
        threshold: 1.0
        trainon: 1.0
      MinMax:
        _type: MinMax
        allow-none: false
        discrete_threshold: 10
        features: [state;1, state;2, state;3, state;4, state;5, state;6, state;7, state;8,
          state;9, state;10, state;11, state;12, state;13, state;14, state;15, state;16,
          state;17, state;18, state;19, state;20, state;21, state;22, state;23, state;24,
          state;25, state;26, state;27, state;28, state;29, state;30, state;31, state;32,
          state;33, state;34, state;35, state;36, state;37, state;38, state;39, state;40,
          state;41]
        model-file: MinMax
        preprocessors: []
        save-training: null
        threshold: 1.0
        trainon: 1.0
    live_ipal: null
###IGNORE-LINE###
    log: 30
    logfile: logfile.txt
    logformat: '%(levelname)s:%(name)s:%(message)s'
    output: test.ipal
    retrain: false
    train_combiner: null
    train_ipal: null
    train_state: null
###IGNORE-LINE###
###IGNORE-LINE###
  done: true
  eTaF0.1: 0.9506473260754612
  eTaF0.5: 0.9504270643119961
  eTaF1: 0.950079671277355
  eTaF10: 0.9495126939958487
  eTaF2: 0.9497325321029638
  eTaP: 0.9506588008394444
  eTaR: 0.949501246882793
  fn: 81
  fp: 3
###IGNORE-LINE###
  iterations_since_restore: 1
###IGNORE-LINE###
###IGNORE-LINE###
###IGNORE-LINE###
###IGNORE-LINE###
###IGNORE-LINE###
###IGNORE-LINE###
  tn: 3996
  tp: 721
  training_iteration: 1
###IGNORE-LINE###
  
###IGNORE-LINE###
###IGNORE-LINE###
  Accuracy: 0.9825036450739429
###IGNORE-LINE###
###IGNORE-LINE###
###IGNORE-LINE###
###IGNORE-LINE###
###IGNORE-LINE###
###IGNORE-LINE###
###IGNORE-LINE###
  Average-Time-to-Detection: 5.0
  BATADAL: 0.9714419779279582
  BATADAL-CLF: 0.9491261531093497
  BATADAL-TTD: 0.9937578027465668
  Detected-Scenarios:
  - '1'
  Detected-Scenarios-Percent: 1.0
  Detection-Delay: 5
  F0.1: 0.9947952241742029
  F0.5: 0.9748512709572743
  F1: 0.9449541284403671
  F10: 0.8998690129009935
  F2: 0.9168362156663276
  FPA: 3
  Fallout: 0.0007501875468867217
  Informedness: 0.8982523062186993
  Inverse-Precision: 0.9801324503311258
  Inverse-Recall: 0.9992498124531133
  Jaccard-Distance: 0.10434782608695647
  Jaccard-Index: 0.8956521739130435
  MCC: 0.9363141534585618
  Markedness: 0.9759888039222862
  Missrate: 0.10099750623441396
  NAB-score-default: 83.47866918562391
  NAB-score-low-fn: 88.98577945708261
  NAB-score-low-fp: 66.9786691856239
  Penalty-Score: 3
  Precision: 0.9958563535911602
  Recall: 0.899002493765586
  Scenario-Recall:
    '1': 0.899002493765586
  TPA: 19
  _evaluation-config:
    alarm_gracetime: 0
###IGNORE-LINE###
    batadal_gamma: 0.5
    compresslevel: 6
    eTaPR_delta: 0.0
    eTaPR_theta_p: 0.5
    eTaPR_theta_r: 0.01
    fscore_beta: [0.1, 0.5, 1, 2, 10]
    input: output.state.gz
    log: 30
    logfile: logfile.txt
    logformat: '%(levelname)s:%(name)s: %(message)s'
    nab_profiles:
      default:
        nab_afn: -1
        nab_afp: -0.11
        nab_atp: 1
      reward_low_fn:
        nab_afn: -2.0
        nab_afp: -0.11
        nab_atp: 1
      reward_low_fp:
        nab_afn: -1
        nab_afp: -0.22
        nab_atp: 1
    output: evaluate.json
    timed_dataset: true
###IGNORE-LINE###
  _iids-config:
    alerts: null
    alerts_update: false
    combiner:
      _type: Matrix
      keys:
      - MinMax
      - Gradient
      - Exists
      lookahead: 0
      matrix:
      - - 0.6834629351721363
      - - 0.7127020269829002
      - - 0.37025075479039493
      model-file: model-combiner
      threshold: 0.5611961860656249
      use_scores: false
    combiner_config: config-combiner.json
    compresslevel: 6
    config: config-iids.json
    hostname: false
    idss:
      Exists:
        _type: ExistsIDS
        exclude: []
        model-file: Exists
        threshold: 10.0
      Gradient:
        _type: MinMax
        allow-none: false
        discrete_threshold: 10
        features: [state;1, state;2, state;3, state;4, state;5, state;6, state;7, state;8,
          state;9, state;10, state;11, state;12, state;13, state;14, state;15, state;16,
          state;17, state;18, state;19, state;20, state;21, state;22, state;23, state;24,
          state;25, state;26, state;27, state;28, state;29, state;30, state;31, state;32,
          state;33, state;34, state;35, state;36, state;37, state;38, state;39, state;40,
          state;41]
        model-file: Gradient
        preprocessors:
        - features: [state;1, state;2, state;3, state;4, state;5, state;6, state;7,
            state;8, state;9, state;10, state;11, state;12, state;13, state;14, state;15,
            state;16, state;17, state;18, state;19, state;20, state;21, state;22, state;23,
            state;24, state;25, state;26, state;27, state;28, state;29, state;30, state;31,
            state;32, state;33, state;34, state;35, state;36, state;37, state;38, state;39,
            state;40, state;41]
          method: Gradient
        save-training: null
        threshold: 1.0
        trainon: 1.0
      MinMax:
        _type: MinMax
        allow-none: false
        discrete_threshold: 10
        features: [state;1, state;2, state;3, state;4, state;5, state;6, state;7, state;8,
          state;9, state;10, state;11, state;12, state;13, state;14, state;15, state;16,
          state;17, state;18, state;19, state;20, state;21, state;22, state;23, state;24,
          state;25, state;26, state;27, state;28, state;29, state;30, state;31, state;32,
          state;33, state;34, state;35, state;36, state;37, state;38, state;39, state;40,
          state;41]
        model-file: MinMax
        preprocessors: []
        save-training: null
        threshold: 1.0
        trainon: 1.0
    live_ipal: null
###IGNORE-LINE###
    log: 30
    logfile: logfile.txt
    logformat: '%(levelname)s:%(name)s:%(message)s'
    output: test.ipal
    retrain: false
    train_combiner: null
    train_ipal: null
    train_state: null
###IGNORE-LINE###
###IGNORE-LINE###
  done: true
  eTaF0.1: 0.9506473260754612
  eTaF0.5: 0.9504270643119961
  eTaF1: 0.950079671277355
  eTaF10: 0.9495126939958487
  eTaF2: 0.9497325321029638
  eTaP: 0.9506588008394444
  eTaR: 0.949501246882793
  fn: 81
  fp: 3
###IGNORE-LINE###
  iterations_since_restore: 1
###IGNORE-LINE###
###IGNORE-LINE###
###IGNORE-LINE###
###IGNORE-LINE###
###IGNORE-LINE###
###IGNORE-LINE###
  tn: 3996
  tp: 721
  training_iteration: 1
###IGNORE-LINE###
  
###IGNORE-LINE###
== Status ==
###IGNORE-LINE###
Using FIFO scheduling algorithm.
###IGNORE-LINE###
###IGNORE-LINE###
###IGNORE-LINE###
Number of trials: 4/4 (4 TERMINATED)
###IGNORE-LINE###
###IGNORE-LINE###
###IGNORE-LINE###
###IGNORE-LINE###
###IGNORE-LINE###
###IGNORE-LINE###
###IGNORE-LINE###
###IGNORE-LINE###


###IGNORE-LINE###
