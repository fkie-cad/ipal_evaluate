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
  Accuracy: 0.9804207456779838
###IGNORE-LINE###
###IGNORE-LINE###
###IGNORE-LINE###
###IGNORE-LINE###
###IGNORE-LINE###
###IGNORE-LINE###
###IGNORE-LINE###
  Average-Time-to-Detection: 5.0
  BATADAL: 0.9708168216388859
  BATADAL-CLF: 0.9478758405312051
  BATADAL-TTD: 0.9937578027465668
  Detected-Scenarios:
  - '1'
  Detected-Scenarios-Percent: 1.0
  Detection-Delay: 5
  F0.1: 0.9813886418155846
  F0.5: 0.964419475655431
  F1: 0.9388020833333334
  F10: 0.8997578273655077
  F2: 0.9145104008117707
  FPA: 4
  Fallout: 0.003250812703175794
  Informedness: 0.8957516810624102
  Inverse-Precision: 0.9800835997049422
  Inverse-Recall: 0.9967491872968242
  Jaccard-Distance: 0.11533742331288344
  Jaccard-Index: 0.8846625766871166
  MCC: 0.9284647113528153
  Markedness: 0.962372428042817
  Missrate: 0.10099750623441396
  NAB-score-default: 28.47866918562389
  NAB-score-low-fn: 52.319112790415936
  NAB-score-low-fp: -43.021330814376135
  Penalty-Score: 13
  Precision: 0.9822888283378747
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
      _type: Any
      model-file: model-combiner
    combiner_config: config-combiner.json
    compresslevel: 6
    config: config-iids.json
    hostname: false
    idss:
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
        model-file: ./model-minmax
        preprocessors: []
        save-training: null
        threshold: 0.4
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
  eTaF0.1: 0.9040914817916592
  eTaF0.5: 0.9124701230867508
  eTaF1: 0.9260132776243559
  eTaF10: 0.9490245807030605
  eTaF2: 0.939964512108935
  eTaP: 0.9036593079842766
  eTaR: 0.949501246882793
  fn: 81
  fp: 13
###IGNORE-LINE###
  iterations_since_restore: 1
###IGNORE-LINE###
###IGNORE-LINE###
###IGNORE-LINE###
###IGNORE-LINE###
###IGNORE-LINE###
###IGNORE-LINE###
  tn: 3986
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
      _type: Any
      model-file: model-combiner
    combiner_config: config-combiner.json
    compresslevel: 6
    config: config-iids.json
    hostname: false
    idss:
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
        model-file: ./model-minmax
        preprocessors: []
        save-training: null
        threshold: 1.2000000000000002
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
      _type: Any
      model-file: model-combiner
    combiner_config: config-combiner.json
    compresslevel: 6
    config: config-iids.json
    hostname: false
    idss:
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
        model-file: ./model-minmax
        preprocessors: []
        save-training: null
        threshold: 0.9
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
      _type: Any
      model-file: model-combiner
    combiner_config: config-combiner.json
    compresslevel: 6
    config: config-iids.json
    hostname: false
    idss:
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
        model-file: ./model-minmax
        preprocessors: []
        save-training: null
        threshold: 1.6
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
