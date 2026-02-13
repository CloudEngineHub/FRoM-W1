# Motion-X Dataset Processing and Representation

We found that processing human motion datasets is a tedious and error-prone process, so we are sharing our specific workflow here for reference. 

This workflow trys to process the dataset according to the original Motion-X readme and fixes known [issues](https://github.com/IDEA-Research/Motion-X/issues). We highly recommend that you carefully and thoroughly read the original paper, the original repository, and all known issues before you start.

Please note that the following content was compiled based on our previous processing documents. There may be some shortcomings; please submit an issue on the [GitHub repository](https://github.com/OpenMOSS/FRoM-W1) if there are any problems related to this document.

And if you find this document useful, please consider citing the original [Motion-X dataset](https://github.com/IDEA-Research/Motion-X) and our work [FRoM-W1](https://github.com/OpenMOSS/FRoM-W1). Many thx!

## Final Folder Structure

```bash
H-GPT/datasets/motionx
|-- README.md
|-- data # final dataset
|   |-- TOKENS
|   |   |-- EgoBody
|   |   |-- GRAB
|   |   |-- HAA500
|   |   |-- aist
|   |   |-- animation
|   |   |-- dance
|   |   |-- fitness
|   |   |-- game_motion
|   |   |-- humanml
|   |   |-- humman
|   |   |-- idea400
|   |   |-- kungfu
|   |   |-- music
|   |   `-- perform
|   |-- VQVAE
|   |   |-- EgoBody
|   |   |-- GRAB
|   |   |-- HAA500
|   |   |-- aist
|   |   |-- animation
|   |   |-- dance
|   |   |-- fitness
|   |   |-- game_motion
|   |   |-- humanml
|   |   |-- humman
|   |   |-- idea400
|   |   |-- kungfu
|   |   |-- music
|   |   `-- perform
|   |-- data_backup
|   |   |-- GRAB_text
|   |   |-- humanml_humanml3d_texts
|   |   |-- smplx322_EgoBody_no_face
|   |   |-- smplx322_GRAB_no_face
|   |   |-- smplx322_GRAB_with_face_with_issue29
|   |   `-- smplx322_humanml_no_face
|   |-- face_motion_data
|   |   `-- smplx_322
|   |-- instructions
|   |   |-- template_instructions.json
|   |   |-- template_pretrain.json
|   |   |-- template_pretrain_cot.json
|   |   `-- template_pretrain_orig.json
|   |-- mean_std
|   |   |-- vectors_263
|   |   `-- vectors_623
|   |-- motion_data
|   |   |-- joints_263
|   |   |-- joints_322
|   |   |-- joints_623
|   |   |-- smplx_322
|   |   |-- vectors_263
|   |   |-- vectors_623
|   |   `-- vectors_673
|   |-- split
|   |   |-- README.md
|   |   |-- all.txt
|   |   |-- test.txt
|   |   |-- train.txt
|   |   `-- val.txt
|   |-- texts
|   |   |-- body_texts
|   |   |-- cot
|   |   |-- face_texts
|   |   |-- hand_texts
|   |   |-- semantic_labels
|   |   `-- semantic_labels_wo_parsing
|   `-- visualization_30fps
|       |-- EgoBody
|       |-- GRAB
|       |-- HAA500
|       |-- aist
|       |-- animation
|       |-- dance
|       |-- fitness
|       |-- game_motion
|       |-- humanml
|       |-- humman
|       |-- idea400
|       |-- kungfu
|       |-- music
|       `-- perform
|-- downloads # raw data downloading
|   |-- AMASS-SMPLX-G.zip
|   |-- EgoBody.zip
|   |-- GRAB.zip
|   |-- Motion-X-main.zip
|   |-- body_visualizer
|   |-- human_body_prior-master
|   |-- models_smplx_v1_1.zip
|   |-- motionx_face_motion_data.zip
|   |-- motionx_pose_text.zip
|   |-- motionx_seq_text.zip
|   |-- motionx_seq_text_face.zip
|   |-- motionx_smplx.zip
|   |-- motionx_visualization.zip
|   `-- texts.zip
`-- prepare # dataset processing folder
    |-- LICENSE
    |-- PoseText
    |-- README.md
    |-- assets
    |-- datasets
    |-- mocap-dataset-process
    |-- non-mocap-dataset-process
    |-- process_texts.py
    |-- stat.py
    `-- visualization
```

## Dataset Processing Pipeline

1. Download and organize (do not process) the Motion-X 1.0 dataset according to the official [dataset download readme](https://github.com/IDEA-Research/Motion-X?tab=readme-ov-file#1-request-authorization), and update it according to News before (including) [2023.11.15].
2. Update the sequential motion text descriptions text_v1.1 according to the News [2023.12.22].
3. Update the frame-level textual descriptions according to News [2024.1.9].
4. Process the non mocap datasets according to [this section](https://github.com/IDEA-Research/Motion-X?tab=readme-ov-file#2-non-mocap-subsets).
5. Process the mocap datasets according to [this section](https://github.com/IDEA-Research/Motion-X?tab=readme-ov-file#3-mocap-subsets).     
(a) When processing Egobody, the numpy version should be `1.23.5`.     
(b) When processing GRAB, you may need to check the original [GRAB readme](https://github.com/otaheri/GRAB/tree/master). Please note do not change the file names of the downloaded dataset, and be careful about the file pathes. Then fix this [issue-29](https://github.com/IDEA-Research/Motion-X/issues/29). You only have to process it untill you get `grab/s1,s2,...`, do not use the `grab_process.py`.
(c) When processing AMASS, you may need to rename subfolders according to the [readme](https://github.com/IDEA-Research/Motion-X/tree/main/mocap-dataset-process#1-data-preparing). Then remove abuntant and unused subsets (`BMLhandball`, `GRAB` and `WEIZMANN`). Skip problematic motions in this [issue-56](https://github.com/IDEA-Research/Motion-X/issues/56), this [issue-43](https://github.com/IDEA-Research/Motion-X/issues/43) and this [issue-56](https://github.com/IDEA-Research/Motion-X/issues/56). Keep the unaugmented face as original according to [issue-97](https://github.com/IDEA-Research/Motion-X/issues/97).
6. After the above processing, you can obtain the following motion clip statistics
```bash
humanml 26292
HAA500 5231
aist 1470
humman 744
GRAB 1335
EgoBody 980
idea400 12513
fitness 16730
dance 163
animation 329
game_motion 10217
perform 475
kungfu 1040
music 3565
all:  81084
```
and text statistics (we also parsed these Motion-X texts in the [humanml3d](https://github.com/EricGuo5513/HumanML3D) format)
```bash
humanml 29232
HAA500 5231
aist 1470
humman 744
GRAB 2670 # may be doubled, to check.
EgoBody 1960 # may be doubled, to check.
idea400 12513
fitness 16730
dance 163
animation 329
game_motion 10218
perform 475
kungfu 1040
music 3565
all:  86340
```
and frame statistics
```bash
dataset frames min_len max_len mean_len
humanml 26292 1 300 204.07142857142858
aist 1470 12 300 231.92380952380952
GRAB 1335 123 1115 304.31760299625466
dance 163 3 1497 221.33742331288343
animation 329 21 334 115.91489361702128
HAA500 5231 5 392 59.56643089275473
perform 475 4 554 215.8357894736842
fitness 16730 1 1994 214.2595935445308
game_motion 10217 3 2919 109.62141528824507
kungfu 1040 2 784 247.85
music 3565 2 944 245.9321178120617
humman 744 8 511 141.1034946236559
idea400 12513 2 570 207.37297210900664
EgoBody 980 83 680 447.9142857142857
all:  81084
```

## Dataset Representation Pipeline
Then represent the dataset according to [this readme](https://github.com/IDEA-Research/Motion-X/tree/main/tomato_represenation).

Here are some notes:   
1. After run `raw_pose_processing.py`, you can get folder `joints_322`.
2. After run `motion_representation.py`, you can get folders `joints_623` and `vectors_623`.    
(a) There may be 7 motions with shape `(1,52,3)` can not be processed, just skip them.    
(b) We also use a `transfer_to_body_only_vector.py` and `transfer_to_body_only_joints.py` to get folder `vectors_263` and `joints_263`, but you may not need them.
3. When running `cal_mean_var.py`, there may be about 10 `npy` files with errors, just skip them.

## Dataset Visualization
Please refer to the [visualization code](https://github.com/IDEA-Research/Motion-X/tree/main/tomato_represenation) in the original repository to check whether your processing results are reasonable.

Although we have spent a great deal of effort processing this dataset, as indicated by the relevant issues in the original GitHub repository, there are still quite a few issues that have not been completely resolved. However, we hope that this script can be helpful to some extent in the data processing of this dataset.